from typing import Dict, Any, Optional, List
from ocular.core.export import Export
from ocular.api import OcularApiClient
from ocular.utils.logging import get_logger
from ocular.utils.config import OcularConfig
from ocular.utils.errors import ValidationError

logger = get_logger()


class Version:
    """
    Represents a specific version of a project in the Ocular AI platform.
    """

    def __init__(self, version_info: Dict[str, Any], config: OcularConfig):
        """
        Initialize a version instance.

        Args:
            version_info (Dict[str, Any]): Version information dictionary
            config (OcularConfig): Ocular configuration object
        """
        if not config.api_key:
            raise ValidationError("API key is required")
        self.config = config
        self.id = version_info["id"]
        self.version = version_info["version"]
        self.project_id = version_info["project_id"]
        self.created_at = version_info["created_at"]
        self.updated_at = version_info["updated_at"]
        self.status = version_info["status"]
        self.description = version_info["description"]
        self.creator = version_info["creator"]
        self.finished_at = version_info["finished_at"]

        self.api_client = OcularApiClient(
            api_key=self.config.api_key,
            api_url=self.config.api_url,
            timeout=self.config.timeout,
            max_retries=self.config.max_retries,
            backoff_factor=self.config.backoff_factor,
        )

    def list_exports(self) -> List[Dict[str, Any]]:
        """
        List all exports for the version.

        Returns:
            List[Dict[str, Any]]: List of export information
        """
        logger.debug(f"Listing exports for version: {self.id}")
        exports = self.api_client.get_version_exports(self.project_id, self.id)
        return exports

    def export(self, export_id: str) -> Export:
        """
        Get a specific export for this version.

        Args:
            export_id (str): The export ID to retrieve

        Returns:
            Export: An export object
        """
        logger.debug(f"Getting export {export_id} for version: {self.id}")
        export_info = self.api_client.get_version_export(
            self.project_id, self.id, export_id
        )
        return Export(export_info, self.config)
