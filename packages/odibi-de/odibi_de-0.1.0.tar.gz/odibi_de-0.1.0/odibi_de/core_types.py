from abc import ABC, abstractmethod
from enum import Enum
from typing import Any

import pandas as pd

class DataType(Enum):
    """
    Enum class representing various data formats supported by the framework.
    Attributes:
        CSV (str): Represents CSV file format.
        JSON (str): Represents JSON file format.
        AVRO (str): Represents AVRO file format.
        PARQUET (str): Represents Parquet file format.
        DELTA (str): Represents Delta Lake format.
    """
    CSV = 'csv'
    JSON = 'json'
    AVRO = 'avro'
    PARQUET = 'parquet'
    DELTA = 'delta'
    CLOUDFILES = 'cloudFiles'


class CloudService(Enum):
    """
    Enum class representing different cloud services supported by the
    framework.

    Attributes:
        AZURE (str): Represents Microsoft Azure.
        AWS (str): Represents Amazon Web Services.
        GCP (str): Represents Google Cloud Platform.
    """
    AZURE = "azure"
    AWS = "aws"
    GCP = "gcp"


class Framework(Enum):
    """
    Enum class representing various data processing frameworks
    supported by the framework.

    Attributes:
        PANDAS (str): Represents the Pandas data analysis library.
        SPARK (str): Represents the Apache Spark distributed data
        processing framework.
        SNOWFLAKE (str): Represents the Snowflake cloud data platform.
    """
    PANDAS = "pandas"
    SPARK = "spark"
    SNOWFLAKE = "snowflake"


class ValidationType(Enum):
    """
    Enum class representing different types of data validations that can
    be performed.

    Attributes:
        MISSING_COLUMNS (str): Checks for missing columns in the dataset.
        EXTRA_COLUMNS (str): Checks for unexpected columns in the dataset.
        DATA_TYPE (str): Validates column data types.
        NULL_VALUES (str): Validates that specified columns do not contain
            null values.
        VALUE_RANGE (str): Checks that column values fall within a specified
            range.
        UNIQUENESS (str): Ensures column values are unique.
        ROW_COUNT (str): Validates the number of rows in the dataset.
        NON_EMPTY (str): Ensures the dataset is not empty.
        VALUE (str): Validates specific values in columns.
        REFERENTIAL_INTEGRITY (str): Checks that values in a column match a
            reference dataset.
        REGEX (str): Validates column values against a regular expression.
        DUPLICATE_ROWS (str): Identifies duplicate rows in the dataset.
        COLUMN_DEPENDENCY (str): Validates dependencies between columns.
    """
    MISSING_COLUMNS = "missing_columns"
    EXTRA_COLUMNS = "extra_columns"
    DATA_TYPE = "data_type"
    NULL_VALUES = "null_values"
    VALUE_RANGE = "value_range"
    UNIQUENESS = "uniqueness "
    ROW_COUNT = "row_count"
    NON_EMPTY = "non_empty"
    VALUE = "value"
    REFERENTIAL_INTEGRITY = "referential_integrity"
    REGEX = "regex"
    DUPLICATE_ROWS = "duplicate_rows"
    COLUMN_DEPENDENCY = "column_dependency"
    SCHEMA = "schema"
    COLUMN_TYPE = "column_type"

