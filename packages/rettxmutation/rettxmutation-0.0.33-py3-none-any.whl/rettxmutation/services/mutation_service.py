import re
import logging
from typing import Dict, Optional
from rettxmutation.models.gene_models import TranscriptMutation, GeneMutation
from rettxmutation.adapters.mutalyzer_mutation_adapter import MutalyzerMutationAdapter, MutationMappingError
from rettxmutation.adapters.variant_validator_adapter import VariantValidatorMutationAdapter, VariantValidatorNormalizationError


logger = logging.getLogger(__name__)


def parse_transcript_description(hgvs_full: str):
    """
    Extract transcript ID, version, and coding mutation from a full HGVS transcript description.
    
    Example:
      Input: "NM_004992.4:c.916C>T"
      Returns: ("NM_004992", 4, "c.916C>T")
    """
    match = re.match(r"(?P<transcript_id>NM_\d+)\.(?P<version>\d+):(?P<hgvs_c>.+)", hgvs_full)
    if match:
        return match.group('transcript_id'), int(match.group('version')), match.group('hgvs_c')
    raise ValueError(f"Invalid transcript HGVS format: {hgvs_full}")


def parse_protein_description(hgvs_full: str):
    """
    Extract protein ID, version, and protein mutation from a full HGVS protein description.
    
    Example:
      Input: "NP_004983.1:p.(Arg306Cys)"
      Returns: ("NP_004983", 1, "p.(Arg306Cys)")
    """
    match = re.match(r"(?P<protein_id>NP_\d+)\.(?P<version>\d+):p\.\((?P<hgvs_p>.+)\)", hgvs_full)
    if match:
        return match.group('protein_id'), int(match.group('version')), f"p.({match.group('hgvs_p')})"
    raise ValueError(f"Invalid protein HGVS format: {hgvs_full}")


class MutationService:
    """
    Combined mutation service that uses the Mutalyzer API for transcript mapping and 
    the VariantValidator API for normalization.
    
    Flow:
      1. Check if the input HGVS string is already in the correct transcript format.
      2. Use Mutalyzer to map the input mutation to the primary and secondary transcripts (if necessary).
      3. Normalize the mapped mutations using VariantValidator.
      4. Parse the returned JSON responses using helper functions (with regex) to extract:
         - Transcript-level details (transcript_id, transcript_version, hgvs_c, and full_transcript_description).
         - Protein-level details (protein_id, protein_version, hgvs_p, and full_protein_description).
      5. Extract the genomic coordinate from the primary normalization response.
      6. Build and return a GeneMutation instance.
    """
    def __init__(
        self,
        primary_transcript: str = "NM_004992.4",
        secondary_transcript: Optional[str] = "NM_001110792.2",
        target_assembly: str = "GRCh38",
        mutalyzer_map_url: str = "https://mutalyzer.nl/api/map/",
        variantvalidator_norm_url: str = "https://rest.variantvalidator.org/VariantValidator/variantvalidator/"
    ):
        self.primary_transcript = primary_transcript
        self.secondary_transcript = secondary_transcript
        self.target_assembly = target_assembly
        self.mutalyzer_adapter = MutalyzerMutationAdapter(
            target_assembly=target_assembly,
            map_base_url=mutalyzer_map_url,
            norm_base_url=""  # Mapping calls only.
        )
        self.variantvalidator_adapter = VariantValidatorMutationAdapter(
            target_assembly=target_assembly,
            canonical_transcript=primary_transcript.split(":")[0],
            norm_base_url=variantvalidator_norm_url
        )

    def parse_transcript_data(self, transcript_json: Dict) -> TranscriptMutation:
        """
        Given a transcript-level normalization JSON, parse the transcript and protein details,
        and return a TranscriptMutation instance.
        """
        # Parse transcript-level information.
        transcript_id, transcript_version, hgvs_c = parse_transcript_description(
            transcript_json["hgvs_transcript_variant"]
        )
        # Parse protein-level information.
        protein_desc = transcript_json["hgvs_predicted_protein_consequence"]["tlr"]
        protein_id, protein_version, hgvs_p = parse_protein_description(protein_desc)
        return TranscriptMutation(
            transcript_id=transcript_id,
            transcript_version=transcript_version,
            hgvs_c=hgvs_c,
            full_transcript_description=transcript_json["hgvs_transcript_variant"],
            protein_id=protein_id,
            protein_version=protein_version,
            hgvs_p=hgvs_p,
            full_protein_description=protein_desc,
        )

    def get_gene_mutation(self, input_hgvs: str) -> GeneMutation:
        """
        Given an input HGVS mutation, obtain a mapped and normalized GeneMutation.
        
        It maps the mutation to the primary and secondary transcripts using the Mutalyzer API,
        normalizes them using the VariantValidator API, and then parses the results to create
        a comprehensive GeneMutation instance.
        """
        try:
            # Determine which transcript the input belongs to.
            if input_hgvs.startswith(self.primary_transcript.split(":")[0]):
                primary_hgvs = input_hgvs
                secondary_hgvs = (
                    self.mutalyzer_adapter.map_mutation(input_hgvs, self.secondary_transcript)
                    if self.secondary_transcript else None
                )
            elif self.secondary_transcript and input_hgvs.startswith(self.secondary_transcript.split(":")[0]):
                secondary_hgvs = input_hgvs
                primary_hgvs = self.mutalyzer_adapter.map_mutation(input_hgvs, self.primary_transcript)
            else:
                # If unclear, map to both transcripts.
                primary_hgvs = self.mutalyzer_adapter.map_mutation(input_hgvs, self.primary_transcript)
                secondary_hgvs = (
                    self.mutalyzer_adapter.map_mutation(input_hgvs, self.secondary_transcript)
                    if self.secondary_transcript else None
                )
            
            # Call the VariantValidator API for normalization.
            primary_norm = self.variantvalidator_adapter.normalize_mutation(primary_hgvs)
            secondary_norm = (
                self.variantvalidator_adapter.normalize_mutation(secondary_hgvs)
                if secondary_hgvs else None
            )
            
            # Extract the genomic coordinate from the primary normalization response.
            primary_assembly = primary_norm.get("primary_assembly_loci", {})
            assembly_data = primary_assembly.get(self.target_assembly.lower()) or primary_assembly.get(self.target_assembly)
            if not assembly_data or not assembly_data.get("hgvs_genomic_description"):
                raise Exception("Genomic coordinate not found in normalization response.")
            genomic_coordinate = assembly_data["hgvs_genomic_description"]
            
            # Parse transcript mutation details.
            primary_transcript = self.parse_transcript_data(primary_norm)
            secondary_transcript = (
                self.parse_transcript_data(secondary_norm) if secondary_norm else None
            )
            
            return GeneMutation(
                genomic_coordinate=genomic_coordinate,
                primary_transcript=primary_transcript,
                secondary_transcript=secondary_transcript
            )
        except (MutationMappingError, VariantValidatorNormalizationError) as e:
            logger.error(f"Error processing mutation {input_hgvs}: {e}")
            raise Exception("Failed to process mutation input") from e
        except Exception as e:
            logger.error(f"Unexpected error processing mutation {input_hgvs}: {e}")
            raise

    def close(self):
        """Clean up resources for both adapters."""
        self.mutalyzer_adapter.close()
        self.variantvalidator_adapter.close()
