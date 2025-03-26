from typing import Optional
from pydantic import BaseModel, Field


class TranscriptMutation(BaseModel):
    """
    Represents detailed mutation descriptions for transcript and protein levels.
    """
    transcript_id: str = Field(..., description="Transcript identifier (e.g., NM_004992)")
    transcript_version: int = Field(..., description="Version number of the transcript (e.g., 4)")
    hgvs_c: str = Field(..., description="HGVS coding DNA mutation (e.g., c.916C>T)")
    full_transcript_description: str = Field(..., description="Full transcript mutation description (e.g., NM_004992.3:c.916C>T)")
    protein_id: Optional[str] = Field(None, description="Protein identifier (e.g., NP_004983)")
    protein_version: Optional[int] = Field(None, description="Protein version number (e.g., 1)")
    hgvs_p: Optional[str] = Field(None, description="HGVS protein-level mutation (e.g., p.Arg306Cys)")
    full_protein_description: Optional[str] = Field(None, description="Full protein mutation description (e.g., NP_004983.1:p.(Arg306Cys))")


class GeneMutation(BaseModel):
    """
    Comprehensive mutation data model for Rett Syndrome (MECP2) mutations.
    """
    genomic_coordinate: str = Field(
        ..., description="Canonical genomic coordinate (e.g., NC_000023.11:g.154030912G>A)"
    )

    primary_transcript: TranscriptMutation = Field(
        ..., description="Primary (reference) transcript mutation details (e.g., NM_004992.4)"
    )

    secondary_transcript: Optional[TranscriptMutation] = Field(
        None, description="Secondary (alternate) transcript mutation details (e.g., NM_001110792.2)"
    )


# Raw mutation data model (returned by the OpenAI model)
class RawMutation(BaseModel):
    """
    Represents the raw mutation data returned by the OpenAI model.
    """
    mutation: str = Field(..., description="Raw mutation string (e.g., 'NM_004992.4:c.916C>T')")
    confidence: float = Field(..., description="Confidence score for the mutation (0.0 to 1.0)")