class TransformerType(Enum):
    """
    An enumeration of supported data transformation operations for Pandas DataFrames.

    Each member represents a specific transformation type that can be applied during
    ETL, data cleaning, or pipeline execution.

    ### Available Transformations

    - `COLUMN_ADDER`: Adds new columns to the DataFrame.
    - `COLUMN_ADDER_STATIC`: Adds static columns with fixed values.
    - `COLUMN_DROPPER`: Drops specified columns.
    - `COLUMN_MERGER`: Merges multiple columns into one.
    - `COLUMN_NAME_PREFIX_SUFFIX`: Adds prefixes or suffixes to column names.
    - `COLUMN_NAME_REGEX_RENAMER`: Renames columns using regex.
    - `COLUMN_NAME_STANDARDIZER`: Standardizes column names.
    - `COLUMN_PATTERN_DROPPER`: Drops columns matching a pattern.
    - `COLUMN_RENAMER`: Renames columns using a mapping.
    - `COLUMN_REORDERER`: Reorders columns based on a list.
    - `COLUMN_SPLITTER`: Splits a column into multiple columns.
    - `COLUMN_TYPE_DROPPER`: Drops columns by data type.
    - `EMPTY_COLUMN_DROPPER`: Drops empty columns.
    - `NULL_RATIO_COLUMN_DROPPER`: Drops columns with too many nulls.
    - `ROW_AGGREGATOR`: Aggregates rows.
    - `ROW_APPENDER`: Appends new rows.
    - `ROW_DEDUPLICATOR`: Removes duplicates.
    - `ROW_DUPLICATOR`: Duplicates matching rows.
    - `ROW_EXPANDER`: Expands rows based on a condition.
    - `ROW_FILTER`: Filters rows based on a condition.
    - `ROW_SAMPLER`: Samples rows.
    - `ROW_SORTER`: Sorts rows.
    - `ROW_SPLITTER`: Splits rows into multiple.
    - `VALUE_REPLACER`: Replaces values in the DataFrame.
    """

    COLUMN_ADDER = "column_adder"
    COLUMN_ADDER_STATIC = "column_adder_static"
    COLUMN_DROPPER = "column_dropper"
    COLUMN_MERGER = "column_merger"
    COLUMN_NAME_PREFIX_SUFFIX = "column_name_prefix_suffix"
    COLUMN_NAME_REGEX_RENAMER = "column_name_regex_renamer"
    COLUMN_NAME_STANDARDIZER = "column_name_standardizer"
    COLUMN_PATTERN_DROPPER = "column_pattern_dropper"
    COLUMN_RENAMER = "column_renamer"
    COLUMN_REORDERER = "column_reorderer"
    COLUMN_SPLITTER = "column_splitter"
    COLUMN_TYPE_DROPPER = "column_type_dropper"
    EMPTY_COLUMN_DROPPER = "empty_column_dropper"
    NULL_RATIO_COLUMN_DROPPER = "null_ratio_column_dropper"
    ROW_AGGREGATOR = "row_aggregator"
    ROW_APPENDER = "row_appender"
    ROW_DEDUPLICATOR = "row_deduplicator"
    ROW_DUPLICATOR = "row_duplicator"
    ROW_EXPANDER = "row_expander"
    ROW_FILTER = "row_filter"
    ROW_SAMPLER = "row_sampler"
    ROW_SORTER = "row_sorter"
    ROW_SPLITTER = "row_splitter"
    VALUE_REPLACER = "value_replacer"

class DataReader(ABC):
    """
    Abstract base class defining the interface for reading data from various
    file formats.

    Attributes:
        file_path (str): The path to the file to be read.

    Methods:
        read_data(**kwargs):
            Abstract method for reading the entire dataset from the file.
        read_sample_data(n: int = 100, **kwargs):
            Method for reading a sample of the dataset, typically for schema
            inference.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path

    @abstractmethod
    def read_data(self, **kwargs):
        """
        Abstract method for reading full datasets.
        Must be implemented by child classes.
        """
        pass

    def read_sample_data(
        self,
        n: int = 100,
        **kwargs
    ):
        """
        Read the first `n` rows of the dataset for schema inference.

        Args:
            n (int): Number of rows to sample. Defaults to 100.
            **kwargs: Additional arguments passed to `read_data`.

        Returns:
            pd.DataFrame: Sampled data.
        """
        try:
            self.logger.log(
                "info", f"Reading a sample of {n} rows from{self.file_path}")
            data = self.read_data(**kwargs).head(n)
            self.logger.log(
                "info",
                f"Successfully read a sample of {n} rows from {self.file_path}"
                )
            return data
        except Exception as e:
            self.logger.log(
                "error",
                f"Failed to read sample data from {self.file_path}: {e}"
                )
            raise


class DataSaver(ABC):
    """
    Abstract base class defining the interface for saving data to various
    file formats.

    Attributes:
        file_path (str): The path to the file where data will be saved.

    Methods:
        save_data(**kwargs):
            Abstract method for saving the dataset to a file.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path

    @abstractmethod
    def save_data(self, **kwargs):
        """
        This is an abstract method that should be implemented by the
        child classes.
        It will save data from a specific file format.
        """
        pass


class ReaderFactory(ABC):
    """
    Abstract base class for creating data readers for different file formats.

    Methods:
        csv_reader(file_path: str) -> DataReader:
            Abstract method to create a CSV reader instance.
        json_reader(file_path: str) -> DataReader:
            Abstract method to create a JSON reader instance.
        avro_reader(file_path: str) -> DataReader:
            Abstract method to create an AVRO reader instance.
        pandas_reader(file_path: str) -> DataReader:
            Abstract method to create a Pandas reader instance.
    """
    @abstractmethod
    def csv_reader(self, file_path: str) -> DataReader:
        pass

    @abstractmethod
    def json_reader(self, file_path: str) -> DataReader:
        pass

    @abstractmethod
    def avro_reader(self, file_path: str) -> DataReader:
        pass

    @abstractmethod
    def parquet_reader(self, file_path: str) -> DataReader:
        pass


