import re
from pyspark.sql.window import Window
from pyspark.sql.types import (StructType)
from pyspark.sql.streaming import DataStreamWriter
from pyspark.sql import SparkSession, DataFrame, Column
from pyspark.sql.functions import (
    when, col, lit, count, isnan,
    split, concat_ws, explode, array_repeat)

from odibi_de.core_types import (
    DataReader, ReaderFactory, DataType, CloudConnector, ReaderProvider,
    DataSaver, SaverFactory, DBConnector, Validator, Transformer,
    ValidatorFactory, ValidatorProvider, ValidationType, TransformerFactory,
    TransformerProvider, TransformerType, BaseDataWorkflow
)
from odibi_de.utils import (
    PandasValidationUtils, SparkValidationUtils, apply_methods, get_logger,
    validate_options, resolve_function, log_message
)


class SparkDataReader(DataReader):
    def __init__(
        self,
        file_path: str,
        spark: SparkSession,
        data_type: DataType
    ):
        """
        A generalized class for reading various file formats using Spark.
        The `SparkDataReader` provides a flexible way to read data from
        files of different formats (e.g., CSV, JSON, Parquet, Delta) into
        Spark DataFrames. It integrates with Spark's `DataFrameReader`
        and supports additional dynamic configurations.
        Args:
            file_path (str): The file path of the data to be read.
            spark (SparkSession): An active Spark session instance.
            data_type (DataType): The type of the file to read
                (e.g., CSV, JSON).
        Raises:
            ValueError: If any of the inputs are invalid.
        Examples:
            # Example 1: Reading a CSV file
            from pyspark.sql import SparkSession
            from Data_Engineering_Class_Enums_and_Abstract_Classes import (
                DataType)
            spark = SparkSession.builder.appName(
                "DataReaderExample").getOrCreate()
            # Initialize the reader
            reader = SparkDataReader(
                file_path="/path/to/data.csv",
                spark=spark,
                data_type=DataType.CSV
            )
            # Read the data
            df = reader.read_data()
            df.show()
            # Example 2: Reading a JSON file with additional options
            reader = SparkDataReader(
                file_path="/path/to/data.json",
                spark=spark,
                data_type=DataType.JSON
            )
            df = reader.read_data(
                methods_with_args={
                    "option": {"multiline": True, "mode": "PERMISSIVE"}
                }
            )
            df.show()
        """
        # Validate inputs

        PandasValidationUtils.validate_is_non_empty_string(file_path)
        PandasValidationUtils.validate_instance(
            data_type,
            DataType, "data_type")
        super().__init__(file_path)
        self.spark = spark
        self.data_type = data_type.value
        PandasValidationUtils.log_init_arguments(self)

    def read_data(self, methods_with_args: dict = None):
        """
        Read data using Spark with dynamically applied methods and options.

        Args:
            methods_with_args (dict, optional): Dictionary of methods and
                arguments to apply to the reader.

        Returns:
            DataFrame: Spark DataFrame containing the read data.

        Raises:
            FileNotFoundError: If the specified file is not found.
            ValueError: If the file format is invalid.
            IOError: If there's an error reading the file.

        Example Usage:
        from pyspark.sql import SparkSession
        from Data_Engineering_Class_Enums_and_Abstract_classes import (
            DataType)
        from my_module import SparkDataReader

        # Initialize Spark session
        spark = SparkSession.builder.appName(
            "DataReaderExample").getOrCreate()
        # Initialize the reader
        reader = SparkDataReader(
            file_path="/path/to/data.json",
            spark=spark,
            data_type=DataType.JSON
        # Read the data with additional options
        df = reader.read_data(
            methods_with_args={
                "option": {"multiline": True, "mode": "PERMISSIVE"}
            }
        )
        print(df.show())
        )

        """
        try:
            log_message(
                "info",
                f"Attempting to read {self.data_type} " +
                f"data from {self.file_path}")

            # Initialize the reader
            reader = self.spark.read.format(self.data_type)

            # Apply dynamic methods (e.g., options, schema, etc.)
            if methods_with_args:
                # Validate the input
                reader = apply_methods(reader, methods_with_args)

            # Load the data
            return reader.load(self.file_path)
        except FileNotFoundError:
            error_message = (
                f"File not found: {self.file_path}"
            )
            log_message(
                "error",
                error_message)
            raise FileNotFoundError(error_message)

        except ValueError as e:
            error_message = (
                f"Invalid {self.data_type} file at " +
                f"{self.file_path}: {e}"
            )
            log_message(
                "error",
                error_message)
            raise ValueError(error_message) from e

        except Exception as e:
            error_message = (
                f"Unexpected error while reading {self.data_type} data from "
                f"{self.file_path}: {e}"
            )
            log_message(
                "error",
                error_message)
            raise Exception(error_message) from e

    def read_sample_data(
        self,
        methods_with_args: dict = None
    ):
        """
        Read a sample of the data (first 100 rows) for schema inference
            or validation.

        Args:
            methods_with_args (dict, optional): Dictionary of methods
                and arguments to apply to the reader.

        Returns:
            DataFrame: Sampled Spark DataFrame containing the first
                100 rows of data.
        """
        return self.read_data(
            methods_with_args=methods_with_args).limit(100)


class SparkReaderFactory(ReaderFactory):
    """
    Factory class for creating SparkDataReader instances.
    The `SparkReaderFactory` provides methods to create readers for specific
    file formats (e.g., CSV, JSON, Parquet, Delta) using the
    z`SparkDataReader` class.
    Methods:
        csv_reader(file_path, spark): Creates a reader for CSV files.
        json_reader(file_path, spark): Creates a reader for JSON files.
        avro_reader(file_path, spark): Creates a reader for Avro files.
        parquet_reader(file_path, spark): Creates a reader for Parquet files.
        delta_reader(file_path, spark): Creates a reader for Delta files.

    Examples:
        # Example 1: Creating a CSV reader
        factory = SparkReaderFactory()
        reader = factory.csv_reader(file_path="/path/to/data.csv", spark=spark)
        # Example 2: Creating a Parquet reader
        reader = factory.parquet_reader(
            file_path="/path/to/data.parquet", spark=spark)

    """

    def _create_reader(
        self, file_path: str, spark: SparkSession, data_type: DataType
    ) -> DataReader:
        """
        Create a SparkDataReader instance for the specified file path and
        data type.
        Args:
            file_path (str): The file path of the data to be read.
            spark (SparkSession): An active Spark session instance.
            data_type (DataType): The type of the file to read
                (e.g., CSV, JSON).
        Returns:
            SparkDataReader: A SparkDataReader instance for the specified file
            path and data type.
        Raises:
            ValueError: If any of the inputs are invalid.
        Example Usage:
            from pyspark.sql import SparkSession
            from Data_Engineering_Class_Enums_and_Abstract_classes import (
                DataType)
            from my_module import SparkReaderFactory
            # Initialize Spark session
            spark = SparkSession.builder.appName(
                "DataReaderExample").getOrCreate()
            # Create a CSV reader
            factory = SparkReaderFactory()
            reader = factory.csv_reader(
                file_path="/path/to/data.csv", spark=spark)

        """
        return SparkDataReader(
            file_path=file_path, spark=spark, data_type=data_type)

    def csv_reader(self, file_path: str, spark: SparkSession) -> DataReader:
        """
        Create a SparkDataReader instance for CSV files.
        Args:
            file_path (str): The file path of the data to be read.
            spark (SparkSession): An active Spark session instance.
        Returns:
            SparkDataReader: A SparkDataReader instance for CSV files.
        Raises:
            ValueError: If any of the inputs are invalid.
        Example Usage:
            from pyspark.sql import SparkSession
            from my_module import (
                DataType)
            from my_module import SparkReaderFactory

            # Initialize Spark session
            spark = SparkSession.builder.appName(
                "DataReaderExample").getOrCreate()

            # Create a CSV reader
            factory = SparkReaderFactory()
            reader = factory.csv_reader(
                file_path="/path/to/data.csv", spark=spark)
        """
        return self._create_reader(file_path, spark, DataType.CSV)

    def json_reader(self, file_path: str, spark: SparkSession) -> DataReader:
        """
        Create a SparkDataReader instance for JSON files.
        Args:
            file_path (str): The file path of the data to be read.
            spark (SparkSession): An active Spark session instance.
        Returns:
            SparkDataReader: A SparkDataReader instance for JSON files.
        Raises:
            ValueError: If any of the inputs are invalid.
        Example Usage:
            from pyspark.sql import SparkSession
            from my_module import (
                DataType)
            from my_module import SparkReaderFactory

            # Initialize Spark session
            spark = SparkSession.builder.appName(
                "DataReaderExample").getOrCreate()

            # Create a JSON reader
            factory = SparkReaderFactory()
            reader = factory.json_reader(
                file_path="/path/to/data.json", spark=spark)
        """
        return self._create_reader(file_path, spark, DataType.JSON)

    def avro_reader(self, file_path: str, spark: SparkSession) -> DataReader:
        """
        Create a SparkDataReader instance for Avro files.
        Args:
            file_path (str): The file path of the data to be read.
            spark (SparkSession): An active Spark session instance.
        Returns:
            SparkDataReader: A SparkDataReader instance for Avro files.
        Raises:
            ValueError: If any of the inputs are invalid.
        Example Usage:
            from pyspark.sql import SparkSession
            from my_module import (
                DataType)
            from my_module import SparkReaderFactory

            # Initialize Spark session
            spark = SparkSession.builder.appName(
                "DataReaderExample").getOrCreate()

            # Create an Avro reader
            factory = SparkReaderFactory()
            reader = factory.avro_reader(
                file_path="/path/to/data.avro", spark=spark)
        """
        return self._create_reader(file_path, spark, DataType.AVRO)

    def parquet_reader(
        self, file_path: str, spark: SparkSession
    ) -> DataReader:
        """
        Create a SparkDataReader instance for Parquet files.
        Args:
            file_path (str): The file path of the data to be read.
            spark (SparkSession): An active Spark session instance.
        Returns:
            SparkDataReader: A SparkDataReader instance for Parquet files.
        Raises:
            ValueError: If any of the inputs are invalid.
        Example Usage:
            from pyspark.sql import SparkSession
            from my_module import (
                DataType)
            from my_module import SparkReaderFactory

            # Initialize Spark session
            spark = SparkSession.builder.appName(
                "DataReaderExample").getOrCreate()

            # Create a Parquet reader
            factory = SparkReaderFactory()
            reader = factory.parquet_reader(
                file_path="/path/to/data.parquet", spark=spark)
        """
        return self._create_reader(file_path, spark, DataType.PARQUET)

    def delta_reader(self, file_path: str, spark: SparkSession) -> DataReader:
        """
        Create a SparkDataReader instance for Delta files.
        Args:
            file_path (str): The file path of the data to be read.
            spark (SparkSession): An active Spark session instance.
        Returns:
            SparkDataReader: A SparkDataReader instance for Delta files.
        Raises:
            ValueError: If any of the inputs are invalid.
        Example Usage:
            from pyspark.sql import SparkSession
            from my_module import (
                DataType)
            from my_module import SparkReaderFactory

            # Initialize Spark session
            spark = SparkSession.builder.appName(
                "DataReaderExample").getOrCreate()

            # Create a Delta reader
            factory = SparkReaderFactory()
            reader = factory.delta_reader(
                file_path="/path/to/data.delta", spark=spark)
        """
        return self._create_reader(file_path, spark, DataType.DELTA)


class SparkReaderProviderBase(ReaderProvider):
    def __init__(
        self,
        factory: ReaderFactory,
        data_type: DataType,
        spark: SparkSession
    ):
        """
        Base class for handling shared logic across Spark Reader Providers.
        The `SparkReaderProviderBase` class provides common functionality for
        providers that manage the creation of Spark readers. It abstracts
        shared logic such as input validation, logging, and the integration
        of file paths with the `ReaderFactory`.
        Args:
            factory (ReaderFactory): An instance of the `ReaderFactory`
                class to create readers.
            data_type (DataType): The type of data to be read
                (e.g., CSV, JSON).
            spark (SparkSession): An active Spark session instance.
        Methods:
            create_reader(file_path):
                Create a reader for the specified data type and file path.
        Examples:
            # Example 1: Initializing a reader provider
            provider = SparkReaderProviderBase(
                factory=factory, data_type=DataType.CSV, spark=spark)
            # Example 2: Creating a CSV reader through the provider
            reader = provider.create_reader(file_path="/path/to/data.csv")
            df = reader.read_data()
            df.show()
        """
        PandasValidationUtils.validate_inheritance(
            factory,
            ReaderFactory,
            "factory")
        PandasValidationUtils.validate_instance(
            spark,
            SparkSession,
            "spark",
            False)

        self.factory = factory
        self.data_type = data_type
        self.spark = spark
        PandasValidationUtils.log_init_arguments(self)

    def create_reader(self, file_path: str):
        """
        Create a reader for Spark using the data type and file path.

        Args:
            file_path (str): The path to the file.

        Returns:
            DataReader: An instance of the appropriate Spark reader for the
            specified data type.

        Raises:
            ValueError: If the data type is not supported.
        """
        log_message(
            "info",
            f"Creating Spark reader for file: {file_path} " +
            f"with data type: {self.data_type.value}"
        )

        # Use the factory to create the appropriate reader
        match self.data_type:
            case DataType.CSV:
                return self.factory.csv_reader(
                    file_path=file_path,
                    spark=self.spark)
            case DataType.JSON:
                return self.factory.json_reader(
                    file_path=file_path,
                    spark=self.spark)
            case DataType.AVRO:
                return self.factory.avro_reader(
                    file_path=file_path,
                    spark=self.spark)
            case DataType.PARQUET:
                return self.factory.parquet_reader(
                    file_path=file_path, spark=self.spark)
            case DataType.DELTA:
                return self.factory.delta_reader(
                    file_path=file_path,
                    spark=self.spark)
            case _:
                error_message = (
                    f"Unsupported data type: {self.data_type.value}")
                log_message(
                    "error",
                    error_message)
                raise ValueError(error_message)


class SparkCloudReaderProvider(SparkReaderProviderBase):
    """
    Initialize the SparkCloudReaderProvider with cloud-specific configurations.
    This provider extends the base reader functionality to handle
    cloud-specific requirements, such as generating file paths using a
    `CloudConnector` and setting necessary Spark configurations for
    cloud storage.
    Args:
        factory (ReaderFactory): An instance of the `ReaderFactory` to create
                readers.
        data_type (DataType): The type of data to be read
            (e.g., CSV, JSON, Delta).
        connector (CloudConnector): A cloud connector instance for resolving
                file paths and managing cloud-specific configurations.
        spark (SparkSession): An active Spark session instance.
    Raises:
        ValueError: If the factory, data_type, connector, or spark session is
        invalid.
    Examples:
        # Example 1: Initializing the provider
        connector = CloudConnector(
            account_name="my_account",
            account_key="my_key")
        provider = SparkCloudReaderProvider(
            factory=factory,
            data_type=DataType.CSV,
            connector=connector,
            spark=spark)
        # Example 2: Creating a reader for cloud-based CSV files
        reader = provider.create_reader(
            storage_unit="my-container", object_name="path/to/data.csv")
        df = reader.read_data()
        df.show()
    """
    def __init__(
        self,
        factory,
        data_type: DataType,
        connector,
        spark: SparkSession
    ):
        super().__init__(factory, data_type, spark)
        self.framework = "spark"
        self.connector = connector
        PandasValidationUtils.validate_inheritance(
            connector,
            CloudConnector,
            "connector")

    def create_reader(self, storage_unit: str, object_name: str):
        """
        Create a reader for cloud-based files using Spark.

        This method extends the base create_reader functionality by
        incorporating cloud-specific logic. It generates the full file path
        using the cloud connector, sets necessary Spark configurations
        for cloud storage, and then creates the appropriate reader.

        Args:
            storage_unit (str): The name of the storage unit(e.g., container
                name in Azure Blob Storage or bucket name in AWS S3).
            object_name (str): The name (or path) of the object within
                the storage unit.

        Returns:
            DataReader: An instance of the appropriate Spark reader for the
            specified data type, configured for cloud storage.

        Raises:
            ValueError: If the data type is not supported or if there's
                an issue with cloud configuration.

        Example:
            reader = cloud_provider.create_reader(
                "my-container", "path/to/data.csv")
            df = reader.read_data()
        """
        # Generate the file path from the connector
        file_path = self.connector.get_file_path(
            storage_unit, object_name, framework=self.framework
        )

        # Get the framework configuration for Spark
        spark_config = self.connector.get_framework_config("spark")

        # Set each configuration in Spark
        for key, value in spark_config.items():
            self.spark.conf.set(key, value)

        return super().create_reader(file_path)


class SparkLocalReaderProvider(SparkReaderProviderBase):
    """
    Initialize the SparkLocalReaderProvider for local file systems.
    This provider is designed to handle file reading operations for local file
    systems, such as files stored on the local disk or within Databricks File
    System (DBFS). It simplifies the process of creating readers for different
    file types (e.g., CSV, JSON).
    
    Args:
        factory (ReaderFactory): An instance of the `ReaderFactory` used to
        create readers for specific file formats.
        data_type (DataType): The type of data to be read
            (e.g., CSV, JSON, Parquet).
        spark (SparkSession): An active Spark session instance for handling
            Spark operations.

    Raises:
        ValueError: If the factory, data_type, or spark session is invalid.

    Examples:
    
        # Example 1: Initializing the provider
        
        from pyspark.sql import SparkSession
        
        from Data_Engineering_Class_Enums_and_Abstract_Classes import DataType
        
        spark = SparkSession.builder.appName(
            "LocalReaderExample").getOrCreate()
            
        provider = SparkLocalReaderProvider(
            factory=factory,
            data_type=DataType.CSV,
            spark=spark)

        # Example 2: Creating a reader for a local file
        reader = provider.create_reader(file_path="/path/to/local_file.csv")
        df = reader.read_data()
        df.show()
    """
    def create_reader(self, file_path: str):
        """
        Create a reader for local files using Spark.

        Args:
            file_path (str): The path to the local file.

        Returns:
            DataReader: An instance of the appropriate Spark reader for the
            specified data type, configured for local file systems.

        Raises:
            ValueError: If the data type is not supported.

        Example:
            reader = local_provider.create_reader(
                file_path="/path/to/local_file.csv")
            df = reader.read_data()
        `"""
        return super().create_reader(file_path)


class SparkDataWorkflow(BaseDataWorkflow):
    """
    Orchestrates data-related tasks for both local and cloud
    environments using Spark.
    """

    def __init__(
        self,
        spark_session,
        reader_factory=None,
        saver_factory=None
    ):
        """
        Initializes the workflow.

        Args:
            reader_factory (SparkReaderFactory, optional): Factory for
                reader providers.Defaults to SparkReaderFactory().
            connector (CloudConnector, optional): Connector for resolving
                cloud paths.
            spark_session (SparkSession, optional): The SparkSession instance.
        """
        super().__init__()
        self.spark_session = spark_session
        self.reader_factory = reader_factory or SparkReaderFactory()
        self.saver_factory = saver_factory or SparkSaverFactory()

    def get_reader_provider(self, dataset_config):
        """
        Dynamically resolves the appropriate provider for the dataset.

        Args:
            dataset_config (dict): Configuration for a specific dataset.

        Returns:
            SparkReaderProvider: The appropriate provider based on the source.

        Raises:
            ValueError: If the dataset configuration is missing
                required fields.

        Example Usage:
        reader_provider = workflow.get_reader_provider(
            {
                "reader": {
                    "data_type": "CSV",
                    "local": {
                        "file_path": "/path/to/local_data.csv"}
        """
        data_type = dataset_config["reader"]["data_type"]
        reader_config = dataset_config["reader"]

        # Handle local source
        if reader_config.get("local", {}).get("file_path"):
            return SparkLocalReaderProvider(
                self.reader_factory)

        # Handle cloud source
        elif reader_config.get(
            "cloud", {}).get(
                "storage_unit") and reader_config.get(
                    "cloud", {}).get("object_name"):
            if not self.data_connector:
                raise ValueError(
                    "A data_connector is required for cloud workflows.")
            return SparkCloudReaderProvider(
                self.reader_factory,
                DataType[data_type.upper()],
                self.data_connector,
                self.spark_session
            )

        # Raise error if neither is valid
        raise ValueError(
            "Dataset configuration must include a valid " +
            "'local' or 'cloud' source with all required fields."
        )

    def get_saver_provider(self, dataset_config):
        """
        Dynamically resolves the appropriate provider for the dataset.

        Args:
            dataset_config (dict): Configuration for a specific dataset.

        Returns:
            SparkReaderProvider: The appropriate provider based on the source.
        """
        reader_config = dataset_config["writer"]

        # Handle local source
        if reader_config.get("local", {}).get("file_path"):
            return SparkLocalSaverProvider(
                self.saver_factory)

        # Handle cloud source
        elif reader_config.get(
            "cloud", {}).get(
                "storage_unit") and reader_config.get(
                    "cloud", {}).get("object_name"):
            if not self.data_connector:
                raise ValueError(
                    "A data_connector is required for cloud workflows.")
            return SparkCloudSaverProvider(
                self.saver_factory,
                self.data_connector
            )

        # Raise error if neither is valid
        raise ValueError(
            "Dataset configuration must include a valid " +
            "'local' or 'cloud' source with all required fields."
        )


class SparkStreamingDataWorkflow(BaseDataWorkflow):
    """
    Orchestrates data-related tasks for both local and cloud environments
    using Spark.
    """

    def __init__(
        self,
        spark_session,
        reader_factory=None,
        saver_factory=None
    ):
        """
        Initializes the workflow.

        Args:
            reader_factory (SparkStreamReaderFactory, optional): Factory
                for reader providers. Defaults to SparkStreamReaderFactory().
            connector (CloudConnector, optional): Connector for resolving
                cloud paths.
            spark_session (SparkSession, optional): The SparkSession instance.
        """
        super().__init__()
        self.spark_session = spark_session
        self.reader_factory = reader_factory or SparkStreamReaderFactory()
        self.saver_factory = saver_factory or SparkStreamSaverFactory()

    def get_reader_provider(self, dataset_config):
        """
        Dynamically resolves the appropriate provider for the dataset.

        Args:
            dataset_config (dict): Configuration for a specific dataset.

        Returns:
            SparkReaderProvider: The appropriate provider based on the source.
        Raises:
            ValueError: If the dataset configuration is missing
                required fields.

        Example Usage:
        reader_provider = workflow.get_reader_provider(
            {
                "reader": {
                    "data_type": "CSV",
                    "local": {
                        "file_path": "/path/to/local_data.csv"}
        """
        data_type = dataset_config["reader"]["data_type"]
        reader_config = dataset_config["reader"]

        # Handle local source
        if reader_config.get("local", {}).get("file_path"):
            raise ValueError(
                "Streaming data is not supported for local files.")

        # Handle cloud source
        elif reader_config.get(
            "cloud", {}).get(
                "storage_unit") and reader_config.get(
                    "cloud", {}).get("object_name"):
            if not self.data_connector:
                raise ValueError(
                    "A data_connector is required for cloud workflows.")
            return SparkCloudStreamReaderProvider(
                self.reader_factory,
                DataType[data_type.upper()],
                self.data_connector,
                self.spark_session
            )

        # Raise error if neither is valid
        raise ValueError(
            "Dataset configuration must include a valid " +
            "'local' or 'cloud' source with all required fields.")

    def get_saver_provider(self, dataset_config):
        """
        Dynamically resolves the appropriate provider for the dataset.

        Args:
            dataset_config (dict): Configuration for a specific dataset.

        Returns:
            SparkReaderProvider: The appropriate provider based on the source.
        Raises:
        ValueError: If the dataset configuration is missing
        required fields.

        Example Usage:
            saver_provider = workflow.get_saver_provider(
                {
                    "writer": {
                        "data_type": "CSV",
                        "local": {
                            "file_path": "/path/to/local_data.csv"}

        """
        reader_config = dataset_config["writer"]

        # Handle local source
        if reader_config.get("local", {}).get("file_path"):
            return SparkLocalStreamSaverProvider(
                self.saver_factory)

        # Handle cloud source
        elif reader_config.get(
            "cloud", {}).get(
                "storage_unit") and reader_config.get(
                    "cloud", {}).get("object_name"):
            if not self.data_connector:
                raise ValueError(
                    "A data_connector is required for cloud workflows.")
            return SparkCloudStreamSaverProvider(
                self.saver_factory,
                self.data_connector,
                self.spark_session
            )

        # Raise error if neither is valid
        raise ValueError(
            "Dataset configuration must include a valid " +
            "'local' or 'cloud' source with all required fields."
        )

    def _get_additional_saver_args(self, save_config):
        """
        Add Spark Streaming-specific checkpoint location for cloud saves.

        Args:
            save_config (dict): Configuration for saving the dataset.

        Returns:
            dict: Additional arguments for the saver.
        """
        writer_config = save_config.get("writer", {})
        cloud_config = writer_config.get("cloud", {})
        if cloud_config and "checkpoint_location" in writer_config:
            return {
                "checkpoint_location": writer_config["checkpoint_location"]}
        return {}

    def validate_datasets(self, *args, **kwargs):
        raise NotImplementedError(
            "Validations are not supported for streaming workflows. "
            "If validation is required, consider applying it in the " +
            "batch processing layer."
        )

    def transform_datasets(self, *args, **kwargs):
        raise NotImplementedError(
            "Transformations are not supported for streaming workflows. " +
            "Use the `save_data` method with `foreachBatch` to apply " +
            "transformations per micro-batch."
        )


class SparkDataSaver(DataSaver):
    SUPPORTED_FORMATS = set(DataType)

    def __init__(
        self,
        data: DataFrame,
        file_path: str,
        data_type: DataType
    ):
        """
        Initialize the SparkDataSaver for writing data to various file formats.
        This class is designed to save a Spark DataFrame to a specified file
        format and path. It supports common formats such as CSV, JSON,
        Parquet, Avro, and Delta. Additional write options can be configured
        dynamically when saving the data.
        Args:
            data (DataFrame): The Spark DataFrame to be saved.
            file_path (str): The file path where the data will be written.
            data_type (DataType): The file format to save the data in
                (e.g., CSV, JSON, Parquet).
        Raises:
            ValueError: If the inputs are invalid
                (e.g., unsupported file format or missing file path).
        Examples:
            # Example 1: Saving a DataFrame as a Parquet file
            from pyspark.sql import SparkSession
            from my_module import DataType
            spark = SparkSession.builder.appName(
                "DataSaverExample").getOrCreate()
            # Sample DataFrame
            df = spark.createDataFrame([
                {"id": 1, "name": "Alice"},
                {"id": 2, "name": "Bob"}
            ])
            # Initialize the saver
            saver = SparkDataSaver(
                data=df, file_path="/path/to/output.parquet",
                data_type=DataType.PARQUET)
            # Save the DataFrame
            saver.save_data(mode="overwrite")
            # Example 2: Saving a DataFrame as a CSV file with additional
            # options
            saver = SparkDataSaver(
                data=df,
                file_path="/path/to/output.csv",
                data_type=DataType.CSV)
            saver.save_data(
                methods_with_args={
                    "option": {"header": True, "delimiter": ","}
                },
                mode="overwrite"
            )
        """
        self.logger = get_logger()
        SparkValidationUtils.validate_is_dataframe(
            data,
            "data")
        self.data = data
        PandasValidationUtils.validate_is_non_empty_string(
            file_path)
        self.file_path = file_path
        PandasValidationUtils.validate_instance(
            data_type,
            DataType,
            "data_type",)
        self.data_type = data_type
        PandasValidationUtils.log_init_arguments(self)

    def save_data(
        self,
        methods_with_args: dict = None
    ):
        """
        Save the Spark DataFrame to the specified file format.
        Args:
            methods_with_args (dict, optional): Additional write
                options to be applied to the DataFrame writer. The keys
                should be method names and the values should be the
                corresponding arguments. Defaults to None.
        Raises:
            ValueError: If the file format is unsupported or if
                the DataFrame writer fails to save the data.
        Examples:
            # Example 1: Saving a DataFrame as a Parquet file with additional
            from pyspark.sql import SparkSession
            from my_module import DataType

            saver = SparkDataSaver(
                data=df, file_path="/path/to/output.parquet",
                data_type=DataType.PARQUET)
            saver.save_data(
                methods_with_args={
                    "option": {"header": True, "delimiter": ","}
                }
            )
        # Example 2: Saving a DataFrame as a CSV file
            saver = SparkDataSaver(
                data=df,
                file_path="/path/to/output.csv",
                data_type=DataType.CSV)
            saver.save_data()
        """
        if self.data_type not in self.SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported file format: {self.data_type.value}. "
                f"Supported formats: {self.SUPPORTED_FORMATS}")
        try:
            self.logger.log(
                "info",
                (
                    f"Attempting to save {self.data_type.value} " +
                    f"data to {self.file_path}"))

            # Initialize the writer
            writer = self.data.write.format(self.data_type.value)

            # Apply dynamically specified methods
            if methods_with_args:
                writer = apply_methods(writer, methods_with_args)

            # Save the data to the specified path
            writer.save(self.file_path)

        except Exception as e:
            error_message = (
                f"Error while saving {self.data_type.value} data to " +
                f"{self.file_path}: {e}")
            self.logger.log(
                "error",
                error_message)
            raise Exception(error_message)


class SparkSaverFactory(SaverFactory):
    """
    Factory class for creating SparkDataSaver instances.
    The `SparkSaverFactory` provides methods to create saver instances
    for specific file formats (e.g., CSV, JSON, Parquet, Delta).
    These savers are used to write Spark DataFrames to various file
    formats efficiently.
    Methods:
        csv_saver(file_path, data): Creates a saver for CSV files.
        json_saver(file_path, data): Creates a saver for JSON files.
        avro_saver(file_path, data): Creates a saver for Avro files.
        parquet_saver(file_path, data): Creates a saver for Parquet files.
        delta_saver(file_path, data): Creates a saver for Delta files.
    Examples:
        # Example 1: Creating a CSV saver
        factory = SparkSaverFactory()
        saver = factory.csv_saver(file_path="/path/to/output.csv", data=df)
        saver.save_data(methods_with_args = {"mode": "overwrite"})
        # Example 2: Creating a Delta saver
        saver = factory.delta_saver(file_path="/path/to/delta_table", data=df)
        saver.save_data(methods_with_args = {"mode": "append"})
    """
    def _create_saver(
        self,
        data: DataFrame,
        file_path: str,
        data_type: DataType
    ) -> DataReader:
        """
        Create a SparkDataSaver instance for the specified file format.
        Args:
            file_path (str): The file path of the data to be saved.
            data (DataFrame): The Spark DataFrame to be saved.
        Returns:
            SparkDataSaver: A SparkDataSaver instance for the specified
            file format.
        Raises:
            ValueError: If any of the inputs are invalid.
        Example Usage:
            from pyspark.sql import SparkSession
            from my_module import (
                DataType)
            from my_module import SparkSaverFactory

            # Initialize Spark session
            spark = SparkSession.builder.appName(
                "DataSaverExample").getOrCreate()

            # Create a CSV saver
            factory = SparkSaverFactory()
            saver = factory.csv_saver(
                file_path="/path/to/output.csv", data=df)
            saver.save_data(methods_with_args = {"mode": "overwrite"})
        """
        return SparkDataSaver(
            data=data,
            file_path=file_path,
            data_type=data_type)

    def csv_saver(self, file_path: str, data: DataFrame) -> DataSaver:
        """
        Create a SparkDataSaver instance for CSV files.
        Args:
            file_path (str): The file path of the CSV data to be saved.
            data (DataFrame): The Spark DataFrame to be saved.
        Returns:
            SparkDataSaver: A SparkDataSaver instance for CSV files.
        Raises:
            ValueError: If any of the inputs are invalid.

        Example Usage:
        from pyspark.sql import SparkSession
        from my_module import (
            DataType)
            from my_module import SparkSaverFactory
            saver = SparkSaverFactory().csv_saver(
                file_path="/path/to/output.csv", data=df)
                saver.save_data(methods_with_args = {"mode": "overwrite"})

        """
        return self._create_saver(
            data,
            file_path,
            DataType.CSV)

    def json_saver(self, file_path: str, data: DataFrame) -> DataSaver:
        """
        Create a SparkDataSaver instance for JSON files.
        Args:
            file_path (str): The file path of the JSON data to be saved.
            data (DataFrame): The Spark DataFrame to be saved.
        Returns:
            SparkDataSaver: A SparkDataSaver instance for JSON files.
        Raises:
            ValueError: If any of the inputs are invalid.

        Example Usage:
        from pyspark.sql import SparkSession
        from my_module import (
            DataType)
            from my_module import SparkSaverFactory
            saver = SparkSaverFactory().json_saver(
                file_path="/path/to/output.json", data=df)
                saver.save_data(methods_with_args = {"mode": "overwrite"})
        """
        return self._create_saver(
            data,
            file_path,
            DataType.JSON)

    def avro_saver(self, file_path: str, data: DataFrame) -> DataSaver:
        """
        Create a SparkDataSaver instance for Avro files.
        Args:
            file_path (str): The file path of the Avro data to be saved.
            data (DataFrame): The Spark DataFrame to be saved.
        Returns:
            SparkDataSaver: A SparkDataSaver instance for Avro files.
        Raises:
            ValueError: If any of the inputs are invalid.

        Example Usage:
        from pyspark.sql import SparkSession
        from my_module import (
            DataType)
            from my_module import SparkSaverFactory
            saver = SparkSaverFactory().avro_saver(
                file_path="/path/to/output.avro", data=df)
                saver.save_data(methods_with_args = {"mode": "overwrite"})
        """
        return self._create_saver(
            data,
            file_path,
            DataType.AVRO)

    def parquet_saver(self, file_path: str, data: DataFrame) -> DataSaver:
        """
        Create a SparkDataSaver instance for Parquet files.
        Args:
            file_path (str): The file path of the Parquet data to be saved.
            data (DataFrame): The Spark DataFrame to be saved.
        Returns:
            SparkDataSaver: A SparkDataSaver instance for Parquet files.
        Raises:
            ValueError: If any of the inputs are invalid.

        Example Usage:
        from pyspark.sql import SparkSession
        from my_module import (
            DataType)
            from my_module import SparkSaverFactory
            saver = SparkSaverFactory().parquet_saver(
                file_path="/path/to/output.parquet", data=df)
                saver.save_data(methods_with_args = {"mode": "overwrite"})
        """
        return self._create_saver(
            data,
            file_path,
            DataType.PARQUET)

    def delta_saver(self, file_path: str, data: DataFrame) -> DataSaver:
        """
        Create a SparkDataSaver instance for Delta files.
        Args:
            file_path (str): The file path of the Delta data to be saved.
            data (DataFrame): The Spark DataFrame to be saved.
        Returns:
            SparkDataSaver: A SparkDataSaver instance for Delta files.
        Raises:
            ValueError: If any of the inputs are invalid.

        Example Usage:
        from pyspark.sql import SparkSession
        from my_module import (
            DataType)
            from my_module import SparkSaverFactory
            saver = SparkSaverFactory().delta_saver(
                file_path="/path/to/delta_table", data=df)
                saver.save_data(methods_with_args = {"mode": "append"})
        """
        return self._create_saver(
            data,
            file_path,
            DataType.DELTA)


