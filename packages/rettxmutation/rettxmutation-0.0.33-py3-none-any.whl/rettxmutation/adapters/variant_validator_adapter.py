import requests
import logging
import backoff
from typing import Dict

logger = logging.getLogger(__name__)

class VariantValidatorNormalizationError(Exception):
    """Raised when normalization of a mutation via VariantValidator fails."""
    pass

class VariantValidatorMutationAdapter:
    """
    Adapter for the VariantValidator API.

    This adapter implements a normalization method that sends a GET request to the
    VariantValidator endpoint to retrieve normalized mutation data.
    
    The expected endpoint URL structure is:
        <norm_base_url>/<target_assembly>/<mutation>/<canonical_transcript>
    
    For example, given:
      - target_assembly = "GRCh38"
      - mutation = "NM_004992.4:c.916C>T"
      - canonical_transcript = "NM_004992.4"
    
    The resulting URL is:
      https://rest.variantvalidator.org/VariantValidator/variantvalidator/GRCh38/NM_004992.4:c.916C>T/NM_004992.4

    Since VariantValidator does not support a mapping function, only the normalize_mutation
    method is implemented.
    """
    def __init__(self,
                 target_assembly: str = "GRCh38",
                 canonical_transcript: str = "NM_004992.4",
                 norm_base_url: str = "https://rest.variantvalidator.org/VariantValidator/variantvalidator/"):
        self.target_assembly = target_assembly
        self.canonical_transcript = canonical_transcript
        self.NORM_BASE_URL = norm_base_url
        self.session = requests.Session()

    def close(self):
        """Clean up the underlying session."""
        self.session.close()

    @backoff.on_exception(
        backoff.expo,
        (requests.exceptions.HTTPError, requests.exceptions.ConnectionError, requests.exceptions.Timeout),
        max_tries=5,
    )
    def normalize_mutation(self, description: str) -> Dict:
        """
        Normalize the mutation using the VariantValidator API.

        Parameters:
            description (str): The input HGVS mutation string (e.g., "NM_004992.4:c.916C>T").

        Returns:
            dict: The JSON response from VariantValidator containing normalized mutation details.

        Raises:
            VariantValidatorNormalizationError: If normalization fails or returns an empty response.
        """
        # Construct the URL using the target assembly, input mutation, and canonical transcript.
        url = f"{self.NORM_BASE_URL}{self.target_assembly}/{description}/{self.canonical_transcript}"
        logger.debug(f"Normalizing mutation via URL: {url}")
        try:
            response = self.session.get(url)
            response.raise_for_status()
            norm_data = response.json()
            if not norm_data:
                raise VariantValidatorNormalizationError(f"Empty normalization data for {description}")
            logger.debug(f"Normalization data: {norm_data}")
            return norm_data
        except Exception as e:
            logger.error(f"Error normalizing mutation {description}: {e}")
            raise VariantValidatorNormalizationError(f"Error normalizing mutation {description}") from e