class SaverFactory(ABC):
    """
    Abstract base class for creating data savers for different file formats.

    Methods:
        csv_saver(file_path: str, data: pd.DataFrame) -> DataSaver:
            Abstract method to create a CSV saver instance.
        json_saver(file_path: str, data: pd.DataFrame) -> DataSaver:
            Abstract method to create a JSON saver instance.
        avro_saver(file_path: str, data: pd.DataFrame) -> DataSaver:
            Abstract method to create an AVRO saver instance.
        parquet_saver(file_path: str, data: pd.DataFrame) -> DataSaver:
            Abstract method to create a Parquet saver instance.
    """

    @abstractmethod
    def csv_saver(self, file_path: str, data: pd.DataFrame) -> DataSaver:
        pass

    @abstractmethod
    def json_saver(self, file_path: str, data: pd.DataFrame) -> DataSaver:
        pass

    @abstractmethod
    def avro_saver(self, file_path: str, data: pd.DataFrame) -> DataSaver:
        pass

    @abstractmethod
    def parquet_saver(self, file_path: str, data: pd.DataFrame) -> DataSaver:
        pass


class CloudConnector(ABC):
    """
    Abstract base class defining the interface for connecting to and
    interacting with cloud storage.

    Methods:
        get_connection():
            Abstract method to establish a connection to the cloud service.
        get_file_path(storage_unit: str, object_name: str) -> str:
            Abstract method to generate the file path for a given container
            and blob.
        get_framework_config(framework: str) -> dict:
            Abstract method to retrieve framework-specific configuration
            details for the cloud service.
    """
    @abstractmethod
    def get_connection(self):
        """Establish a connection to the cloud service."""
        pass

    @abstractmethod
    def get_file_path(self, storage_unit: str, object_name: str) -> str:
        """Generate the file path for the given container and blob."""
        pass

    @abstractmethod
    def get_framework_config(self, framework: str) -> dict:
        pass


class ReaderProvider(ABC):
    """
    Abstract base class for providing data readers based on the data type
        and cloud connector.

    Attributes:
        factory (ReaderFactory): Instance of a ReaderFactory for creating
            data readers.
        data_type (DataType): The type of data to be read.
        connector (CloudConnector): The cloud connector for accessing the file.

    Methods:
        create_reader(storage_unit: str, object_name: str):
            Abstract method for creating a reader for the specified data type
            and storage location.
    """
    def __init__(
        self, factory: ReaderFactory,
        data_type: DataType,
        connector: CloudConnector
    ):
        self.factory = factory
        self.data_type = data_type
        self.connector = connector

    @abstractmethod
    def create_reader(self, storage_unit: str, object_name: str):
        pass


class SaverProvider(ABC):
    """
    Abstract base class for providing data savers based on the data type and
    cloud connector.

    Attributes:
        factory (SaverFactory): Instance of a SaverFactory for creating data
            savers.
        data_type (DataType): The type of data to be saved.
        connector (CloudConnector): The cloud connector for resolving file
            paths and storage options.

    Methods:
        create_saver(storage_unit: str, object_name: str, data: pd.DataFrame):
            Abstract method for creating a saver for the specified data type
            and storage location.
    """

    def __init__(
        self, factory: SaverFactory,
        connector: CloudConnector
    ):
        """
        Initialize the SaverProvider.

        Args:
            factory (SaverFactory): Factory for creating data savers.
                data_type (DataType): Data type to determine the saver
                (e.g., CSV, JSON, Parquet, Avro).
            connector (CloudConnector): Cloud connector for file path
                resolution and storage options.
        """
        self.factory = factory
        self.connector = connector

    @abstractmethod
    def create_saver(
        self,
        data: pd.DataFrame,
        storage_unit: str,
        object_name: str,
        data_type: DataType
    ):
        pass


class Validator(ABC):
    """
    Abstract base class defining the interface for data validation.

    Methods:
        validate(data):
            Abstract method to perform validation on the given data.
    """

    @abstractmethod
    def validate(self, data):
        """
        Validate the given data.
        """
        pass