class SparkSaverProviderBase:
    """
    Base class for Spark Saver Providers to handle common logic.
    """
    def __init__(
        self,
        factory: SaverFactory
    ):
        """
        Initialize the SparkSaverProviderBase.
        This provider serves as the base class for managing saver objects
        and delegating the creation of savers to the provided factory.
        Args:
            factory (SaverFactory): A factory instance for creating saver
                objects for various file formats (e.g., CSV, JSON, Parquet).
        Raises:
            ValueError: If the factory is invalid.
        Examples:
            from my_module import (SparkSaverProviderBase)
            from my_module import (SparkSaverFactory)

            # Example 1: Initializing the provider
            factory = SparkSaverFactory()
            provider = SparkSaverProviderBase(factory=factory)
            # Example 2: Creating a saver for a specific file format
            saver = provider.create_saver(
                file_path="/path/to/output.parquet",
                data=df,
                data_type=DataType.PARQUET
            )
            saver.save_data(methods_with_args = {"mode": "overwrite"}")
        """
        self.factory = factory
        PandasValidationUtils.validate_inheritance(
            factory,
            SaverFactory,
            "factory")

    def create_saver(
        self,
        data: DataFrame,
        file_path: str,
        data_type: DataType
    ) -> DataSaver:
        """
        Create a SparkSaver instance based on the provided data type.
        Args:
            data (DataFrame): The Spark DataFrame to be saved.
            file_path (str): The file path where the data will be saved.
            data_type (DataType): The type of the data to be saved
            (e.g., CSV, JSON, etc.).
        Returns:
            DataSaver: A SparkSaver instance for the specified file format.
        Raises:
            ValueError: If the data type is unsupported.
        Examples:
            from my_module import (SparkSaverProviderBase)
            from my_module import (SparkSaverFactory)

            # Example 1: Creating a saver for CSV data
            factory = SparkSaverFactory()
            provider = SparkSaverProviderBase(factory=factory)
            saver = provider.create_saver(
                data=df,
                file_path="/path/to/output.csv",
                data_type=DataType.CSV
            )
            saver.save_data(methods_with_args = {"mode": "overwrite"})
        """
        match data_type:
            case DataType.CSV:
                return self.factory.csv_saver(file_path, data)
            case DataType.JSON:
                return self.factory.json_saver(file_path, data)
            case DataType.AVRO:
                return self.factory.avro_saver(file_path, data)
            case DataType.PARQUET:
                return self.factory.parquet_saver(file_path, data)
            case DataType.DELTA:
                return self.factory.delta_saver(file_path, data)
            case _:
                raise ValueError(f"Unsupported file format: {data_type.value}")


class SparkCloudSaverProvider(SparkSaverProviderBase):
    """
    Cloud-specific implementation of the Spark Saver Provider.
    """
    def __init__(self, factory: SaverFactory, connector):
        """
        Initialize the SparkCloudSaverProvider with cloud-specific
        configurations. This provider is designed for saving Spark
        DataFrames to cloud-based storage systems. It uses the
        `CloudConnector` to resolve file paths and manage necessary
        configurations for writing data to the cloud.
        Args:
            factory (SaverFactory): A factory instance for creating saver
                objects for various file formats (e.g., CSV, JSON, Parquet).
            connector (CloudConnector): A connector instance for resolving
            file pathsand managing cloud-specific configurations
                (e.g., Azure Blob Storage).
        Raises:
            ValueError: If the factory or connector is invalid.
        Examples:
            # Example 1: Initializing the provider
            connector = CloudConnector(
                account_name="my_account",
                account_key="my_key")
            factory = SparkSaverFactory()
            provider = SparkCloudSaverProvider(
                factory=factory,
                connector=connector)
            # Example 2: Creating a saver for cloud-based Parquet files
            saver = provider.create_saver(
                storage_unit="my-container",
                object_name="path/to/output.parquet",
                data=df,
                data_type=DataType.PARQUET
            )
            saver.save_data(
                methods_with_args={
        "mode": "overwrite"
    }
            )
        """
        super().__init__(factory)
        self.connector = connector
        PandasValidationUtils.validate_inheritance(
            connector,
            CloudConnector,
            "connector")

    def create_saver(
        self,
        data: DataFrame,
        storage_unit: str,
        object_name: str,
        data_type: DataType
    ):
        """
        Create a SparkSaver instance for cloud-based data storage.
        Args:
            data (DataFrame): The Spark DataFrame to be saved.
            storage_unit (str): The name of the storage unit (e.g., Azure
            Blob Storage container). object_name (str): The name of the
            object (e.g., file name or directory path). data_type (DataType):
            The type of the data to be saved (e.g., CSV, JSON, etc.).
        Returns:
            DataSaver: A SparkSaver instance for the specified file format.
        Raises:
            ValueError: If the data type is unsupported.
        Examples:
        from my_module import (SparkCloudSaverProvider)
        from my_module import (SparkSaverFactory)

        # Example 1: Creating a saver for cloud-based Parquet files
        connector = CloudConnector(
            account_name="my_account",
            account_key="my_key")
        factory = SparkSaverFactory()
        provider = SparkCloudSaverProvider(
            factory=factory,
            connector=connector)
        saver = provider.create_saver(
            storage_unit="my-container",
            object_name="path/to/output.parquet",
            data=df,
            data_type=DataType.PARQUET
        )
        saver.save_data(
            methods_with_args={
                "mode": "overwrite"  # Specifying write mode
            }
        )
        """
        file_path = self.connector.get_file_path(
            storage_unit,
            object_name,
            framework="spark"
        )
        return super().create_saver(data, file_path, data_type)


class SparkLocalSaverProvider(SparkSaverProviderBase):
    """
    Initialize the SparkLocalSaverProvider for saving data to local file
    systems. This provider handles saving Spark DataFrames to local file
    systems, such as files stored on local disks or within Databricks
    File System (DBFS).
    Args:
        factory (SaverFactory): A factory instance for creating saver objects
            for various file formats (e.g., CSV, JSON, Parquet).
    Raises:
        ValueError: If the factory is invalid.
    Examples:
        # Example 1: Initializing the provider
        factory = SparkSaverFactory()
        provider = SparkLocalSaverProvider(factory=factory)
        # Example 2: Creating a saver for a local Parquet file
        saver = provider.create_saver(
            file_path="/path/to/output.parquet",
            data=df,
            data_type=DataType.PARQUET
        )
        saver.save_data(
            methods_with_args={
                "mode": "overwrite"  # Specifying write mode
            }
        )
        # Example 3: Creating a saver for a CSV file with custom delimiter
        saver = provider.create_saver(
            file_path="/path/to/output.csv",
            data=df,
            data_type=DataType.CSV
        )
        saver.save_data(
            methods_with_args={
                "option": {"header": True, "delimiter": ","},
                "mode": "overwrite"  # Specifying write mode
            }
        )
    """
    def create_saver(
        self,
        data: DataFrame,
        file_path: str,
        data_type: DataType
    ):
        """
        Create a SparkSaver instance for local file systems.
        Args:
            data (DataFrame): The Spark DataFrame to be saved.
            file_path (str): The file path where the data will be saved.
            data_type (DataType): The type of the data to be saved (e.g., CSV,
                JSON, etc.).
        Returns:
            DataSaver: A SparkSaver instance for the specified file format.
        Raises:
            ValueError: If the data type is unsupported.

        Examples:
        from my_module import (SparkLocalSaverProvider)
        from my_module import (SparkSaverFactory)

        # Example 1: Creating a saver for a local Parquet file
        factory = SparkSaverFactory()
        provider = SparkLocalSaverProvider(factory=factory)
        saver = provider.create_saver(
            file_path="/path/to/output.parquet",
            data=df,
            data_type=DataType.PARQUET
        )
        saver.save_data(
            methods_with_args={
                "mode": "overwrite"  # Specifying write mode
            }
        )

        """
        return super().create_saver(data, file_path, data_type)


class SparkStreamReader(DataReader):
    def __init__(
        self,
        file_path: str,
        spark: SparkSession,
        data_type: DataType
    ):
        """
        Initialize the SparkStreamReader for streaming data sources.
        This class provides functionality for reading streaming data sources
        (e.g., Kafka, files with structured streaming) into Spark DataFrames.
        It supports dynamic configurations for handling schema inference and
        stream-specific options.
        Args:
            file_path (str): Path or source identifier for the streaming data
            (e.g., a directory or Kafka topic).
            spark (SparkSession): An active Spark session instance.
            data_type (DataType): The type of the streaming source
            (e.g., JSON, CSV, Delta).
        Raises:
            ValueError: If the inputs are invalid (e.g., unsupported data
            type or missing file path).
        Examples:
            # Example 1: Reading streaming JSON data
            from pyspark.sql import SparkSession
            from Data_Engineering_Class_Enums_and_Abstract_Classes import (
                DataType)
            spark = SparkSession.builder.appName(
                "StreamingExample").getOrCreate()
            # Initialize the streaming reader
            reader = SparkStreamReader(
                file_path=path,
                spark=spark,
                data_type=DataType.CLOUDFILES
            )

            streaming_df = reader.read_data(
                    methods_with_args={"options":{
                    "cloudFiles.format": "avro",
                    "cloudFiles.schemaLocation": "schema_location"
                    }
                                    }
            )

            display(streaming_df)
        """
        self.logger = get_logger()
        PandasValidationUtils.validate_is_non_empty_string(file_path)
        super().__init__(file_path)
        PandasValidationUtils.validate_instance(spark, SparkSession, "spark")
        self.spark = spark
        PandasValidationUtils.validate_instance(
            data_type,
            DataType,
            "data_type",)
        self.data_type = data_type
        PandasValidationUtils.log_init_arguments(self)

    def read_data(
        self,
        methods_with_args: dict = None
    ):
        """
        Read streaming data from the specified source.
        Args:
            methods_with_args (dict, optional): A dictionary containing dynamic
            method arguments (e.g., options, schema, etc.). Defaults to None.
        Returns:
            DataFrame: A Spark DataFrame containing the streaming data.
        Raises:
            FileNotFoundError: If the file at the specified path does
                not exist.
            ValueError: If the file at the specified path is invalid.
            Exception: If an unexpected error occurs while reading the data.
        Examples:
        from pyspark.sql import SparkSession
        from my_module import (
            DataType)
            spark = SparkSession.builder.appName(
                "StreamingExample").getOrCreate()
            # Initialize the streaming reader
            reader = SparkStreamReader(
                file_path=path,
                spark=spark,
                data_type=DataType.CLOUDFILES
            )

            streaming_df = reader.read_data(
                    methods_with_args={"options":{
                    "cloudFiles.format": "avro",
                    "cloudFiles.schemaLocation": "schema_location"
                    }
                                    }
            )

            display(streaming_df)
        """
        try:
            self.logger.log(
                "info",
                (
                    f"Attempting to read {self.data_type.value} " +
                    f"data from {self.file_path}"))

            # Initialize the streaming reader
            reader = self.spark.readStream.format(self.data_type.value)

            # Apply dynamic methods (e.g., options, schema, etc.)
            if methods_with_args:
                reader = apply_methods(reader, methods_with_args)

            # Load the streaming data
            return reader.load(self.file_path)

        except FileNotFoundError:
            self.logger.log(
                "error",
                f"File not found: {self.file_path}")
            raise

        except ValueError as e:
            self.logger.log(
                "error", (
                    f"Invalid {self.data_type.value} file at " +
                    f"{self.file_path}: {e}"))
            raise

        except Exception as e:
            self.logger.log(
                "error", (
                    "Unexpected error while reading " +
                    f"{self.data_type.value} data from " +
                    f"{self.file_path}: {e}"))
            raise

    def read_sample_data(self, methods_with_args: dict = None, **kwargs):
        """
        Reading sample data is not supported in streaming mode.
        :raises NotImplementedError: Streaming readers do not support
        sample data reads.
        """
        raise NotImplementedError(
            "Sampling is not supported for streaming data sources.")


class SparkStreamReaderFactory(ReaderFactory):
    """
    Initialize the SparkStreamReaderFactory for creating stream readers.
    This factory provides methods to create instances of `SparkStreamReader`
    for different streaming data types, such as JSON, CSV, Avro, Parquet,
    and Delta. It simplifies the creation process for stream-specific
    readers by encapsulating the logic for instantiating them.
    Examples:
        # Example 1: Initializing the factory
        factory = SparkStreamReaderFactory()
        # Example 2: Creating a JSON stream reader
        reader = factory.json_reader(
            file_path="/path/to/streaming/data", spark=spark)
        # Example 3: Creating a Delta stream reader
        reader = factory.delta_reader(
            file_path="/path/to/streaming/delta", spark=spark)
    """

    def _create_reader(
        self, file_path: str, spark: SparkSession, data_type: DataType
    ) -> DataReader:
        """
        Create a SparkStreamReader instance for CSV files.
        Args:
            file_path (str): The file path of the data to be read.
            spark (SparkSession): An active Spark session instance.
        Returns:
            SparkStreamReader: A SparkStreamReader instance for CSV files.
        Raises:
            ValueError: If any of the inputs are invalid.
        Example Usage:
            from pyspark.sql import SparkSession
            from my_module import (
                DataType)
            from my_module import SparkStreamReaderFactory

            # Initialize Spark session
            spark = SparkSession.builder.appName(
                "DataReaderExample").getOrCreate()

            # Create a CSV reader
            factory = SparkStreamReaderFactory()
            reader = factory.csv_reader(
                file_path="/path/to/data.csv", spark=spark)
        """
        return SparkStreamReader(
            file_path=file_path, spark=spark, data_type=data_type)

    def csv_reader(self, file_path: str, spark: SparkSession) -> DataReader:
        """
        Create a SparkStreamReader instance for CSV files.
        Args:
            file_path (str): The file path of the data to be read.
            spark (SparkSession): An active Spark session instance.
        Returns:
            SparkStreamReader: A SparkStreamReader instance for CSV files.
        Raises:
            ValueError: If any of the inputs are invalid.
        Example Usage:
            from pyspark.sql import SparkSession
            from my_module import (
                DataType)
            from my_module import SparkStreamReaderFactory

            # Initialize Spark session
            spark = SparkSession.builder.appName(
                "DataReaderExample").getOrCreate()

            # Create a CSV reader
            factory = SparkStreamReaderFactory()
            reader = factory.csv_reader(
                file_path="/path/to/data.csv", spark=spark)
        """
        return self._create_reader(
            file_path=file_path,
            spark=spark,
            data_type=DataType.CSV)

    def json_reader(self, file_path: str, spark: SparkSession) -> DataReader:
        """
        Create a SparkStreamReader instance for JSON files.
        Args:
            file_path (str): The file path of the data to be read.
            spark (SparkSession): An active Spark session instance.
        Returns:
            SparkStreamReader: A SparkStreamReader instance for JSON files.
        Raises:
            ValueError: If any of the inputs are invalid.
        Example Usage:
            from pyspark.sql import SparkSession
            from my_module import (
                DataType)
            from my_module import SparkStreamReaderFactory

            # Initialize Spark session
            spark = SparkSession.builder.appName(
                "DataReaderExample").getOrCreate()

            # Create a JSON reader
            factory = SparkStreamReaderFactory()
            reader = factory.json_reader(
                file_path="/path/to/data.json", spark=spark)
        """
        return self._create_reader(
            file_path=file_path,
            spark=spark,
            data_type=DataType.JSON)

    def avro_reader(self, file_path: str, spark: SparkSession) -> DataReader:
        """
        Create a SparkStreamReader instance for Avro files.
        Args:
            file_path (str): The file path of the data to be read.
            spark (SparkSession): An active Spark session instance.
        Returns:
            SparkStreamReader: A SparkStreamReader instance for Avro files.
        Raises:
            ValueError: If any of the inputs are invalid.
        Example Usage:
            from pyspark.sql import SparkSession
            from my_module import (
                DataType)
            from my_module import SparkStreamReaderFactory

            # Initialize Spark session
            spark = SparkSession.builder.appName(
                "DataReaderExample").getOrCreate()

            # Create an Avro reader
            factory = SparkStreamReaderFactory()
            reader = factory.avro_reader(
                file_path="/path/to/data.avro", spark=spark)
        """
        return self._create_reader(
            file_path=file_path,
            spark=spark,
            data_type=DataType.AVRO)

    def parquet_reader(
        self, file_path: str, spark: SparkSession
    ) -> DataReader:
        """
        Create a SparkStreamReader instance for Parquet files.
        Args:
            file_path (str): The file path of the data to be read.
            spark (SparkSession): An active Spark session instance.
        Returns:
            SparkStreamReader: A SparkStreamReader instance for Parquet files.
        Raises:
            ValueError: If any of the inputs are invalid.
        Example Usage:
            from pyspark.sql import SparkSession
            from my_module import (
                DataType)
            from my_module import SparkStreamReaderFactory

            # Initialize Spark session
            spark = SparkSession.builder.appName(
                "DataReaderExample").getOrCreate()

            # Create a Parquet reader
            factory = SparkStreamReaderFactory()
            reader = factory.parquet_reader(
                file_path="/path/to/data.parquet", spark=spark)
        """
        return self._create_reader(
            file_path=file_path,
            spark=spark,
            data_type=DataType.PARQUET)

    def delta_reader(self, file_path: str, spark: SparkSession) -> DataReader:
        """
        Create a SparkStreamReader instance for Delta Lake files.
        Args:
            file_path (str): The file path of the data to be read.
            spark (SparkSession): An active Spark session instance.
        Returns:
            SparkStreamReader: A SparkStreamReader instance for Delta
            Lake files.
        Raises:
            ValueError: If any of the inputs are invalid.
        Example Usage:
            from pyspark.sql import SparkSession
            from my_module import (
                DataType)
            from my_module import SparkStreamReaderFactory

            # Initialize Spark session
            spark = SparkSession.builder.appName(
                "DataReaderExample").getOrCreate()

            # Create a Delta reader
            factory = SparkStreamReaderFactory()
            reader = factory.delta_reader(
                file_path="/path/to/data.delta", spark=spark)
        """
        return self._create_reader(
            file_path=file_path,
            spark=spark,
            data_type=DataType.DELTA)

    def cloudfiles_reader(
        self, file_path: str, spark: SparkSession
    ) -> DataReader:
        """
        Create a SparkStreamReader instance for Cloud Files files.
        Args:
            file_path (str): The file path of the data to be read.
            spark (SparkSession): An active Spark session instance.
        Returns:
            SparkStreamReader: A SparkStreamReader instance for Cloud
            Files files.
        Raises:
            ValueError: If any of the inputs are invalid.
        Example Usage:
            from pyspark.sql import SparkSession
            from my_module import (
                DataType)
            from my_module import SparkStreamReaderFactory

            # Initialize Spark session
            spark = SparkSession.builder.appName(
                "DataReaderExample").getOrCreate()

            # Create a Cloud Files reader
            factory = SparkStreamReaderFactory()
            reader = factory.cloudfiles_reader(
                file_path="/path/to/data.cf", spark=spark)
        """
        return self._create_reader(
            file_path=file_path,
            spark=spark,
            data_type=DataType.CLOUDFILES)


class SparkStreamReaderProviderBase:
    """
    Base class for Spark Stream Reader Providers to handle common logic.
    """
    def __init__(
        self,
        factory,
        spark: SparkSession
    ):
        """
        Initialize the SparkStreamReaderProviderBase for managing streaming
        readers. This base provider class handles shared logic for creating
        stream readers using a factory. It abstracts common tasks such as
        input validation and logging, and it supports creating readers for
        various streaming data types.
        Args:
            factory: A factory instance for creating
                stream readers.
            spark (SparkSession): An active Spark session instance for
                managing streams.
        Raises:
            ValueError: If the factory or spark session is invalid.
        Examples:
            # Example 1: Initializing the provider
            factory = SparkStreamReaderFactory()
            provider = SparkStreamReaderProviderBase(
                factory=factory, spark=spark)
            # Example 2: Creating a streaming reader
            reader = provider.create_reader(
                file_path="/path/to/streaming/data",
                data_type=DataType.JSON
            )
            streaming_df = reader.read_data(
                methods_with_args={
                    "option": {"maxFilesPerTrigger": 1}
                }
            )
            streaming_df.writeStream.format("console").start().awaitTermination()
        """
        self.logger = get_logger()
        # PandasValidationUtils.validate_inheritance(
        #     factory,
        #     SparkStreamReaderProviderBase,
        #     "factory")
        PandasValidationUtils.validate_instance(
            spark,
            SparkSession,
            "spark")
        self.factory = factory
        self.spark = spark
        PandasValidationUtils.log_init_arguments(self)

    def create_reader(
        self,
        file_path: str,
        data_type: DataType
    ):
        """
        Create a Spark Stream Reader for the specified file path and data type.

        Args:
            file_path (str): Path to the streaming source.
            data_type (DataType): Data type (e.g., "csv", "json").

        Returns:
            DataReader: Instance of a Spark Stream Reader.

        Raises:
            ValueError: If the data type is unsupported.
        """
        PandasValidationUtils.validate_is_non_empty_string(file_path)

        self.logger.log(
            "info",
            f"Creating Spark Stream Reader for {file_path} ({data_type})")

        match data_type:
            case DataType.CSV:
                return self.factory.csv_reader(file_path, self.spark)
            case DataType.JSON:
                return self.factory.json_reader(file_path, self.spark)
            case DataType.AVRO:
                return self.factory.avro_reader(file_path, self.spark)
            case DataType.PARQUET:
                return self.factory.parquet_reader(file_path, self.spark)
            case DataType.DELTA:
                return self.factory.delta_reader(file_path, self.spark)
            case DataType.CLOUDFILES:
                return self.factory.cloudfiles_reader(file_path, self.spark)
            case _:
                error_message = f"Unsupported data type: {data_type}"
                self.logger.log(
                    "error",
                    error_message)
                raise ValueError(error_message)


class SparkCloudStreamReaderProvider(SparkStreamReaderProviderBase):
    """
    Initialize the SparkCloudStreamReaderProvider with cloud-specific
    configurations. This provider extends the base functionality for
    handling streaming data sources stored in cloud storage systems.
    It uses the `CloudConnector` to resolve cloud file paths and set
    required Spark configurations for accessing the storage.
    Args:
        factory (ReaderFactory): A factory instance for creating
            stream readers.
        connector (CloudConnector): A cloud connector for resolving file
            paths and managing cloud-specific configurations
            (e.g., Azure Blob Storage, S3).
        spark (SparkSession): An active Spark session instance.
    Raises:
        ValueError: If the factory, connector, or spark session is invalid.
    Examples:
        # Example 1: Initializing the provider
        from my_module import CloudConnector
        from my_module import SparkStreamReaderFactory
        from my_module import DataType
        from my_module import SparkCloudStreamReaderProvider

        connector = CloudConnector(
            account_name="my_account",
            account_key="my_key")
        factory = SparkStreamReaderFactory()
        provider = SparkCloudStreamReaderProvider(
            factory=factory, connector=connector, spark=spark)
        # Example 2: Creating a streaming reader for cloud-based JSON files
        reader = provider.create_reader(
            storage_unit="my-container",
            object_name="path/to/streaming/data",
            data_type=DataType.JSON
        )
        streaming_df = reader.read_data(
            methods_with_args={
                "option": {"maxFilesPerTrigger": 1}
            }
        )
    """
    def __init__(
        self,
        factory: ReaderFactory,
        data_type: DataType,
        connector,
        spark: SparkSession
    ):
        super().__init__(factory, spark)
        self.connector = connector
        PandasValidationUtils.validate_inheritance(
            connector,
            CloudConnector,
            "connector")
        PandasValidationUtils.validate_instance(
            data_type,
            DataType)
        self.data_type = data_type

    def create_reader(
        self,
        storage_unit: str,
        object_name: str
    ):
        """
        Create a Spark Stream Reader for the specified cloud-based file path
        and data type.

        Args:
            storage_unit (str): Name of the storage unit
                (e.g., "my-container").
            object_name (str): Name of the object (e.g.,
                "path/to/streaming/data").
        Returns:
            DataReader: Instance of a Spark Stream Reader.
        Raises:
            ValueError: If the data type is unsupported.

        Examples:
            # Example 1: Initializing the provider
            from my_module import CloudConnector
            from my_module import SparkStreamReaderFactory
            from my_module import DataType
            from my_module import SparkCloudStreamReaderProvider

            connector = CloudConnector(
                account_name="my_account",
                account_key="my_key")
            factory = SparkStreamReaderFactory()
            provider = SparkCloudStreamReaderProvider(
                factory=factory, connector=connector, spark=spark)
            # Example 2: Creating a streaming reader for cloud-based JSON files
            reader = provider.create_reader(
                storage_unit="my-container",
                object_name="path/to/streaming/data",
                data_type=DataType.JSON
            )
            streaming_df = reader.read_data(
                methods_with_args={
                    "option": {"maxFilesPerTrigger": 1}
                }
            )
        """
        PandasValidationUtils.validate_is_non_empty_string(storage_unit)
        PandasValidationUtils.validate_is_non_empty_string(object_name)

        # Resolve file path using the connector
        file_path = self.connector.get_file_path(
            storage_unit,
            object_name,
            framework="spark"
            )
        # Get the framework configuration for Spark
        spark_config = self.connector.get_framework_config("spark")

        # Set each configuration in Spark
        for key, value in spark_config.items():
            self.spark.conf.set(key, value)

        return super().create_reader(file_path, self.data_type)


class SparkLocalStreamReaderProvider(SparkStreamReaderProviderBase):
    """
    Initialize the SparkLocalStreamReaderProvider for local streaming sources.
    This provider is designed for managing streaming data sources stored in
    local file systems, such as files on disk or within Databricks File
    System (DBFS). It simplifies the creation of readers for streaming data
    formats like JSON, CSV, and Parquet.
    Args:
        factory (ReaderFactory): A factory instance for creating streaming
            readers.
        spark (SparkSession): An active Spark session instance for managing
            streams.
    Raises:
        ValueError: If the factory or spark session is invalid.
    Examples:
        # Example 1: Initializing the provider
        factory = SparkStreamReaderFactory()
        provider = SparkLocalStreamReaderProvider(factory=factory, spark=spark)
        # Example 2: Creating a streaming reader for a local JSON file
        reader = provider.create_reader(
            file_path="/path/to/streaming/data",
            data_type=DataType.JSON
        )
        streaming_df = reader.read_data(
            methods_with_args={
                "option": {"maxFilesPerTrigger": 1}
            }
        )
    """
    def create_reader(
        self,
        file_path: str,
        data_type: DataType
    ):
        """
        Create a Spark Stream Reader for the specified local file path
            and data type.
        Args:
            file_path (str): Path to the local streaming source.
            data_type (DataType): Data type (e.g., "csv", "json").
        Returns:
            DataReader: Instance of a Spark Stream Reader.
        Raises:
            ValueError: If the data type is unsupported.

        Examples:
        # Example 1: Initializing the provider
        factory = SparkStreamReaderFactory()
        provider = SparkLocalStreamReaderProvider(factory=factory, spark=spark)
        # Example 2: Creating a streaming reader for a local JSON file
        reader = provider.create_reader(
            file_path="/path/to/streaming/data",
            data_type=DataType.JSON
        )
        streaming_df = reader.read_data(
            methods_with_args={
                "option": {"maxFilesPerTrigger": 1}
            }
        )
        """
        return super().create_reader(file_path, data_type)


class SparkStreamSaver(DataSaver):
    def __init__(
        self,
        data: DataFrame,
        file_path: str,
        data_type: DataType,
        checkpoint_location: str
    ):
        """
        Initialize the SparkStreamSaver for saving streaming data.
        This class handles saving streaming Spark DataFrames to various
        file formats (e.g., CSV, JSON, Parquet, Delta) and ensures reliable
        processing through checkpointing. It supports dynamic configurations
        for stream-specific options, such as trigger intervals and
        output modes.
        Args:
            data (DataFrame): The streaming Spark DataFrame to be saved.
            file_path (str): The file path where the streaming data will
                be written.
            data_type (DataType): The file format to save the streaming data in
                (e.g., CSV, JSON, Parquet, Delta).
            checkpoint_location (str): The location for storing checkpoint
                data to ensure fault-tolerance and exactly-once processing.
        Raises:
            ValueError: If the inputs are invalid (e.g., missing checkpoint
                location or unsupported file format).
        Examples:
            # Example 1: Creating a reader for cloud-based CSV files
            factory = SparkStreamReaderFactory()
            provider = SparkCloudStreamReaderProvider(
                factory=factory,
                connector=connector,
                spark=spark)
            reader = provider.create_reader(
                data_type=DataType.CLOUDFILES,
                storage_unit="digital-manufacturing",
                object_name="raw_OEE_Aspen")
            df = reader.read_data(
                        methods_with_args={"options":{
                    "cloudFiles.format": "avro",
                    "cloudFiles.schemaLocation": (
                        "abfss://<storage_unit>@<account_name>.dfs.core.windows.net/<object_name>")
                    }}
            )

            # Initialize the saver
            saver = SparkStreamSaver(
                data=df,
                file_path=path2,
                data_type=DataType.DELTA,
                checkpoint_location="abfss://<storage_unit>@<account_name>.dfs.core.windows.net/<object_name>"
            )
            # Save the streaming data
            saver.save_data(
                methods_with_args={
                    "trigger": {"availableNow": True}
                }
            )

        """
        self.logger = get_logger()
        PandasValidationUtils.validate_instance(data, DataFrame, "data")
        self.data = data
        PandasValidationUtils.validate_is_non_empty_string(file_path)
        super().__init__(file_path)
        PandasValidationUtils.validate_instance(
            data_type,
            DataType,
            "data_type")
        self.data_type = data_type
        PandasValidationUtils.validate_is_non_empty_string(checkpoint_location)
        self.checkpoint_location = checkpoint_location
        PandasValidationUtils.log_init_arguments(self)

    def save_data(
        self,
        methods_with_args: dict = None
    ):
        self.supported_formats = set(DataType)
        """
        Save the streaming data to the specified file path using the
        provided data type and checkpoint location.
        Args:
            methods_with_args (dict, optional): Additional configuration
                options for the streaming query. Defaults to None.
        Raises:
            ValueError: If the file format is unsupported or the data type
                is missing.
        Examples:
        # Example 1: Saving a streaming DataFrame to a local CSV file
        saver = SparkStreamSaver(
            data=df,
            file_path="/path/to/output.csv",
            data_type=DataType.CSV,
            checkpoint_location="/path/to/checkpoint"
        )
        saver.save_data()
        """
        if self.data_type not in self.supported_formats:
            raise ValueError(
                f"Unsupported file format: {self.data_type.value}. "
                f"Supported formats: {self.supported_formats}")
        try:
            self.logger.log(
                "info", (
                    f"Attempting to save {self.data_type.value} " +
                    f"data to {self.file_path}"))

            # Initialize the writer
            writer: DataStreamWriter = self.data.writeStream.format(
                self.data_type.value).option(
                    "checkpointLocation", self.checkpoint_location)

            # Handle foreachBatch separately
            foreach_batch_function = None
            if methods_with_args and "foreachBatch" in methods_with_args:
                foreach_batch_function_path = methods_with_args[
                    "foreachBatch"].get(
                    "function")
                if not foreach_batch_function_path:
                    raise ValueError(
                        "No function specified for " +
                        "'foreachBatch' in the configuration."
                        )
                foreach_batch_function = resolve_function(
                    foreach_batch_function_path)

                writer = writer.foreachBatch(foreach_batch_function)
            # Apply other dynamically specified methods
            if methods_with_args:
                filtered_methods = {
                    k: v for k, v in methods_with_args.items(
                        ) if k != "foreachBatch"}
                writer = apply_methods(writer, filtered_methods)

            # Start the streaming query
            query = writer.start(self.file_path)
            query.awaitTermination()

            self.logger.log(
                "info", (
                    f"Successfully saved {self.data_type.value} " +
                    f"data to {self.file_path}"))

        except Exception as e:
            error_message = (
                "Unexpected error while saving " +
                f"{self.data_type.value} data to " +
                f"{self.file_path}: {e}")
            self.logger.log(
                "error",
                error_message)
            raise Exception(error_message)


