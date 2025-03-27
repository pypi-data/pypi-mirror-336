from typing import Optional
from pydantic import BaseModel, Field


class TranscriptMutation(BaseModel):
    """
    Represents detailed mutation descriptions for transcript and protein levels.
    """
    hgvs_transcript_variant: str = Field(..., description="Full transcript mutation description (e.g., NM_004992.3:c.916C>T)")
    protein_consequence_tlr: Optional[str] = Field(None, description="Full protein consequence description (e.g., NP_004983.2:p.Ser306Cys)")
    protein_consequence_slr: Optional[str] = Field(None, description="Short protein consequence description in SLR format (e.g., NP_004983.1:p.(R306C))")


class GeneMutation(BaseModel):
    """
    Comprehensive mutation data model for Rett Syndrome (MECP2) mutations.
    """
    genome_assembly: str = Field(..., description="Genome assembly version (e.g., GRCh37 or GRCh38)")
    genomic_coordinate: str = Field(..., description="Canonical genomic coordinate (e.g., NC_000023.11:g.154030912G>A)")
    primary_transcript: TranscriptMutation = Field(..., description="Primary transcript mutation details NM_004992.4")
    secondary_transcript: Optional[TranscriptMutation] = Field(None, description="Secondary transcript mutation details NM_001110792.2")


# Raw mutation data model (returned by the OpenAI model)
class RawMutation(BaseModel):
    """
    Represents the raw mutation data returned by the OpenAI model.
    """
    mutation: str = Field(..., description="Raw mutation string (e.g., 'NM_004992.4:c.916C>T')")
    confidence: float = Field(..., description="Confidence score for the mutation (0.0 to 1.0)")