class ValidatorFactory(ABC):
    """
    Abstract base class for creating validators for various validation types.

    Methods:
        create_missing_columns_validator(required_columns: list) -> Validator:
            Creates a validator to check for missing columns.
        create_extra_columns_validator(allowed_columns: list) -> Validator:
            Creates a validator to check for extra columns.
        create_data_type_validator(schema: dict) -> Validator:
            Creates a validator to check for column data types.
        create_null_value_validator(critical_columns: list) -> Validator:
            Creates a validator to check for null values in critical columns.
        create_value_range_validator(column_ranges: list) -> Validator:
            Creates a validator to check that column values fall within
            specified ranges.
        create_uniqueness_validator(unique_columns: list) -> Validator:
            Creates a validator to ensure values in specified columns are
            unique.
        create_rowCount_validator(min_rows: int = None, max_rows: int = None)
            -> Validator:
            Creates a validator to check the number of rows in the dataset.
        create_non_empty_validator() -> Validator:
            Creates a validator to ensure the dataset is not empty.
        create_value_validator(column_values: dict, allow_only: bool = True)
            -> Validator:
            Creates a validator to check specific column values.
        create_referential_integrity_validator(column: str, reference_data:
            pd.Series) -> Validator:
            Creates a validator to ensure referential integrity
        create_regex_validator(column_patterns: dict) -> Validator:
            Creates a validator to validate column values against regex
            patterns.
        create_duplicate_row_validator() -> Validator:
            Creates a validator to identify duplicate rows in the dataset.
        create_column_dependency_validator(dependencies: dict) -> Validator:
            Creates a validator to check dependencies between columns.
    """

    @abstractmethod
    def create_missing_columns_validator(
        self,
        required_columns: list
    ) -> Validator:
        pass

    @abstractmethod
    def create_extra_columns_validator(
        self,
        allowed_columns: list
    ) -> Validator:
        pass

    @abstractmethod
    def create_data_type_validator(
        self,
        schema: dict
    ) -> Validator:
        pass

    @abstractmethod
    def create_null_value_validator(
        self,
        critical_columns: list
    ) -> Validator:
        pass

    @abstractmethod
    def create_value_range_validator(
        self,
        column_ranges: list
    ) -> Validator:
        pass

    @abstractmethod
    def create_uniqueness_validator(
        self,
        unique_columns: list
    ) -> Validator:
        pass

    @abstractmethod
    def create_rowCount_validator(
        self,
        min_rows: int = None,
        max_rows: int = None
    ) -> Validator:
        pass

    @abstractmethod
    def create_non_empty_validator(self) -> Validator:
        pass

    @abstractmethod
    def create_value_validator(
        self,
        column_values: dict,
        allow_only: bool = True
    ) -> Validator:
        pass

    @abstractmethod
    def create_referential_integrity_validator(
        self,
        column: str,
        reference_data: pd.Series
    ) -> Validator:
        pass

    @abstractmethod
    def create_regex_validator(
        self,
        column_patterns: dict
    ) -> Validator:
        pass

    @abstractmethod
    def create_duplicate_row_validator(self) -> Validator:
        pass

    @abstractmethod
    def create_column_dependency_validator(
        self,
        dependencies: dict
    ) -> Validator:
        pass

    @abstractmethod
    def create_schema_validator(
        self,
        schema: dict,
        enforce_order: bool = False,
        allow_extra_columns: bool = True
    ) -> Validator:
        pass


class ValidatorProvider(ABC):
    """
    Abstract base class for providing validators based on the validation type
    and options.

    Methods:
        create_validator(validation_type: Any, **options) -> Any:
            Abstract method to create a validator for the given validation
            type and configuration options.
    """

    @abstractmethod
    def create_validator(self, validation_type: Any, **options) -> Any:
        """
        Create a validator based on the provided validation type and options.
        :param validation_type: The type of validation to perform
            (e.g., missing columns, extra columns).
        :param options: Additional configuration for the validator.
        :return: An instance of a framework-specific validator.
        """
        pass


class InferSchema(ABC):
    """
    Abstract base class for inferring schema from a dataset.

    Methods:
        infer(data, **kwargs):
            Abstract method to infer schema from the given dataset.
    """

    @abstractmethod
    def infer(self, data, **kwargs):
        """
        Infer schema from the given dataset.
        :param data: Input dataset (e.g., DataFrame for Pandas/Spark).
        :param kwargs: Additional arguments for framework-specific
            configurations.
        :return: Inferred schema as a dictionary.
        """
        pass


class InferSchemaFactory(ABC):
    """
    Abstract base class for creating schema inference objects.

    Methods:
        create_infer_schema() -> InferSchema:
            Abstract method to create an instance of a schema inference
            implementation.
    """

    @abstractmethod
    def create_infer_schema(self) -> InferSchema:
        """
        Create an instance of an InferSchema implementation.
        :return: An instance of InferSchema.
        """
        pass


class SchemaReader(ABC):
    """
    Abstract base class for reading schemas from external sources.

    Methods:
        read_schema_json(data_reader, source_name: str, **kwargs):
            Abstract method to read a schema from a JSON file.
    """

    @abstractmethod
    def read_schema_json(self, data_reader, source_name: str, **kwargs):
        """
        Abstract method to read schema from a JSON file.
        :param data_reader: Reader object to access schema data.
        :param source_name: Name of the source schema to extract.
        :param kwargs: Additional options for schema reading.
        :return: Schema in a format suitable for the target framework.
        """
        pass


class DBConnector(ABC):
    """
    Abstract base class defining the interface for database connections
    and queries.

    Attributes:
        host (str): Database server hostname or IP address.
        database (str): Name of the database to connect to.
        user (str): Username for authentication.
        password (str): Password for authentication.
        connection (Any): The database connection object.

    Methods:
        connect(): Abstract method to establish a connection to the database.
        fetch_data(query: str, params: dict = None): Abstract method to fetch
            data as a DataFrame.
        execute_query(query: str, params: dict = None): Abstract method to
            execute non-SELECT queries.
        disconnect(): Closes the database connection.
    """

    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    @abstractmethod
    def connect(self):
        """
        Establishes a connection to the database.
        """
        pass

    @abstractmethod
    def fetch_data(self, query: str, params: dict = None):
        """
        Fetches data as a DataFrame.
        :param query: The SQL query to execute.
        :param params: Optional parameters to be passed to the query.
        :return: A DataFrame containing the results of the query.
        """
        pass

    @abstractmethod
    def execute_query(self, query: str, params: dict = None):
        """
        Executes a non-SELECT query.
        :param query: The SQL query to execute.
        :param params: Optional parameters to be passed to the query.
        """
        pass

    def disconnect(self):
        """
        Closes the database connection.
        """
        if self.connection:
            self.connection.close()
            print("Disconnected from database.")