class SparkStreamSaverFactory(SaverFactory):
    """
        Initialize the SparkStreamSaverFactory for creating streaming
        data savers. This factory provides methods to create instances
        of `SparkStreamSaver` for different file formats (e.g., CSV, JSON,
        Parquet, Delta). It simplifies the process of saving streaming
        Spark DataFrames by encapsulating the logic for creating and
        configuring savers.
    """

    def _create_saver(
        self,
        data: DataFrame,
        file_path: str,
        data_type: DataType,
        checkpoint_location: str
    ) -> DataReader:
        """
        Create a SparkStreamSaver instance for the specified file format.
        Args:
            file_path (str): The file path of the data to be saved.
            data (DataFrame): The Spark DataFrame to be saved.
        Returns:
            SparkStreamSaver: A SparkStreamSaver instance for the specified
            file format.
        Raises:
            ValueError: If any of the inputs are invalid.
        Example Usage:
            from pyspark.sql import SparkSession
            from my_module import (
                DataType)
            from my_module import SparkStreamSaverFactory

            # Initialize Spark session
            spark = SparkSession.builder.appName(
                "DataSaverExample").getOrCreate()

            # Create a CSV saver
            factory = SparkStreamSaverFactory()
            saver = factory.csv_saver(
                data=df,
                file_path="/path/to/output.csv",
                checkpoint_location="/path/to/checkpoint")
            saver.save_data(methods_with_args = {"mode": "overwrite"})
        """
        return SparkStreamSaver(
            data=data,
            file_path=file_path,
            data_type=data_type,
            checkpoint_location=checkpoint_location)

    def csv_saver(
        self,
        data: DataFrame,
        file_path: str,
        checkpoint_location: str
    ) -> DataSaver:
        """
        Create a SparkStreamSaver instance for CSV files.
        Args:
            file_path (str): The file path of the CSV data to be saved.
            data (DataFrame): The Spark DataFrame to be saved.
        Returns:
            SparkStreamSaver: A SparkStreamSaver instance for CSV files.
        Raises:
            ValueError: If any of the inputs are invalid.
        Example Usage:
            from pyspark.sql import SparkSession
            from my_module import (
                DataType)
            from my_module import SparkStreamSaverFactory
            # Initialize Spark session
            spark = SparkSession.builder.appName(
                "DataSaverExample").getOrCreate()
            # Create a CSV saver
            saver = SparkStreamSaverFactory().csv_saver(
                data=df,
                file_path="/path/to/output.csv",
                checkpoint_location="/path/to/checkpoint")
            saver.save_data(methods_with_args = {"mode": "overwrite"})
        """
        return self._create_saver(
            data,
            file_path,
            DataType.CSV,
            checkpoint_location)

    def json_saver(
        self,
        data: DataFrame,
        file_path: str,
        checkpoint_location: str
    ) -> DataSaver:
        """
        Create a SparkStreamSaver instance for JSON files.
        Args:
            file_path (str): The file path of the JSON data to be saved.
            data (DataFrame): The Spark DataFrame to be saved.
        Returns:
            SparkStreamSaver: A SparkStreamSaver instance for JSON files.
        Raises:
            ValueError: If any of the inputs are invalid.
        Example Usage:
        from pyspark.sql import SparkSession
        from my_module import (
                DataType)
        from my_module import SparkStreamSaverFactory
        # Initialize Spark session
        spark = SparkSession.builder.appName(
                "DataSaverExample").getOrCreate()
            # Create a JSON saver
            saver = SparkStreamSaverFactory().json_saver(
                data=df,
                file_path="/path/to/output.json",
                checkpoint_location="/path/to/checkpoint")
            saver.save_data(methods_with_args = {"mode": "overwrite"})
        """
        return self._create_saver(
            data,
            file_path,
            DataType.JSON,
            checkpoint_location)

    def avro_saver(
        self,
        data: DataFrame,
        file_path: str,
        checkpoint_location: str
    ) -> DataSaver:
        """
        Create a SparkStreamSaver instance for Avro files.
        Args:
            file_path (str): The file path of the Avro data to be saved.
            data (DataFrame): The Spark DataFrame to be saved.
        Returns:
            SparkStreamSaver: A SparkStreamSaver instance for Avro files.
        Raises:
            ValueError: If any of the inputs are invalid.
        Example Usage:
        from pyspark.sql import SparkSession
        from my_module import (
                DataType)
        from my_module import SparkStreamSaverFactory
        # Initialize Spark session
        spark = SparkSession.builder.appName(
                "DataSaverExample").getOrCreate()
            # Create an Avro saver
            saver = SparkStreamSaverFactory().avro_saver(
                data=df,
                file_path="/path/to/output.avro",
                checkpoint_location="/path/to/checkpoint")
        """
        return self._create_saver(
            data,
            file_path,
            DataType.AVRO,
            checkpoint_location)

    def parquet_saver(
        self,
        data: DataFrame,
        file_path: str,
        checkpoint_location: str
    ) -> DataSaver:
        """
        Create a SparkStreamSaver instance for Parquet files.
        Args:
            file_path (str): The file path of the Parquet data to be saved.
            data (DataFrame): The Spark DataFrame to be saved.
        Returns:
            SparkStreamSaver: A SparkStreamSaver instance for Parquet files.
        Raises:
            ValueError: If any of the inputs are invalid.
        Example Usage:
        from pyspark.sql import SparkSession
        from my_module import (
                DataType)
        from my_module import SparkStreamSaverFactory
        # Initialize Spark session
        spark = SparkSession.builder.appName(
                "DataSaverExample").getOrCreate()
            # Create a Parquet saver
            saver = SparkStreamSaverFactory().parquet_saver(
                data=df,
                file_path="/path/to/output.parquet",
                checkpoint_location="/path/to/checkpoint")
        """
        return self._create_saver(
            data,
            file_path,
            DataType.PARQUET,
            checkpoint_location)

    def delta_saver(
        self,
        data: DataFrame,
        file_path: str,
        checkpoint_location: str
    ) -> DataSaver:
        """
        Create a SparkStreamSaver instance for Delta files.
        Args:
            file_path (str): The file path of the Delta data to be saved.
            data (DataFrame): The Spark DataFrame to be saved.
        Returns:
            SparkStreamSaver: A SparkStreamSaver instance for Delta files.
        Raises:
            ValueError: If any of the inputs are invalid.
        Example Usage:
        from pyspark.sql import SparkSession
        from my_module import (
                DataType)
        from my_module import SparkStreamSaverFactory
        # Initialize Spark session
        spark = SparkSession.builder.appName(
                "DataSaverExample").getOrCreate()
            # Create a Delta saver
            saver = SparkStreamSaverFactory().delta_saver(
                data=df,
                file_path="/path/to/output.delta",
                checkpoint_location="/path/to/checkpoint")
        """
        return self._create_saver(
            data,
            file_path,
            DataType.DELTA,
            checkpoint_location)


class SparkStreamSaverProviderBase:
    """
    Base class for Spark Stream Saver Providers to handle common logic.
    """
    def __init__(
        self,
        factory
    ):
        """
        Initialize the SparkStreamSaverProviderBase for managing stream savers.
        This base provider class handles the shared logic for creating
        streaming data savers using a factory. It abstracts the common
        functionality needed for configuring and managing streaming
        savers for various file formats.
        Args:
            factory (SaverFactory): A factory instance for creating stream
            saver objects for different file formats (e.g., CSV, JSON,
            Parquet, Delta).
        Raises:
            ValueError: If the factory is invalid.
        Examples:
            # Example 1: Initializing the provider
            factory = SparkStreamSaverFactory()
            provider = SparkStreamSaverProviderBase(factory=factory)
            # Example 2: Creating a Parquet streaming saver
            saver = provider.create_saver(
                file_path="abfss://<storage_unit>@<account_name>.dfs.core.windows.net/<object_name>",
                data=df,
                data_type=DataType.PARQUET,
                checkpoint_location="abfss://<storage_unit>@<account_name>.dfs.core.windows.net/<object_name>"
            )
            saver.save_data(
                methods_with_args={
                    "trigger": {"availableNow": True}
                }
            )
        """
        self.logger = get_logger()
        # PandasValidationUtils.validate_inheritance(
        #     factory,
        #     SaverFactory,
        #     "factory")
        self.factory = factory
        PandasValidationUtils.log_init_arguments(self)

    def create_saver(
        self,
        data: DataFrame,
        file_path: str,
        data_type: DataType,
        checkpoint_location: str
    ):
        """
        Create a Spark Stream Saver for the specified file path and format.

        Args:
            data (DataFrame): The streaming Spark DataFrame to save.
            file_path (str): Path to save the streaming data.
            data_type (DataType): Format to save the data
                (e.g., 'csv', 'json').
            checkpoint_location (str): Location for checkpointing.

        Returns:
            DataSaver: Instance of a Spark Stream Saver.

        Raises:
            ValueError: If the file format is unsupported.

        Examples:
        # Example: Creating a CSV streaming saver
        saver = provider.create_saver(
            data=df,
            file_path="abfss://<storage_unit>@<account_name>.dfs.core.windows.net/<object_name>.csv",
            data_type=DataType.CSV,
            checkpoint_location="abfss://<storage_unit>@<account_name>.dfs.core.windows.net/<object_name>"
        )
        saver.save_data(
            methods_with_args={
                "trigger": {"availableNow": True}
            }
        )
        """
        self.logger.log(
            "info",
            f"Creating Spark Stream Saver for {file_path} " +
            f"({data_type}) with checkpoint at {checkpoint_location}"
        )
        match data_type:
            case DataType.CSV:
                return self.factory.csv_saver(
                    data,
                    file_path,
                    checkpoint_location)
            case DataType.JSON:
                return self.factory.json_saver(
                    data,
                    file_path,
                    checkpoint_location)
            case DataType.AVRO:
                return self.factory.avro_saver(
                    data,
                    file_path,
                    checkpoint_location)
            case DataType.PARQUET:
                return self.factory.parquet_saver(
                    data,
                    file_path,
                    checkpoint_location)
            case DataType.DELTA:
                return self.factory.delta_saver(
                    data,
                    file_path,
                    checkpoint_location)
            case _:
                error_message = f"Unsupported file format: {data_type.value}"
                self.logger.log(
                    "error",
                    error_message)
                raise ValueError(error_message)


class SparkCloudStreamSaverProvider(SparkStreamSaverProviderBase):
    """
    Initialize the SparkCloudStreamSaverProvider for saving streaming
    data to cloud storage.This provider extends the functionality of
    the base saver provider to handle cloud-specific configurations and
    file path resolution. It uses a `CloudConnector` to resolve storage
    paths and manage cloud configurations required for saving streaming
    data to services like Azure Blob Storage, AWS S3, or Google Cloud Storage.
    Args:
        factory (SaverFactory): A factory instance for creating streaming
            savers.
        connector (CloudConnector): A cloud connector instance for resolving
        file paths and managing cloud-specific configurations (e.g.,
        credentials, endpoints).
    Raises:
        ValueError: If the factory or connector is invalid.
    Examples:
        # Example 1: Initializing the provider
        factory = SparkStreamSaverFactory()
        provider = SparkCloudStreamSaverProvider(
            factory=factory, connector=connector, spark=spark)
        # Example 2: Creating a saver for cloud-based Parquet files
        saver = provider.create_saver(
            storage_unit="storage_unit",
            object_name="object_name",
            data=df,
            data_type=DataType.PARQUET,
            checkpoint_location="abfss://<storage_unit>@<account_name>.dfs.core.windows.net/<object_name>"
        )
        saver.save_data(
            methods_with_args={
                "trigger": {"availableNow": True}
            }
        )
    """
    def __init__(
        self,
        factory: SaverFactory,
        connector: CloudConnector,
        spark: SparkSession
    ):
        super().__init__(factory)
        self.connector = connector
        self.spark = spark
        PandasValidationUtils.validate_instance(
            connector,
            CloudConnector,
            "connector")

    def create_saver(
        self,
        data: DataFrame,
        storage_unit: str,
        object_name: str,
        data_type: DataType,
        checkpoint_location: str
    ):
        """
        Create a Spark Stream Saver for the specified cloud-based file path.

        Args:
            storage_unit (str): The storage unit for resolving file paths.
            object_name (str): The object name for resolving file paths.
            data (DataFrame): The streaming Spark DataFrame to save.
            data_type (DataType): Format to save the data
            checkpoint_location (str): Location for checkpointing.
        Returns:
            DataSaver: Instance of a Spark Stream Saver.
        Raises:
            ValueError: If the file format is unsupported.
        Examples:
            # Example: Creating a saver for cloud-based Parquet files
            saver = provider.create_saver(
                storage_unit="storage_unit",
                object_name="object_name",
                data=df,
                data_type=DataType.PARQUET,
                checkpoint_location="abfss://<storage_unit>@<account_name>.dfs.core.windows.net/<object_name>"
            )
            saver.save_data(
                methods_with_args={
                    "trigger": {"availableNow": True}
                }
            )
        """
        PandasValidationUtils.validate_is_non_empty_string(storage_unit)
        PandasValidationUtils.validate_is_non_empty_string(object_name)

        # Resolve file path using the connector
        file_path = self.connector.get_file_path(
            storage_unit,
            object_name,
            framework="spark")
        # Get the framework configuration for Spark
        spark_config = self.connector.get_framework_config("spark")

        # Set each configuration in Spark
        for key, value in spark_config.items():
            self.spark.conf.set(key, value)

        return super().create_saver(
            data,
            file_path,
            data_type,
            checkpoint_location)


class SparkLocalStreamSaverProvider(SparkStreamSaverProviderBase):
    """
    Initialize the SparkLocalStreamSaverProvider for saving streaming
    data locally. This provider is designed for saving streaming Spark
    DataFrames to local file systems, such as files on disk or within
    Databricks File System (DBFS). It manages the creation and configuration
    of savers for streaming data formats like JSON, CSV, Parquet, and Delta.
    Args:
        factory (SaverFactory): A factory instance for creating streaming
            savers for various file formats.
    Raises:
        ValueError: If the factory is invalid.
    Examples:
        # Example 1: Initializing the provider
        factory = SparkStreamSaverFactory()
        provider = SparkLocalStreamSaverProvider(factory=factory)
        # Example 2: Creating a saver for a local Parquet file
        saver = provider.create_saver(
            file_path="/path/to/output",
            data=streaming_df,
            data_type=DataType.PARQUET,
            checkpoint_location="/path/to/checkpoints"
        )
        saver.save_data(
            methods_with_args={
                "trigger": {"availableNow": True}
            }
        )
        # Example 3: Creating a saver for a CSV file with custom options
        saver = provider.create_saver(
            file_path="/path/to/output.csv",
            data=streaming_df,
            data_type=DataType.CSV,
            checkpoint_location="/path/to/csv_checkpoints"
        )
        saver.save_data(
            methods_with_args={
                "option": {"header": True, "delimiter": ","},
                "trigger": {"once": True}
            }
        )
    """
    def create_saver(
        self,
        data: DataFrame,
        file_path: str,
        data_type: DataType,
        checkpoint_location: str
    ):
        """
        Create a Spark Stream Saver for the specified local file path.

        Args:
            file_path (str): The local file path to save the streaming
                DataFrame.
            data (DataFrame): The streaming Spark DataFrame to save.
            data_type (DataType): Format to save the data.
            checkpoint_location (str): Location for checkpointing.
        Returns:
            DataSaver: Instance of a Spark Stream Saver.
        Raises:
            ValueError: If the file format is unsupported.

        Examples:
        # Example: Creating a saver for a local Parquet file
        saver = provider.create_saver(
            file_path="/path/to/output.parquet",
            data=streaming_df,
            data_type=DataType.PARQUET,
            checkpoint_location="/path/to/checkpoints"
        )
        saver.save_data(
            methods_with_args={
                "trigger": {"availableNow": True}
            }
        )

        """
        return super().create_saver(
            data,
            file_path,
            data_type,
            checkpoint_location)


class SparkDBConnector(DBConnector):
    """
    Spark implementation of DBConnector for SQL Server.

    This connector uses Spark's native JDBC functionality to interact
    with the database.
    """

    def __init__(
        self,
        spark: SparkSession,
        host: str,
        database: str,
        user: str,
        password: str,
        port: int = 1433,
    ):
        """
        Initialize SparkDBConnector.

        Args:
            spark (SparkSession): The active Spark session.
            host (str): Database server hostname or IP.
            database (str): Name of the database.
            user (str): Username for authentication.
            password (str): Password for authentication.
            port (int): Port number for SQL Server. Defaults to 1433.
        Example"
        # Step 1: Initialize SparkSession
        from my_module import SparkDBConnector
        spark = SparkSession.builder.appName(
            "SparkDBConnectorExample").getOrCreate()

        # Step 2: Initialize the SparkDBConnector
        connector = SparkDBConnector(
            spark=spark,
            host="<name>.database.windows.net",
            database="",
            user="",
            password="",
            port=1433,
        )

        # Step 3: Fetch Data
        query = "SELECT * FROM S_Curve_Data WHERE year = 2024"
        data = connector.fetch_data(query)
        data.display()
        """
        self.logger = get_logger()
        PandasValidationUtils.validate_is_non_empty_string(
            host)
        PandasValidationUtils.validate_is_non_empty_string(
            database)
        PandasValidationUtils.validate_is_non_empty_string(
            user)
        PandasValidationUtils.validate_is_non_empty_string(
            password)
        PandasValidationUtils.validate_is_integer(
            port,
            'port')
        super().__init__(host, database, user, password)
        self.spark = spark
        self.port = port
        self.logger.log("info", "SparkDBConnector initialized successfully")
        PandasValidationUtils.log_init_arguments(self)

    def connect(self):
        """
        Connection conceptually exists via SparkSession; nothing to implement.

        Example:
        # Example: Connecting to the SparkDBConnector
        from my_module import SparkDBConnector

        spark = SparkSession.builder.appName(
            "SparkDBConnectorExample").getOrCreate()
        connector = SparkDBConnector(
            spark=spark,
            host="<name>.database.windows.net",
            database="",
            user="",
            password="",
            port=1433,
        )
        connector.connect()

        """
        self.logger.log("info", "SparkSession manages connections implicitly.")

    def fetch_data(
        self,
        query: str,
    ) -> DataFrame:
        """
        Fetch data from SQL Server as a Spark DataFrame.

        Args:
            query (str): SQL query string to execute.

        Returns:
            DataFrame: A Spark DataFrame containing query results.
        Raises:
        NotImplementedError: Direct execution of arbitrary queries
        isn't supported via Spark JDBC.
        Examples:
        # Example: Fetching data from SQL Server
        from my_module import SparkDBConnector
        spark = SparkSession.builder.appName(
            "SparkDBConnectorExample").getOrCreate()
        connector = SparkDBConnector(
            spark=spark,
            host="<name>.database.windows.net",
            database="",
            user="",
            password="",
            port=1433)

        query = "SELECT * FROM S_Curve_Data WHERE year = 2024"
        data = connector.fetch_data(query)
        data.display()

        """
        PandasValidationUtils.validate_is_non_empty_string(
            query)
        self.logger.log("info", f"Fetching data with query: {query}")
        try:
            jdbc_url = (
                f"jdbc:sqlserver://{self.host}:{self.port};" +
                f"databaseName={self.database};" +
                f"user={self.user};password={self.password}"
            )
            df = (
                self.spark.read.format("jdbc")
                .option("url", jdbc_url)
                .option("query", query)
                .option(
                    "driver",
                    "com.microsoft.sqlserver.jdbc.SQLServerDriver")
                .load()
            )
            self.logger.log(
                "info",
                "Data fetched successfully as Spark DataFrame.")
            return df
        except Exception as e:
            error_message = f"Error fetching data: {e}"
            self.logger.log("error", error_message)
            raise Exception(error_message)

    def execute_query(
        self,
        query: str
    ):
        """
        Execute a non-SELECT SQL query (e.g., INSERT, UPDATE, DELETE) using
        Spark's JDBC writer.

        Args:
            query (str): SQL query string.

        Raises:
            NotImplementedError: Direct execution of arbitrary queries
                isn't supported via Spark JDBC.
        """
        PandasValidationUtils.validate_is_non_empty_string(
            query
        )
        self.logger.log(
            "error",
            "execute_query is not supported in Spark JDBC mode.")
        raise NotImplementedError(
            "Non-SELECT operations like INSERT/UPDATE " +
            "must use Spark DataFrame writes."
        )

    def write_data(
        self,
        df: DataFrame,
        table: str,
        mode: str = "append"
    ):
        """
        Write a Spark DataFrame to a database table.

        Args:
            df (DataFrame): The Spark DataFrame to write.
            table (str): Target table name (e.g., "dbo.my_table").
            mode (str): Write mode ('append', 'overwrite', 'error', 'ignore').
        Raises:
            FailedToWriteDataError: If the write operation fails.

        Examples:
        # Example: Writing a Spark DataFrame to SQL Server
        from my_module import SparkDBConnector
        spark = SparkSession.builder.appName(
            "SparkDBConnectorExample").getOrCreate()
        connector = SparkDBConnector(
            spark=spark,
            host="<name>.database.windows.net",
            database="",
            user="",
            password="",
            port=1433)

        df = spark.createDataFrame([
            ("John Doe", 25, "New York"),
            ("Jane Smith", 30, "Los Angeles")
        ], ["name", "age", "city"])

        connector.write_data(df, "dbo.my_table", mode="overwrite")

        Returns:
            None
        """
        SparkValidationUtils.validate_is_dataframe(
            df,
            "df")
        PandasValidationUtils.validate_is_non_empty_string(
            table)
        PandasValidationUtils.validate_is_non_empty_string(
            mode)
        self.logger.log(
            "info",
            f"Writing DataFrame to table: {table} in mode: {mode}")
        try:
            jdbc_url = (
                f"jdbc:sqlserver://{self.host}:{self.port};" +
                f"databaseName={self.database};" +
                f"user={self.user};password={self.password}"
            )
            df.write.format(
                "jdbc").option("url", jdbc_url).option(
                    "dbtable", table).option(
                "driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver"
            ).mode(mode).save()
            self.logger.log(
                "info",
                f"Data written successfully to table: {table}")
        except Exception as e:
            self.logger.log(
                "error",
                f"Failed to write data: {e}")
            raise


# ######### Validators ##################

class SparkMissingColumnsValidator(Validator):
    """
    Validator to ensure required columns are present in a Spark DataFrame.
    Attributes:
        required_columns (list): A list of column names expected to be in
            the DataFrame.
    Example Usage:
        validator = SparkMissingColumnsValidator(
            required_columns=["col1", "col2", "col3"])
        data = spark.createDataFrame([(1, 2)], ["col1", "col2"])
        result = validator.validate(data)
        print(result)
        # Output:
        # {
        #     "validator": "SparkMissingColumnsValidator",
        #     "is_valid": False,
        #     "errors": [{"error_type": "missing_columns",
        "details": "Missing columns: ['col3']"}],
        #     "invalid_columns": ["col3"]
        # }
    """
    def __init__(self, required_columns: list):
        """
        Initialize the SparkMissingColumnsValidator.
        Args:
            required_columns (list): A list of column names expected to be in
            the DataFrame.
        """
        self.logger = get_logger()
        PandasValidationUtils.validate_is_non_empty_list(required_columns)
        self.required_columns = required_columns
        self.logger.log(
            "info",
            f"Initialized with required columns: {required_columns}")

    def validate(self, data: DataFrame) -> dict:
        """
        Validate that the required columns are present in the DataFrame.
        Args:
            data (DataFrame): The Spark DataFrame to validate.
        Returns:
            dict: Validation result with the following keys:
                - "validator" (str): Name of the validator.
                - "is_valid" (bool): Whether the validation passed.
                - "errors" (list): List of errors, if any.
                - "invalid_columns" (list): List of missing columns.
        """
        self.logger.log("info", "Validating presence of required columns.")
        SparkValidationUtils.validate_is_dataframe(data, "data")
        missing_columns = SparkValidationUtils.check_missing_columns(
            data,
            self.required_columns,
            False)
        if missing_columns:
            self.logger.log(
                "error",
                f"Missing columns detected: {missing_columns}")
            return {
                "validator": "SparkMissingColumnsValidator",
                "is_valid": False,
                "errors": [{
                    "error_type": "missing_columns",
                    "details": f"Missing columns: {missing_columns}"}],
                "invalid_columns": missing_columns,
            }
        self.logger.log("info", "All required columns are present.")
        return {
            "validator": "SparkMissingColumnsValidator",
            "is_valid": True,
            "errors": [],
            "invalid_columns": [],
        }


class SparkExtraColumnsValidator(Validator):
    """
        Validator to ensure no unexpected columns are present in
        a Spark DataFrame.
        Attributes:
            allowed_columns (list): A list of allowed column names
            in the DataFrame.
        Example Usage:
            validator = SparkExtraColumnsValidator(
                allowed_columns=["col1", "col2", "col3"])
            data = spark.createDataFrame(
                [(1, 2, 3, 4)], ["col1", "col2", "col3", "extra_col"])
            result = validator.validate(data)
            print(result)
            # Output:
            # {
            #     "validator": "SparkExtraColumnsValidator",
            #     "is_valid": False,
            #     "errors": [{"error_type": "extra_columns",
            "details": "Unexpected columns: ['extra_col']"}],
            #     "extra_columns": ["extra_col"]
            # }
        """

    def __init__(self, allowed_columns: list):
        """
        Initialize the SparkExtraColumnsValidator.
        Args:
            allowed_columns (list): A list of allowed column names
            in the DataFrame.
        """
        self.logger = get_logger()
        PandasValidationUtils.validate_is_non_empty_list(allowed_columns)
        self.allowed_columns = allowed_columns
        self.logger.log(
            "info",
            f"Initialized with allowed columns: {allowed_columns}")

    def validate(self, data: DataFrame) -> dict:
        """
        Validate that no unexpected columns are present in the DataFrame.
        Args:
            data (DataFrame): The Spark DataFrame to validate.
        Returns:
            dict: Validation result with the following keys:
                - "validator" (str): Name of the validator.
                - "is_valid" (bool): Whether the validation passed.
                - "errors" (list): List of errors, if any.
                - "extra_columns" (list): List of unexpected columns.
        """
        self.logger.log("info", "Validating for unexpected columns.")
        SparkValidationUtils.validate_is_dataframe(data, "data")

        extra_columns = list(set(data.columns) - set(self.allowed_columns))

        if extra_columns:
            self.logger.log
            ("error",
                f"Unexpected columns detected: {extra_columns}")
            return {
                "validator": "SparkExtraColumnsValidator",
                "is_valid": False,
                "errors": [{"error_type": "extra_columns",
                            "details": (
                                f"Unexpected columns: {extra_columns}")}],
                "extra_columns": extra_columns,
            }
        self.logger.log(
            "info",
            "No unexpected columns found.")
        return {
            "validator": "SparkExtraColumnsValidator",
            "is_valid": True,
            "errors": [],
            "extra_columns": [],
        }


class SparkDataTypeValidator(Validator):
    """
    Validator to ensure column data types match the expected schema
    in a Spark DataFrame.
    Attributes:
        expected_schema (dict): Dictionary mapping column names to
            expected data types.
    Example Usage:
        validator = SparkDataTypeValidator(
            expected_schema={
                "col1": IntegerType(),
                "col2": StringType()
            }
        )
        data = spark.createDataFrame([(1, "A")], ["col1", "col2"])
        result = validator.validate(data)
        print(result)
        # Output:
        # {
        #     "validator": "SparkDataTypeValidator",
        #     "is_valid": True,
        #     "errors": [],
        #     "invalid_columns": [],
        #     "missing_columns": []
        # }
    """
    def __init__(self, expected_schema: dict):
        """
        Initialize the SparkDataTypeValidator.
        Args:
            expected_schema (dict): A dictionary mapping column names to
            expected data types.
        """
        self.logger = get_logger()
        PandasValidationUtils.validate_is_non_empty_dict(expected_schema)
        self.expected_schema = expected_schema
        self.logger.log(
            "info",
            f"Initialized with expected schema: {expected_schema}")

    def validate(self, data: DataFrame) -> dict:
        """
        Validate that column data types in the DataFrame match the
        expected schema.
        Args:
            data (DataFrame): The Spark DataFrame to validate.
        Returns:
            dict: Validation result with the following keys:
                - "validator" (str): Name of the validator.
                - "is_valid" (bool): Whether the validation passed.
                - "errors" (list): List of errors, if any.
                - "invalid_columns" (list): List of columns with incorrect
                    data types.
                - "missing_columns" (list): List of columns missing
                    from the dataset.
        """
        self.logger.log(
            "info",
            "Validating column data types against the expected schema.")
        SparkValidationUtils.validate_is_dataframe(data, "data")
        missing_columns = []
        invalid_columns = []
        errors = []
        # Step 1: Check for missing columns
        missing_columns = SparkValidationUtils.check_missing_columns(
            data,
            list(self.expected_schema.keys()),
            False)
        if missing_columns:
            self.logger.log(
                "error",
                f"Missing columns: {missing_columns}")
            errors.extend([
                {
                    "error_type": "missing_column",
                    "details": f"Missing column: {col}"}
                for col in missing_columns
            ])

        for column, expected_dtype in self.expected_schema.items():
            if column in data.columns:
                actual_dtype = data.schema[column].dataType
                if actual_dtype != expected_dtype:
                    self.logger.log(
                        "error",
                        f"Type mismatch for column '{column}': " +
                        f"Expected {expected_dtype}, Got {actual_dtype}"
                    )
                    errors.append({
                        "error_type": "type_mismatch",
                        "details": f"Column '{column}' has incorrect type. " +
                        f"Expected: {expected_dtype}, Got: {actual_dtype}"
                    })
                    invalid_columns.append(column)

        result = {
            "validator": "SparkDataTypeValidator",
            "is_valid": not bool(errors),
            "errors": errors,
            "invalid_columns": invalid_columns,
            "missing_columns": missing_columns,
        }
        if errors:
            self.logger.log(
                "error",
                f"Data type validation failed with {len(errors)} errors.")
        else:
            self.logger.log(
                "info",
                "Data type validation passed successfully.")
        return result


class SparkNullValueValidator(Validator):
    """
    Validator to check for null or empty values in critical columns
    of a Spark DataFrame.
    Attributes:
        critical_columns (list): List of critical columns to validate.
        null_values (list): List of values considered as null/empty.
    Example Usage:
        validator = SparkNullValueValidator(
            critical_columns=["col1", "col2"],
            null_values=["", None]
        )
        data = spark.createDataFrame([(1, None), (2, ""),
        (3, "valid")], ["col1", "col2"])
        result = validator.validate(data)
        print(result)
        # Output:
        # {
        #     "validator": "SparkNullValueValidator",
        #     "is_valid": False,
        #     "errors": [{"error_type": "null_values",
        "details": "Column 'col2' contains null/empty values."}],
        #     "invalid_rows": DataFrame,  # Rows with null/empty values
        #     "missing_columns": []
        # }
    """
    def __init__(self, critical_columns: list, null_values: list = None):
        """
        Initialize the SparkNullValueValidator.
        Args:
            critical_columns (list): List of critical columns to validate.
            null_values (list): Values considered as null/empty.
                Defaults to [None, ""]
        """
        self.logger = get_logger()
        PandasValidationUtils.validate_is_non_empty_list(critical_columns)
        self.critical_columns = critical_columns
        self.null_values = null_values or [None, ""]

    def validate(self, data: DataFrame) -> dict:
        """
        Validate the DataFrame for null or empty values in critical columns.
        Args:
            data (DataFrame): The Spark DataFrame to validate.
        Returns:
            dict: Validation result with the following keys:
                - "validator" (str): Name of the validator.
                - "is_valid" (bool): Whether the validation passed.
                - "errors" (list): List of errors, if any.
                - "invalid_rows" (DataFrame): Rows with null/empty values.
                - "missing_columns" (list): List of missing columns.
        """
        self.logger.log(
            "info",
            "Validating critical columns for null or empty values.")
        SparkValidationUtils.validate_is_dataframe(data, "data")
        errors = []
        invalid_rows = None
        # Step 1: Check for missing columns
        missing_columns = SparkValidationUtils.check_missing_columns(
            data,
            self.critical_columns,
            False)
        if missing_columns:
            for column in missing_columns:
                errors.append({
                    "error_type": "missing_column",
                    "details": f"Column '{column}' is missing from the dataset"
                })
            self.logger.log("error", f"Missing columns: {missing_columns}")
        # Step 2: Validate for null or empty values
        for col_name in set(self.critical_columns) - set(missing_columns):
            condition = (col(col_name).isNull() | isnan(col(col_name)))
            if self.null_values:
                condition |= col(col_name).isin(self.null_values)
            invalid_data = data.filter(condition)
            if invalid_data.count() > 0:
                errors.append({
                    "error_type": "null_values",
                    "details": (
                        f"Column '{col_name}' contains null/empty values.")
                })
                self.logger.log(
                    "error",
                    f"Column '{col_name}' contains null/empty values.")
                invalid_rows = invalid_data if (
                    invalid_rows) is None else invalid_rows\
                    .union(invalid_data)
        # Prepare the validation result
        result = {
            "validator": "SparkNullValueValidator",
            "is_valid": not bool(errors),
            "errors": errors,
            "invalid_rows": invalid_rows if invalid_rows else data.limit(0),
        }
        if errors:
            self.logger.log(
                "error",
                f"Null value validation failed with {len(errors)} errors.")
        else:
            self.logger.log(
                "info",
                "Null value validation passed successfully.")
        return result


class SparkRangeValidator(Validator):
    """
    Validator to ensure numerical values fall within specified ranges
    for columns in a Spark DataFrame.

    Attributes:
        column_ranges (dict): Dictionary specifying the range for each column.
        inclusive (bool): If True, range boundaries are inclusive.
            Defaults to True.

    Example Usage:
        validator = SparkRangeValidator(
            column_ranges={"col1": (0.0, 100.0), "col2": (10.0, 50.0)},
            inclusive=True
        )
        data = spark.createDataFrame([(5, 20), (110, 30)], ["col1", "col2"])
        result = validator.validate(data)
        print(result)
        # Output:
        # {
        #     "validator": "SparkRangeValidator",
        #     "is_valid": False,
        #     "errors": [
        #         {"error_type": "range_violation", "details": "Column 'col1'
        # has values outside the inclusive range (0, 100)."}
        #     ],
        #     "invalid_rows": DataFrame,  # Rows with out-of-range values
        #     "missing_columns": []
        # }
    """

    def __init__(self, column_ranges: dict, inclusive: bool = True):
        """
        Initialize the SparkRangeValidator.

        Args:
            column_ranges (dict): Dictionary of column names and their allowed
                (min, max) ranges.
            inclusive (bool): If True, range boundaries are inclusive.
                Defaults to True.
        """
        self.logger = get_logger()
        PandasValidationUtils.validate_is_non_empty_dict(column_ranges)
        self.column_ranges = column_ranges
        PandasValidationUtils.validate_is_boolean(inclusive)
        self.inclusive = inclusive
        self.logger.log(
            "info", (
                f"Initialized with column ranges: {column_ranges}, " +
                f"inclusive={inclusive}"))

    def validate(self, data: DataFrame) -> dict:
        """
        Validate the DataFrame to ensure values in specified columns
        fall within defined ranges.

        Args:
            data (DataFrame): The Spark DataFrame to validate.

        Returns:
            dict: Validation result with the following keys:
                - "validator" (str): Name of the validator.
                - "is_valid" (bool): Whether the validation passed.
                - "errors" (list): List of errors, if any.
                - "invalid_rows" (DataFrame): Rows with out-of-range values.
                - "missing_columns" (list): List of missing columns.
        """
        self.logger.log(
            "info",
            f"Starting range validation with inclusive={self.inclusive}.")
        SparkValidationUtils.validate_is_dataframe(data, "data")

        errors = []
        invalid_rows = None

        # Step 1: Check for missing columns
        missing_columns = SparkValidationUtils.check_missing_columns(
            data,
            list(self.column_ranges.keys()),
            False)
        if missing_columns:
            for col_name in missing_columns:
                errors.append({
                    "error_type": "missing_column",
                    "details": (
                        f"Column '{col_name}' is missing from the dataset.")
                })
                self.logger.log(
                    "error",
                    f"Column '{col_name}' is missing from the dataset.")

        # Step 2: Validate ranges for existing columns using
        # `check_value_range`
        for col_name, (min_val, max_val) in self.column_ranges.items():
            if col_name not in missing_columns:
                invalid_data = SparkValidationUtils.check_value_range(
                    data, col_name, min_val, max_val, self.inclusive
                )

                if invalid_data.count() > 0:
                    errors.append({
                        "error_type": "range_violation",
                        "details": (
                            f"Column '{col_name}' has values outside the " +
                            f"{'inclusive' if self.inclusive else 'exclusive'}"
                            + f"range ({min_val}, {max_val}).")
                    })
                    self.logger.log(
                        "error",
                        f"Column '{col_name}' has values outside the " +
                        f"{'inclusive' if self.inclusive else 'exclusive'} " +
                        f"range ({min_val}, {max_val})."
                    )
                    invalid_rows = invalid_data if invalid_rows is None\
                        else invalid_rows.union(invalid_data)

        # Step 3: Prepare the validation result
        result = {
            "validator": "SparkRangeValidator",
            "is_valid": not bool(errors),
            "errors": errors,
            "invalid_rows": invalid_rows if invalid_rows else data.limit(0),
            "missing_columns": missing_columns,
        }

        if errors:
            self.logger.log(
                "error",
                f"Range validation failed with {len(errors)} errors.")
        else:
            self.logger.log(
                "info",
                "Range validation passed successfully.")

        return result


