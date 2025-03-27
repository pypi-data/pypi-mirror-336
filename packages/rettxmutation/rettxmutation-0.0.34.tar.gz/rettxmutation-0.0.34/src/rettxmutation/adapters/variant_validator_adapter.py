import requests
import logging
import backoff
from typing import Dict
from requests.exceptions import HTTPError


logger = logging.getLogger(__name__)


class VariantValidatorNormalizationError(Exception):
    """Raised when normalization of a mutation via VariantValidator fails."""
    pass

def giveup_on_non_429(e):
    """Only retry if the error is a 429 (Too Many Requests)."""
    return not (isinstance(e, HTTPError) and e.response.status_code == 429)


class VariantValidatorMutationAdapter:
    """
    Adapter for the VariantValidator API.

    This adapter implements a normalization method that sends a GET request to the
    VariantValidator endpoint to retrieve normalized mutation data.

    The expected endpoint URL structure is:
        <norm_base_url>/<target_assembly>/<variant_description>/<select_transcripts>
    
    For example, given:
      - target_assembly = "GRCh38"
      - variant_description = "NM_004992.4:c.916C>T" or a genomic coordinate,
      - select_transcripts = "NM_004992.4" or "NM_004992.4,NM_001110792.2"
    
    The resulting URL might be:
      https://rest.variantvalidator.org/VariantValidator/variantvalidator/GRCh38/NM_004992.4:c.916C>T/NM_004992.4

    The caller is responsible for determining the correct inputs for variant_description and select_transcripts.
    """
    def __init__(self,
                 target_assembly: str = "GRCh38",
                 norm_base_url: str = "https://rest.variantvalidator.org/VariantValidator/variantvalidator/"):
        self.target_assembly = target_assembly
        self.NORM_BASE_URL = norm_base_url
        self.session = requests.Session()

    def close(self):
        """Clean up the underlying session."""
        self.session.close()


    @backoff.on_exception(
        backoff.expo,
        (requests.exceptions.HTTPError, requests.exceptions.ConnectionError, requests.exceptions.Timeout),
        max_tries=5,
        giveup=giveup_on_non_429
    )
    def normalize_mutation(self, variant_description: str, select_transcripts: str) -> Dict:
        """
        Normalize the mutation using the VariantValidator API.

        Parameters:
            variant_description (str): The variant description to check (e.g., an HGVS string or genomic coordinate).
            select_transcripts (str): The transcript(s) to select (e.g., "NM_004992.4" or "NM_004992.4,NM_001110792.2").

        Returns:
            dict: The JSON response from VariantValidator containing normalized mutation details.

        Raises:
            VariantValidatorNormalizationError: If normalization fails or returns an empty response.
        """
        url = f"{self.NORM_BASE_URL}{self.target_assembly}/{variant_description}/{select_transcripts}"
        logger.debug(f"Normalizing mutation via URL: {url}")
        try:
            response = self.session.get(url)
            response.raise_for_status()
            norm_data = response.json()
            if not norm_data:
                raise VariantValidatorNormalizationError(f"Empty normalization data for {variant_description}")
            logger.debug(f"Normalization data: {norm_data}")
            return norm_data

        except HTTPError as http_err:
            if response.status_code == 429:
                logger.warning(f"Rate limit exceeded for {variant_description}. Retrying...")
                raise http_err
            else:
                logger.error(f"HTTP error occurred: {http_err}")
                raise VariantValidatorNormalizationError(f"HTTP error occurred: {http_err}") from http_err

        except Exception as e:
            logger.error(f"Error normalizing mutation {variant_description}: {e}")
            raise VariantValidatorNormalizationError(f"Error normalizing mutation {variant_description}") from e