class Transformer(ABC):
    @abstractmethod
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Apply the transformation to the input DataFrame.

        This abstract method defines the interface for transforming data.
        Concrete implementations should override this method to provide
        specific transformation logic.
        Args:
            data (pd.DataFrame): The input DataFrame to be transformed.

        Returns:
            pd.DataFrame: The transformed DataFrame after applying
                the transformation logic.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        pass


class Workflow(ABC):
    """
    Abstract base class for defining workflows.

    This class provides a blueprint for implementing workflows in different
    environments(e.g., local, cloud). It enforces a consistent interface for
    reading, validating, transforming, and saving data.

    Attributes:
        config_loader (UnifiedConfigLoader): The configuration loader.
        data_reader (DataReader): The reader for loading the configuration
        file.
        config (dict): The loaded configuration.
        datasets (dict): The loaded datasets.
        logger (DynamicLogger): Logger instance for logging workflow
        operations.

    Methods:
        load_config(): Load the unified configuration file.
        read(): Abstract method to read datasets.
        save(): Abstract method to save datasets.
        validate(): Abstract method to validate datasets.
        transform(): Abstract method to transform datasets.
    """
    @abstractmethod
    def read(self):
        """
        Abstract method to read datasets based on the configuration.
        """
        pass

    @abstractmethod
    def save(self, variable_name: str, file_path: str, data_type: str):
        """
        Abstract method to save datasets.

        Args:
            variable_name (str): The dataset's variable name to save.
            file_path (str): Path where the dataset will be saved.
            data_type (str): Format of the saved dataset (e.g., "CSV").
        """
        pass

    @abstractmethod
    def validate(self):
        """
        Abstract method to validate datasets.
        """
        pass

    @abstractmethod
    def transform(self, module):
        """
        Abstract method to transform datasets.

        Args:
            module: The module containing transformer classes.
        """
        pass