class SparkRowCountValidator(Validator):
    """
    Validator to ensure the dataset meets a specified row count range.

    This validator checks if the number of rows in a Spark DataFrame
    falls within a defined range.

    Attributes:
        min_rows (int, optional): Minimum number of rows required.
        max_rows (int, optional): Maximum number of rows allowed.

    Example Usage:
        validator = SparkRowCountValidator(min_rows=2, max_rows=5)
        data = spark.createDataFrame(
            [(1, "a"), (2, "b"), (3, "c")], ["col1", "col2"])
        result = validator.validate(data)
        print(result)
    """

    def __init__(self, min_rows: int = None, max_rows: int = None):
        """
        Initialize the SparkRowCountValidator.

        Args:
            min_rows (int, optional): Minimum number of rows required.
                Defaults to None.
            max_rows (int, optional): Maximum number of rows allowed.
                Defaults to None.
        """
        self.logger = get_logger()

        # Validate min_rows and max_rows using PandasValidationUtils
        if min_rows is not None:
            PandasValidationUtils.validate_is_integer(min_rows, "min_rows")
            if min_rows < 0:
                error_message = "min_rows must be a positive integer."
                self.logger.log("error", error_message)
                raise ValueError(error_message)

        if max_rows is not None:
            PandasValidationUtils.validate_is_integer(max_rows, "max_rows")
            if max_rows < 0:
                error_message = "max_rows must be a positive integer."
                self.logger.log("error", error_message)
                raise ValueError(error_message)

        if min_rows is not None and (
                max_rows) is not None and min_rows > max_rows:
            error_message = "min_rows cannot be greater than max_rows."
            self.logger.log(
                "error",
                error_message)
            raise ValueError(error_message)

        self.min_rows = min_rows
        self.max_rows = max_rows
        self.logger.log(
            "info",
            f"Initialized with min_rows={min_rows}, max_rows={max_rows}")

    def validate(self, data: DataFrame) -> dict:
        """
        Validate the row count of the DataFrame.

        Args:
            data (DataFrame): The Spark DataFrame to validate.

        Returns:
            dict: Validation result with the following keys:
                - "validator" (str): Name of the validator.
                - "is_valid" (bool): Whether the validation passed.
                - "errors" (list): List of errors, if any.
                - "invalid_rows" (DataFrame): Empty DataFrame
                    (always returned for compatibility).
        """
        self.logger.log("info", "Validating row count.")
        SparkValidationUtils.validate_is_dataframe(data, "data")

        # Get the row count
        row_count = data.count()
        self.logger.log("info", f"Row count: {row_count}")

        errors = []

        # Step 1: Check min_rows
        if self.min_rows is not None and row_count < self.min_rows:
            errors.append({
                "error_type": "row_count_violation",
                "details": f"Row count {row_count} " +
                f"is less than the minimum required {self.min_rows}."
            })
            self.logger.log(
                "error",
                f"Row count {row_count} " +
                f"is less than the minimum required {self.min_rows}."
            )

        # Step 2: Check max_rows
        if self.max_rows is not None and row_count > self.max_rows:
            errors.append({
                "error_type": "row_count_violation",
                "details": f"Row count {row_count} " +
                f"exceeds the maximum allowed {self.max_rows}."
            })
            self.logger.log(
                "error", (
                    f"Row count {row_count} exceeds the maximum allowed " +
                    f"{self.max_rows}.")
            )

        # Step 3: Prepare the validation result
        result = {
            "validator": "SparkRowCountValidator",
            "is_valid": not bool(errors),
            "errors": errors,
            "invalid_rows": data.limit(0),
        }

        if errors:
            self.logger.log(
                "error",
                f"Row count validation failed with {len(errors)} errors.")
        else:
            self.logger.log(
                "info",
                "Row count validation passed successfully.")

        return result


class SparkNonEmptyValidator(Validator):
    """
    Validator to ensure the dataset is not empty.

    This validator checks if a Spark DataFrame contains at least one row and
        one column.

    Example Usage:
        validator = SparkNonEmptyValidator()
        data = spark.createDataFrame([(1, "a")], ["col1", "col2"])
        result = validator.validate(data)
        print(result)
    """

    def __init__(self):
        """
        Initialize the SparkNonEmptyValidator.
        """
        self.logger = get_logger()
        self.logger.log("info", "Initialized SparkNonEmptyValidator.")

    def validate(self, data: DataFrame) -> dict:
        """
        Validate if the DataFrame is not empty.

        Args:
            data (DataFrame): The Spark DataFrame to validate.

        Returns:
            dict: Validation result with the following keys:
                - "validator" (str): Name of the validator.
                - "is_valid" (bool): Whether the validation passed.
                - "errors" (list): List of errors, if any.
                - "invalid_rows" (DataFrame): Entire dataset if it is empty.
        """
        self.logger.log("info", "Validating if the dataset is non-empty.")
        SparkValidationUtils.validate_is_dataframe(data, "data")

        errors = []

        # Step 1: Check if the DataFrame has at least one column
        if not data.columns:
            errors.append({
                "error_type": "empty_columns",
                "details": "The dataset has no columns."
            })
            self.logger.log("error", "The dataset has no columns.")

        # Step 2: Check if the DataFrame has at least one row
        row_count = data.count()
        if row_count == 0:
            errors.append({
                "error_type": "empty_rows",
                "details": "The dataset has no rows."
            })
            self.logger.log("error", "The dataset has no rows.")

        # Prepare the validation result
        result = {
            "validator": "SparkNonEmptyValidator",
            "is_valid": not bool(errors),
            "errors": errors,
            "invalid_rows": data if errors else data.limit(0),
        }

        if errors:
            self.logger.log(
                "error",
                f"Non-empty validation failed with {len(errors)} errors.")
        else:
            self.logger.log(
                "info",
                "Non-empty validation passed successfully.")

        return result


class SparkSchemaValidator(Validator):
    """
    Validator to ensure a Spark DataFrame matches the expected schema.

    Attributes:
        expected_schema (StructType): The expected schema
            (column names and data types).

    Example Usage:
        from pyspark.sql.types import (
            StructType, StructField, IntegerType, StringType)

        expected_schema = StructType([
            StructField("col1", IntegerType(), True),
            StructField("col2", StringType(), True)
        ])

        validator = SparkSchemaValidator(expected_schema=expected_schema)
        data = spark.createDataFrame([(1, "a"), (2, "b")], ["col1", "col2"])
        result = validator.validate(data)
        print(result)
        # Output:
        # {
        #     "validator": "SparkSchemaValidator",
        #     "is_valid": True,
        #     "errors": [],
        #     "missing_columns": [],
        #     "mismatched_columns": [],
        #     "invalid_rows": <empty DataFrame>
        # }
    """

    def __init__(self, expected_schema: StructType):
        """
        Initialize the SparkSchemaValidator.

        Args:
            expected_schema (StructType): The expected schema for
                the DataFrame.
        """
        self.logger = get_logger()
        PandasValidationUtils.validate_instance(
            expected_schema,
            StructType,
            "expected_schema")
        self.expected_schema = expected_schema
        self.logger.log(
            "info", (
                "Initialized with expected schema: " +
                f"{expected_schema.simpleString()}"))

    def validate(self, data: DataFrame) -> dict:
        """
        Validate that the DataFrame matches the expected schema.

        Args:
            data (DataFrame): The Spark DataFrame to validate.

        Returns:
            dict: Validation result with the following keys:
                - "validator" (str): Name of the validator.
                - "is_valid" (bool): Whether the validation passed.
                - "errors" (list): List of errors, if any.
                - "missing_columns" (list): Columns missing from the DataFrame.
                - "mismatched_columns" (list): Columns with mismatched
                    data types.
                - "invalid_rows" (DataFrame): Empty DataFrame
                    (always returned for compatibility).
        """
        self.logger.log("info", "Validating DataFrame schema.")
        SparkValidationUtils.validate_is_dataframe(data, "data")

        errors = []
        missing_columns = []
        mismatched_columns = []

        # Step 1: Check for missing columns
        actual_columns = {field.name for field in data.schema.fields}
        expected_columns = {
            field.name for field in self.expected_schema.fields}
        missing_columns = list(expected_columns - actual_columns)

        if missing_columns:
            for column in missing_columns:
                errors.append({
                    "error_type": "missing_column",
                    "details": (
                        f"Column '{column}' is missing from the dataset.")
                })
            self.logger.log(
                "error",
                f"Missing columns: {missing_columns}")

        # Step 2: Check for mismatched column data types
        for field in self.expected_schema.fields:
            col_name = field.name
            if col_name in actual_columns:
                actual_field = next((
                    f for f in data.schema.fields if f.name == col_name), None)
                if actual_field and actual_field.dataType != field.dataType:
                    mismatched_columns.append({
                        "column": col_name,
                        "expected_type": field.dataType,
                        "actual_type": actual_field.dataType
                    })
                    errors.append({
                        "error_type": "mismatched_column",
                        "details": (
                            f"Column '{col_name}' has type mismatch. " +
                            f"Expected: {field.dataType} " +
                            f"Got: {actual_field.dataType}")
                    })
                    self.logger.log(
                        "error",
                        f"Column '{col_name}' has type mismatch. "
                        f"Expected: {field.dataType}, " +
                        f"Got: {actual_field.dataType}."
                    )

        # Step 3: Prepare the validation result
        result = {
            "validator": "SparkSchemaValidator",
            "is_valid": not bool(errors),
            "errors": errors,
            "missing_columns": missing_columns,
            "mismatched_columns": mismatched_columns,
            "invalid_rows": data.limit(0),
        }

        if errors:
            self.logger.log(
                "error",
                f"Schema validation failed with {len(errors)} errors.")
        else:
            self.logger.log(
                "info",
                "Schema validation passed successfully.")

        return result


class SparkRegexValidator(Validator):
    """
    Validator to ensure column values match specific regex patterns.

    Attributes:
        column_patterns (dict): A dictionary where keys are column names
        and values are regex patterns.

    Example Usage:
        from pyspark.sql import SparkSession

        spark = SparkSession.builder.getOrCreate()
        data = spark.createDataFrame([
            ("user1@example.com", "123-456-7890"),
            ("user2@example.com", "987-654-3210"),
            ("invalid_email", "invalid_phone")
        ], ["email", "phone"])

        patterns = {
            "email": "^[\\w\\.\\-]+@[\\w\\.\\-]+\\.\\w+$",
            "phone": "^\\d{3}-\\d{3}-\\d{4}$"
        }

        validator = SparkRegexValidator(column_patterns=patterns)
        result = validator.validate(data)
        print(result)
    """

    def __init__(self, column_patterns: dict):
        """
        Initialize the SparkRegexValidator.

        Args:
            column_patterns (dict): Dictionary where keys are column names
            and values are regex patterns.
        """
        self.logger = get_logger()
        PandasValidationUtils.validate_is_non_empty_dict(column_patterns)
        self.column_patterns = column_patterns

        # Validate provided regex patterns
        for column, pattern in column_patterns.items():
            try:
                re.compile(pattern)  # Check if the pattern is valid
            except re.error as e:
                error_message = (
                    f"Invalid regex pattern for column '{column}': {e}")
                self.logger.log(
                    "error",
                    error_message)
                raise ValueError(error_message)

        self.logger.log(
            "info",
            f"Initialized with column patterns: {column_patterns}")

    def validate(self, data: DataFrame) -> dict:
        """
        Validate that column values match their respective regex patterns.

        Args:
            data (DataFrame): The Spark DataFrame to validate.

        Returns:
            dict: Validation result with the following keys:
                - "validator" (str): Name of the validator.
                - "is_valid" (bool): Whether the validation passed.
                - "errors" (list): List of errors, if any.
                - "invalid_rows" (DataFrame): Rows with values
                    that fail validation.
        """
        self.logger.log(
            "info",
            "Validating column values against regex patterns.")
        SparkValidationUtils.validate_is_dataframe(data, "data")

        errors = []
        invalid_rows = None

        # Step 1: Validate column values against patterns
        for col_name, pattern in self.column_patterns.items():
            if col_name not in data.columns:
                errors.append({
                    "error_type": "missing_column",
                    "details": (
                        f"Column '{col_name}' is missing from the dataset.")
                })
                self.logger.log(
                    "error",
                    f"Column '{col_name}' is missing from the dataset.")
                continue

            # Filter rows that do not match the pattern
            invalid_data = data.filter(~col(col_name).rlike(pattern))

            if invalid_data.count() > 0:
                errors.append({
                    "error_type": "regex_violation",
                    "details": f"Column '{col_name}' " +
                    "contains values not matching the " +
                    f"regex pattern '{pattern}'."
                })
                self.logger.log(
                    "error",
                    f"Column '{col_name}' " +
                    "contains values not matching the " +
                    f"regex pattern '{pattern}'."
                )
                invalid_rows = (
                    invalid_data if invalid_rows is None else
                    invalid_rows.union(invalid_data))

        # Ensure invalid_rows contains only unique rows
        if invalid_rows:
            invalid_rows = invalid_rows.dropDuplicates()

        # Prepare the validation result
        result = {
            "validator": "SparkRegexValidator",
            "is_valid": not bool(errors),
            "errors": errors,
            "invalid_rows": invalid_rows if invalid_rows else data.limit(0),
        }

        if errors:
            self.logger.log(
                "error",
                f"Regex validation failed with {len(errors)} errors.")
        else:
            self.logger.log("info", "Regex validation passed successfully.")

        return result


class SparkColumnTypeValidator(Validator):
    """
    Validator to ensure specified columns have the expected data types.

    Attributes:
        column_types (dict): A dictionary where keys are column names and
        values are expected data types.

    Example Usage:
        from pyspark.sql.types import IntegerType, StringType

        data = spark.createDataFrame([
            (1, "a"),
            (2, "b")
        ], ["col1", "col2"])

        column_types = {
            "col1": IntegerType(),
            "col2": StringType()
        }

        validator = SparkColumnTypeValidator(column_types=column_types)
        result = validator.validate(data)
        print(result)
    """

    def __init__(self, column_types: dict):
        """
        Initialize the SparkColumnTypeValidator.

        Args:
            column_types (dict): Dictionary where keys are column names
                and values are expected data types.
        """
        self.logger = get_logger()
        PandasValidationUtils.validate_is_non_empty_dict(column_types)
        self.column_types = column_types

        # Validate provided data types
        for column, dtype in column_types.items():
            if not isinstance(dtype, DataType):
                error_message = (
                    f"Invalid data type for column '{column}': " +
                    "Expected a Spark DataType instance.")
                self.logger.log(
                    "error",
                    error_message
                )
                raise ValueError(error_message)

        self.logger.log(
            "info",
            f"Initialized with column types: {column_types}")

    def validate(self, data: DataFrame) -> dict:
        """
        Validate that specified columns have the expected data types.

        Args:
            data (DataFrame): The Spark DataFrame to validate.

        Returns:
            dict: Validation result with the following keys:
                - "validator" (str): Name of the validator.
                - "is_valid" (bool): Whether the validation passed.
                - "errors" (list): List of errors, if any.
                - "mismatched_columns" (list): List of columns with
                    mismatched data types.
        """
        self.logger.log("info", "Validating column data types.")
        SparkValidationUtils.validate_is_dataframe(data, "data")

        errors = []
        mismatched_columns = []

        # Step 1: Validate column data types
        for col_name, expected_type in self.column_types.items():
            if col_name not in data.columns:
                errors.append({
                    "error_type": "missing_column",
                    "details": (
                        f"Column '{col_name}' is missing from the dataset.")
                })
                self.logger.log(
                    "error",
                    f"Column '{col_name}' is missing from the dataset.")
                continue

            # Check the actual column type
            actual_field = next(
                (f for f in data.schema.fields if f.name == col_name), None)
            if actual_field and actual_field.dataType != expected_type:
                mismatched_columns.append({
                    "column": col_name,
                    "expected_type": expected_type.simpleString(),
                    "actual_type": actual_field.dataType.simpleString()
                })
                errors.append({
                    "error_type": "type_mismatch",
                    "details": (
                        f"Column '{col_name}' has a type mismatch. "
                        f"Expected: {expected_type.simpleString()}, " +
                        f"Got: {actual_field.dataType.simpleString()}.")
                })
                self.logger.log(
                    "error",
                    f"Column '{col_name}' has a type mismatch. "
                    f"Expected: {expected_type.simpleString()}, " +
                    f"Got: {actual_field.dataType.simpleString()}."
                )

        # Step 2: Prepare the validation result
        result = {
            "validator": "SparkColumnTypeValidator",
            "is_valid": not bool(errors),
            "errors": errors,
            "mismatched_columns": mismatched_columns,
        }

        if errors:
            self.logger.log(
                "error",
                f"Column type validation failed with {len(errors)} errors.")
        else:
            self.logger.log(
                "info",
                "Column type validation passed successfully.")

        return result


class SparkUniquenessValidator(Validator):
    """
    Validator to ensure values in specified columns are unique
        in a Spark DataFrame.

    Attributes:
        unique_columns (list): List of column names to check for uniqueness.

    Example Usage:
        data = spark.createDataFrame([
            (1, "a"),
            (2, "b"),
            (3, "a")
        ], ["col1", "col2"])

        validator = SparkUniquenessValidator(unique_columns=["col1", "col2"])
        result = validator.validate(data)
        print(result)
    """

    def __init__(self, unique_columns: list):
        """
        Initialize the SparkUniquenessValidator.

        Args:
            unique_columns (list): List of column names to validate
                for uniqueness.
        """
        self.logger = get_logger()
        PandasValidationUtils.validate_is_non_empty_list(unique_columns)
        self.unique_columns = unique_columns
        self.logger.log(
            "info",
            f"Initialized with unique columns: {unique_columns}")

    def validate(self, data: DataFrame) -> dict:
        """
        Validate that specified columns contain unique values.

        Args:
            data (DataFrame): The Spark DataFrame to validate.

        Returns:
            dict: Validation result with the following keys:
                - "validator" (str): Name of the validator.
                - "is_valid" (bool): Whether the validation passed.
                - "errors" (list): List of errors, if any.
                - "duplicate_rows" (DataFrame): Rows containing
                    duplicate values.
                - "missing_columns" (list): List of missing columns.
        """
        self.logger.log(
            "info",
            "Validating uniqueness for specified columns.")
        SparkValidationUtils.validate_is_dataframe(data, "data")

        errors = []
        duplicate_rows = None

        missing_columns = SparkValidationUtils.check_missing_columns(
            data,
            self.unique_columns,
            False)
        if missing_columns:
            for col_name in missing_columns:
                errors.append({
                    "error_type": "missing_column",
                    "details": (
                        f"Column '{col_name}' is missing from the dataset.")
                })
                self.logger.log(
                    "error",
                    f"Column '{col_name}' is missing from the dataset.")

        if not missing_columns:
            # Add a duplicate count column using a Window function
            window_spec = Window.partitionBy(
                *[col(c) for c in self.unique_columns])
            duplicate_data = data.withColumn(
                "duplicate_count",
                count("*").over(window_spec))
            duplicate_rows = duplicate_data.filter(
                col("duplicate_count") > 1).drop(
                "duplicate_count")

            if duplicate_rows.count() > 0:
                errors.append({
                    "error_type": "duplicate_values",
                    "details": "Duplicate values found in columns: " +
                    f"{self.unique_columns}."
                })
                self.logger.log(
                    "error", (
                        "Duplicate values found in columns: " +
                        f"{self.unique_columns}.")
                )

        result = {
            "validator": "SparkUniquenessValidator",
            "is_valid": not bool(errors),
            "errors": errors,
            "duplicate_rows": duplicate_rows if duplicate_rows and
            duplicate_rows.count() > 0 else data.limit(0),
            "missing_columns": missing_columns,
        }

        if errors:
            self.logger.log(
                "error",
                f"Uniqueness validation failed with {len(errors)} errors.")
        else:
            self.logger.log(
                "info",
                "Uniqueness validation passed successfully.")

        return result


class SparkColumnDependencyValidator(Validator):
    """
    Validator to ensure dependencies between columns are met.

    If a primary column has a value, a dependent column must also have a value.

    Attributes:
        primary_column (str): The column that enforces the dependency.
        dependent_column (str): The column that depends on the primary column.

    Example Usage:
        data = spark.createDataFrame([
            (1, "a"),
            (None, "b"),
            (2, None)
        ], ["col1", "col2"])

        validator = SparkColumnDependencyValidator(
            primary_column="col1", dependent_column="col2")
        result = validator.validate(data)
        print(result)
    """

    def __init__(self, primary_column: str, dependent_column: str):
        """
        Initialize the SparkColumnDependencyValidator.

        Args:
            primary_column (str): The column that enforces the dependency.
            dependent_column (str): The column that depends on the
                primary column.
        """
        self.logger = get_logger()
        PandasValidationUtils.validate_is_non_empty_string(primary_column)
        PandasValidationUtils.validate_is_non_empty_string(dependent_column)
        self.primary_column = primary_column
        self.dependent_column = dependent_column
        self.logger.log(
            "info",
            f"Initialized with primary_column={primary_column}, " +
            f"dependent_column={dependent_column}")

    def validate(self, data: DataFrame) -> dict:
        """
        Validate that the dependency between the columns is met.

        Args:
            data (DataFrame): The Spark DataFrame to validate.

        Returns:
            dict: Validation result with the following keys:
                - "validator" (str): Name of the validator.
                - "is_valid" (bool): Whether the validation passed.
                - "errors" (list): List of errors, if any.
                - "violating_rows" (DataFrame): Rows that violate
                    the dependency.
                - "missing_columns" (list): Columns missing from the DataFrame.
        """
        self.logger.log("info", "Validating column dependency.")
        SparkValidationUtils.validate_is_dataframe(data, "data")

        errors = []
        violating_rows = None

        # Step 1: Check for missing columns
        missing_columns = SparkValidationUtils.check_missing_columns(
            data,
            [
                self.primary_column,
                self.dependent_column],
            False)
        if missing_columns:
            for col_name in missing_columns:
                errors.append({
                    "error_type": "missing_column",
                    "details": (
                        f"Column '{col_name}' is missing from the dataset.")
                })
                self.logger.log(
                    "error",
                    f"Column '{col_name}' is missing from the dataset.")

        # Step 2: Check for dependency violations
        if not missing_columns:
            violating_rows = data.filter(
                (col(self.primary_column).isNotNull()) &
                (col(self.dependent_column).isNull() |
                    isnan(col(self.dependent_column)))
            )

            if violating_rows.count() > 0:
                errors.append({
                    "error_type": "dependency_violation",
                    "details": f"Rows where '{self.primary_column}' " +
                    f"is not null but '{self.dependent_column}' " +
                    "is null or NaN."
                })
                self.logger.log(
                    "error",
                    f"Dependency violation: '{self.primary_column}' " +
                    f"has values while '{self.dependent_column}' " +
                    "is null or NaN."
                )

        # Step 3: Prepare the validation result
        result = {
            "validator": "SparkColumnDependencyValidator",
            "is_valid": not bool(errors),
            "errors": errors,
            "violating_rows": violating_rows if violating_rows and
            violating_rows.count() > 0 else data.limit(0),
            "missing_columns": missing_columns,
        }

        if errors:
            self.logger.log(
                "error",
                f"Dependency validation failed with {len(errors)} errors.")
        else:
            self.logger.log(
                "info",
                "Dependency validation passed successfully.")

        return result


class SparkDuplicateRowsValidator(Validator):
    """
    Validator to check for duplicate rows in a Spark DataFrame.

    Attributes:
        group_columns (list, optional): List of columns to group by for
        duplicate checks. If None, all columns are used.

    Example Usage:
        data = spark.createDataFrame([
            (1, "a"),
            (2, "b"),
            (1, "a"),
            (3, "c")
        ], ["col1", "col2"])

        validator = SparkDuplicateRowsValidator(group_columns=["col1", "col2"])
        result = validator.validate(data)
        print(result)
    """

    def __init__(self, group_columns: list = None):
        """
        Initialize the SparkDuplicateRowsValidator.

        Args:
            group_columns (list, optional): Columns to group by for duplicate
                checks. If None, all columns are used.
        """
        self.logger = get_logger()
        if group_columns is not None:
            PandasValidationUtils.validate_is_non_empty_list(group_columns)
        self.group_columns = group_columns
        self.logger.log(
            "info",
            "Initialized with group_columns: " +
            f"{group_columns if group_columns else 'All columns'}")

    def validate(self, data: DataFrame) -> dict:
        """
        Validate the DataFrame for duplicate rows.

        Args:
            data (DataFrame): The Spark DataFrame to validate.

        Returns:
            dict: Validation result with the following keys:
                - "validator" (str): Name of the validator.
                - "is_valid" (bool): Whether the validation passed
                    (no duplicates).
                - "errors" (list): List of errors, if any.
                - "duplicate_rows" (DataFrame): Rows that are duplicated.
        """
        self.logger.log("info", "Validating DataFrame for duplicate rows.")
        SparkValidationUtils.validate_is_dataframe(data, "data")

        errors = []
        duplicate_rows = None

        # Step 1: Check for duplicates
        if self.group_columns:
            # Validate if all specified columns exist
            missing_columns = SparkValidationUtils.check_missing_columns(
                data,
                self.group_columns,
                False)
            if missing_columns:
                for column in missing_columns:
                    errors.append({
                        "error_type": "missing_column",
                        "details": (
                            f"Column '{column}' is missing from the dataset.")
                    })
                    self.logger.log(
                        "error",
                        f"Column '{column}' is missing from the dataset.")
            else:
                # Count duplicates based on specified columns
                duplicate_rows = data.groupBy(
                    self.group_columns).count().filter("count > 1")
        else:
            # Count duplicates for all columns
            duplicate_rows = data.groupBy(
                *data.columns).count().filter("count > 1")

        if duplicate_rows and duplicate_rows.count() > 0:
            errors.append({
                "error_type": "duplicate_rows",
                "details": (
                    "Duplicate rows found based on " +
                    ("all columns" if not self.group_columns
                        else str(self.group_columns)))
            })
            duplicate_values = duplicate_rows.drop("count")
            duplicate_rows = data.join(
                duplicate_values, on=self.group_columns if self.group_columns
                else data.columns, how="inner").drop_duplicates()

        result = {
            "validator": "SparkDuplicateRowsValidator",
            "is_valid": not bool(errors),
            "errors": errors,
            "duplicate_rows": duplicate_rows if duplicate_rows else data.limit(
                0),
        }

        if errors:
            self.logger.log(
                "error",
                f"Duplicate rows validation failed with {len(errors)} errors.")
        else:
            self.logger.log(
                "info",
                "Duplicate rows validation passed successfully.")

        return result


class SparkReferentialIntegrityValidator(Validator):
    """
    Validator to ensure values in a column (or set of columns) match a
    reference dataset.

    Attributes:
        columns_to_check (list): List of column names in the source dataset
            to validate.
        reference_data (DataFrame): Reference DataFrame containing
            valid values.
        reference_columns (list): List of column names in the reference
            dataset to compare against.
    """

    def __init__(
        self,
        columns_to_check: list,
        reference_data: DataFrame,
        reference_columns: list
    ):
        """
        Initialize the SparkReferentialIntegrityValidator.

        Args:
            columns_to_check (list): Columns in the source DataFrame to check.
            reference_data (DataFrame): Reference DataFrame with valid values.
            reference_columns (list): Columns in the reference DataFrame to
            compare against.
        """
        self.logger = get_logger()

        # Validate inputs
        PandasValidationUtils.validate_is_non_empty_list(columns_to_check)
        SparkValidationUtils.validate_is_dataframe(
            reference_data,
            "reference_data")
        PandasValidationUtils.validate_is_non_empty_list(reference_columns)

        # Ensure column lists are the same length
        if len(columns_to_check) != len(reference_columns):
            raise ValueError(
                "The number of columns in 'columns_to_check' " +
                "and 'reference_columns' must match.")

        self.columns_to_check = columns_to_check
        self.reference_data = reference_data
        self.reference_columns = reference_columns
        self.logger.log(
            "info",
            f"Initialized with columns_to_check={columns_to_check}, " +
            f"reference_columns={reference_columns}"
        )

    def validate(self, data: DataFrame) -> dict:
        """
        Validate the DataFrame for referential integrity.

        Args:
            data (DataFrame): The Spark DataFrame to validate.

        Returns:
            dict: Validation result with the following keys:
                - "validator" (str): Name of the validator.
                - "is_valid" (bool): Whether the validation passed.
                - "errors" (list): List of errors, if any.
                - "violating_rows" (DataFrame): Rows violating
                    referential integrity.
                - "missing_columns" (list): Missing columns in the
                    source DataFrame.
        """
        self.logger.log(
            "info",
            "Validating referential integrity.")
        SparkValidationUtils.validate_is_dataframe(data, "data")

        errors = []
        violating_rows = None

        # Step 1: Check for missing columns
        missing_columns = SparkValidationUtils.check_missing_columns(
            data,
            self.columns_to_check,
            False)
        if missing_columns:
            for column in missing_columns:
                errors.append({
                    "error_type": "missing_column",
                    "details": (
                        f"Column '{column}' is " +
                        "missing from the source dataset.")
                })
                self.logger.log(
                    "error",
                    f"Column '{column}' is missing from the source dataset.")

        # Step 2: Check referential integrity
        if not missing_columns:
            # Alias the reference DataFrame to avoid column ambiguity
            aliased_reference_data = self.reference_data.select(
                *[
                    col(
                        ref_col).alias(
                            f"ref_{ref_col}"
                            ) for ref_col in self.reference_columns]
            )

            # Create join condition
            join_condition = [
                col(source_col) == col(f"ref_{ref_col}")
                for source_col, ref_col in zip(
                    self.columns_to_check, self.reference_columns)
            ]

            # Find rows in the source data that are not in the reference data
            violating_rows = data.join(
                aliased_reference_data,
                on=join_condition,
                how="left_anti"
            )

            if violating_rows.count() > 0:
                errors.append({
                    "error_type": "referential_integrity_violation",
                    "details": "Source data contains rows that are " +
                    "not present in the reference dataset."
                })
                self.logger.log(
                    "error",
                    "Referential integrity violation: Source data " +
                    "contains rows not present in the reference dataset."
                )

        # Step 3: Prepare the validation result
        result = {
            "validator": "SparkReferentialIntegrityValidator",
            "is_valid": not bool(errors),
            "errors": errors,
            "violating_rows": violating_rows if violating_rows else data.limit(
                0),
            "missing_columns": missing_columns,
        }

        if errors:
            self.logger.log(
                "error", "Referential integrity validation failed with " +
                f"{len(errors)} errors.")
        else:
            self.logger.log(
                "info",
                "Referential integrity validation passed successfully.")

        return result


class SparkValueValidator(Validator):
    """
    Validator to check for specific required or prohibited values in
    columns of a Spark DataFrame.

    This validator ensures that column values either:
    - Only include the specified allowed values (`allow_only=True`).
    - Exclude the specified prohibited values (`allow_only=False`).

    Attributes:
        column_values (dict): A dictionary where keys are column names
            and values are lists of allowed/prohibited values.
        allow_only (bool): Whether to validate only allowed values (True)
            or disallowed values (False).

    Example Usage:
        from pyspark.sql import SparkSession

        spark = SparkSession.builder.getOrCreate()
        data = spark.createDataFrame(
            [(1, "A"), (2, "B"), (3, "C")],
            ["col1", "col2"]
        )

        # Allow only specific values in columns
        validator = SparkValueValidator(
            column_values={"col1": [1, 2], "col2": ["A", "B"]},
            allow_only=True
        )
        result = validator.validate(data)
        print(result)
    """

    def __init__(self, column_values: dict, allow_only: bool = True):
        """
        Initialize the SparkValueValidator.

        Args:
            column_values (dict): Dictionary of column names and their
                allowed/prohibited values.
            allow_only (bool): If True, validates that only specified
                values are allowed. Defaults to True.
        """
        self.logger = get_logger()
        PandasValidationUtils.validate_is_non_empty_dict(column_values)
        self.column_values = column_values
        PandasValidationUtils.validate_is_boolean(allow_only, "allow_only")
        self.allow_only = allow_only
        self.logger.log(
            "info", (
                f"Initialized with column_values={column_values}, " +
                f"allow_only={allow_only}")
        )

    def validate(self, data: DataFrame) -> dict:
        """
        Validate the DataFrame based on column value rules.

        Args:
            data (DataFrame): The Spark DataFrame to validate.

        Returns:
            dict: Validation result with the following keys:
                - "validator" (str): Name of the validator.
                - "is_valid" (bool): Whether the validation passed.
                - "errors" (list): List of errors, if any.
                - "invalid_rows" (DataFrame): Rows with invalid values.
                - "missing_columns" (list): List of missing columns.
        """
        SparkValidationUtils.validate_is_dataframe(data, "data")
        self.logger.log(
            "info",
            "Starting value validation for specified columns.")

        # Handle empty DataFrame
        if data.count() == 0:
            self.logger.log("error", "The input DataFrame is empty.")
            return {
                "validator": "SparkValueValidator",
                "is_valid": False,
                "errors": [{
                    "error_type": "empty_dataset",
                    "details": "The dataset is empty."
                }],
                "invalid_rows": data.limit(0),
                "missing_columns": []
            }

        # Initialize validation results
        errors = []
        invalid_rows = None
        missing_columns = []

        for col_name, values in self.column_values.items():
            if col_name in data.columns:
                # Validate values in column
                condition = None
                if self.allow_only:
                    condition = ~col(col_name).isin(values)
                else:
                    condition = col(col_name).isin(values)

                invalid_data = data.filter(condition)

                if invalid_data.count() > 0:
                    invalid_values = invalid_data.select(
                        col_name).distinct().collect()
                    invalid_values = [row[col_name] for row in invalid_values]
                    self.logger.log(
                        "error",
                        f"Column '{col_name}' contains disallowed values: " +
                        f"{invalid_values[:5]}..."
                    )
                    errors.append({
                        "error_type": "value_violation",
                        "details": (
                            f"Column '{col_name}' contains disallowed values. "
                            f"Invalid values: {invalid_values[:5]}...")
                    })
                    invalid_rows = invalid_data if invalid_rows is None \
                        else invalid_rows.union(invalid_data)
            else:
                # Log and append missing column error
                error_message = (
                    f"Column '{col_name}' is missing from the dataset.")
                self.logger.log("error", error_message)
                missing_columns.append(col_name)
                errors.append({
                    "error_type": "missing_column",
                    "details": error_message
                })

        self.logger.log(
            "info",
            f"Value validation completed with {len(errors)} errors.")

        result = {
            "validator": "SparkValueValidator",
            "is_valid": not bool(errors),
            "errors": errors,
            "invalid_rows": invalid_rows if invalid_rows else data.limit(0),
            "missing_columns": missing_columns
        }
        return result


