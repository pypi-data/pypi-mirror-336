from odibi_de.core_types import CloudConnector
from azure.storage.blob import BlobServiceClient
from odibi_de.utils import (
    get_logger, PandasValidationUtils)


class AzureBlobConnector(CloudConnector):
    """
    Connector class for Azure Blob Storage.

    This class interacts with Azure Blob Storage to provide:
        - Connections to the Blob service.
        - Resolved file paths based on the framework (Pandas or Spark).
        - Framework-specific configurations for cloud access.

    Methods:
        get_connection(): Establish a connection to Azure Blob Storage.
        get_file_path(storage_unit, object_name, framework): Generate
            the file path for the blob.
        get_framework_config(framework): Retrieve framework-specific
            configurations.

    Returns:
    AzureBlobConnector: An instance of AzureBlobConnector with the
        necessary configurations.

    Examples:
        blob_connector = AzureBlobConnector(
        "my_account_name",
        "my_account_key")
    """

    def __init__(self, account_name: str, account_key: str):
        """
        Initialize the AzureBlobConnector with account details.

        Args:
            account_name (str): The name of the Azure Storage account.
            account_key (str): The access key for the Azure Storage account.
        """
        # Validate input parameters.
        PandasValidationUtils.validate_is_non_empty_string(account_name)
        PandasValidationUtils.validate_is_non_empty_string(account_key)

        self.account_name = account_name
        self.account_key = account_key
        self.logger = get_logger()

    def get_connection(self):
        """
        Establish a connection to Azure Blob Storage using the
        BlobServiceClient.

        Returns:
            BlobServiceClient: The Azure Blob Service client instance.

        Raises:
            Exception: If there is an error establishing the connection.

        Example:
        blob_connector = AzureBlobConnector(
            "my_account_name",
            "my_account_key")
        blob_connector.get_connection()
        """

        self.logger.log(
            "info", "Establishing connection to Azure Blob Storage.")

        # Create a BlobServiceClient object using the connection string
        try:
            url = f"https://{self.account_name}.blob.core.windows.net"
            conntection = BlobServiceClient(
                account_url=url,
                credential=self.account_key)
            self.logger.log(
                "info",
                "Connection established successfully for account: " +
                f"{self.account_name}.")
            return conntection

        except Exception as e:
            error_message = (
                "Failed to establish connection to Azure Blob Storage for " +
                f"account: {self.account_name}. Error: {e}")
            self.logger.log(
                "error",
                error_message)
            raise Exception(error_message) from e

    def get_file_path(
        self,
        storage_unit: str,
        object_name: str,
        framework: str
    ) -> str:
        """
        Generate a file path for the specified framework.

        Args:
            storage_unit (str): The container name in Azure Blob Storage.
            object_name (str): The name/path of the blob/file.
            framework (str): Target framework ('pandas' or 'spark').

        Returns:
            str: Resolved file path compatible with the specified framework.

        Raises:
            ValueError: If the framework is not supported.

        Example:
        blob_connector = AzureBlobConnector(
            "my_account_name",
            "my_account_key")
        file_path = blob_connector.get_file_path(
            "my_container",
            "my_blob.csv",
            "pandas")
        """
        # Validate input parameters.
        PandasValidationUtils.validate_is_non_empty_string(storage_unit)
        PandasValidationUtils.validate_is_non_empty_string(object_name)
        PandasValidationUtils.validate_is_non_empty_string(framework)

        self.logger.log(
            "info",
            f"Generating file path for storage unit: {storage_unit}, object:" +
            f" {object_name}, framework: {framework}")
        if framework == "spark":
            path = (
                f"abfss://{storage_unit}@{self.account_name}.dfs.core" +
                f".windows.net/{object_name}"
            )
        elif framework == "pandas":
            path = f"az://{storage_unit}/{object_name}"
        else:
            error_message = f"Unsupported framework: {framework}"
            self.logger.log(
                "error",
                error_message)
            raise ValueError(error_message)

        self.logger.log(
            "info",
            f"Resolved file path for {framework}: {path}")
        return path

    def get_framework_config(
        self,
        framework: str
    ) -> dict:
        """
        Generate cloud-specific configuration for the specified framework.

        Args:
            framework (str): Target framework ('pandas' or 'spark').

        Returns:
            dict: Framework-specific configuration options.

        Raises:
            ValueError: If the framework is not supported.

        Example:
        blob_connector = AzureBlobConnector(
            "my_account_name",
            "my_account_key")
        """
        # Validate input parameters.
        PandasValidationUtils.validate_is_non_empty_string(framework)
        spark_config_key = (
            f"fs.azure.account.key.{self.account_name}.dfs.core.windows.net")
        config_map = {
            "pandas": lambda: {
                "account_name": self.account_name,
                "account_key": self.account_key,
            },
            "spark": lambda: {
                spark_config_key: self.account_key
            }
        }

        if framework not in config_map:
            self.logger.log(
                "error",
                f"Unsupported framework for config: {framework}")
            raise ValueError(f"Unsupported framework: {framework}")

        config = config_map[framework]()
        self.logger.log("info", f"Generated configuration for {framework}.")
        return config