class TransformerFactory(ABC):
    """
    Abstract base class for creating transformers for various Pandas
    transformation types.

    Methods:
        create_column_adder(columns: dict) -> Transformer:
            Creates a transformer to add new columns.
        create_column_adder_static(column_name: str, value: any) -> Transformer:
            Creates a transformer to add a static column with a fixed value.
        create_column_dropper(columns: list) -> Transformer:
            Creates a transformer to drop specified columns.
        create_column_merger(columns: list, separator: str) -> Transformer:
            Creates a transformer to merge multiple columns into one.
        create_column_name_prefix_suffix(
            prefix: str = None, suffix: str = None) -> Transformer:
            Creates a transformer to add a prefix or suffix to column names.
        create_column_name_regex_renamer(pattern: str, replacement: str) -> Transformer:
            Creates a transformer to rename columns using regex.
        create_column_name_standardizer() -> Transformer:
            Creates a transformer to standardize column names.
        create_column_pattern_dropper(pattern: str) -> Transformer:
            Creates a transformer to drop columns matching a specific pattern.
        create_column_renamer(renaming_map: dict) -> Transformer:
            Creates a transformer to rename columns.
        create_column_reorderer(order: list) -> Transformer:
            Creates a transformer to reorder columns based on a given order.
        create_column_splitter(column: str, delimiter: str) -> Transformer:
            Creates a transformer to split a column into multiple columns.
        create_column_type_dropper(data_types: list) -> Transformer:
            Creates a transformer to drop columns of specific data types.
        create_empty_column_dropper() -> Transformer:
            Creates a transformer to drop columns that are completely empty.
        create_null_ratio_column_dropper(threshold: float) -> Transformer:
            Creates a transformer to drop columns exceeding a null value ratio.
        create_row_aggregator(aggregation_map: dict) -> Transformer:
            Creates a transformer to aggregate rows based on a function.
        create_row_appender(rows: list) -> Transformer:
            Creates a transformer to append rows to the DataFrame.
        create_row_deduplicator() -> Transformer:
            Creates a transformer to remove duplicate rows.
        create_row_duplicator(row_indices: list) -> Transformer:
            Creates a transformer to duplicate specified rows.
        create_row_expander(expansion_rule: dict) -> Transformer:
            Creates a transformer to expand rows based on a rule.
        create_row_filter(condition: str) -> Transformer:
            Creates a transformer to filter rows based on a condition.
        create_row_sampler(
            sample_fraction: float, random_state: int = None) -> Transformer:
            Creates a transformer to sample rows from the DataFrame.
        create_row_sorter(columns: list, ascending: list) -> Transformer:
            Creates a transformer to sort rows based on specified columns.
        create_row_splitter(column: str, split_values: list) -> Transformer:
            Creates a transformer to split rows into groups.
        create_value_replacer(replacement_map: dict) -> Transformer:
            Creates a transformer to replace specific values in the DataFrame.
    """

    @abstractmethod
    def create_column_adder(self, columns: dict) -> "Transformer":
        pass

    @abstractmethod
    def create_column_adder_static(self, column_name: str, value: any) -> "Transformer":
        pass

    @abstractmethod
    def create_column_dropper(self, columns: list) -> "Transformer":
        pass

    @abstractmethod
    def create_column_merger(self, columns: list, separator: str) -> "Transformer":
        pass

    @abstractmethod
    def create_column_name_prefix_suffix(
        self, prefix: str = None, suffix: str = None) -> "Transformer":
        pass

    @abstractmethod
    def create_column_name_regex_renamer(
        self, pattern: str, replacement: str) -> "Transformer":
        pass

    @abstractmethod
    def create_column_name_standardizer(self) -> "Transformer":
        pass

    @abstractmethod
    def create_column_pattern_dropper(self, pattern: str) -> "Transformer":
        pass

    @abstractmethod
    def create_column_renamer(self, renaming_map: dict) -> "Transformer":
        pass

    @abstractmethod
    def create_column_reorderer(self, order: list) -> "Transformer":
        pass

    @abstractmethod
    def create_column_splitter(self, column: str, delimiter: str) -> "Transformer":
        pass

    @abstractmethod
    def create_column_type_dropper(self, data_types: list) -> "Transformer":
        pass

    @abstractmethod
    def create_empty_column_dropper(self) -> "Transformer":
        pass

    @abstractmethod
    def create_null_ratio_column_dropper(self, threshold: float) -> "Transformer":
        pass

    @abstractmethod
    def create_row_aggregator(self, aggregation_map: dict) -> "Transformer":
        pass

    @abstractmethod
    def create_row_appender(self, rows: list) -> "Transformer":
        pass

    @abstractmethod
    def create_row_deduplicator(self) -> "Transformer":
        pass

    @abstractmethod
    def create_row_duplicator(self, row_indices: list) -> "Transformer":
        pass

    @abstractmethod
    def create_row_expander(self, expansion_rule: dict) -> "Transformer":
        pass

    @abstractmethod
    def create_row_filter(self, condition: str) -> "Transformer":
        pass

    @abstractmethod
    def create_row_sampler(
        self, sample_fraction: float, random_state: int = None) -> "Transformer":
        pass

    @abstractmethod
    def create_row_sorter(self, columns: list, ascending: list) -> "Transformer":
        pass

    @abstractmethod
    def create_row_splitter(self, column: str, split_values: list) -> "Transformer":
        pass

    @abstractmethod
    def create_value_replacer(self, replacement_map: dict) -> "Transformer":
        pass


class TransformerProvider(ABC):
    """
    Abstract base class for providing transformers based on the transformer type
    and options.

    Methods:
        create_transformer(transformer_type: Any, **options) -> Any:
            Abstract method to create a transformer for the given transformer
            type and configuration options.
    """

    @abstractmethod
    def create_transformer(self, transformer_type: Any, **options) -> Any:
        """
        Create a transformer based on the provided transformer type and options.

        Args:
            transformer_type: The type of transformer to create.
            **options: Additional configuration for the transformer.

        Returns:
            An instance of a framework-specific transformer.
        """
        pass