class SparkValidatorFactory(ValidatorFactory):
    """
    Factory class for creating various types of Spark validators.

    Example Usage:
        # Initialize the factory
        factory = SparkValidatorFactory()

        # Create a Missing Columns Validator
        missing_columns_validator = factory.create_missing_columns_validator(
            required_columns=["col1", "col2"]
        )
        data = spark.createDataFrame([(1, 2)], ["col1", "col3"])
        result = missing_columns_validator.validate(data)
        print(result)

        # Output:
        # {
        #     "validator": "SparkMissingColumnsValidator",
        #     "is_valid": False,
        #     "errors": [
        #         {"error_type": "missing_columns",
        "details": "Missing columns: ['col2']"}
        #     ],
        #     "invalid_columns": ["col2"]
        # }
    """

    def __init__(self):
        """
        Initialize the SparkValidatorFactory.
        """
        self.logger = get_logger()

    def log_creation(self, validator_name: str, **params):
        """
        Log the creation of a validator.

        Args:
            validator_name (str): Name of the validator being created.
            params (dict): Parameters used to create the validator.
        """
        self.logger.log(
            "info",
            f"Creating {validator_name} with parameters: {params}"
        )

    def create_missing_columns_validator(
        self,
        required_columns: list
    ) -> Validator:
        """
        Create and return a SparkMissingColumnsValidator.

        Args:
            required_columns (list): List of required columns.

        Returns:
            SparkMissingColumnsValidator: A SparkMissingColumnsValidator
            instance.

        Example Usage:
            from my_module import SparkValidatorFactory
            factory = SparkValidatorFactory()
            validator = factory.create_missing_columns_validator(
                required_columns=["col1", "col2"]
            )
        """
        self.log_creation(
            "SparkMissingColumnsValidator",
            required_columns=required_columns
        )
        return SparkMissingColumnsValidator(required_columns)

    def create_extra_columns_validator(
        self,
        allowed_columns: list
    ) -> Validator:
        """
        Create and return a SparkExtraColumnsValidator.

        Args:
            allowed_columns (list): List of allowed columns.

        Returns:
            SparkExtraColumnsValidator: A SparkExtraColumnsValidator
            instance.

        Example Usage:
            from my_module import SparkValidatorFactory
            factory = SparkValidatorFactory()
            validator = factory.create_extra_columns_validator(
                allowed_columns=["col1", "col2"]
            )
        """
        self.log_creation(
            "SparkExtraColumnsValidator",
            allowed_columns=allowed_columns
        )
        return SparkExtraColumnsValidator(allowed_columns)

    def create_data_type_validator(self, expected_schema: dict) -> Validator:
        """
        Create and return a SparkDataTypeValidator.

        Args:
            expected_schema (dict): Expected schema for the DataFrame.

        Returns:
            SparkDataTypeValidator: A SparkDataTypeValidator instance.

        Example Usage:
            from my_module import SparkValidatorFactory
            factory = SparkValidatorFactory()
            validator = factory.create_data_type_validator(
                expected_schema={
                    "col1": "integer",
                    "col2": "string"
                }
            )
        """
        self.log_creation(
            "SparkDataTypeValidator",
            expected_schema=expected_schema
        )
        return SparkDataTypeValidator(expected_schema)

    def create_null_value_validator(
        self,
        critical_columns: list,
        null_values=None
    ) -> Validator:
        """
        Create and return a SparkNullValueValidator.

        Args:
            critical_columns (list): Columns that should not contain
                null values.
            null_values (list, optional): List of specific null values to
                consider. Defaults to None, which means any null value is
                considered invalid.

        Returns:
            SparkNullValueValidator: A SparkNullValueValidator instance.

        Example Usage:
            from my_module import SparkValidatorFactory
            factory = SparkValidatorFactory()
            validator = factory.create_null_value_validator(
                critical_columns=["col1", "col2"],
                null_values=["null", ""]
            )
        """
        self.log_creation(
            "SparkNullValueValidator",
            critical_columns=critical_columns,
            null_values=null_values
        )
        return SparkNullValueValidator(
            critical_columns=critical_columns,
            null_values=null_values
        )

    def create_value_range_validator(
        self,
        column_ranges: dict,
        inclusive: bool = True
    ) -> Validator:
        """
        Create and return a SparkRangeValidator.

        Args:
            column_ranges (dict): Column names and their respective
                ranges.
            inclusive (bool, optional): Whether the range should be inclusive
                or exclusive. Defaults to True.

        Returns:
            SparkRangeValidator: A SparkRangeValidator instance.

        Example Usage:
            from my_module import SparkValidatorFactory
            factory = SparkValidatorFactory()
            validator = factory.create_value_range_validator(
                column_ranges={
                    "col1": {"min": 0, "max": 100},
                    "col2": {"min": -100, "max": 0}
                }
            )
        """
        self.log_creation(
            "SparkRangeValidator",
            column_ranges=column_ranges,
            inclusive=inclusive
        )
        return SparkRangeValidator(column_ranges, inclusive)

    def create_rowCount_validator(
        self,
        min_rows: int = None,
        max_rows: int = None
    ) -> Validator:
        """
        Create and return a SparkRowCountValidator.

        Args:
            min_rows (int, optional): Minimum number of rows required.
                Defaults to None.
            max_rows (int, optional): Maximum number of rows allowed.
                Defaults to None.

        Returns:
            SparkRowCountValidator: A SparkRowCountValidator instance.

        Example Usage:
            from my_module import SparkValidatorFactory
            factory = SparkValidatorFactory()
            validator = factory.create_rowCount_validator(
                min_rows=1000,
                max_rows=5000
            )
        """
        self.log_creation(
            "SparkRowCountValidator",
            min_rows=min_rows,
            max_rows=max_rows
        )
        return SparkRowCountValidator(min_rows=min_rows, max_rows=max_rows)

    def create_non_empty_validator(self) -> Validator:
        """
        Create and return a SparkNonEmptyValidator.

        Returns:
            SparkNonEmptyValidator: A SparkNonEmptyValidator instance.

        Example Usage:
            from my_module import SparkValidatorFactory
            factory = SparkValidatorFactory()
            validator = factory.create_non_empty_validator()
        """
        self.log_creation(
            "SparkNonEmptyValidator")
        return SparkNonEmptyValidator()

    def create_uniqueness_validator(self, unique_columns: list) -> Validator:
        """
        Create and return a SparkUniquenessValidator.

        Args:
            unique_columns (list): Columns that should have unique values.

        Returns:
            SparkUniquenessValidator: A SparkUniquenessValidator instance.

        Example Usage:
            from my_module import SparkValidatorFactory
            factory = SparkValidatorFactory()
            validator = factory.create_uniqueness_validator(
                unique_columns=["col1", "col2"]
            )
        """
        self.log_creation(
            "SparkUniquenessValidator",
            unique_columns=unique_columns
        )
        return SparkUniquenessValidator(unique_columns)

    def create_column_dependency_validator(
        self,
        primary_column: str,
        dependent_column: str
    ) -> Validator:
        self.log_creation(
            "SparkColumnDependencyValidator",
            primary_column=primary_column,
            dependent_column=dependent_column
        )
        return SparkColumnDependencyValidator(primary_column, dependent_column)

    def create_duplicate_row_validator(
        self,
        group_columns: list = None
    ) -> Validator:
        """
        Create and return a SparkDuplicateRowsValidator.

        Args:
            group_columns (list, optional): Columns to group duplicate rows on.
                Defaults to None, which means all columns should be grouped.

        Returns:
            SparkDuplicateRowsValidator: A SparkDuplicateRowsValidator
                instance.

        Example Usage:
            from my_module import SparkValidatorFactory
            factory = SparkValidatorFactory()
            validator = factory.create_duplicate_row_validator(
                group_columns=["col1", "col2"]
            )
        """
        self.log_creation(
            "SparkDuplicateRowsValidator",
            group_columns=group_columns
        )
        return SparkDuplicateRowsValidator(group_columns)

    def create_referential_integrity_validator(
        self,
        columns_to_check: list,
        reference_data: DataFrame,
        reference_columns: list
    ) -> Validator:
        """
        Create and return a SparkReferentialIntegrityValidator.

        Args:
            columns_to_check (list): Columns to check for referential
                integrity.
            reference_data (DataFrame): Reference DataFrame to compare against.
            reference_columns (list): Columns in the reference DataFrame to
            compare against.

        Returns:
            SparkReferentialIntegrityValidator: A
                SparkReferentialIntegrityValidator instance.

        Example Usage:
            from my_module import SparkValidatorFactory
            from pyspark.sql.types import StructType
            factory = SparkValidatorFactory()
            reference_data = spark.read.format(
                "csv").option("header", "true").load("reference_data.csv")
            validator = factory.create_referential_integrity_validator(
                columns_to_check=["col1", "col2"],
                reference_data=reference_data,
                reference_columns=["reference_col1", "reference_col2"]
            )
        """
        self.log_creation(
            "SparkReferentialIntegrityValidator",
            columns_to_check=columns_to_check,
            reference_columns=reference_columns
        )
        return SparkReferentialIntegrityValidator(
            columns_to_check=columns_to_check,
            reference_data=reference_data,
            reference_columns=reference_columns
        )

    def create_regex_validator(self, column_patterns: dict) -> Validator:
        self.log_creation(
            "SparkRegexValidator",
            column_patterns=column_patterns
        )
        return SparkRegexValidator(column_patterns)

    def create_column_type_validator(self, column_types: dict) -> Validator:
        """
        Create a SparkColumnTypeValidator.

        Args:
            column_types (dict): Dictionary of column names and expected
                data types.

        Returns:
            SparkColumnTypeValidator: Validator to ensure specified
                columns have the expected types.

        Example Usage:
            from my_module import SparkValidatorFactory
            factory = SparkValidatorFactory()
            validator = factory.create_column_type_validator(
                column_types={
                    "col1": IntegerType(),
                    "col2": StringType()
                }
        """
        self.log_creation(
            "SparkColumnTypeValidator",
            column_types=column_types
        )
        return SparkColumnTypeValidator(column_types)

    def create_schema_validator(
        self, expected_schema: StructType
    ) -> Validator:
        """
        Create a SparkSchemaValidator.

        Args:
            expected_schema (StructType): Expected schema for the DataFrame.

        Returns:
            SparkSchemaValidator: Validator to ensure the DataFrame matches the
            expected schema.

        Example Usage:
            from my_module import SparkValidatorFactory
            factory = SparkValidatorFactory()
            expected_schema = StructType([
                StructField("id", IntegerType(), True),
                StructField("name", StringType(), True),
                StructField("age", IntegerType(), True)
            ])
        """
        self.log_creation(
            "SparkSchemaValidator",
            expected_schema=expected_schema.simpleString()
        )
        return SparkSchemaValidator(expected_schema)

    def create_value_validator(
        self,
        column_values: dict,
        allow_only: bool = True
    ) -> Validator:
        """
        Create an instance of SparkValueValidator.

        Args:
            column_values (dict): Dictionary where keys are column names
                and values are lists of allowed or prohibited values.
            allow_only (bool, optional): Whether to allow only specified values
                (True) or prohibit specified values (False). Defaults to True.

        Returns:
            Validator: An instance of SparkValueValidator.

        Raises:
            ValueError: If `column_values` is not provided or is invalid.

        Example Usage:
        from my_module import SparkValidatorFactory
        factory = SparkValidatorFactory()
        validator = factory.create_value_validator(
            column_values={
                "col1": ["value1", "value2"],
                "col2": ["value3", "value4"]
            },
            allow_only=True)
        """
        self.log_creation(
            "SparkValueValidator",
            column_values=column_values,
            allow_only=allow_only
        )

        if not isinstance(column_values, dict) or not column_values:
            error_message = "`column_values` must be a non-empty dictionary."
            self.logger.log(
                "error",
                error_message)
            raise ValueError(error_message)

        return SparkValueValidator(
            column_values=column_values, allow_only=allow_only)


class SparkValidatorProvider(ValidatorProvider):
    """
    Provider class to create Spark validators dynamically based on the
    validation type.

    This class uses an instance of `SparkValidatorFactory` to create8
    validators for different validation types as defined in the
        `ValidationType` enum.

    Example Usage:
        factory = SparkValidatorFactory()
        provider = SparkValidatorProvider(factory)

        # Example 1: Missing Columns Validation
        missing_validator = provider.create_validator(
            validation_type=ValidationType.MISSING_COLUMNS,
            required_columns=["col1", "col2"]
        )
        data = spark.createDataFrame([(1, 2)], ["col1", "col2"])
        result = missing_validator.validate(data)
        print(result)

        # Example 2: Range Validation
        range_validator = provider.create_validator(
            validation_type=ValidationType.VALUE_RANGE,
            column_ranges={"col1": (0, 100)}
        )
        data = spark.createDataFrame([(50,), (200,)], ["col1"])
        result = range_validator.validate(data)
        print(result)
    """

    def __init__(self, factory: SparkValidatorFactory):
        """
        Initialize the SparkValidatorProvider.

        Args:
            factory (SparkValidatorFactory): An instance of the
                SparkValidatorFactory to create validators.
        """
        self.logger = get_logger()
        PandasValidationUtils.validate_inheritance(
            factory,
            ValidatorFactory,
            "factory")
        self.factory = factory

    def create_validator(
        self,
        validation_type: ValidationType,
        **options
    ) -> Validator:
        """
        Create a validator dynamically based on the validation type.

        Args:
            validation_type (ValidationType): Enum specifying the
                type of validation.
            **options: Additional options specific to the validator
                being created.

        Returns:
            Validator: An instance of the requested Validator.

        Raises:
            ValueError: If required options are missing or the validation
            type is unsupported.
        """
        PandasValidationUtils.validate_instance(
            validation_type,
            ValidationType,
            "validation_type")

        match validation_type:
            case ValidationType.MISSING_COLUMNS:
                validate_options(
                    options=options,
                    required_keys=["required_columns"],
                    entity_type="validation",
                    entity_name="MISSING_COLUMNS")
                return self.factory.create_missing_columns_validator(
                    required_columns=options["required_columns"])

            case ValidationType.EXTRA_COLUMNS:
                validate_options(
                    options=options,
                    required_keys=["allowed_columns"],
                    entity_type="validation",
                    entity_name="EXTRA_COLUMNS")
                return self.factory.create_extra_columns_validator(
                    allowed_columns=options["allowed_columns"])

            case ValidationType.DATA_TYPE:
                validate_options(
                    options=options,
                    required_keys=["expected_schema"],
                    entity_type="validation",
                    entity_name="DATA_TYPE")
                return self.factory.create_data_type_validator(
                    expected_schema=options["expected_schema"])

            case ValidationType.NULL_VALUES:
                validate_options(
                    options=options,
                    required_keys=["critical_columns", "null_values"],
                    entity_type="validation",
                    entity_name="NULL_VALUES")
                return self.factory.create_null_value_validator(
                    critical_columns=options["critical_columns"],
                    null_values=options["null_values"])

            case ValidationType.VALUE_RANGE:
                validate_options(
                    options=options,
                    required_keys=["column_ranges", "inclusive"],
                    entity_type="validation",
                    entity_name="VALUE_RANGE")
                return self.factory.create_value_range_validator(
                    column_ranges=options["column_ranges"],
                    inclusive=options["inclusive"])

            case ValidationType.UNIQUENESS:
                validate_options(
                    options=options,
                    required_keys=["unique_columns"],
                    entity_type="validation",
                    entity_name="UNIQUENESS")
                return self.factory.create_uniqueness_validator(
                    unique_columns=options["unique_columns"])

            case ValidationType.ROW_COUNT:
                validate_options(
                    options=options,
                    required_keys=["min_rows", "max_rows"],
                    entity_type="validation",
                    entity_name="ROW_COUNT")
                return self.factory.create_rowCount_validator(
                    min_rows=options["min_rows"],
                    max_rows=options["max_rows"])

            case ValidationType.NON_EMPTY:
                return self.factory.create_non_empty_validator()

            case ValidationType.VALUE:
                validate_options(
                    options=options,
                    required_keys=["column_values", "allow_only"],
                    entity_type="validation",
                    entity_name="VALUE")
                return self.factory.create_value_validator(
                    column_values=options["column_values"],
                    allow_only=options["allow_only"])

            case ValidationType.REFERENTIAL_INTEGRITY:
                validate_options(
                    options=options,
                    required_keys=[
                        "columns_to_check",
                        "reference_data",
                        "reference_columns"],
                    entity_type="validation",
                    entity_name="REFERENTIAL_INTEGRITY")
                return self.factory.create_referential_integrity_validator(
                    columns_to_check=options["columns_to_check"],
                    reference_data=options["reference_data"],
                    reference_columns=options["reference_columns"])

            case ValidationType.REGEX:
                validate_options(
                    options=options,
                    required_keys=["column_patterns"],
                    entity_type="validation",
                    entity_name="REGEX")
                return self.factory.create_regex_validator(
                    column_patterns=options["column_patterns"])

            case ValidationType.DUPLICATE_ROWS:
                validate_options(
                    options=options,
                    required_keys=["group_columns"],
                    entity_type="validation",
                    entity_name="DUPLICATE_ROWS")
                return self.factory.create_duplicate_row_validator(
                    group_columns=options["group_columns"])

            case ValidationType.COLUMN_DEPENDENCY:
                validate_options(
                    options=options,
                    required_keys=["primary_column", "dependent_column"],
                    entity_type="validation",
                    entity_name="COLUMN_DEPENDENCY")
                return self.factory.create_column_dependency_validator(
                    primary_column=options["primary_column"],
                    dependent_column=options["dependent_column"])

            case ValidationType.SCHEMA:
                validate_options(
                    options=options,
                    required_keys=["expected_schema"],
                    entity_type="validation",
                    entity_name="SCHEMA")
                return self.factory.create_schema_validator(
                    expected_schema=options["expected_schema"])

            case ValidationType.COLUMN_TYPE:
                validate_options(
                    options=options,
                    required_keys=["column_types"],
                    entity_type="validation",
                    entity_name="COLUMN_TYPE")
                return self.factory.create_column_type_validator(
                    column_types=options["column_types"])

            case _:
                error_message = (
                    f"Unsupported validation type: {validation_type}")
                self.logger.log(
                    "error",
                    error_message)
                raise ValueError(error_message)

# ############################# Transformers #############################


class SparkColumnRenamer(Transformer):
    """
    Transformer to rename columns in a Spark DataFrame.

    Attributes:
        column_map (dict): A dictionary where keys are the current column
        names and values are the new column names.

    Example Usage:
        column_map = {"old_col1": "new_col1", "old_col2": "new_col2"}
        column_renamer = SparkColumnRenamer(column_map=column_map)
        transformed_data = column_renamer.transform(data)
    """

    def __init__(self, column_map: dict):
        """
        Initialize the SparkColumnRenamer.

        Args:
            column_map (dict): A dictionary mapping current column names
            to new column names.

        Raises:
            ValueError: If column_map is not a dictionary or is empty.
        """
        self.logger = get_logger()
        # Validate that column_map is a non-empty dictionary
        PandasValidationUtils.validate_is_non_empty_dict(column_map)
        self.column_map = column_map
        self.logger.log(
            "info",
            f"Initialized with column_map: {column_map}")

    def transform(self, data: DataFrame, **kwargs) -> DataFrame:
        """
        Rename columns in the Spark DataFrame.

        Args:
            data (DataFrame): The input Spark DataFrame.
            **kwargs: Additional parameters (not applicable for Spark but kept
            for interface consistency).

        Returns:
            DataFrame: The Spark DataFrame with renamed columns.

        Raises:
            KeyError: If any column in the column_map does not exist in
            the DataFrame.

        Example:
        from pyspark.sql import SparkSession
        from pyspark.sql.functions import col

        spark = SparkSession.builder.appName(
            "ColumnRenamerExample").getOrCreate()
        data = spark.createDataFrame(
            [(1, "Alice", 30), (2, "Bob", 25)], ["id", "name", "age"])
        column_map = {"id": "user_id", "name": "full_name"}
        column_renamer = SparkColumnRenamer(column_map=column_map)
        transformed_data = column_renamer.transform(data)
        transformed_data.show()

        """
        # Validate that the input is a Spark DataFrame
        SparkValidationUtils.validate_is_dataframe(data, "data", False)

        # Validate that all columns in column_map exist in the DataFrame
        SparkValidationUtils.validate_columns_exist(
            data,
            list(self.column_map.keys()),
            False)

        self.logger.log(
            "info",
            f"Renaming columns using column_map: {self.column_map}"
        )

        # Apply the column renaming
        renamed_data = data.selectExpr(
            *[f"`{col}` as `{self.column_map.get(col, col)}`"
                for col in data.columns]
        )

        self.logger.log(
            "info",
            "Columns renamed successfully.")

        return renamed_data


class SparkColumnDropper(Transformer):
    """
    Transformer to drop specified columns from a Spark DataFrame.

    Attributes:
        columns_to_drop (list): List of column names to drop.

    Example Usage:
        from pyspark.sql import SparkSession

        # Initialize Spark session
        spark = SparkSession.builder.appName(
            "ColumnDropperExample").getOrCreate()

        # Sample data
        data = spark.createDataFrame(
            [(1, 2, 3), (4, 5, 6)],
            ["col1", "col2", "col3"]
        )

        # Define columns to drop
        columns_to_drop = ["col2", "col3"]

        # Apply transformer
        column_dropper = SparkColumnDropper(columns_to_drop=columns_to_drop)
        transformed_data = column_dropper.transform(data)

        # Show the transformed data
        transformed_data.show()

        # Output:
        # +----+
        # |col1|
        # +----+
        # |   1|
        # |   4|
        # +----+
    """

    def __init__(self, columns_to_drop: list):
        """
        Initialize the SparkColumnDropper.

        Args:
            columns_to_drop (list): List of column names to drop.

        Raises:
            ValueError: If columns_to_drop is not a list or is empty.
        """
        self.logger = get_logger()
        # Validate that columns_to_drop is a non-empty list
        PandasValidationUtils.validate_is_non_empty_list(columns_to_drop)
        self.columns_to_drop = columns_to_drop
        self.logger.log(
            "info",
            f"Initialized with columns_to_drop: {columns_to_drop}")

    def transform(self, data: DataFrame, **kwargs) -> DataFrame:
        """
        Drop specified columns from the Spark DataFrame.

        Args:
            data (DataFrame): The input Spark DataFrame.
            **kwargs: Additional parameters (not applicable for Spark but kept
            for interface consistency).

        Returns:
            DataFrame: The Spark DataFrame with specified columns dropped.

        Raises:
            KeyError: If any column in columns_to_drop does not exist in
            the DataFrame.

        Example:
        from pyspark.sql import SparkSession
        from pyspark.sql.functions import col
        spark = SparkSession.builder.appName(
            "ColumnDropperExample").getOrCreate()
        data = spark.createDataFrame(
            [(1, 2, 3), (4, 5, 6)],
            ["col1", "col2", "col3"]
        )
        columns_to_drop = ["col2", "col3"]
        column_dropper = SparkColumnDropper(columns_to_drop=columns_to_drop)
        transformed_data = column_dropper.transform(data)
        transformed_data.show()

        """
        # Validate that the input is a Spark DataFrame
        SparkValidationUtils.validate_is_dataframe(data, "data")

        # Validate that all columns to drop exist in the DataFrame
        SparkValidationUtils.validate_columns_exist(
            data,
            self.columns_to_drop,
            False)

        self.logger.log(
            "info",
            f"Dropping columns: {self.columns_to_drop}"
        )

        # Drop the specified columns
        remaining_columns = [
            col for col in data.columns if
            col not in self.columns_to_drop]
        transformed_data = data.select(*remaining_columns)

        self.logger.log(
            "info",
            "Columns dropped successfully.")

        return transformed_data


class SparkValueReplacer(Transformer):
    """
    Transformer to replace values in specified columns of a Spark DataFrame.

    Attributes:
        value_map (dict): A dictionary where keys are column names, and values
            are dictionaries mapping old values to new values.

    Example Usage:
        from pyspark.sql import SparkSession

        # Initialize Spark session
        spark = SparkSession.builder.appName(
            "ValueReplacerExample").getOrCreate()

        # Sample data
        data = spark.createDataFrame(
            [("A", 1), ("B", 2), ("C", 3)],
            ["column1", "column2"]
        )

        # Define value map
        value_map = {
            "column1": {"A": "X", "B": "Y"},
            "column2": {1: 100, 2: 200}
        }

        # Apply transformer
        value_replacer = SparkValueReplacer(value_map=value_map)
        transformed_data = value_replacer.transform(data)

        # Show the transformed data
        transformed_data.show()

        # Output:
        # +-------+-------+
        # |column1|column2|
        # +-------+-------+
        # |      X|    100|
        # |      Y|    200|
        # |      C|      3|
        # +-------+-------+
    """

    def __init__(self, value_map: dict):
        """
        Initialize the SparkValueReplacer.

        Args:
            value_map (dict): Dictionary specifying columns and their
            respective value mappings.

        Raises:
            ValueError: If value_map is not a dictionary.
        """
        self.logger = get_logger()
        PandasValidationUtils.validate_is_non_empty_dict(value_map)
        self.value_map = value_map
        self.logger.log(
            "info",
            f"Initialized with value_map: {value_map}")

    def transform(self, data: DataFrame) -> DataFrame:
        """
        Replace values in the specified columns based on the value_map.

        Args:
            data (DataFrame): Input DataFrame to transform.

        Returns:
            DataFrame: Transformed DataFrame.

        Raises:
            KeyError: If any column in value_map is missing from the DataFrame.

        Example:
        from pyspark.sql import SparkSession
        from pyspark.sql.functions import col
        spark = SparkSession.builder.appName(
            "ValueReplacerExample").getOrCreate()
        data = spark.createDataFrame(
            [("A", 1), ("B", 2), ("C", 3)],
            ["column1", "column2"]
        )
        value_map = {
            "column1": {"A": "X", "B": "Y"},
            "column2": {1: 100, 2: 200}
        }
        value_replacer = SparkValueReplacer(value_map=value_map)
        transformed_data = value_replacer.transform(data)
        transformed_data.show()
        """
        SparkValidationUtils.validate_is_dataframe(data, "data")
        self.logger.log(
            "info",
            "Starting value replacement transformation.")
        transformed_data = data

        for column, replacements in self.value_map.items():
            if column not in transformed_data.columns:
                error_message = f"Column '{column}' not found in DataFrame."
                self.logger.log(
                    "error",
                    error_message)
                raise KeyError(error_message)

            self.logger.log(
                "info",
                f"Replacing values in column '{column}'.")

            # Apply replacements using when()
            replacement_expr = col(column)
            for old_value, new_value in replacements.items():
                replacement_expr = when(
                    col(column) == old_value, new_value).otherwise(
                        replacement_expr)

            transformed_data = transformed_data.withColumn(
                column, replacement_expr)

        self.logger.log(
            "info",
            "Value replacement transformation completed.")
        return transformed_data


class SparkColumnReorderer(Transformer):
    """
    Transformer to reorder columns in a Spark DataFrame.

    Attributes:
        column_order (list): List specifying the desired order of columns.
        retain_unspecified (bool): If True, columns not in `column_order`
        are appended at the end.

    Example Usage:
        from pyspark.sql import SparkSession

        # Initialize Spark session
        spark = SparkSession.builder.appName(
            "ColumnReordererExample").getOrCreate()

        # Sample data
        data = spark.createDataFrame(
            [(1, "A", 3.0), (4, "B", 6.0)],
            ["column1", "column2", "column3"]
        )

        # Define column order
        column_order = ["column2", "column1"]

        # Apply transformer
        reorderer = SparkColumnReorderer(
            column_order=column_order,
            retain_unspecified=True
        )
        transformed_data = reorderer.transform(data)

        # Show the transformed data
        transformed_data.show()

        # Output:
        # +-------+-------+-------+
        # |column2|column1|column3|
        # +-------+-------+-------+
        # |      A|      1|    3.0|
        # |      B|      4|    6.0|
        # +-------+-------+-------+
    """

    def __init__(self, column_order: list, retain_unspecified: bool = False):
        """
        Initialize the SparkColumnReorderer.

        Args:
            column_order (list): List specifying the desired order of columns.
            retain_unspecified (bool): Whether to retain columns not
            in `column_order`.

        Raises:
            ValueError: If column_order is not a list or is empty.
        """
        self.logger = get_logger()
        PandasValidationUtils.validate_is_non_empty_list(column_order)
        PandasValidationUtils.validate_is_boolean(retain_unspecified)
        self.column_order = column_order
        self.retain_unspecified = retain_unspecified
        self.logger.log(
            "info",
            f"Initialized with column_order: {column_order}, " +
            f"retain_unspecified: {retain_unspecified}")

    def transform(self, data: DataFrame) -> DataFrame:
        """
        Reorder columns in the Spark DataFrame.

        Args:
            data (DataFrame): The input Spark DataFrame.

        Returns:
            DataFrame: The Spark DataFrame with reordered columns.
        """
        SparkValidationUtils.validate_is_dataframe(data, "data")

        # Validate that specified columns exist
        SparkValidationUtils.validate_columns_exist(
            data,
            self.column_order,
            False)

        # Determine the final column order
        existing_cols = [
            col for col in self.column_order if col in data.columns
        ]
        if self.retain_unspecified:
            unspecified_cols = [
                col for col in data.columns if col not in self.column_order
            ]
            final_order = existing_cols + unspecified_cols
        else:
            final_order = existing_cols

        self.logger.log(
            "info",
            f"Final column order: {final_order}")
        return data.select(*final_order)


class SparkColumnAdder(Transformer):
    """
    Transformer to add a new column to a Spark DataFrame.

    This class supports:
    1. Static Value Assignment: Assign a single value to the new column.
    2. Column Copying: Copy values from an existing column to the new column.
    3. Expression-Based Computation: Compute the column using a Spark SQL
        expression.
    4. Callable-Based Computation: Compute the column dynamically using a
        callable function.
    5. Multi-Column Aggregation: Combine multiple columns into a new column
        using an aggregation function.

    Attributes:
        column_name (str): The name of the new column to be added.
        value (Any or Callable or str, optional): Specifies the values for
        the new column.
        aggregation (dict, optional): Settings for column aggregation:
            - columns (list): List of column names to aggregate.
            - agg_func (Callable): Aggregation function (e.g., sum, mean).

    Example Usage:
        from pyspark.sql import SparkSession

        # Initialize Spark session
        spark = SparkSession.builder.appName(
            "ColumnAdderExample").getOrCreate()

        # Sample data
        data = spark.createDataFrame(
            [(1, 2), (3, 4)],
            ["col1", "col2"]
        )

        # Static value example
        adder_static = SparkColumnAdder(
            column_name="static_col",
            value="static_value"
        )
        result_static = adder_static.transform(data)

        # Aggregation example
        adder_agg = SparkColumnAdder(
            column_name="sum_col",
            aggregation={"columns": ["col1", "col2"],
            "agg_func": lambda df: df["col1"] + df["col2"]}
        )
        result_agg = adder_agg.transform(data)

        # Show results
        result_static.show()
        result_agg.show()
    """

    def __init__(
        self,
        column_name: str,
        value: any = None,
        aggregation: dict = None
    ):
        """
        Initialize the SparkColumnAdder.

        Args:
            column_name (str): The name of the new column to be added.
            value (Any or Callable or str, optional): Specifies the values for
            the new column.
            aggregation (dict, optional): Settings for column aggregation:
                - columns (list): List of column names to aggregate.
                - agg_func (Callable): Aggregation function.

        Raises:
            ValueError: If both `value` and `aggregation` are None.
            ValueError: If aggregation is improperly defined.
        """
        self.logger = get_logger()

        if value is None and aggregation is None:
            error_message = "Either value or aggregation must be provided."
            self.logger.log(
                "error",
                error_message)
            raise ValueError(error_message)

        if aggregation:
            if not isinstance(
                aggregation, dict) or "columns" not in (
                    aggregation) or "agg_func" not in aggregation:
                error_message = (
                    "Aggregation must include 'columns' and 'agg_func'.")
                self.logger.log(
                    "error",
                    error_message)
                raise ValueError(error_message)

        PandasValidationUtils.validate_is_non_empty_string(column_name)
        self.column_name = column_name
        self.value = value
        self.aggregation = aggregation
        self.logger.log(
            "info",
            f"Initialized with column_name: {column_name}, " +
            f"value: {value}, aggregation: {aggregation}")

    def transform(self, data: DataFrame) -> DataFrame:
        """
        Add the new column to the DataFrame.

        Args:
            data (DataFrame): The input DataFrame.

        Returns:
            DataFrame: The DataFrame with the new column added.

        Raises:
            ValueError: If column_name already exists in the DataFrame.

        Example:
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.appName(
            "ColumnAdderExample").getOrCreate()
        data = spark.createDataFrame(
            [(1, 2), (3, 4)],
            ["col1", "col2"]
        )
        adder = SparkColumnAdder(
            column_name="new_col",
            aggregation={
                "columns": ["col1", "col2"],
                "agg_func": lambda df: df["col1"] + df["col2"]}
        )
        result = adder.transform(data)
        result.show()
        """
        SparkValidationUtils.validate_is_dataframe(data, "data")

        try:
            if self.aggregation:
                # Perform multi-column aggregation
                columns = self.aggregation.get(
                    "columns", [])
                agg_func = self.aggregation.get(
                    "agg_func", None)

                # Validate columns exist
                SparkValidationUtils.validate_columns_exist(
                    data,
                    columns,
                    False)

                self.logger.log(
                    "info",
                    f"Aggregating columns {columns} into " +
                    f"'{self.column_name}'.")

                # Apply aggregation function
                data = data.withColumn(self.column_name, agg_func(data))

            elif callable(self.value):
                # Compute column values dynamically using a callable
                self.logger.log(
                    "info",
                    f"Computing column '{self.column_name}' using a callable.")
                data = data.withColumn(self.column_name, self.value(data))

            elif isinstance(self.value, str) and self.value.strip(
                    ) in data.columns:
                # Copy values from an existing column
                self.logger.log(
                    "info",
                    f"Copying column '{self.value}' to '{self.column_name}'.")
                data = data.withColumn(self.column_name, col(self.value))

            elif isinstance(self.value, str):
                # Assign a static value if it's not an existing column
                if self.value.strip() not in data.columns:
                    self.logger.log(
                        "info",
                        f"Assigning static value '{self.value}' " +
                        f"to column '{self.column_name}'."
                    )
                    data = data.withColumn(self.column_name, lit(self.value))
                else:
                    # Copy values from an existing column
                    self.logger.log(
                        "info", (
                            "Copying column '{self.value}' " +
                            f"to '{self.column_name}'.")
                    )
                    data = data.withColumn(self.column_name, col(self.value))

            else:
                # Assign static value
                self.logger.log(
                    "info",
                    f"Assigning static value '{self.value}' " +
                    f"to column '{self.column_name}'.")
                data = data.withColumn(self.column_name, lit(self.value))

            self.logger.log(
                "info",
                f"Column '{self.column_name}' added successfully.")

        except Exception as e:
            error_message = (
                f"Error while adding column '{self.column_name}': {e}")
            self.logger.log(
                "error",
                error_message)
            raise Exception(error_message)

        return data


class SparkColumnNameStandardizer(Transformer):
    """
    Transformer to standardize column names in a Spark DataFrame, with
    support for excluding specific columns.

    Attributes:
        case_style (str): The desired case style for column names. Options:
            - "snake_case"
            - "camelCase"
            - "PascalCase"
            - "lowercase"
            - "uppercase"
        exclude_columns (list): List of column names to exclude from
            standardization.

    Example Usage:
        from pyspark.sql import SparkSession

        # Initialize Spark session
        spark = SparkSession.builder.appName(
            "ColumnNameStandardizerExample").getOrCreate()

        # Sample data
        data = spark.createDataFrame(
            [(1, "A", 3.0), (2, "B", 6.0)],
            ["Column 1", "column_2", "COLUMN_3"]
        )

        # Apply standardizer
        standardizer = SparkColumnNameStandardizer(
            case_style="snake_case",
            exclude_columns=["column_2"]
        )
        transformed_data = standardizer.transform(data)

        # Show results
        transformed_data.printSchema()
    """

    def __init__(
        self,
        case_style: str = "snake_case",
        exclude_columns: list = None
    ):
        """
        Initialize the SparkColumnNameStandardizer.

        Args:
            case_style (str): The desired case style for column names.
            exclude_columns (list, optional): List of column names to exclude
                from standardization.

        Raises:
            ValueError: If an invalid `case_style` is provided.
        """
        self.logger = get_logger()
        valid_styles = [
            "snake_case", "camelCase", "PascalCase", "lowercase", "uppercase"]

        # Validate inputs
        PandasValidationUtils.validate_is_non_empty_string(case_style)
        PandasValidationUtils.validate_case_style(
            case_style,
            valid_styles)

        self.case_style = case_style
        self.exclude_columns = exclude_columns or []
        self.logger.log(
            "info",
            f"Initialized with case_style: {case_style}, " +
            f"exclude_columns: {self.exclude_columns}")

    def transform(self, data: DataFrame) -> DataFrame:
        """
        Standardize column names in the DataFrame, excluding specified columns.

        Args:
            data (DataFrame): The input DataFrame.

        Returns:
            DataFrame: The DataFrame with standardized column names.

        Raises:
            KeyError: If any columns in `exclude_columns` do not exist in the
            DataFrame.

        Example:
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.appName(
            "ColumnNameStandardizerExample").getOrCreate()
        data = spark.createDataFrame(
            [(1, "A", 3.0), (2, "B", 6.0)],
            ["Column 1", "column_2", "COLUMN_3"]
        )
        standardizer = SparkColumnNameStandardizer(
            case_style="snake_case",
            exclude_columns=["column_2"]
        )
        transformed_data = standardizer.transform(data)
        transformed_data.show()
        """
        SparkValidationUtils.validate_is_dataframe(data, "data")

        # Validate excluded columns
        SparkValidationUtils.validate_columns_exist(
            data,
            self.exclude_columns,
            False)

        self.logger.log(
            "info",
            "Standardizing column names.")

        # Use the reusable PandasValidationUtils.transform_column_name
        new_columns = [
            col if col in self.exclude_columns else
            PandasValidationUtils.transform_column_name(col, self.case_style)
            for col in data.columns
        ]

        self.logger.log(
            "info",
            f"Column names standardized: {new_columns}")

        # Rename columns in the DataFrame
        data = data.toDF(*new_columns)
        return data


class SparkColumnNameRegexRenamer(Transformer):
    """
    Transformer to rename column names in a Spark DataFrame using
    regex patterns, with support for excluding specific columns.

    Attributes:
        pattern (str): The regex pattern to search for in column names.
        replacement (str): The replacement string for matching patterns.
        exclude_columns (list): List of column names to exclude from
            the transformation.

    Example Usage:
        from pyspark.sql import SparkSession

        # Initialize Spark session
        spark = SparkSession.builder.appName(
            "ColumnNameRegexRenamerExample").getOrCreate()

        # Sample data
        data = spark.createDataFrame(
            [(1, "A", 3.0), (2, "B", 6.0)],
            ["Column 1", "column-2", "COLUMN.3"]
        )

        # Apply renamer
        renamer = SparkColumnNameRegexRenamer(
            pattern=r"[^a-zA-Z0-9]",
            replacement="_",
            exclude_columns=["column-2"]
        )
        transformed_data = renamer.transform(data)

        # Show results
        transformed_data.printSchema()

        # Output schema:
        # root
        #  |-- Column_1: long (nullable = true)
        #  |-- column-2: string (nullable = true)
        #  |-- COLUMN_3: double (nullable = true)
    """

    def __init__(
        self,
        pattern: str,
        replacement: str,
        exclude_columns: list = None
    ):
        """
        Initialize the SparkColumnNameRegexRenamer.

        Args:
            pattern (str): The regex pattern to search for.
            replacement (str): The string to replace matching patterns with.
            exclude_columns (list, optional): List of column names to
                exclude from transformation.

        Raises:
            ValueError: If `pattern` or `replacement` is not a string.
        """
        self.logger = get_logger()
        PandasValidationUtils.validate_is_non_empty_string(pattern)
        PandasValidationUtils.validate_is_non_empty_string(replacement)
        self.pattern = pattern
        self.replacement = replacement
        self.exclude_columns = exclude_columns or []
        self.logger.log(
            "info",
            f"Initialized with pattern: {pattern}, replacement: \
                {replacement}, exclude_columns: {self.exclude_columns}")

    def transform(self, data: DataFrame) -> DataFrame:
        """
        Rename columns using regex patterns, excluding specified columns.

        Args:
            data (DataFrame): The input DataFrame.

        Returns:
            DataFrame: The DataFrame with updated column names.

        Raises:
            KeyError: If any columns in `exclude_columns` do not exist in
            the DataFrame.

        Example:
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.appName(
            "ColumnNameRegexRenamerExample").getOrCreate()
        data = spark.createDataFrame(
            [(1, "A", 3.0), (2, "B", 6.0)],
            ["Column 1", "column-2", "COLUMN.3"]
        )
        renamer = SparkColumnNameRegexRenamer(
            pattern=r"[^a-zA-Z0-9]",
            replacement="_",
            exclude_columns=["column-2"]
        )
        transformed_data = renamer.transform(data)
        transformed_data.show()
        """
        SparkValidationUtils.validate_is_dataframe(data, "data")
        if self.exclude_columns:
            SparkValidationUtils.validate_columns_exist(
                data,
                self.exclude_columns,
                False)

        self.logger.log(
            "info",
            f"Renaming columns using pattern '{self.pattern}' \
                with replacement '{self.replacement}'.")

        updated_columns = [
            PandasValidationUtils.rename_column_with_regex(
                col, self.pattern, self.replacement)
            if col not in self.exclude_columns else col
            for col in data.columns
        ]

        self.logger.log(
            "info",
            f"Updated column names: {updated_columns}")

        # Rename columns in the DataFrame
        data = data.toDF(*updated_columns)
        return data


class SparkColumnAdderStatic(Transformer):
    """
    Transformer to add a column with a static value to a Spark DataFrame.

    Attributes:
        column_name (str): The name of the new column.
        value (Any): The static value to assign to the new column.
        overwrite (bool): Whether to overwrite the column if it already exists.

    Example Usage:
        from pyspark.sql import SparkSession

        # Initialize Spark session
        spark = SparkSession.builder.appName(
            "StaticColumnAdderExample").getOrCreate()

        # Sample data
        data = spark.createDataFrame(
            [(1, "A"), (2, "B")],
            ["id", "name"]
        )

        # Apply static column adder
        static_adder = SparkColumnAdderStatic(
            column_name="status",
            value="active",
            overwrite=False
        )
        transformed_data = static_adder.transform(data)

        # Show results
        transformed_data.show()

        # Output:
        # +---+----+------+
        # | id|name|status|
        # +---+----+------+
        # |  1|   A|active|
        # |  2|   B|active|
        # +---+----+------+
    """

    def __init__(self, column_name: str, value: any, overwrite: bool = False):
        """
        Initialize the SparkColumnAdderStatic.

        Args:
            column_name (str): The name of the new column.
            value (Any): The static value to assign to the new column.
            overwrite (bool, optional): Whether to overwrite the column if
            it already exists. Defaults to False.

        Raises:
            ValueError: If `column_name` is not a string.
        """
        self.logger = get_logger()
        PandasValidationUtils.validate_is_non_empty_string(column_name)
        PandasValidationUtils.validate_is_boolean(overwrite)
        self.column_name = column_name
        self.value = value
        self.overwrite = overwrite
        self.logger.log(
            "info",
            f"Initialized with column_name: {column_name}, " +
            f"value: {value}, overwrite: {overwrite}")

    def transform(self, data: DataFrame) -> DataFrame:
        """
        Add a new column with a static value.

        Args:
            data (DataFrame): The input DataFrame.

        Returns:
            DataFrame: The DataFrame with the new column added.

        Raises:
            ValueError: If `column_name` already exists and
            `overwrite` is False.

        Example:
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.appName(
            "StaticColumnAdderExample").getOrCreate()
        data = spark.createDataFrame(
            [(1, "A"), (2, "B")],
            ["id", "name"]
        )
        static_adder = SparkColumnAdderStatic(
            column_name="status",
            value="active",
            overwrite=False
        )
        transformed_data = static_adder.transform(data)
        transformed_data.show()
        """
        SparkValidationUtils.validate_is_dataframe(data, "data")

        if self.column_name in data.columns and not self.overwrite:
            error_message = (
                f"Column '{self.column_name}' " +
                "already exists. Set overwrite=True to replace it."
            )
            self.logger.log(
                "error",
                error_message
            )
            raise ValueError(error_message)

        try:
            if self.column_name in data.columns and self.overwrite:
                self.logger.log(
                    "warning",
                    f"Overwriting existing column '{self.column_name}'."
                )
            data = data.withColumn(self.column_name, lit(self.value))
            self.logger.log(
                "info",
                f"Successfully added column '{self.column_name}' " +
                f"with static value: {self.value}"
            )
        except Exception as e:
            error_message = (
                f"Error adding static column '{self.column_name}': {e}")
            self.logger.log(
                "error",
                error_message)
            raise
        return data


class SparkColumnPatternDropper(Transformer):
    """
    Transformer to drop columns from a Spark DataFrame based on a
    regex pattern.

    Attributes:
        pattern (str): The regex pattern to match column names.
        exclude_columns (list): List of column names to exclude from
        being dropped.

    Example Usage:
        from pyspark.sql import SparkSession

        # Initialize Spark session
        spark = SparkSession.builder.appName(
            "ColumnPatternDropperExample").getOrCreate()

        # Sample data
        data = spark.createDataFrame(
            [(1, 2, 3)],
            ["temp_a", "temp_b", "temp_keep"]
        )

        # Apply pattern dropper
        pattern_dropper = SparkColumnPatternDropper(
            pattern=r"temp_.*",
            exclude_columns=["temp_keep"]
        )
        transformed_data = pattern_dropper.transform(data)

        # Show results
        transformed_data.printSchema()

        # Output schema:
        # root
        #  |-- temp_keep: long (nullable = true)
    """

    def __init__(
        self,
        pattern: str,
        exclude_columns: list = None
    ):
        """
        Initialize the SparkColumnPatternDropper.

        Args:
            pattern (str): The regex pattern to match column names.
            exclude_columns (list, optional): List of column names to exclude
            from dropping.

        Raises:
            ValueError: If `pattern` is not a string.
        """
        self.logger = get_logger()
        PandasValidationUtils.validate_is_non_empty_string(pattern)
        self.pattern = pattern
        self.exclude_columns = exclude_columns or []
        self.logger.log(
            "info",
            f"Initialized with pattern: {pattern}, " +
            f"exclude_columns: {self.exclude_columns}")

    def transform(self, data: DataFrame) -> DataFrame:
        """
        Drop columns matching the regex pattern.

        Args:
            data (DataFrame): The input DataFrame.

        Returns:
            DataFrame: The DataFrame with matching columns dropped.

        Raises:
            KeyError: If any columns in `exclude_columns` do not exist in
            the DataFrame.
        """
        SparkValidationUtils.validate_is_dataframe(data, "data")
        if self.exclude_columns:
            SparkValidationUtils.validate_columns_exist(
                data,
                self.exclude_columns,
                False)

        # Identify columns matching the pattern using SparkValidationUtils
        matching_columns = SparkValidationUtils.get_columns_matching_pattern(
            data,
            self.pattern,
            False)
        self.logger.log(
            "info",
            f"Columns matching pattern '{self.pattern}': {matching_columns}"
        )

        # Exclude specified columns
        columns_to_drop = [
            col for col in matching_columns if col not in self.exclude_columns
        ]
        self.logger.log(
            "info",
            f"Columns to drop (after exclusions): {columns_to_drop}"
        )

        # Drop matching columns
        remaining_columns = [
            col for col in data.columns if col not in columns_to_drop
        ]
        return data.select(*remaining_columns)


class SparkEmptyColumnDropper(Transformer):
    """
    Transformer to drop empty columns (all values are null) from a
    Spark DataFrame.

    Attributes:
        exclude_columns (list): List of column names to exclude from
            being dropped.

    Example Usage:
            from pyspark.sql import SparkSession
            from pyspark.sql.types import StructType, StructField, IntegerType

            # Initialize Spark session
            spark = SparkSession.builder.appName(
                "EmptyColumnDropperExample").getOrCreate()

            # Define schema
            schema = StructType([
                StructField("empty_col1", IntegerType(), True),
                StructField("non_empty_col", IntegerType(), True),
                StructField("empty_col2", IntegerType(), True)
            ])

            # Sample data
            data = spark.createDataFrame(
                [(None, 2, None)],
                schema=schema
            )

            # Apply empty column dropper
            empty_dropper = SparkEmptyColumnDropper(
                exclude_columns=["non_empty_col"]
            )
            transformed_data = empty_dropper.transform(data)

            # Show results
            transformed_data.printSchema()

            # Output schema:
            # root
            #  |-- non_empty_col: integer (nullable = true)
    """

    def __init__(self, exclude_columns: list = None):
        """
        Initialize the SparkEmptyColumnDropper.

        Args:
            exclude_columns (list, optional): List of column names to exclude
            from dropping.

        Raises:
            ValueError: If `exclude_columns` is not a list.
        """
        self.logger = get_logger()
        if exclude_columns:
            PandasValidationUtils.validate_is_non_empty_list(exclude_columns)
        self.exclude_columns = exclude_columns or []
        self.logger.log(
            "info",
            f"Initialized with exclude_columns: {self.exclude_columns}")

    def transform(self, data: DataFrame) -> DataFrame:
        """
        Drop columns where all values are null.

        Args:
            data (DataFrame): The input DataFrame.

        Returns:
            DataFrame: The DataFrame with empty columns dropped.

        Raises:
            KeyError: If any columns in `exclude_columns` do not exist in the
            DataFrame.

        Example:
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.appName(
            "EmptyColumnDropperExample").getOrCreate()
        data = spark.createDataFrame(
            [(None, 2, None)],
            schema="integer integer integer"
        )
        empty_dropper = SparkEmptyColumnDropper(
            exclude_columns=["integer"]
        )
        transformed_data = empty_dropper.transform(data)
        transformed_data.show()
        """
        SparkValidationUtils.validate_is_dataframe(data, "data")
        if self.exclude_columns:
            SparkValidationUtils.validate_columns_exist(
                data,
                self.exclude_columns,
                False)

        # Identify empty columns using SparkValidationUtils
        empty_columns = SparkValidationUtils.get_empty_columns(
            data,
            False)
        self.logger.log(
            "info",
            f"Empty columns identified: {empty_columns}"
        )

        # Exclude specified columns
        columns_to_drop = [
            col for col in empty_columns if col not in self.exclude_columns
        ]
        self.logger.log(
            "info",
            f"Columns to drop (after exclusions): {columns_to_drop}"
        )

        # Drop empty columns
        remaining_columns = [
            col for col in data.columns if col not in columns_to_drop
        ]
        return data.select(*remaining_columns)


class SparkColumnTypeDropper(Transformer):
    """
    Transformer to drop columns of specific data types from a Spark DataFrame.

    Attributes:
        data_types (list): List of data types to drop
            (e.g., [IntegerType, FloatType]).
        exclude_columns (list): List of column names to exclude
            from being dropped.

    Example Usage:
        from pyspark.sql import SparkSession
        from pyspark.sql.types import LongType, DoubleType

        # Initialize Spark session
        spark = SparkSession.builder.appName(
            "ColumnTypeDropperExample").getOrCreate()

        # Sample data
        data = spark.createDataFrame(
            [(1, 2.5, "text")],
            ["int_col", "float_col", "string_col"]
        )

        # Apply type dropper
        type_dropper = SparkColumnTypeDropper(
            data_types=[IntegerType, FloatType],
            exclude_columns=["int_col"]
        )
        transformed_data = type_dropper.transform(data)

        # Show results
        transformed_data.printSchema()

        # Output schema:
        # root
        #  |-- int_col: integer (nullable = true)
        #  |-- string_col: string (nullable = true)
    """

    def __init__(
        self,
        data_types: list,
        exclude_columns: list = None
    ):
        """
        Initialize the SparkColumnTypeDropper.

        Args:
            data_types (list): List of data types to drop
                (e.g., [IntegerType, FloatType]).
            exclude_columns (list, optional): List of column names to exclude
                from dropping.

        Raises:
            ValueError: If `data_types` is not a non-empty list.
        """
        self.logger = get_logger()
        PandasValidationUtils.validate_is_non_empty_list(data_types)
        self.data_types = data_types
        if exclude_columns:
            PandasValidationUtils.validate_is_non_empty_list(exclude_columns)
        self.exclude_columns = exclude_columns or []
        self.logger.log(
            "info",
            f"Initialized with data_types: {data_types}, " +
            f"exclude_columns: {self.exclude_columns}")

    def transform(self, data: DataFrame) -> DataFrame:
        """
        Drop columns of specified data types.

        Args:
            data (DataFrame): The input DataFrame.

        Returns:
            DataFrame: The DataFrame with specified columns dropped.

        Raises:
            KeyError: If any columns in `exclude_columns` do not exist
                in the DataFrame.

        Example:
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.appName(
            "ColumnTypeDropperExample").getOrCreate()
        data = spark.createDataFrame(
            [(1, 2.5, "text")],
            ["int_col", "float_col", "string_col"]
        )
        type_dropper = SparkColumnTypeDropper(
            data_types=[IntegerType, FloatType],
            exclude_columns=["int_col"]
        )
        transformed_data = type_dropper.transform(data)
        transformed_data.show()
        """
        SparkValidationUtils.validate_is_dataframe(data, "data")
        if self.exclude_columns:
            SparkValidationUtils.validate_columns_exist(
                data,
                self.exclude_columns,
                False)

        # Identify columns of specified data types using SparkValidationUtils
        columns_by_dtype = SparkValidationUtils.get_columns_by_dtypes(
            data,
            self.data_types,
            False)
        self.logger.log(
            "info",
            f"Columns with data types {self.data_types}: {columns_by_dtype}"
        )

        # Exclude specified columns
        columns_to_drop = [
            col for col in columns_by_dtype if col not in self.exclude_columns
        ]
        self.logger.log(
            "info",
            f"Columns to drop (after exclusions): {columns_to_drop}"
        )

        # Drop specified columns
        remaining_columns = [
            col for col in data.columns if col not in columns_to_drop
        ]
        return data.select(*remaining_columns)


class SparkNullRatioColumnDropper(Transformer):
    """
    Transformer to drop columns with a high percentage of null values from a
    Spark DataFrame.

    Attributes:
        threshold (float): The maximum null ratio allowed
            (e.g., 0.5 for 50% nulls).
        exclude_columns (list): List of column names to exclude
            from being dropped.

    Example Usage:
        from pyspark.sql import SparkSession
        from pyspark.sql.types import StructType, StructField, IntegerType

        # Initialize Spark session
        spark = SparkSession.builder.appName(
            "NullRatioColumnDropperExample").getOrCreate()

        # Define schema
        schema = StructType([
            StructField("col1", IntegerType(), True),
            StructField("col2", IntegerType(), True),
            StructField("col3", IntegerType(), True)
        ])

        # Sample data
        data = spark.createDataFrame(
            [(None, 2, None), (None, 3, 4)],
            schema=schema
        )

        # Apply null ratio dropper
        null_ratio_dropper = SparkNullRatioColumnDropper(
            threshold=0.5,
            exclude_columns=["col2"]
        )
        transformed_data = null_ratio_dropper.transform(data)

        # Show results
        transformed_data.printSchema()

        # Output schema:
        # root
        #  |-- col2: integer (nullable = true)
    """

    def __init__(
        self,
        threshold: float,
        exclude_columns: list = None
    ):
        """
        Initialize the SparkNullRatioColumnDropper.

        Args:
            threshold (float): The maximum null ratio allowed
                (e.g., 0.5 for 50% nulls).
            exclude_columns (list, optional): List of column names to exclude
                from dropping.

        Raises:
            ValueError: If `threshold` is not between 0 and 1.
        """
        self.logger = get_logger()
        PandasValidationUtils.validate_float(threshold)
        if not (0 <= threshold <= 1):
            error_message = "threshold must be between 0 and 1."
            self.logger.log(
                "error",
                error_message)
            raise ValueError(error_message)
        self.threshold = threshold
        self.exclude_columns = exclude_columns or []
        self.logger.log(
            "info",
            f"Initialized with threshold: {threshold}, " +
            f"exclude_columns: {self.exclude_columns}")

    def transform(self, data: DataFrame) -> DataFrame:
        """
        Drop columns with null ratios exceeding the threshold.

        Args:
            data (DataFrame): The input DataFrame.

        Returns:
            DataFrame: The DataFrame with columns dropped based on null ratio.

        Raises:
            KeyError: If any columns in `exclude_columns` do not exist
                in the DataFrame.

        Example:
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.appName(
            "NullRatioColumnDropperExample").getOrCreate()
        data = spark.createDataFrame(
            [(None, 2, None), (None, 3, 4)],
            schema=StructType([
                StructField("col1", IntegerType(), True),
                StructField("col2", IntegerType(), True),
                StructField("col3", IntegerType(), True)
        NullRatioDropper = SparkNullRatioColumnDropper(
            threshold=0.5,
            exclude_columns=["col2"])
        transformed_data = null_ratio_dropper.transform(data)
        transformed_data.show()
        """
        SparkValidationUtils.validate_is_dataframe(data, "data")
        if self.exclude_columns:
            SparkValidationUtils.validate_columns_exist(
                data,
                self.exclude_columns,
                False)

        # Identify columns with high null ratio
        total_rows = data.count()
        null_ratios = data.select([
            (count(when(
                col(c).isNull() | isnan(col(c)), c)) / total_rows).alias(c)
            for c in data.columns
        ]).first().asDict()

        columns_to_drop = [
            col for col, ratio in null_ratios.items()
            if ratio > self.threshold and col not in self.exclude_columns
        ]
        self.logger.log(
            "info",
            f"Columns to drop (based on null ratio): {columns_to_drop}"
        )

        # Drop columns
        remaining_columns = [
            col for col in data.columns if col not in columns_to_drop
        ]
        return data.select(*remaining_columns)


class SparkColumnSplitter(Transformer):
    """
    Transformer to split a column into multiple columns based on a delimiter
    or regex.

    Attributes:
        column (str): The column to split.
        pattern (str): The delimiter or regex pattern to use for splitting.
        regex (bool): Whether to treat the pattern as a regex. Defaults
            to False.
        new_columns (list): Optional list of new column names for the split
            columns. If not provided, dynamic names are used.

    Example Usage:
        from pyspark.sql import SparkSession

        # Initialize Spark session
        spark = SparkSession.builder.appName(
            "ColumnSplitterExample").getOrCreate()

        # Sample data
        data = spark.createDataFrame(
            [("John Doe",), ("Jane Smith",)],
            ["full_name"]
        )

        # Apply column splitter
        splitter = SparkColumnSplitter(
            column="full_name",
            pattern=" ",
            regex=False,
            new_columns=["first_name", "last_name"],
            drop_original=False
        )
        transformed_data = splitter.transform(data)

        # Show results
        transformed_data.show()

        # Output:
        # +----------+-----------+----------+
        # | full_name| first_name| last_name|
        # +----------+-----------+----------+
        # |  John Doe|       John|       Doe|
        # |Jane Smith|       Jane|     Smith|
        # +----------+-----------+----------+
    """

    def __init__(
        self,
        column: str,
        pattern: str,
        regex: bool = False,
        new_columns: list = None,
        drop_original: bool = True
    ):
        """
        Initialize the SparkColumnSplitter.

        Args:
            column (str): The column to split.
            pattern (str): The delimiter or regex pattern to use for splitting.
            regex (bool): Whether to treat the pattern as a regex. Defaults
                to False.
            new_columns (list, optional): List of new column names for
                the split columns.
            drop_original (bool): Whether to drop the original column after
                splitting. Defaults to True.
        """
        self.logger = get_logger()
        PandasValidationUtils.validate_is_non_empty_string(column)
        PandasValidationUtils.validate_is_non_empty_string(pattern)
        PandasValidationUtils.validate_is_boolean(regex)
        PandasValidationUtils.validate_is_boolean(drop_original)
        if new_columns:
            PandasValidationUtils.validate_is_non_empty_list(new_columns)
        self.column = column
        self.pattern = pattern
        self.regex = regex
        self.drop_original = drop_original
        self.new_columns = new_columns
        self.logger.log(
            "info",
            f"Initialized with column: {column}, pattern: {pattern}, regex: " +
            f"{regex}, new_columns: {new_columns}")

    def transform(self, data: DataFrame) -> DataFrame:
        """
        Split a column into multiple columns.

        Args:
            data (DataFrame): The input DataFrame.

        Returns:
            DataFrame: The DataFrame with the column split into new columns.

        Raises:
            ValueError: If the number of new columns does not match
                the number of splits.

        Example:
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.appName(
            "ColumnSplitterExample").getOrCreate()
        data = spark.createDataFrame(
            [("John Doe",), ("Jane Smith",)],
            ["full_name"]
        )
        splitter = SparkColumnSplitter(
            column="full_name",
            pattern=" ",
            regex=False,
            new_columns=["first_name", "last_name"],
            drop_original=False)
        transformed_data = splitter.transform(data)
        transformed_data.show()

        """
        SparkValidationUtils.validate_is_dataframe(data, "data")
        SparkValidationUtils.validate_columns_exist(
            data,
            [self.column],
            False)

        self.logger.log(
            "info",
            f"Splitting column '{self.column}' using pattern " +
            f"'{self.pattern}' (regex={self.regex}).")

        # Perform the split
        split_col = split(col(self.column), self.pattern) if \
            not self.regex else split(col(self.column), self.pattern, -1)

        # Determine the number of splits dynamically
        num_splits = data.select(split_col).head(1)[0][0].__len__()

        # Dynamically assign column names if new_columns is not provided
        if not self.new_columns:
            self.logger.log(
                "info",
                "No new_columns provided. Generating default column names.")
            self.new_columns = [
                f"{self.column}_split_{i}" for i in range(num_splits)]
        elif len(self.new_columns) != num_splits:
            error_message = (
                f"Number of new_columns ({len(self.new_columns)}) " +
                f"does not match the number of splits ({num_splits})."
            )
            self.logger.log(
                "error",
                error_message)
            raise ValueError(error_message)

        self.logger.log(
            "info",
            f"Split columns: {self.new_columns}")

        # Add the split columns to the DataFrame
        for i, new_col in enumerate(self.new_columns):
            data = data.withColumn(new_col, split_col.getItem(i))

        # Drop the original column
        if self.drop_original:
            data = data.drop(self.column)
            self.logger.log(
                "info",
                f"Column '{self.column}' dropped after splitting.")

        return data


class SparkColumnMerger(Transformer):
    """
    Transformer to merge multiple columns into a single column.

    Attributes:
        columns (list): List of columns to merge.
        new_column (str): Name of the new merged column.
        separator (str): Separator to use between values.
        drop_originals (bool): Whether to drop the original columns
        after merging.

    Example Usage:
        from pyspark.sql import SparkSession

        # Initialize Spark session
        spark = SparkSession.builder.appName(
            "ColumnMergerExample").getOrCreate()

        # Sample data
        data = spark.createDataFrame(
            [("John", "Doe"), ("Jane", "Smith")],
            ["first_name", "last_name"]
        )

        # Apply column merger
        merger = SparkColumnMerger(
            columns=["first_name", "last_name"],
            new_column="full_name",
            separator=" ",
            drop_originals=True
        )
        transformed_data = merger.transform(data)

        # Show results
        transformed_data.show()

        # Output:
        # +----------+
        # | full_name|
        # +----------+
        # |  John Doe|
        # |Jane Smith|
        # +----------+
    """

    def __init__(
        self,
        columns: list,
        new_column: str,
        separator: str = " ",
        drop_originals: bool = True
    ):
        """
        Initialize the SparkColumnMerger.

        Args:
            columns (list): List of columns to merge.
            new_column (str): Name of the new merged column.
            separator (str): Separator to use between values.
            drop_originals (bool): Whether to drop the original columns after
                merging. Defaults to True.

        Raises:
            ValueError: If `columns` is not a list or `new_column` is not
            a string.
        """
        self.logger = get_logger()
        PandasValidationUtils.validate_is_non_empty_list(columns)
        PandasValidationUtils.validate_is_non_empty_string(new_column)
        PandasValidationUtils.validate_is_non_empty_string(separator)
        PandasValidationUtils.validate_is_boolean(drop_originals)
        self.columns = columns
        self.new_column = new_column
        self.separator = separator
        self.drop_originals = drop_originals
        self.logger.log(
            "info",
            f"Initialized with columns: {columns}, " +
            f"new_column: {new_column}, " +
            f"separator: {separator}, drop_originals: {drop_originals}")

    def transform(self, data: DataFrame) -> DataFrame:
        """
        Merge multiple columns into a single column.

        Args:
            data (DataFrame): The input DataFrame.

        Returns:
            DataFrame: The DataFrame with the new merged column.

        Raises:
            KeyError: If any of the specified columns do not exist in
            the DataFrame.

        Example:
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.appName(
            "ColumnMergerExample").getOrCreate()
        data = spark.createDataFrame(
            [("John", "Doe"), ("Jane", "Smith")],
            ["first_name", "last_name"]
        )
        merger = SparkColumnMerger(
            columns=["first_name", "last_name"],
            new_column="full_name",
            separator=" ",
            drop_originals=True)
        transformed_data = merger.transform(data)
        transformed_data.show()
        """
        SparkValidationUtils.validate_is_dataframe(data, "data")
        SparkValidationUtils.validate_columns_exist(
            data,
            self.columns,
            False)

        # Log the merging operation
        self.logger.log(
            "info",
            f"Merging columns {self.columns} into '{self.new_column}' "
            f"with separator '{self.separator}'."
        )

        # Perform the merge
        try:
            data = data.withColumn(
                self.new_column,
                concat_ws(self.separator, *[col(c) for c in self.columns]))
            self.logger.log(
                "info",
                f"New column '{self.new_column}' created successfully."
            )
        except Exception as e:
            error_message = (
                f"Error while creating new column '{self.new_column}': {e}")
            self.logger.log(
                "error",
                error_message
            )
            raise Exception(error_message)

        # Drop the original columns if specified
        if self.drop_originals:
            data = data.drop(*self.columns)
            self.logger.log(
                "info",
                f"Original columns {self.columns} dropped after merging."
            )

        return data


class SparkRowFilter(Transformer):
    """
    Transformer to filter rows in a Spark DataFrame based on a condition.

    Attributes:
        condition (Callable): A function that takes a DataFrame and returns a
        Boolean column, where `True` indicates rows to keep and
        `False` indicates rows to drop.

    Example Usage:
        from pyspark.sql import SparkSession
        from pyspark.sql.functions import col

        # Initialize Spark session
        spark = SparkSession.builder.appName("RowFilterExample").getOrCreate()

        # Sample data
        data = spark.createDataFrame(
            [(1,), (2,), (3,)],
            ["value"]
        )

        # Apply row filter
        row_filter = SparkRowFilter(condition=lambda df: col("value") > 1)
        transformed_data = row_filter.transform(data)

        # Show results
        transformed_data.show()

        # Output:
        # +-----+
        # |value|
        # +-----+
        # |    2|
        # |    3|
        # +-----+
    """
    def __init__(self, condition):
        """
        Initialize the SparkRowFilter.

        Args:
            condition (Callable or str): A function or a string representation
            of a function that takes a DataFrame and returns a Boolean column.

        Raises:
            ValueError: If `condition` is not callable or a valid
                function string.
        """
        self.logger = get_logger()

        # If condition is a string, evaluate it into a callable function
        if isinstance(condition, str):
            try:
                self.condition = eval(condition)
                if not callable(self.condition):
                    raise ValueError("Condition is not a valid callable.")
            except Exception as e:
                self.logger.log(
                    "error",
                    f"Failed to evaluate condition: {e}")
                raise ValueError(
                    "Condition string must evaluate to a callable.")
        elif callable(condition):
            self.condition = condition
        else:
            error_message = (
                f"Condition must be callable. Got {type(condition)}.")
            self.logger.log(
                "error",
                error_message)
            raise ValueError(error_message)

        self.logger.log(
            "info",
            f"Row filter initialized with condition: {condition}")

    def transform(self, data: DataFrame, **kwargs) -> DataFrame:
        """
        Filter rows based on the provided condition.

        Args:
            data (DataFrame): The input DataFrame.
            **kwargs: Additional parameters for future filtering logic.

        Returns:
            DataFrame: The filtered DataFrame.

        Raises:
            ValueError: If the condition does not return a Boolean column.

        Example:
        from pyspark.sql import SparkSession
        from pyspark.sql.functions import col
        spark = SparkSession.builder.appName("RowFilterExample").getOrCreate()
        data = spark.createDataFrame(
            [(1,), (2,), (2,)],
            ["value"]
        )
        row_filter = SparkRowFilter(condition=lambda df: col("value") > 1)
        transformed_data = row_filter.transform(data)
        transformed_data.show()
        """

        SparkValidationUtils.validate_is_dataframe(data, "data")

        self.logger.log(
            "info",
            "Applying row filter condition.")
        try:
            # Apply the condition
            mask = self.condition(data)
            if not isinstance(mask, Column):
                error_message = (
                    "Condition must return a Boolean column. " +
                    "Got {type(mask)}.")
                self.logger.log(
                    "error",
                    error_message)
                raise ValueError(error_message)

            # Filter rows based on the mask
            filtered_data = data.filter(mask)
            self.logger.log(
                "info",
                f"Rows filtered: {filtered_data.count()} rows retained."
            )
            return filtered_data
        except Exception as e:
            self.logger.log(
                "error",
                f"Error applying row filter: {e}"
            )
            raise