class BaseDataWorkflow(ABC):
    """
    Abstract base class for data workflows.

    Attributes:
        config_loader (UnifiedConfigLoader): Loads the unified configuration.
        logger (Logger): Logger for workflow activity.
    """

    def __init__(self):
        """
        Initializes the base class.
        """
        from Data_Engineering_Class_Libraries_and_Utility_Functions import (
            UnifiedConfigLoader, get_logger
        )
        self.config_loader = UnifiedConfigLoader()
        self.logger = get_logger()
        self.config = None

    def load_config(self, file_path, config_connector=None):
        from Data_Engineering_Class_Pandas_Implementation import PandasJsonReader
        from Data_Engineering_Class_Libraries_and_Utility_Functions import (
            PandasValidationUtils)
        """
        Loads the unified configuration using the provided data reader.

        Args:
            config_data_reader: The data reader instance for the configuration.
        """
        PandasValidationUtils.validate_is_non_empty_string(file_path)
        if config_connector:
            PandasValidationUtils.validate_inheritance(config_connector,DBConnector)
        self.config_connector = config_connector
        self.logger.log("info", "Loading configuration...")
        if self.config_connector:
            storage_options = self.config_connector.get_framework_config("pandas")
            config_data_reader = PandasJsonReader(
                file_path = file_path,
                storage_options = storage_options
            )
        else:
            config_data_reader = PandasJsonReader(
                file_path = file_path)
        self.config = self.config_loader.load_config(config_data_reader)
        self.logger.log("info", "Configuration loaded successfully.")

    def read_datasets(
        self,
        data_connector: DBConnector = None
        ):
        from Data_Engineering_Class_Libraries_and_Utility_Functions import (
            PandasValidationUtils)
        """
        Reads datasets based on the configuration.

        Returns:
            dict: A dictionary of dataset names and their corresponding DataFrames.
        """
        self.data_connector = data_connector
        self.datasets = {}

        for dataset_config in self.config["datasets"]:
            try:
                variable_name, data = self._read_single_dataset(dataset_config)
                self.datasets[variable_name] = data
                self.logger.log(
                    "info",
                    f"Dataset '{variable_name}' loaded successfully.")
            except Exception as e:
                error_message = (
                    "Failed to read dataset "+
                    f"'{dataset_config['reader']['variable_name']}': {e}")
                self.logger.log(
                    "error",
                    error_message)
                raise Exception(error_message)

        return self.datasets

    def _read_single_dataset(self, dataset_config):
        from Data_Engineering_Class_Libraries_and_Utility_Functions import (
            PandasValidationUtils, ConfigValidator)
        """
        Reads a single dataset based on its configuration.

        Args:
            dataset_config (dict): Configuration for the dataset.

        Returns:
            tuple: (variable_name, DataFrame)

        Raises:
            ValueError: If neither `local` nor `cloud` is configured properly.
        """
        PandasValidationUtils.validate_is_non_empty_dict(dataset_config)

        variable_name = dataset_config["reader"]["variable_name"]
        # Validate the dataset configuration
        ConfigValidator.validate_dataset_config(dataset_config)

        provider = self.get_reader_provider(dataset_config)
        reader_config = dataset_config["reader"]
        kwargs = reader_config.get("kwargs", {})

        # Check for exclusivity of local and cloud configurations
        local_config = reader_config.get("local", {})
        cloud_config = reader_config.get("cloud", {})

        if local_config:
            data = provider.create_reader(local_config["file_path"]).read_data(**kwargs)
        elif cloud_config:
            data = provider.create_reader(
                cloud_config["storage_unit"], cloud_config["object_name"]
            ).read_data(**kwargs)

        return variable_name, data

    def validate_datasets(self, validator_module):
        from Data_Engineering_Class_Libraries_and_Utility_Functions import (
            PandasValidationUtils, ValidatorRunner, DynamicValidatorFactory)
        """
        Applies validators to datasets based on the configuration.

        For each dataset, this method initializes a validator runner
        and applies the specified validators. Validation results are stored in
        `self.validation_reports`.

        Raises:
            ValueError: If the configuration or datasets are invalid.
        """
        self.validation_summaries = {}
        self.validation_reports = {}
        self.validator_module = validator_module

        if not self.config:
            error_message = ("Configuration not loaded. Call " +
            "'load_config' before 'validate'.")
            self.logger.log(
                "error",
                error_message)
            raise ValueError(error_message)

        for dataset_config in self.config["datasets"]:
            dataset_name = dataset_config["reader"]["variable_name"]

            PandasValidationUtils.validate_dataset_in_workflow(
                dataset_name,
                self.datasets)
            data = self.datasets[dataset_name]

            validator_configs = dataset_config.get("validators", [])
            if not validator_configs:
                self.logger.log(
                    "warning",
                    f"No validators specified for dataset '{dataset_name}'"
                    ". Skipping validation.")
                continue

            factory = DynamicValidatorFactory(validator_module)
            runner = ValidatorRunner(validator_configs, factory)

            try:
                validation_report = runner.run_validations(data)
                self.validation_reports[dataset_name] = validation_report
                self.validation_summaries[dataset_name] = validation_report\
                    .generate_summary()
                self.logger.log(
                    "info",
                    f"Validation sucessfully completed for '{dataset_name}':")
            except Exception as e:
                error_message = (
                    f"Validation failed for dataset '{dataset_name}': {e}")
                self.logger.log(
                    "error",
                    error_message)
                raise Exception(error_message)

    def transform_datasets(self, transformer_module):
        from Data_Engineering_Class_Libraries_and_Utility_Functions import (
            DynamicTransformerFactory)
        """
        Applies transformers to datasets sequentially based on
        the configuration.

        Args:
            module: The module containing transformer classes.

        Raises:
            ValueError: If the configuration is not loaded or datasets
                        are not initialized.
            KeyError: If a dataset is missing from the workflow.
            Exception: For any issues during the transformation process.
        """
        self.transformed_datasets = {}
        self.transformer_module = transformer_module
        if not self.config:
            error_message = (
                "Configuration not loaded. Call 'load_config' before " +
                "'transform'."
            )
            self.logger.log(
                "error",
                error_message)
            raise ValueError(error_message)

        transformer_factory = DynamicTransformerFactory(self.transformer_module)

        for dataset_config in self.config["datasets"]:
            dataset_name = dataset_config["reader"]["variable_name"]

            # Retrieve dataset from transformed_datasets
            data = self.transformed_datasets.get(
                dataset_name, self.datasets.get(dataset_name))

            if data is None:
                error_message = (
                    f"Dataset '{dataset_name}' not found in the workflow."
                )
                self.logger.log(
                    "error",
                    error_message)
                raise KeyError(error_message)

            # Apply transformers sequentially
            for transformer_config in dataset_config.get("transformers", []):
                try:
                    # Validate transformer configuration if necessary
                    transformer = transformer_factory.create_transformer(
                        transformer_config)
                    data = transformer.transform(data)
                    self.logger.log(
                        "info",
                        f"Applied transformer '{transformer_config['type']}' "
                        f"to dataset '{dataset_name}'."
                    )

                    # Save the transformed dataset
                    self.transformed_datasets[dataset_name] = data

                except Exception as e:
                    error_message = (
                        f"Transformation failed for dataset '{dataset_name}' "
                        f"using transformer '{transformer_config['type']}':"
                        f" {e}."
                    )
                    self.logger.log(
                        "error",
                        error_message)
                    raise Exception(error_message)

    def save_datasets(self, save_connector=None):
        """
        Saves datasets to the specified locations based on the configuration.

        Args:
            save_connector (DBConnector, optional): Connector for cloud or
            local destinations.

        Returns:
            dict: A dictionary of dataset names and their save statuses
            (success/failure).
        """
        from Data_Engineering_Class_Libraries_and_Utility_Functions import (
            PandasValidationUtils)

        self.save_connector = save_connector or self.data_connector
        save_status = {}

        for dataset_name, df in self.datasets.items():
            try:
                save_config = self._get_save_config(dataset_name)
                self._save_single_dataset(df, save_config)
                save_status[dataset_name] = "success"
                self.logger.log(
                    "info",
                    f"Dataset '{dataset_name}' saved successfully.")
            except Exception as e:
                error_message = f"Failed to save dataset '{dataset_name}': {e}"
                save_status[dataset_name] = f"failed: {e}"
                self.logger.log(
                    "error",
                    error_message)
                raise Exception(error_message)

        return save_status

    def _get_save_config(self, dataset_name):
        """
        Retrieve the save configuration for a specific dataset.

        Args:
            dataset_name (str): Name of the dataset.

        Returns:
            dict: Save configuration for the dataset.

        Raises:
            ValueError: If no configuration is found for the dataset.
        """
        for dataset_config in self.config["datasets"]:
            if dataset_config["reader"]["variable_name"] == dataset_name:
                return dataset_config
        raise ValueError(f"No save configuration found for dataset '{dataset_name}'.")

    def _pre_save_hook(self, save_config, kwargs):
        """
        Hook to customize arguments for saving datasets.

        Args:
            save_config (dict): Configuration for saving the dataset.
            kwargs (dict): Existing parameters for the saver.

        Returns:
            dict: Modified kwargs.
        """
        return kwargs

    def _get_additional_saver_args(self, save_config):
        """
        Hook to provide additional arguments for the saver.

        Args:
            save_config (dict): Configuration for saving the dataset.

        Returns:
            dict: Additional arguments for the saver.
        """
        return {}

    def _save_single_dataset(self, df, save_config):
        from Data_Engineering_Class_Libraries_and_Utility_Functions import (
            PandasValidationUtils, ConfigValidator)
        """
        Saves a single dataset based on its configuration.

        Args:
            df (DataFrame): The DataFrame to save.
            save_config (dict): Configuration for saving the dataset.

        Raises:
            ValueError: If neither `local` nor `cloud` is configured properly.
        """
        writer_config = save_config["writer"]
        variable_name = writer_config["variable_name"]

        # Validate the writer configuration
        ConfigValidator.validate_writer_config(writer_config, variable_name)

        provider = self.get_saver_provider(save_config)
        local_config = writer_config.get("local", {})
        cloud_config = writer_config.get("cloud", {})
        data_type = writer_config["data_type"]
        kwargs = writer_config.get("kwargs", {})

        # Call the pre-save hook for custom modifications
        kwargs = self._pre_save_hook(save_config, kwargs)

        additional_args = self._get_additional_saver_args(save_config)
        if local_config:
            provider.create_saver(
                df,
                local_config["file_path"],
                DataType[data_type.upper()]
                ).save_data(**kwargs)
        elif cloud_config:
            provider.create_saver(
                df,
                cloud_config["storage_unit"],
                cloud_config["object_name"],
                DataType[data_type.upper()],
                **additional_args
            ).save_data(**kwargs)

    @abstractmethod
    def get_reader_provider(self, dataset_config):
        """
        Abstract method to retrieve the appropriate provider for the workflow.

        Args:
            dataset_config (dict): The dataset configuration.

        Returns:
            ReaderProvider: The appropriate reader provider.
        """
        pass