class SparkRowDeduplicator(Transformer):
    """
    Transformer to remove duplicate rows from a Spark DataFrame.

    Attributes:
        subset (list, optional): List of column names to consider for
        identifying duplicates. If None, all columns are considered.
        keep (str, optional): Determines which duplicates to keep:
            - "first" (default): Keep the first occurrence.
            - "last": Keep the last occurrence.

    Example Usage:
        from pyspark.sql import SparkSession

        # Initialize Spark session
        spark = SparkSession.builder.appName(
            "RowDeduplicatorExample").getOrCreate()

        # Sample data
        data = spark.createDataFrame(
            [(1, "A"), (2, "B"), (1, "A")],
            ["col1", "col2"]
        )

        # Apply row deduplicator
        deduplicator = SparkRowDeduplicator(
            subset=["col1", "col2"], keep="first")
        transformed_data = deduplicator.transform(data)

        # Show results
        transformed_data.show()

        # Output:
        # +----+----+
        # |col1|col2|
        # +----+----+
        # |   1|   A|
        # |   2|   B|
        # +----+----+
    """

    def __init__(
        self,
        subset: list = None,
        keep: str = "first"
    ):
        """
        Initialize the SparkRowDeduplicator.

        Args:
            subset (list, optional): List of column names to consider for
                identifying duplicates.
            keep (str, optional): Determines which duplicates to keep.
                Options: "first", "last".

        Raises:
            ValueError: If `keep` is not one of "first" or "last".
        """
        self.logger = get_logger()
        valid_keep_options = {"first", "last"}
        if keep not in valid_keep_options:
            error_message = (
                f"Invalid value for 'keep': {keep}. " +
                f"Must be one of {valid_keep_options}.")
            self.logger.log(
                "error",
                f"Invalid value for 'keep': {keep}. " +
                f"Must be one of {valid_keep_options}."
            )
            raise ValueError(error_message)
        if subset:
            PandasValidationUtils.validate_is_non_empty_list(subset)
        self.subset = subset
        self.keep = keep
        self.logger.log(
            "info",
            f"Initialized with subset: {subset}, keep: {keep}")

    def transform(self, data: DataFrame, **kwargs) -> DataFrame:
        """
        Remove duplicate rows from the DataFrame.

        Args:
            data (DataFrame): The input DataFrame.
            **kwargs: Additional parameters for `dropDuplicates()`.

        Returns:
            DataFrame: The DataFrame with duplicates removed.

        Raises:
            ValueError: If the input data is not a Spark DataFrame.

        Example:
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.appName(
            "RowDeduplicatorExample").getOrCreate()
        data = spark.createDataFrame(
            [(1, "A"), (2, "B"), (1, "A")],
            ["col1", "col2"]
        )
        deduplicator = SparkRowDeduplicator(
            subset=["col1", "col2"], keep="first")
        transformed_data = deduplicator.transform(data)
        transformed_data.show()
        """
        SparkValidationUtils.validate_is_dataframe(data, "data")
        SparkValidationUtils.validate_columns_exist(
            data,
            self.subset,
            False)

        self.logger.log(
            "info",
            "Identifying duplicates.")

        try:
            # Apply deduplication
            if self.keep == "first":
                deduplicated_data = data.dropDuplicates(subset=self.subset)
            elif self.keep == "last":
                deduplicated_data = data.orderBy(
                    *[col(c).desc() for c in self.subset])\
                    .dropDuplicates(subset=self.subset)

            num_duplicates = data.count() - deduplicated_data.count()
            self.logger.log(
                "info",
                f"Duplicates removed. {num_duplicates} rows dropped."
            )

            return deduplicated_data
        except Exception as e:
            self.logger.log(
                "error",
                f"Error during deduplication: {e}"
            )
            raise


class SparkRowSorter(Transformer):
    """
    Transformer to sort rows in a Spark DataFrame.

    Attributes:
        by (list): List of column names to sort by.
        ascending (bool or list): Sort ascending or descending.
            Defaults to True.
        na_position (str): How to handle `NaN` values. Options are "first"
            or "last". Defaults to "last".

    Example Usage:
        from pyspark.sql import SparkSession

        # Initialize Spark session
        spark = SparkSession.builder.appName("RowSorterExample").getOrCreate()

        # Sample data
        data = spark.createDataFrame(
            [(1, "A"), (3, "C"), (2, "B")],
            ["value", "category"]
        )

        # Apply row sorter
        row_sorter = SparkRowSorter(
            by=["value"],
            ascending=True
        )
        transformed_data = row_sorter.transform(data)

        # Show results
        transformed_data.show()

        # Output:
        # +-----+--------+
        # |value|category|
        # +-----+--------+
        # |    1|       A|
        # |    2|       B|
        # |    3|       C|
        # +-----+--------+
    """

    def __init__(
        self,
        by: list,
        ascending: bool = True,
        na_position: str = "last"
    ):
        """
        Initialize the SparkRowSorter.

        Args:
            by (list): List of column names to sort by.
            ascending (bool, optional): Sort ascending or descending.
                Defaults to True.
            na_position (str, optional): How to handle `NaN` values.
                Defaults to "last".

        Raises:
            ValueError: If `by` is not a non-empty list or `na_position`
                is invalid.
        """
        self.logger = get_logger()
        valid_na_positions = {"first", "last"}
        PandasValidationUtils.validate_is_non_empty_list(by)
        if na_position not in valid_na_positions:
            error_message = (
                f"Invalid value for na_position: {na_position}. " +
                f"Must be one of {valid_na_positions}."
            )
            self.logger.log(
                "error",
                error_message)
            raise ValueError(error_message)
        self.by = by
        self.ascending = ascending
        self.na_position = na_position
        self.logger.log(
            "info",
            f"Initialized with by: {by}, ascending: " +
            f"{ascending}, na_position: {na_position}"
        )

    def transform(self, data: DataFrame, **kwargs) -> DataFrame:
        """
        Sort rows in the DataFrame.

        Args:
            data (DataFrame): The input DataFrame.
            **kwargs: Additional parameters for future extensions.

        Returns:
            DataFrame: The sorted DataFrame.

        Raises:
            ValueError: If the input data is not a Spark DataFrame.

        Example:
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.appName(
            "RowSorterExample").getOrCreate()
        data = spark.createDataFrame(
            [(1, "A"), (3, "C"), (2, "B")],
            ["value", "category"]
        )
        row_sorter = SparkRowSorter(
            by=["value"],
            ascending=True
        )
        transformed_data = row_sorter.transform(data)
        transformed_data.show()
        """
        SparkValidationUtils.validate_is_dataframe(data, "data")
        SparkValidationUtils.validate_columns_exist(
            data,
            self.by,
            False)

        self.logger.log(
            "info",
            f"Sorting rows by: {self.by}, ascending: " +
            f"{self.ascending}, na_position: {self.na_position}"
        )

        try:
            # Apply sorting
            sort_cols = [
                col(c).asc() if asc else col(c).desc()
                for c, asc in zip(
                    self.by,
                    self.ascending if isinstance(
                        self.ascending, list)
                    else [self.ascending] * len(self.by))
            ]

            sorted_data = data.sort(*sort_cols)
            self.logger.log(
                "info",
                "Rows sorted successfully."
            )
            return sorted_data
        except Exception as e:
            error_message = f"Error during sorting: {e}"
            self.logger.log(
                "error",
                error_message)
            raise Exception(error_message)


class SparkRowSplitter(Transformer):
    """
    Transformer to split rows in a Spark DataFrame based on a column
    containing lists or delimited strings.

    Attributes:
        column (str): The column to split.
        delimiter (str, optional): The delimiter to split strings in the
            column. Defaults to None (expects lists).

    Example Usage:
        from pyspark.sql import SparkSession

        # Initialize Spark session
        spark = SparkSession.builder.appName(
            "RowSplitterExample").getOrCreate()

        # Sample data with lists
        data = spark.createDataFrame(
            [(1, ["A", "B"]), (2, ["C"]), (3, [])],
            ["id", "tags"]
        )

        # Apply row splitter for lists
        row_splitter = SparkRowSplitter(column="tags")
        transformed_data = row_splitter.transform(data)
        transformed_data.show()

        # Sample data with delimited strings
        data = spark.createDataFrame(
            [(1, "A,B,C"), (2, "D,E")],
            ["id", "tags"]
        )

        # Apply row splitter for delimited strings
        row_splitter = SparkRowSplitter(column="tags", delimiter=",")
        transformed_data = row_splitter.transform(data)
        transformed_data.show()

        # Output:
        # +---+----+
        # | id|tags|
        # +---+----+
        # |  1|   A|
        # |  1|   B|
        # |  1|   C|
        # |  2|   D|
        # |  2|   E|
        # +---+----+
    """

    def __init__(self, column: str, delimiter: str = None):
        """
        Initialize the SparkRowSplitter.

        Args:
            column (str): The column to split.
            delimiter (str, optional): The delimiter to split strings in
            the column. Defaults to None.

        Raises:
            ValueError: If `column` is not a string or empty.
        """
        self.logger = get_logger()
        PandasValidationUtils.validate_is_non_empty_string(column)
        self.column = column
        if delimiter:
            PandasValidationUtils.validate_is_non_empty_string(delimiter)
        self.delimiter = delimiter
        self.logger.log(
            "info",
            f"Initialized with column: {column}, delimiter: {delimiter}")

    def transform(self, data: DataFrame, **kwargs) -> DataFrame:
        """
        Split rows based on the specified column.

        Args:
            data (DataFrame): The input DataFrame.
            **kwargs: Additional parameters for future extensions.

        Returns:
            DataFrame: The DataFrame with rows split based on the column.

        Raises:
            KeyError: If the specified column does not exist in the DataFrame.
            ValueError: If the column values are not lists or strings with the
            specified delimiter.

        Example:
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.appName(
            "RowSplitterExample").getOrCreate()
        data = spark.createDataFrame(
            [(1, ["A", "B"]), (2, ["C"]), (3, [])],
            ["id", "tags"]
        )
        row_splitter = SparkRowSplitter(column="tags")
        transformed_data = row_splitter.transform(data)
        transformed_data.show()
        """
        SparkValidationUtils.validate_is_dataframe(data, "data")
        SparkValidationUtils.validate_columns_exist(
            data,
            [self.column],
            False)

        self.logger.log(
            "info",
            f"Splitting rows based on column '{self.column}'.")
        try:
            if self.delimiter:
                # Validate column contains delimiter
                SparkValidationUtils.validate_column_contains_delimiter(
                    data,
                    self.column,
                    self.delimiter,
                    False
                )
                # Split and explode delimited strings
                expanded_data = data.withColumn(
                    self.column,
                    split(
                        col(self.column), self.delimiter))
            else:
                # Validate column is list type
                SparkValidationUtils.validate_column_is_list_type(
                    data,
                    self.column,
                    False)
                expanded_data = data

            # Explode the column to split rows
            result = expanded_data.withColumn(
                self.column, explode(col(self.column)))
            self.logger.log(
                "info",
                f"Rows expanded. Original rows: {data.count()}, " +
                f"New rows: {result.count()}"
            )
            return result
        except Exception as e:
            error_message = f"Error during row splitting: {e}"
            self.logger.log(
                "error",
                error_message)
            raise Exception(error_message)


class SparkRowAggregator(Transformer):
    """
    Transformer to aggregate rows in a Spark DataFrame by grouping them based
    on specified columns.

    Attributes:
        group_by (list): List of columns to group by.
        agg_config (dict): Dictionary specifying the aggregation configuration.
            Keys are column names, and values are aggregation functions.

    Example Usage:
        from pyspark.sql import SparkSession

        # Initialize Spark session
        spark = SparkSession.builder.appName(
            "RowAggregatorExample").getOrCreate()

        # Sample data
        data = spark.createDataFrame(
            [("A", 10), ("B", 20), ("A", 30)],
            ["category", "value"]
        )

        # Apply row aggregator
        row_aggregator = SparkRowAggregator(
            group_by=["category"],
            agg_config={"value": "sum"}
        )
        transformed_data = row_aggregator.transform(data)

        # Show results
        transformed_data.show()

        # Output:
        # +--------+-----+
        # |category|value|
        # +--------+-----+
        # |       A|   40|
        # |       B|   20|
        # +--------+-----+
    """

    def __init__(
        self,
        group_by: list,
        agg_config: dict
    ):
        """
        Initialize the SparkRowAggregator.

        Args:
            group_by (list): List of columns to group by.
            agg_config (dict): Dictionary specifying the
                aggregation configuration.

        Raises:
            ValueError: If `group_by` is not a non-empty list or `agg_config`
                is not a dictionary.
        """
        self.logger = get_logger()
        PandasValidationUtils.validate_is_non_empty_list(group_by)
        PandasValidationUtils.validate_is_non_empty_dict(agg_config)
        self.group_by = group_by
        self.agg_config = agg_config
        self.logger.log(
            "info",
            f"Initialized with group_by: {group_by}, agg_config: {agg_config}")

    def transform(self, data: DataFrame, **kwargs) -> DataFrame:
        """
        Aggregate rows in the DataFrame.

        Args:
            data (DataFrame): The input DataFrame.
            **kwargs: Additional parameters for future extensions.

        Returns:
            DataFrame: The aggregated DataFrame.

        Raises:
            KeyError: If any columns in `group_by` or `agg_config` do not exist
            in the DataFrame.

        Example:
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.appName(
            "RowAggregatorExample").getOrCreate()
        data = spark.createDataFrame(
            [("A", 10), ("B", 20), ("A", 30)],
            ["category", "value"]
        )
        row_aggregator = SparkRowAggregator(
            group_by=["category"],
            agg_config={"value": "sum"}
        )
        transformed_data = row_aggregator.transform(data)
        transformed_data.show()
        """
        SparkValidationUtils.validate_is_dataframe(data, "data")
        SparkValidationUtils.validate_columns_exist(
            data,
            self.group_by,
            False)
        SparkValidationUtils.validate_columns_exist(
            data,
            list(self.agg_config.keys()),
            False)

        self.logger.log(
            "info",
            f"Aggregating rows grouped by: {self.group_by} " +
            f"with configuration: {self.agg_config}"
        )
        try:
            # Perform group-by and aggregation using utility
            aggregated_data = SparkValidationUtils.group_and_aggregate(
                data,
                self.group_by,
                self.agg_config,
                False,
                **kwargs
            )
            self.logger.log(
                "info",
                "Aggregation completed successfully."
            )
            return aggregated_data
        except Exception as e:
            error_message = f"Error during aggregation: {e}"
            self.logger.log(
                "error",
                error_message)
            raise Exception(error_message)


class SparkRowAppender(Transformer):
    """
    Transformer to append rows to a Spark DataFrame.

    Attributes:
        rows (DataFrame or list): Rows to append to the DataFrame.

    Example Usage:
        from pyspark.sql import SparkSession

        # Initialize Spark session
        spark = SparkSession.builder.appName(
            "RowAppenderExample").getOrCreate()

        # Sample data
        data = spark.createDataFrame(
            [("A", 10), ("B", 20)],
            ["category", "value"]
        )

        # Rows to append
        new_rows = spark.createDataFrame(
            [("C", 30)],
            ["category", "value"]
        )

        # Apply row appender
        row_appender = SparkRowAppender(rows=new_rows)
        transformed_data = row_appender.transform(data)

        # Show results
        transformed_data.show()

        # Output:
        # +--------+-----+
        # |category|value|
        # +--------+-----+
        # |       A|   10|
        # |       B|   20|
        # |       C|   30|
        # +--------+-----+
    """

    def __init__(self, rows: DataFrame):
        """
        Initialize the SparkRowAppender.

        Args:
            rows (DataFrame or list): Rows to append to the DataFrame.

        Raises:
            ValueError: If `rows` is not a Spark DataFrame.
        """
        self.logger = get_logger()
        SparkValidationUtils.validate_is_dataframe(rows, "rows")
        self.rows = rows
        self.logger.log(
            "info",
            f"Initialized with rows to append: {rows.count()} rows.")

    def transform(self, data: DataFrame, **kwargs) -> DataFrame:
        """
        Append rows to the DataFrame.

        Args:
            data (DataFrame): The input DataFrame.
            **kwargs: Additional parameters for future extensions.

        Returns:
            DataFrame: The DataFrame with rows appended.

        Raises:
            ValueError: If appended rows have inconsistent columns.
        Example:
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.appName(
            "RowAppenderExample").getOrCreate()
        data = spark.createDataFrame(
            [("A", 10), ("B", 20)],
            ["category", "value"]
        )
        new_rows = spark.createDataFrame(
            [("C", 30)],
            ["category", "value"]
        )
        row_appender = SparkRowAppender(rows=new_rows)
        transformed_data = row_appender.transform(data)
        transformed_data.show()
        """
        SparkValidationUtils.validate_is_dataframe(data, "data")

        self.logger.log(
            "info",
            "Appending rows to the DataFrame.")
        try:
            # Validate that columns match
            if set(
                    self.rows.columns) != set(data.columns):
                error_message = (
                    "Appended rows must have the same columns as" +
                    "the existing DataFrame.")
                self.logger.log(
                    "error",
                    error_message)
                raise ValueError(error_message)

            # Append rows
            transformed_data = data.unionByName(self.rows)
            self.logger.log(
                "info",
                f"Rows appended successfully. Original rows: {data.count()}, "
                f"New rows: {self.rows.count()}, "
                f"Final rows: {transformed_data.count()}"
            )
            return transformed_data
        except Exception as e:
            error_message = f"Error appending rows: {e}"
            self.logger.log(
                "error",
                error_message)
            raise Exception(error_message)


class SparkRowSampler(Transformer):
    """
    Transformer to sample rows from a Spark DataFrame.

    Attributes:
        mode (str): Sampling mode. Options are:
            - "random": Random sampling.
            - "head": Select the first `n` rows.
            - "tail": Select the last `n` rows.
        n (int, optional): Number of rows to sample. Required for
            "head" and "tail".
        frac (float, optional): Fraction of rows to sample.
            Required for "random".
        replace (bool, optional): Whether to sample with replacement
            (only applicable for "random"). Defaults to False.

    Example Usage:
        from pyspark.sql import SparkSession

        # Initialize Spark session
        spark = SparkSession.builder.appName("RowSamplerExample").getOrCreate()

        # Sample data
        data = spark.createDataFrame(
            [(1, "A"), (2, "B"), (3, "C")],
            ["id", "category"]
        )

        # Random sampling
        sampler = SparkRowSampler(mode="random", frac=0.5, replace=False)
        transformed_data = sampler.transform(data)
        transformed_data.show()

        # Select the first 2 rows
        sampler = SparkRowSampler(mode="head", n=2)
        transformed_data = sampler.transform(data)
        transformed_data.show()

        # Select the last 2 rows
        sampler = SparkRowSampler(mode="tail", n=2)
        transformed_data = sampler.transform(data)
        transformed_data.show()
    """

    def __init__(
        self,
        mode: str,
        n: int = None,
        frac: float = None,
        replace: bool = False
    ):
        """
        Initialize the SparkRowSampler.

        Args:
            mode (str): Sampling mode. Options are "random", "head", "tail".
            n (int, optional): Number of rows to sample for "head" or "tail".
            frac (float, optional): Fraction of rows to sample for "random".
            replace (bool, optional): Whether to sample with replacement for
                "random". Defaults to False.

        Raises:
            ValueError: If invalid sampling parameters are provided.
        """
        self.logger = get_logger()
        valid_modes = {"random", "head", "tail"}
        if mode not in valid_modes:
            error_message = (
                f"Invalid mode: {mode}. Must be one of {valid_modes}.")
            self.logger.log(
                "error",
                error_message)
            raise ValueError(error_message)
        PandasValidationUtils.validate_is_non_empty_string(mode)
        self.mode = mode
        if n is not None:
            PandasValidationUtils.validate_is_integer(n)
        self.n = n
        if frac is not None:
            PandasValidationUtils.validate_float(frac)
        self.frac = frac
        PandasValidationUtils.validate_is_boolean(replace)
        self.replace = replace
        self.logger.log(
            "info",
            (
                f"Initialized with mode: {mode}, n: " +
                f"{n}, frac: {frac}, replace: {replace}")
        )

    def transform(self, data: DataFrame, **kwargs) -> DataFrame:
        """
        Sample rows from the DataFrame.

        Args:
            data (DataFrame): The input DataFrame.
            **kwargs: Additional parameters for sampling.

        Returns:
            DataFrame: The sampled DataFrame.

        Example:
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.appName("RowSamplerExample").getOrCreate()
        data = spark.createDataFrame(
            [(1, "A"), (2, "B"), (3, "C")],
            ["id", "category"]
        )
        sampler = SparkRowSampler(mode="random", frac=0.5, replace=False)
        transformed_data = sampler.transform(data)
        transformed_data.show()
        """
        SparkValidationUtils.validate_is_dataframe(data, "data")

        self.logger.log(
            "info",
            f"Sampling rows with mode: {self.mode}, n: {self.n}, frac: "
            f"{self.frac}, replace: {self.replace}"
        )
        try:
            if self.mode == "random":
                sampled_data = data.sample(
                    withReplacement=self.replace,
                    fraction=self.frac,
                    **kwargs
                )
            elif self.mode == "head":
                sampled_data = data.limit(self.n)
            elif self.mode == "tail":
                total_rows = data.count()
                start_row = max(0, total_rows - self.n)
                sampled_data = data.rdd.zipWithIndex().filter(
                    lambda row_index: row_index[1] >= start_row
                ).map(lambda row_index: row_index[0]).toDF(data.schema)
            else:
                error_message = f"Unsupported sampling mode: {self.mode}"
                self.logger.log(
                    "error",
                    error_message)
                raise ValueError(error_message)

            self.logger.log(
                "info",
                f"Sampling completed. Result: {sampled_data.count()} rows."
            )
            return sampled_data
        except Exception as e:
            error_message = f"Error sampling rows: {e}"
            self.logger.log(
                "error",
                error_message)
            raise Exception(error_message)


class SparkRowDuplicator(Transformer):
    """
    Transformer to duplicate rows in a Spark DataFrame based on a condition.

    Attributes:
        condition (Callable): A function that takes a DataFrame and returns a
            Boolean column, where `True` indicates rows to duplicate.
        times (int, optional): Number of times to duplicate the matching rows.
            Defaults to 1.

    Example Usage:
        from pyspark.sql import SparkSession
        from pyspark.sql.functions import col

        # Initialize Spark session
        spark = SparkSession.builder.appName(
            "RowDuplicatorExample").getOrCreate()

        # Sample data
        data = spark.createDataFrame(
            [(1, "Pending"), (2, "Complete"), (3, "Pending")],
            ["id", "status"]
        )

        # Duplicate rows where status is 'Pending'
        duplicator = SparkRowDuplicator(
            condition=lambda df: df["status"] == "Pending",
            times=2
        )
        transformed_data = duplicator.transform(data)
        transformed_data.show()

        # Output:
        # +---+---------+
        # | id|   status|
        # +---+---------+
        # |  1|  Pending|
        # |  1|  Pending|
        # |  2| Complete|
        # |  3|  Pending|
        # |  3|  Pending|
        # +---+---------+
    """

    def __init__(
        self,
        condition: callable,
        times: int = 1
    ):
        """
        Initialize the SparkRowDuplicator.

        Args:
            condition (Callable): A function that takes a DataFrame and
                returns a Boolean column.
            times (int, optional): Number of times to duplicate rows.
                Defaults to 1.

        Raises:
            ValueError: If `condition` is not callable or `times` is not
            a positive integer.
        """
        self.logger = get_logger()
        if not isinstance(times, int) or times <= 0:
            error_message = "times must be a positive integer."
            self.logger.log(
                "error",
                error_message)
            raise ValueError(error_message)
        PandasValidationUtils.validate_is_callable(condition, "condition")
        self.condition = condition
        self.times = times
        self.logger.log(
            "info",
            f"Initialized with condition: {condition}, times: {times}"
        )

    def transform(self, data: DataFrame, **kwargs) -> DataFrame:
        """
        Duplicate rows in the DataFrame based on the condition.

        Args:
            data (DataFrame): The input DataFrame.
            **kwargs: Additional parameters for Spark operations.

        Returns:
            DataFrame: The DataFrame with duplicated rows.

        Example:
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.appName(
            "RowDuplicatorExample").getOrCreate()
        data = spark.createDataFrame(
            [(1, "Pending"), (2, "Complete"), (3, "Pending")],
            ["id", "status"]
        )
        duplicator = SparkRowDuplicator(
            condition=lambda df: df["status"] == "Pending",
            times=2
        )
        transformed_data = duplicator.transform(data)
        transformed_data.show()
        """
        SparkValidationUtils.validate_is_dataframe(data, "data")

        self.logger.log(
            "info",
            "Duplicating rows based on the condition."
        )
        try:
            # Filter rows matching the condition
            matching_rows = data.filter(self.condition(data))

            # Duplicate rows
            duplicated_rows = matching_rows.withColumn(
                "duplicate_id", lit(1))
            for i in range(2, self.times + 1):
                duplicated_rows = duplicated_rows.union(
                    matching_rows.withColumn(
                        "duplicate_id", lit(i)))

            # Combine original and duplicated rows
            combined_data = data.union(duplicated_rows.drop(
                "duplicate_id"))
            self.logger.log(
                "info", (
                    "Rows duplicated successfully. " +
                    f"Original rows: {data.count()}, "
                    f"Final rows: {combined_data.count()}")
            )
            return combined_data
        except Exception as e:
            error_message = f"Error during row duplication: {e}"
            self.logger.log(
                "error",
                error_message)
            raise Exception(error_message)


class SparkRowExpander(Transformer):
    """
    Transformer to expand rows in a Spark DataFrame based on a column value
    or logic.

    Attributes:
        expand_column (str): The column containing the number of times
        to repeat each row.

    Example Usage:
        from pyspark.sql import SparkSession

        # Initialize Spark session
        spark = SparkSession.builder.appName(
            "RowExpanderExample").getOrCreate()

        # Sample data
        data = spark.createDataFrame(
            [(1, 100, 2), (2, 200, 3), (3, 300, 1)],
            ["id", "value", "repeat_count"]
        )

        # Expand rows based on the 'repeat_count' column
        row_expander = SparkRowExpander(expand_column="repeat_count")
        transformed_data = row_expander.transform(data)
        transformed_data.show()
    """

    def __init__(self, expand_column: str):
        """
        Initialize the SparkRowExpander.

        Args:
            expand_column (str): The column containing the number of times
            to repeat each row.

        Raises:
            ValueError: If `expand_column` is not a string or empty.
        """
        self.logger = get_logger()
        PandasValidationUtils.validate_is_non_empty_string(expand_column)
        self.expand_column = expand_column
        self.logger.log(
            "info",
            f"Initialized with expand_column: {expand_column}")

    def transform(self, data: DataFrame, **kwargs) -> DataFrame:
        """
        Expand rows based on the specified column.

        Args:
            data (DataFrame): The input DataFrame.
            **kwargs: Additional parameters for Spark operations.

        Returns:
            DataFrame: The DataFrame with expanded rows.

        Raises:
            KeyError: If the `expand_column` does not exist in the DataFrame.
            ValueError: If the `expand_column` contains invalid values
            (non-integer or negative).

        Example:
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.appName(
            "RowExpanderExample").getOrCreate()
        data = spark.createDataFrame(
            [(1, 100, 2), (2, 200, 3), (3, 300, 1)],
            ["id", "value", "repeat_count"]
        )
        row_expander = SparkRowExpander(expand_column="repeat_count")
        transformed_data = row_expander.transform(data)
        transformed_data.show()
        """
        SparkValidationUtils.validate_is_dataframe(data, "data")
        SparkValidationUtils.validate_columns_exist(
            data,
            [self.expand_column],
            False)

        # Validate positive integer values in expand_column
        SparkValidationUtils.validate_is_positive_integer(
            col(self.expand_column), self.expand_column, data
        )

        self.logger.log(
            "info",
            f"Expanding rows based on column '{self.expand_column}'."
        )
        try:
            # Cast repeat_count to INT and expand rows
            expanded_data = data.withColumn(
                "expanded_array",
                array_repeat(col(
                    "id"), col(self.expand_column).cast(
                        "int"))
            ).withColumn(
                "id",
                explode(col(
                    "expanded_array"))
            ).drop(
                "expanded_array")

            self.logger.log(
                "info",
                f"Rows expanded successfully. Original rows: {data.count()}, "
                f"Expanded rows: {expanded_data.count()}"
            )
            return expanded_data
        except Exception as e:
            error_message = f"Error during row expansion: {e}"
            self.logger.log(
                "error",
                error_message)
            raise Exception(error_message)


class SparkColumnNamePrefixSuffix(Transformer):
    """
    Transformer to add a prefix or suffix to column names in a Spark DataFrame,
    with support for excluding specific columns.

    Attributes:
        prefix (str): The prefix to add to column names.
            Defaults to an empty string.
        suffix (str): The suffix to add to column names.
            Defaults to an empty string.
        exclude_columns (list): List of column names to exclude
            from the transformation.

    Example Usage:
        transformer = SparkColumnNamePrefixSuffix(
            prefix="prod_",
            suffix="_2025",
            exclude_columns=["ID", "Date"]
        )
        transformed_data = transformer.transform(data)
    """

    def __init__(
        self,
        prefix: str = "",
        suffix: str = "",
        exclude_columns: list = None
    ):
        """
        Initialize the SparkColumnNamePrefixSuffix.

        Args:
            prefix (str): The prefix to add to column names.
                Defaults to an empty string.
            suffix (str): The suffix to add to column names.
                Defaults to an empty string.
            exclude_columns (list, optional): List of column names
                to exclude from the transformation.

        Raises:
            ValueError: If `prefix` or `suffix` is not a string.
        """
        self.logger = get_logger()
        if prefix:
            PandasValidationUtils.validate_is_non_empty_string(prefix)
        if suffix:
            PandasValidationUtils.validate_is_non_empty_string(suffix)
        if exclude_columns:
            PandasValidationUtils.validate_is_non_empty_list(exclude_columns)

        self.prefix = prefix
        self.suffix = suffix
        self.exclude_columns = exclude_columns or []
        self.logger.log(
            "info", (
                f"Initialized with prefix: '{self.prefix}', " +
                f"suffix: '{self.suffix}', " +
                f"and exclude_columns: {self.exclude_columns}")
        )

    def transform(self, data: DataFrame) -> DataFrame:
        """
        Add a prefix or suffix to column names, excluding specified columns.

        Args:
            data (DataFrame): The input Spark DataFrame.

        Returns:
            DataFrame: The Spark DataFrame with updated column names.

        Raises:
            ValueError: If any columns in `exclude_columns` do not exist
            in the DataFrame.

        Example:
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.appName(
            "ColumnNamePrefixSuffixExample").getOrCreate()
        data = spark.createDataFrame(
            [(1, 100), (2, 200), (3, 300)],
            ["id", "value"]
        )
        transformer = SparkColumnNamePrefixSuffix(
            prefix="prod_",
            suffix="_2025",
            exclude_columns=["id"]
        )
        transformed_data = transformer.transform(data)
        transformed_data.show()
        """
        SparkValidationUtils.validate_is_dataframe(data, "data")
        if self.exclude_columns:
            SparkValidationUtils.validate_columns_exist(
                data,
                self.exclude_columns,
                False)

        self.logger.log(
            "info", (
                f"Adding prefix '{self.prefix}' " +
                f"and suffix '{self.suffix}' to column names.")
        )

        updated_columns = [
            f"{self.prefix}{col}{self.suffix}" if
            col not in self.exclude_columns else
            col for col in data.columns
        ]

        self.logger.log(
            "info",
            f"Updated column names: {updated_columns}"
        )

        # Rename columns in the DataFrame
        data = data.toDF(*updated_columns)

        self.logger.log(
            "info",
            "Column names updated successfully."
        )

        return data


class SparkTransformerFactory(TransformerFactory):
    """
    Factory class for creating Spark transformers.
    """

    def __init__(self):
        """
        Initialize the SparkTransformerFactory with a logger.
        """
        self.logger = get_logger()

    def log_creation(self, transformer_name: str, **params):
        """
        Log the creation of a transformer.
        """
        self.logger.log(
            "info", f"Creating {transformer_name} with parameters: {params}"
        )

    def create_column_adder(
        self,
        column_name: str,
        value: any,
        aggregation: dict = None
    ) -> SparkColumnAdder:
        """
        Create a SparkColumnAdder transformer.

        Args:
            column_name (str): The name of the column to add.
            value (any): The value to add to the column.
            aggregation (dict, optional): Aggregation settings for the column.

        Returns:
            SparkColumnAdder: The SparkColumnAdder transformer.

        Example:
        from pyspark.sql import SparkSession
        from my_module import SparkTransformerFactory
        factory = SparkTransformerFactory()
        spark = SparkSession.builder.appName(
            "ColumnAdderExample").getOrCreate()
        data = spark.createDataFrame(
            [(1, 100), (2, 200), (3, 300)],
            ["id", "value"]
        )
        column_adder = factory.create_column_adder(
            column_name="new_column",
            value=50)
        transformed_data = column_adder.transform(data)
        transformed_data.show()
        """
        self.log_creation(
            "SparkColumnAdder",
            column_name=column_name,
            value=value,
            aggregation=aggregation)
        return SparkColumnAdder(
            column_name=column_name,
            value=value,
            aggregation=aggregation)

    def create_column_adder_static(
        self,
        column_name: str,
        value: any,
        overwrite: bool = False
    ) -> SparkColumnAdderStatic:
        """
        Create a SparkColumnAdderStatic transformer.

        Args:
            column_name (str): The name of the column to add.
            value (any): The value to add to the column.
            overwrite (bool, optional): Whether to overwrite existing columns.
                Defaults to False.

        Returns:
            SparkColumnAdderStatic: The SparkColumnAdderStatic transformer.

        Example:
        from pyspark.sql import SparkSession
        from my_module import SparkTransformerFactory
        factory = SparkTransformerFactory()
        spark = SparkSession.builder.appName(
            "ColumnAdderStaticExample").getOrCreate()
        data = spark.createDataFrame(
            [(1, 100), (2, 200), (3, 300)],
            ["id", "value"]
        )
        column_adder_static = factory.create_column_adder_static(
            column_name="new_column",
            value=50)
        transformed_data = column_adder_static.transform(data)
        transformed_data.show()
        """
        self.log_creation(
            "SparkColumnAdderStatic",
            column_name,
            value,
            overwrite
        )
        return SparkColumnAdderStatic(
            column_name=column_name,
            value=value,
            overwrite=overwrite
        )

    def create_column_dropper(
        self,
        columns_to_drop: list
    ) -> SparkColumnDropper:
        """
        Create a SparkColumnDropper transformer.

        Args:
            columns_to_drop (list): The names of the columns to drop.

        Returns:
            SparkColumnDropper: The SparkColumnDropper transformer.

        Example:
        from pyspark.sql import SparkSession
        from my_module import SparkTransformerFactory
        factory = SparkTransformerFactory()
        spark = SparkSession.builder.appName(
            "ColumnDropperExample").getOrCreate()
        data = spark.createDataFrame(
            [(1, 100, "A"), (2, 200, "B"), (3, 300, "C")],
            ["id", "value", "category"]
        )
        column_dropper = factory.create_column_dropper(
            columns_to_drop=["category"])
        transformed_data = column_dropper.transform(data)
        transformed_data.show()
        """
        self.log_creation(
            "SparkColumnDropper",
            columns_to_drop=columns_to_drop)
        return SparkColumnDropper(
            columns_to_drop=columns_to_drop)

    def create_column_merger(
        self,
        columns: list,
        new_column: str,
        separator: str = " ",
        drop_originals: bool = True
    ) -> SparkColumnMerger:
        """
        Create a SparkColumnMerger transformer.

        Args:
            columns (list): The names of the columns to merge.
            new_column (str): The name of the new column to create.
            separator (str, optional): The separator to use when merging
                columns. Defaults to " ".
            drop_originals (bool, optional): Whether to drop the original
                columns after merging. Defaults to True.

        Returns:
            SparkColumnMerger: The SparkColumnMerger transformer.

        Example:
        from pyspark.sql import SparkSession
        from my_module import SparkTransformerFactory
        factory = SparkTransformerFactory()
        spark = SparkSession.builder.appName(
            "ColumnNameMergerExample").getOrCreate()
        data = spark.createDataFrame(
            [(1, 100, "A", "Apple"),
            (2, 200, "B", "Banana"),
            (3, 300, "C", "Cherry")],
            ["id", "value", "category", "fruit"]
        )
        column_merger = factory.create_column_merger(
            columns=["fruit"],
            new_column="fruit_description")
        transformed_data = column_merger.transform(data)
    transformed_data.show()
        """
        self.log_creation(
            "SparkColumnMerger",
            columns=columns,
            new_column=new_column,
            separator=separator,
            drop_originals=drop_originals
        )
        return SparkColumnMerger(
            columns=columns,
            new_column=new_column,
            separator=separator,
            drop_originals=drop_originals)

    def create_column_name_prefix_suffix(
        self,
        prefix: str = "",
        suffix: str = "",
        exclude_columns: list = None
    ) -> SparkColumnNamePrefixSuffix:
        """
        Create a SparkColumnNamePrefixSuffix transformer.

        Args:
            prefix (str, optional): The prefix to add to column names.
                Defaults to "".
            suffix (str, optional): The suffix to add to column names.
                Defaults to "".
            exclude_columns (list, optional): A list of column names to exclude
                from the prefix and suffix. Defaults to None.

        Returns:
            SparkColumnNamePrefixSuffix: The SparkColumnNamePrefixSuffix
            transformer.

        Example:
        from pyspark.sql import SparkSession
        from my_module import SparkTransformerFactory
        factory = SparkTransformerFactory()
        spark = SparkSession.builder.appName(
            "ColumnNamePrefixSuffixExample").getOrCreate()
        data = spark.createDataFrame(
            [(1, 100, "A"), (2, 200, "B"), (3, 300, "C")],
            ["id", "value", "category"]
        )
        column_prefix_suffix = factory.create_column_name_prefix_suffix(
            prefix="new_",
            suffix="_suffix")
        transformed_data = column_prefix_suffix.transform(data)
        transformed_data.show()
        """
        self.log_creation(
            "SparkColumnNamePrefixSuffix",
            prefix=prefix,
            suffix=suffix,
            exclude_columns=exclude_columns
        )
        return SparkColumnNamePrefixSuffix(
            prefix=prefix,
            suffix=suffix,
            exclude_columns=exclude_columns)

    def create_column_name_regex_renamer(
        self,
        pattern: str,
        replacement: str,
        exclude_columns: list = None
    ) -> SparkColumnNameRegexRenamer:
        """
        Create a SparkColumnNameRegexRenamer transformer.

        Args:
            pattern (str): The regular expression pattern to match
                column names.
            replacement (str): The replacement string for matched column names.
            exclude_columns (list, optional): A list of column names to exclude
                from the renaming. Defaults to None.

        Returns:
            SparkColumnNameRegexRenamer: The SparkColumnNameRegexRenamer
            transformer.

        Example:
        from pyspark.sql import SparkSession
        from my_module import SparkTransformerFactory
        factory = SparkTransformerFactory()
        spark = SparkSession.builder.appName(
            "ColumnNameRegexRenamerExample").getOrCreate()
        data = spark.createDataFrame(
            [(1, 100, "A"), (2, 200, "B"), (3, 300, "C")],
            ["id", "value", "category"]
        )
        column_regex_renamer = factory.create_column_name_regex_renamer(
            pattern="_.*",
            replacement="")
        transformed_data = column_regex_renamer.transform(data)
        transformed_data.show()
        """
        self.log_creation(
            "SparkColumnNameRegexRenamer",
            pattern=pattern,
            replacement=replacement,
            exclude_columns=exclude_columns
        )
        return SparkColumnNameRegexRenamer(
            pattern=pattern,
            replacement=replacement,
            exclude_columns=exclude_columns
        )

    def create_column_name_standardizer(
        self,
        case_style: str = "snake_case",
        exclude_columns: list = None
    ) -> SparkColumnNameStandardizer:
        """
        Create a SparkColumnNameStandardizer transformer.

        Args:
            case_style (str, optional): The case style to use for standardizing
                column names. Supported styles are "snake_case", "camel_case",
                "pascal_case", upper, and lower". Defaults to "snake_case".
            exclude_columns (list, optional): A list of column names to exclude
                from the standardization. Defaults to None.

        Returns:
            SparkColumnNameStandardizer: The SparkColumnNameStandardizer
            transformer.

        Example:
        from pyspark.sql import SparkSession
        from my_module import SparkTransformerFactory
        factory = SparkTransformerFactory()
        spark = SparkSession.builder.appName(
            "ColumnNameStandardizerExample").getOrCreate()
        data = spark.createDataFrame(
            [(1, 100, "A"), (2, 200, "B"), (3, 300, "C")],
            ["id", "value", "category"]
        )
        column_standardizer = factory.create_column_name_standardizer(
            case_style="pascal_case")
        transformed_data = column_standardizer.transform(data)
        transformed_data.show()
        """
        self.log_creation(
            "SparkColumnNameStandardizer",
            case_style=case_style,
            exclude_columns=exclude_columns)
        return SparkColumnNameStandardizer(
            case_style=case_style,
            exclude_columns=exclude_columns
        )

    def create_column_pattern_dropper(
        self,
        pattern: str,
        exclude_columns: list = None
    ) -> SparkColumnPatternDropper:
        """
        Create a SparkColumnPatternDropper transformer.

        Args:
            pattern (str): The regular expression pattern to match
                column names.
            exclude_columns (list, optional): A list of column names to exclude
                from the dropping. Defaults to None.

        Returns:
            SparkColumnPatternDropper: The SparkColumnPatternDropper
            transformer.

        Example:
        from pyspark.sql import SparkSession
        from my_module import SparkTransformerFactory
        factory = SparkTransformerFactory()
        spark = SparkSession.builder.appName(
            "ColumnNamePatternDropperExample").getOrCreate()
        data = spark.createDataFrame(
            [(1, 100, "A"), (2, 200, "B"), (3, 300, "C")],
            ["id", "value", "category"]
        )
        column_pattern_dropper = factory.create_column_pattern_dropper(
            pattern=".*_id$")
        transformed_data = column_pattern_dropper.transform(data)
        transformed_data.show()
        """
        self.log_creation(
            "SparkColumnPatternDropper",
            pattern=pattern,
            exclude_columns=exclude_columns)
        return SparkColumnPatternDropper(
            pattern=pattern,
            exclude_columns=exclude_columns)

    def create_column_renamer(
        self,
        column_map: dict
    ) -> SparkColumnRenamer:
        """
        Create a SparkColumnRenamer transformer.

        Args:
            column_map (dict): A dictionary mapping original column
                names to new column names.

        Returns:
            SparkColumnRenamer: The SparkColumnRenamer transformer.

        Example:
        from pyspark.sql import SparkSession
        from my_module import SparkTransformerFactory
        factory = SparkTransformerFactory()
        spark = SparkSession.builder.appName(
            "ColumnNameRenamerExample").getOrCreate()
        data = spark.createDataFrame(
            [(1, 100, "A"), (2, 200, "B"), (3, 300, "C")],
            ["id", "value", "category"]
        )
        column_map = {"id": "new_id", "value": "new_value"}
        column_renamer = factory.create_column_renamer(column_map)
        transformed_data = column_renamer.transform(data)
        transformed_data.show()
        """
        self.log_creation(
            "SparkColumnRenamer",
            column_map=column_map)
        return SparkColumnRenamer(
            column_map=column_map)

    def create_column_reorderer(
        self,
        column_order: list,
        retain_unspecified: bool = False
    ) -> SparkColumnReorderer:
        """
        Create a SparkColumnReorderer transformer.

        Args:
            column_order (list): The order of the columns in the final
                DataFrame.
            retain_unspecified (bool, optional): Whether to retain columns
                that are not specified in the column_order list. Defaults to
                False.

        Returns:
            SparkColumnReorderer: The SparkColumnReorderer transformer.

        Example:
        from pyspark.sql import SparkSession
        from my_module import SparkTransformerFactory
        factory = SparkTransformerFactory()
        spark = SparkSession.builder.appName(
            "ColumnNameReordererExample").getOrCreate()
        data = spark.createDataFrame(
            [(1, 100, "A"), (2, 200, "B"), (3, 300, "C")],
            ["id", "value", "category"]
        )
        column_order = ["id", "new_value", "category"]
        column_reorderer = factory.create_column_reorderer(
            column_order=column_order)
        transformed_data = column_reorderer.transform(data)
        transformed_data.show()
        """
        self.log_creation(
            "SparkColumnReorderer",
            column_order=column_order,
            retain_unspecified=retain_unspecified)
        return SparkColumnReorderer(
            column_order=column_order,
            retain_unspecified=retain_unspecified
        )

    def create_column_splitter(
        self,
        column: str,
        pattern: str,
        regex: bool = False,
        new_columns: list = None
    ) -> SparkColumnSplitter:
        """
        Create a SparkColumnSplitter transformer.

        Args:
            column (str): The column to split.
            pattern (str): The pattern to split the column on.
            regex (bool, optional): Whether to use regular expressions for
                splitting. Defaults to False.
            new_columns (list, optional): A list of new column names to
                create for the split values. Defaults to None.

        Returns:
            SparkColumnSplitter: The SparkColumnSplitter transformer.

        Example:
        from pyspark.sql import SparkSession
        from my_module import SparkTransformerFactory
        factory = SparkTransformerFactory()
        spark = SparkSession.builder.appName(
            "ColumnNameSplitterExample").getOrCreate()
        data = spark.createDataFrame(
            [(1, "A,B,C"), (2, "D,E,F"), (3, "G,H,I")],
            ["id", "value"]
        )
        column_splitter = factory.create_column_splitter(
            column="value",
            pattern=",")
        transformed_data = column_splitter.transform(data)
        transformed_data.show()
        """
        self.log_creation(
            "SparkColumnSplitter",
            column=column,
            pattern=pattern,
            regex=regex,
            new_columns=new_columns
        )
        return SparkColumnSplitter(
            column=column,
            pattern=pattern,
            regex=regex,
            new_columns=new_columns
        )

    def create_column_type_dropper(
        self,
        data_types: list,
        exclude_columns: list = None
    ) -> SparkColumnTypeDropper:
        """
        Create a SparkColumnTypeDropper transformer.

        Args:
            data_types (list): A list of data types to drop columns with.
            exclude_columns (list, optional): A list of column names to exclude
                from the dropping. Defaults to None.

        Returns:
            SparkColumnTypeDropper: The SparkColumnTypeDropper transformer.

        Example:
        from pyspark.sql import SparkSession
        from my_module import SparkTransformerFactory
        factory = SparkTransformerFactory()
        spark = SparkSession.builder.appName(
            "ColumnTypeDropperExample").getOrCreate()
        data = spark.createDataFrame(
            [(1, 100, "A"), (2, 200, "B"), (3, 300, "C")],
            ["id", "value", "category"]
        )
        column_type_dropper = factory.create_column_type_dropper(
            data_types=["string"])
        transformed_data = column_type_dropper.transform(data)
        transformed_data.show()
        """
        self.log_creation(
            "SparkColumnTypeDropper",
            data_types=data_types,
            exclude_columns=exclude_columns)
        return SparkColumnTypeDropper(
            data_types=data_types,
            exclude_columns=exclude_columns)

    def create_empty_column_dropper(
        self,
        exclude_columns: list = None
    ) -> SparkEmptyColumnDropper:
        """
        Create a SparkEmptyColumnDropper transformer.

        Args:
            exclude_columns (list, optional): A list of column names to exclude
                from the dropping. Defaults to None.

        Returns:
            SparkEmptyColumnDropper: The SparkEmptyColumnDropper transformer.

        Example:
        from pyspark.sql import SparkSession
        from my_module import SparkTransformerFactory
        factory = SparkTransformerFactory()
        spark = SparkSession.builder.appName(
            "EmptyColumnDropperExample").getOrCreate()
        data = spark.createDataFrame(
            [(1, 100, "A"), (2, 200, "B"), (3, 300, "C")],
            ["id", "value", "category"]
        )
        empty_column_dropper = factory.create_empty_column_dropper()
        transformed_data = empty_column_dropper.transform(data)
        transformed_data.show()
        """
        self.log_creation(
            "SparkEmptyColumnDropper",
            exclude_columns=exclude_columns)
        return SparkEmptyColumnDropper(
            exclude_columns=exclude_columns
        )

    def create_null_ratio_column_dropper(
        self,
        threshold: float,
        exclude_columns: list = None
    ) -> SparkNullRatioColumnDropper:
        """
        Create a SparkNullRatioColumnDropper transformer.

        Args:
            threshold (float): The threshold for the null ratio. If the
                null ratio exceeds this threshold, the column will be dropped.
            exclude_columns (list, optional): A list of column names to exclude
                from the dropping. Defaults to None.

        Returns:
            SparkNullRatioColumnDropper: The SparkNullRatioColumnDropper
                transformer.

        Example:
        from pyspark.sql import SparkSession
        from my_module import SparkTransformerFactory
        factory = SparkTransformerFactory()
        spark = SparkSession.builder.appName(
            "NullRatioColumnDropperExample").getOrCreate()
        data = spark.createDataFrame(
            [(1, 100, "A"), (2, 200, "B"), (3, None, "C")],
            ["id", "value", "category"]
        )
        null_ratio_column_dropper = factory.create_null_ratio_column_dropper(
            threshold=0.5)
        transformed_data = null_ratio_column_dropper.transform(data)
        transformed_data.show()
        """
        self.log_creation(
            "SparkNullRatioColumnDropper",
            threshold=threshold,
            exclude_columns=exclude_columns
        )
        return SparkNullRatioColumnDropper(
            threshold=threshold,
            exclude_columns=exclude_columns)

    def create_row_aggregator(
        self,
        group_by: list,
        agg_config: dict
    ) -> SparkRowAggregator:
        """
        Create a SparkRowAggregator transformer.

        Args:
            group_by (list): A list of column names to group by.
            agg_config (dict): A dictionary of aggregation configurations,
                where the keys are column names and the values are aggregation
                functions.

        Returns:
            SparkRowAggregator: The SparkRowAggregator transformer.

        Example:
        from pyspark.sql import SparkSession, DataFrame
        from my_module import SparkTransformerFactory
        factory = SparkTransformerFactory()
        spark = SparkSession.builder.appName(
            "RowAggregatorExample").getOrCreate()
        data = spark.createDataFrame(
            [(1, 100, "A"), (2, 200, "B"), (1, 300, "C")],
            ["id", "value", "category"]
        )
        agg_config = {
            "value": "sum",
            "category": "first"
        }
        row_aggregator = factory.create_row_aggregator(
            group_by=["id", "category"],
            agg_config=agg_config)
        transformed_data = row_aggregator.transform(data)
        transformed_data.show()
        """
        self.log_creation(
            "SparkRowAggregator",
            group_by=group_by,
            agg_config=agg_config)
        return SparkRowAggregator(
            group_by=group_by,
            agg_config=agg_config
        )

    def create_row_appender(
        self,
        rows: DataFrame
    ) -> SparkRowAppender:
        """
        Create a SparkRowAppender transformer.

        Args:
            rows (DataFrame): The DataFrame to append to the existing data.

        Returns:
            SparkRowAppender: The SparkRowAppender transformer.

        Example:
        from pyspark.sql import SparkSession, DataFrame
        from my_module import SparkTransformerFactory
        factory = SparkTransformerFactory()
        spark = SparkSession.builder.appName(
            "RowAppenderExample").getOrCreate()
        data = spark.createDataFrame(
            [(1, 100, "A"), (2, 200, "B")],
            ["id", "value", "category"]
        )
        additional_rows = spark.createDataFrame(
            [(3, 300, "C")],
            ["id", "value", "category"]
        )
        row_appender = factory.create_row_appender(rows=additional_rows)
        transformed_data = row_appender.transform(data)
        transformed_data.show()
        """
        self.log_creation(
            "SparkRowAppender",
            rows=rows)
        return SparkRowAppender(
            rows=rows)

    def create_row_deduplicator(
        self,
        subset: list = None,
        keep: str = "first"
    ) -> SparkRowDeduplicator:
        """
        Create a SparkRowDeduplicator transformer.

        Args:
            subset (list, optional): A list of column names to consider
                for duplicate detection. Defaults to None, which means all
                columns will be considered.
            keep (str, optional): The strategy to keep the duplicated rows.
                Can be "first" (keep the first occurrence), "last" (keep the
                last occurrence), or "all" (keep all occurrences). Defaults to
                "first".

        Returns:
            SparkRowDeduplicator: The SparkRowDeduplicator transformer.

        Example:
        from pyspark.sql import SparkSession, DataFrame
        from my_module import SparkTransformerFactory
        factory = SparkTransformerFactory()
        spark = SparkSession.builder.appName(
            "RowDeduplicatorExample").getOrCreate()
        data = spark.createDataFrame(
            [(1, 100, "A"), (2, 200, "B"), (1, 300, "C")],
            ["id", "value", "category"]
        )
        row_deduplicator = factory.create_row_deduplicator()
        transformed_data = row_deduplicator.transform(data)
        transformed_data.show()
        """
        self.log_creation(
            "SparkRowDeduplicator",
            subset=subset,
            keep=keep)
        return SparkRowDeduplicator(
            subset=subset,
            keep=keep
        )

    def create_row_duplicator(
        self,
        condition: callable,
        times: int = 1
    ) -> SparkRowDuplicator:
        """
        Create a SparkRowDuplicator transformer.

        Args:
            condition (callable): A condition function to check for duplicates.
            times (int, optional): The number of times to duplicate the rows.
                Defaults to 1.

        Returns:
            SparkRowDuplicator: The SparkRowDuplicator transformer.

        Example:
        from pyspark.sql import SparkSession, DataFrame
        from my_module import SparkTransformerFactory
        factory = SparkTransformerFactory()
        spark = SparkSession.builder.appName(
            "RowDuplicatorExample").getOrCreate()
        data = spark.createDataFrame(
            [(1, 100, "A"), (2, 200, "B"), (1, 300, "C")],
            ["id", "value", "category"]
        )
        condition = lambda row: row["id"] == 1
        row_duplicator = factory.create_row_duplicator(condition)
        transformed_data = row_duplicator.transform(data)
        transformed_data.show()
        """
        self.log_creation(
            "SparkRowDuplicator",
            condition=condition,
            times=times)
        return SparkRowDuplicator(
            condition=condition,
            times=times
        )

    def create_row_expander(
        self,
        expand_column: str
    ) -> SparkRowExpander:
        """
        Create a SparkRowExpander transformer.

        Args:
            expand_column (str): The column name to expand.

        Returns:
            SparkRowExpander: The SparkRowExpander transformer.

        Example:
        from pyspark.sql import SparkSession, DataFrame
        from my_module import SparkTransformerFactory
        factory = SparkTransformerFactory()
        spark = SparkSession.builder.appName(
            "RowExpanderExample").getOrCreate()
        data = spark.createDataFrame(
            [(1, 100, "A")],
            ["id", "value", "category"]
        )
        expander = factory.create_row_expander(expand_column="value")
        transformed_data = expander.transform(data)
        transformed_data.show()
        """
        self.log_creation(
            "SparkRowExpander",
            expand_column=expand_column)
        return SparkRowExpander(
            expand_column=expand_column
        )

    def create_row_filter(
        self,
        condition: callable
    ) -> SparkRowFilter:
        """
        Create a SparkRowFilter transformer.

        Args:
            condition (callable): A condition function to filter rows.

        Returns:
            SparkRowFilter: The SparkRowFilter transformer.

        Example:
        from pyspark.sql import SparkSession, DataFrame
        from my_module import SparkTransformerFactory
        factory = SparkTransformerFactory()
        spark = SparkSession.builder.appName(
            "RowFilterExample").getOrCreate()
        data = spark.createDataFrame(
            [(1, 100, "A"), (2, 200, "B"), (3, 300, "C")],
            ["id", "value", "category"]
        )
        condition = lambda row: row["id"] % 2 == 0
        row_filter = factory.create_row_filter(condition)
        transformed_data = row_filter.transform(data)
        transformed_data.show()
        """
        self.log_creation(
            "SparkRowFilter",
            condition=condition)
        return SparkRowFilter(
            condition=condition
        )

    def create_row_sampler(
        self,
        mode: str,
        n: int = None,
        frac: float = None,
        replace: bool = False
    ) -> SparkRowSampler:
        """
        Create a SparkRowSampler transformer.

        Args:
            mode (str): The sampling mode. Can be "uniform", "stratified", or
                "weighted".
            n (int, optional): The number of samples to draw. Defaults to None,
                which means all rows will be sampled.
            frac (float, optional): The fraction of rows to sample. Defaults to
                None, which means all rows will be sampled.
            replace (bool, optional): Whether to sample with replacement.
                Defaults to False.

        Returns:
            SparkRowSampler: The SparkRowSampler transformer.

        Example:
        from pyspark.sql import SparkSession, DataFrame
        from my_module import SparkTransformerFactory
        factory = SparkTransformerFactory()
        spark = SparkSession.builder.appName(
            "RowSamplerExample").getOrCreate()
        data = spark.createDataFrame(
            [(1, 100, "A"), (2, 200, "B"), (3, 300, "C")],
            ["id", "value", "category"]
        )
        sampler = factory.create_row_sampler(mode="uniform", n=2)
        transformed_data = sampler.transform(data)
        transformed_data.show()
        """
        self.log_creation(
            "SparkRowSampler",
            mode=mode,
            n=n,
            frac=frac,
            replace=replace
        )
        return SparkRowSampler(
            mode=mode,
            n=n,
            frac=frac,
            replace=replace
        )

    def create_row_sorter(
        self,
        by: list,
        ascending: bool = True,
        na_position: str = "last"
    ) -> SparkRowSorter:
        """
        Create a SparkRowSorter transformer.

        Args:
            by (list): The column names to sort by.
            ascending (bool, optional): Whether to sort in ascending order.
                Defaults to True.
            na_position (str, optional): The position of NA values in the
            sorted result. Can be "first" (place NA values at the beginning),
            "last" (place NA values at the end), or "keep" (keep NA values in
            their original order). Defaults to "last".

        Returns:
            SparkRowSorter: The SparkRowSorter transformer.

        Example:
        from pyspark.sql import SparkSession, DataFrame
        from my_module import SparkTransformerFactory
        factory = SparkTransformerFactory()
        spark = SparkSession.builder.appName(
            "RowSorterExample").getOrCreate()
        data = spark.createDataFrame(
            [(1, 100, "A"), (2, 200, "B"), (3, None, "C")],
            ["id", "value", "category"]
        )
        sorter = factory.create_row_sorter(by=["value", "category"])
        transformed_data = sorter.transform(data)
        transformed_data.show()
        """
        self.log_creation(
            "SparkRowSorter",
            by=by,
            ascending=ascending,
            na_position=na_position
            )
        return SparkRowSorter(
            by=by,
            ascending=ascending,
            na_position=na_position
        )

    def create_row_splitter(
        self,
        column: str,
        delimiter: str = None
    ) -> SparkRowSplitter:
        """
        Create a SparkRowSplitter transformer.

        Args:
            column (str): The column name to split.
            delimiter (str, optional): The delimiter used to split the values.
                Defaults to None, which means the delimiter will be inferred
                from the data.

        Returns:
            SparkRowSplitter: The SparkRowSplitter transformer.

        Example:
        from pyspark.sql import SparkSession, DataFrame
        from my_module import SparkTransformerFactory
        factory = SparkTransformerFactory()
        spark = SparkSession.builder.appName(
            "RowSplitterExample").getOrCreate()
        data = spark.createDataFrame(
            [(1, "A,B,C"), (2, "D,E"), (3, "F")],
            ["id", "value"]
        )
        splitter = factory.create_row_splitter(column="value", delimiter=",")
        transformed_data = splitter.transform(data)
        transformed_data.show()
        """
        self.log_creation(
            "SparkRowSplitter",
            column=column,
            delimiter=delimiter
            )
        return SparkRowSplitter(
            column=column,
            delimiter=delimiter
        )

    def create_value_replacer(
        self,
        value_map: dict
    ) -> SparkValueReplacer:
        """
        Create a SparkValueReplacer transformer.

        Args:
            value_map (dict): A dictionary mapping old values to new values.

        Returns:
            SparkValueReplacer: The SparkValueReplacer transformer.

        Example:
        from pyspark.sql import SparkSession, DataFrame
        from my_module import SparkTransformerFactory, TransformerType
        factory = SparkTransformerFactory()
        spark = SparkSession.builder.appName(
            "ValueReplacerExample").getOrCreate()
        data = spark.createDataFrame(
            [(1, "A"), (2, "B"), (3, "C")],
            ["id", "value"]
        )
        value_map = {"A": "X", "B": "Y"}
        replacer = factory.create_value_replacer(value_map=value_map)
        transformed_data = replacer.transform(data)
        transformed_data.show()
        """
        self.log_creation(
            "SparkValueReplacer",
            value_map=value_map
        )
        return SparkValueReplacer(
            value_map=value_map
        )


class SparkTransformerProvider(TransformerProvider):
    """
    A provider class for creating Spark transformers dynamically based on
    the transformer type and configuration options.

    This class integrates with a factory (`SparkTransformerFactory`) to
    dynamically instantiate transformers. It ensures that required parameters
    are validated before creating the transformers, leveraging a centralized
    validation utility.

    """
    def __init__(self, factory: SparkTransformerFactory):
        """
        Initialize the SparkValidatorProvider.

        Args:
            factory (SparkTransformerFactory): An instance of the
                SparkTransformerFactory to create transformers.
        """
        self.logger = get_logger()
        PandasValidationUtils.validate_inheritance(
            factory,
            TransformerFactory,
            'factory')
        self.factory = factory

    def create_transformer(
        self,
        transformer_type: TransformerType,
        **options
    ) -> Transformer:
        """
        Create a validator based on the validation type.
        """
        PandasValidationUtils.validate_instance(
            transformer_type,
            TransformerType,
            "transformer_type")
        match transformer_type:
            case TransformerType.COLUMN_ADDER:
                validate_options(
                    options=options,
                    required_keys=["column_name"],
                    entity_type="transformation",
                    entity_name="COLUMN_ADDER")
                return self.factory.create_column_adder(
                    column_name=options["column_name"],
                    value=options.get("value", None),
                    aggregation=options.get("aggregation", None)
                    )
            case TransformerType.COLUMN_ADDER_STATIC:
                validate_options(
                    options=options,
                    required_keys=["column_name", "value"],
                    entity_type="transformation",
                    entity_name="COLUMN_ADDER_STATIC")
                return self.factory.create_column_adder_static(
                    column_name=options["column_name"],
                    value=options["value"]
                )
            case TransformerType.COLUMN_DROPPER:
                validate_options(
                    options=options,
                    required_keys=["columns_to_drop"],
                    entity_type="transformation",
                    entity_name="COLUMN_DROPPER")
                return self.factory.create_column_dropper(
                    columns_to_drop=options["columns_to_drop"]
                    )
            case TransformerType.COLUMN_MERGER:
                validate_options(
                    options=options,
                    required_keys=[
                        "columns", "new_column", "separator"],
                    entity_type="transformation",
                    entity_name="COLUMN_MERGER")
                return self.factory.create_column_merger(
                        columns=options["columns"],
                        new_column=options["new_column"],
                        separator=options["separator"])
            case TransformerType.COLUMN_NAME_PREFIX_SUFFIX:
                validate_options(
                    options=options,
                    required_keys=["prefix", "suffix"],
                    entity_type="transformation",
                    entity_name="COLUMN_NAME_PREFIX_SUFFIX")
                return self.factory.create_column_name_prefix_suffix(
                    prefix=options["prefix"],
                    suffix=options["suffix"])
            case TransformerType.COLUMN_NAME_REGEX_RENAMER:
                validate_options(
                    options=options,
                    required_keys=["pattern", "replacement"],
                    entity_type="transformation",
                    entity_name="COLUMN_NAME_REGEX_RENAMER")
                return self.factory.create_column_name_regex_renamer(
                    pattern=options["pattern"],
                    replacement=options["replacement"])
            case TransformerType.COLUMN_NAME_STANDARDIZER:
                validate_options(
                    options=options,
                    required_keys=["case_style"],
                    entity_type="transformation",
                    entity_name="COLUMN_NAME_STANDARDIZER")
                return self.factory.create_column_name_standardizer(
                    case_style=options["case_style"])
            case TransformerType.COLUMN_PATTERN_DROPPER:
                validate_options(
                    options=options,
                    required_keys=["pattern"],
                    entity_type="transformation",
                    entity_name="COLUMN_PATTERN_DROPPER")
                return self.factory.create_column_pattern_dropper(
                    pattern=options["pattern"])
            case TransformerType.COLUMN_RENAMER:
                validate_options(
                    options=options,
                    required_keys=["column_map"],
                    entity_type="transformation",
                    entity_name="COLUMN_RENAMER")
                return self.factory.create_column_renamer(
                    column_map=options["column_map"])
            case TransformerType.COLUMN_REORDERER:
                validate_options(
                    options=options,
                    required_keys=["column_order"],
                    entity_type="transformation",
                    entity_name="COLUMN_REORDERER")
                return self.factory.create_column_reorderer(
                    column_order=options["column_order"],
                    retain_unspecified=options.get(
                        "retain_unspecified", False))
            case TransformerType.COLUMN_SPLITTER:
                validate_options(
                    options=options,
                    required_keys=["column", "pattern", "regex"],
                    entity_type="transformation",
                    entity_name="COLUMN_SPLITTER")
                return self.factory.create_column_splitter(
                    column=options["column"],
                    pattern=options["pattern"],
                    regex=options["regex"])
            case TransformerType.COLUMN_TYPE_DROPPER:
                validate_options(
                    options=options,
                    required_keys=["data_types"],
                    entity_type="transformation",
                    entity_name="COLUMN_TYPE_DROPPER")
                return self.factory.create_column_type_dropper(
                    data_types=options["data_types"])
            case TransformerType.EMPTY_COLUMN_DROPPER:
                validate_options(
                    options=options,
                    required_keys=["exclude_columns"],
                    entity_type="transformation",
                    entity_name="EMPTY_COLUMN_DROPPER")
                return self.factory.create_empty_column_dropper(
                    exclude_columns=options["exclude_columns"])
            case TransformerType.NULL_RATIO_COLUMN_DROPPER:
                validate_options(
                    options=options,
                    required_keys=["threshold"],
                    entity_type="transformation",
                    entity_name="NULL_RATIO_COLUMN_DROPPER")
                return self.factory.create_null_ratio_column_dropper(
                    threshold=options["threshold"])
            case TransformerType.ROW_AGGREGATOR:
                validate_options(
                    options=options,
                    required_keys=["group_by", "agg_config"],
                    entity_type="transformation",
                    entity_name="ROW_AGGREGATOR")
                return self.factory.create_row_aggregator(
                    group_by=options["group_by"],
                    agg_config=options["agg_config"])
            case TransformerType.ROW_APPENDER:
                validate_options(
                    options=options,
                    required_keys=["rows"],
                    entity_type="transformation",
                    entity_name="ROW_APPENDER")
                return self.factory.create_row_appender(
                    rows=options["rows"])
            case TransformerType.ROW_DEDUPLICATOR:
                validate_options(
                    options=options,
                    required_keys=["subset", "keep"],
                    entity_type="transformation",
                    entity_name="ROW_DEDUPLICATOR")
                return self.factory.PandasRowDeduplicator(
                    subset=options["subset"],
                    keep=options["keep"])
            case TransformerType.ROW_DUPLICATOR:
                validate_options(
                    options=options,
                    required_keys=["condition", "times"],
                    entity_type="transformation",
                    entity_name="ROW_DUPLICATOR")
                return self.factory.create_row_duplicator(
                    condition=options["condition"],
                    times=options["times"])
            case TransformerType.ROW_EXPANDER:
                validate_options(
                    options=options,
                    required_keys=["expand_column"],
                    entity_type="transformation",
                    entity_name="ROW_EXPANDER")
                return self.factory.create_row_expander(
                    expand_column=options["expand_column"])
            case TransformerType.ROW_FILTER:
                validate_options(
                    options=options,
                    required_keys=["condition"],
                    entity_type="transformation",
                    entity_name="ROW_FILTER")
                return self.factory.create_row_filter(
                    condition=options["condition"])
            case TransformerType.ROW_SAMPLER:
                validate_options(
                    options=options,
                    required_keys=["mode", "n", "frac"],
                    entity_type="transformation",
                    entity_name="ROW_SAMPLER")
                return self.factory.create_row_sampler(
                    mode=options["mode"],
                    n=options["n"],
                    frac=options["frac"])
            case TransformerType.ROW_SORTER:
                validate_options(
                    options=options,
                    required_keys=["by", "ascending", "na_position"],
                    entity_type="transformation",
                    entity_name="ROW_SORTER")
                return self.factory.create_row_sorter(
                    by=options["by"],
                    ascending=options["ascending"],
                    na_position=options["na_position"])
            case TransformerType.ROW_SPLITTER:
                validate_options(
                    options=options,
                    required_keys=["column", "delimiter"],
                    entity_type="transformation",
                    entity_name="ROW_SPLITTER")
                return self.factory.create_row_splitter(
                    column=options["column"],
                    delimiter=options["delimiter"])
            case TransformerType.VALUE_REPLACER:
                validate_options(
                    options=options,
                    required_keys=["value_map"],
                    entity_type="transformation",
                    entity_name="VALUE_REPLACER")
                return self.factory.create_value_replacer(
                    value_map=options["value_map"])
