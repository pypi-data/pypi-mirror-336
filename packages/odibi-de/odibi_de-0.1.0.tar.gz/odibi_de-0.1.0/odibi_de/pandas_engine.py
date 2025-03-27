import re
import time
import numpy as np
import pandas as pd
from typing import Optional, Dict, Any, Union
from fastavro import reader
import fsspec
from odibi_de.core_types import (
    CloudConnector, DBConnector, DataReader, DataSaver, DataType, Framework,
    InferSchema, InferSchemaFactory, ReaderFactory, ReaderProvider,
    SaverFactory, SaverProvider, SchemaReader, Transformer, ValidationType,
    Validator, ValidatorFactory, ValidatorProvider, TransformerFactory,
    TransformerProvider, TransformerType, BaseDataWorkflow)
from odibi_de.utils import (
    PandasValidationUtils, get_logger, validate_kwargs, validate_options,
    log_message)
import pyodbc

class PandasJsonReader(DataReader):
    """
    Reader class for JSON files using Pandas.

    This class provides functionality to read full JSON datasets or sample
    rows, with support for dynamic method application and cloud storage
    options.

    Attributes:
        file_path (str): Path to the JSON file to read.
        storage_options (dict): Storage configuration for reading files from
        cloud or remote locations.

    Example Usage:
        from my_module import PandasJsonReader
        # Reading a full JSON file
        reader = PandasJsonReader(
            "/dbfs/mnt/data/data.json",
            storage_options={
                "account_name": account_name, "account_key": account_key})
        data = reader.read_data()

        # Reading a sample of the JSON file
        sample = reader.read_sample_data(n=5)
    """

    def __init__(
        self,
        file_path: str,
        storage_options: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize PandasJsonReader with the file path and storage options.

        Args:
            file_path (str): Path to the JSON file.
            storage_options (dict, optional): Configuration for remote storage,
            e.g., Azure, AWS. Defaults to None.
        """
        PandasValidationUtils.validate_is_non_empty_string(
            file_path)
        super().__init__(file_path)
        if storage_options:
            PandasValidationUtils.validate_is_non_empty_dict(
                storage_options)
        self.storage_options = storage_options
        PandasValidationUtils.log_init_arguments(self)

    def read_data(
        self,
        **kwargs
    ) -> pd.DataFrame:
        """
        Read the full JSON dataset with error handling and dynamic
        method application.

        Args:
            **kwargs: Additional keyword arguments for Pandas `read_json`.

        Returns:
            pd.DataFrame: Loaded JSON dataset as a Pandas DataFrame.

        Raises:
            FileNotFoundError: If the file path is invalid or the file
            is not found.
            ValueError: If the JSON file is empty or invalid.
            pd.errors.EmptyDataError: If the JSON file is empty.
            Exception: For any unexpected errors during the reading process.

        Example Usage:
            from my_module import PandasJsonReader

            # Example with default arguments
                reader = PandasJsonReader("/dbfs/mnt/data/data.json")
                data = reader.read_data()
                print(data)
            # Example with additional keyword arguments
                reader = PandasJsonReader("/dbfs/mnt/data/data.json")
                data = reader.read_data(orient="records")
                print(data)
            # Example with storage options
                reader = PandasJsonReader(
                    "/dbfs/mnt/data/data.json",
                    storage_options={
                        "account_name": account_name,
                        "account_key": account_key})
                data = reader.read_data()
                print(data)

            # Example reading a sample of the JSON file
            sample = reader.read_sample_data(n=5)
        """
        try:
            log_message(
                "info",
                f"Attempting to read JSON data from {self.file_path}")

            # Use Pandas read_json as the reader
            reader = pd.read_json
            # Execute the reader to load the data
            if kwargs:
                validate_kwargs(
                    pd.read_json,
                    kwargs)
            data = reader(
                self.file_path,
                storage_options=self.storage_options,
                **kwargs)
            log_message(
                "info",
                f"Successfully read JSON data from {self.file_path}")
            return data

        except FileNotFoundError:
            error_message = f"File not found: {self.file_path}"
            log_message(
                "error",
                error_message)
            raise FileNotFoundError(error_message)

        except pd.errors.EmptyDataError:
            error_message = (
                f"JSON file is empty: {self.file_path}")
            log_message(
                "error",
                error_message)
            raise pd.errors.EmptyDataError(error_message)

        except ValueError as e:
            error_message = (
                f"Invalid JSON file at {self.file_path}: {e}")
            log_message(
                "error",
                error_message)
            raise ValueError(error_message) from e

        except Exception as e:
            error_message = (
                "Unexpected error while reading JSON data from " +
                f"{self.file_path}: {e}")
            log_message(
                "error",
                error_message)
            raise Exception(error_message) from e


class PandasParquetReader(DataReader):
    """
    Reader class for Parquet files using Pandas.

    This class provides functionality to read full Parquet datasets or
    sample rows, with support for dynamic method application and
    cloud storage options.

    Attributes:
        file_path (str): Path to the Parquet file to read.
        storage_options (dict): Storage configuration for reading files
        from cloud or remote locations.

    Example Usage:
    from my_module import PandasParquetReader
        # Reading a full Parquet file
        reader = PandasParquetReader(
            "/dbfs/mnt/data/data.parquet",
            storage_options={
                "account_name": account_name, "account_key": account_key})
        data = reader.read_data()

        # Reading a sample of the Parquet file
        sample = reader.read_sample_data(n=5)
    """

    def __init__(
        self,
        file_path: str,
        storage_options: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize PandasParquetReader with the file path and storage options.

        Args:
            file_path (str): Path to the Parquet file.
            storage_options (dict, optional): Configuration for remote storage,
            e.g., Azure, AWS. Defaults to {"anon": True}.
        """
        PandasValidationUtils.validate_is_non_empty_string(
            file_path)
        super().__init__(file_path)
        if storage_options:
            PandasValidationUtils.validate_is_non_empty_dict(
                storage_options)
        self.storage_options = storage_options
        PandasValidationUtils.log_init_arguments(self)

    def read_data(
        self,
        **kwargs
    ) -> pd.DataFrame:
        """
        Read the full Parquet dataset with error handling and dynamic method
        application.

        Args:
            **kwargs: Additional keyword arguments for Pandas `read_parquet`.

        Returns:
            pd.DataFrame: Loaded Parquet dataset as a Pandas DataFrame.

        Raises:
            FileNotFoundError: If the file path is invalid or the file is
            not found.
            ValueError: If the Parquet file is empty or invalid.
            pd.errors.EmptyDataError: If the Parquet file is empty.
            Exception: For any unexpected errors during the reading process.

        Example Usage:
        from my_module import PandasParquetReader
        # Example with default arguments
            reader = PandasParquetReader(
                "/dbfs/mnt/data/data.parquet")
            data = reader.read_data()
            print(data)
        # Example with additional keyword arguments
            reader = PandasParquetReader(
                "/dbfs/mnt/data/data.parquet")
            data = reader.read_data()
            print(data)
        # Example with storage options
            reader = PandasParquetReader(
                "/dbfs/mnt/data/data.parquet",
                storage_options={
                    "account_name": account_name, "account_key": account_key})
            data = reader.read_data()
            print(data)

        # Example reading a sample of the Parquet file
        sample = reader.read_sample_data(n=5)
        """
        try:
            log_message(
                "info",
                f"Attempting to read Parquet data from {self.file_path}")

            # Use Pandas read_parquet as the reader
            reader = pd.read_parquet
            # Execute the reader to load the data
            if kwargs:
                validate_kwargs(
                    pd.read_parquet,
                    kwargs)
            data = reader(
                self.file_path,
                storage_options=self.storage_options,
                **kwargs
                )
            log_message(
                "info",
                f"Successfully read Parquet data from {self.file_path}")
            return data

        except FileNotFoundError:
            error_message = f"File not found: {self.file_path}"
            log_message(
                "error",
                error_message)
            raise FileNotFoundError(error_message)

        except ValueError as e:
            error_message = (
                f"Invalid Parquet file at {self.file_path}: {e}"
            )
            log_message(
                "error",
                error_message)
            raise ValueError(error_message) from e

        except pd.errors.EmptyDataError:
            error_message = (
                f"Parquet file is empty: {self.file_path}"
            )
            log_message(
                "error",
                error_message)
            raise pd.errors.EmptyDataError(error_message)

        except Exception as e:
            error_message = (
                "Unexpected error while reading Parquet data from "
                f"{self.file_path}: {e}"
            )
            log_message(
                "error",
                error_message)
            raise Exception(error_message) from e


class PandasCsvReader(DataReader):
    """
    Reader class for CSV files using Pandas.

    This class provides functionality to read full CSV datasets or sample rows,
    with support for dynamic method application and cloud storage options.

    Attributes:
        file_path (str): Path to the CSV file to read.
        storage_options (dict): Storage configuration for reading files from
        cloud or remote locations.

    Example Usage:
    from my_module import PandasCsvReader
        # Reading a full CSV file
        reader = PandasCsvReader("/dbfs/mnt/data/data.csv",
        storage_options={
            "account_name": account_name, "account_key": account_key})
        data = reader.read_data()

        # Reading a sample of the CSV file
        sample = reader.read_sample_data(n=5)
    """

    def __init__(
        self,
        file_path: str,
        storage_options: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize PandasCsvReader with the file path and storage options.

        Args:
            file_path (str): Path to the CSV file.
            storage_options (dict, optional): Configuration for remote storage,
            e.g., Azure, AWS. Defaults to None.
        """
        PandasValidationUtils.validate_is_non_empty_string(
            file_path)
        super().__init__(file_path)
        if storage_options:
            PandasValidationUtils.validate_is_non_empty_dict(
                storage_options)
        self.storage_options = storage_options
        PandasValidationUtils.log_init_arguments(self)

    def read_data(
        self,
        **kwargs
    ) -> pd.DataFrame:
        """
        Read the full CSV dataset with error handling and dynamic
        method application.

        Args:
            **kwargs: Additional keyword arguments for Pandas `read_csv`.

        Returns:
            pd.DataFrame: Loaded CSV dataset as a Pandas DataFrame.

        Raises:
            FileNotFoundError: If the file path is invalid or the file is
            not found.
            ValueError: If the CSV file is empty or invalid.
            pd.errors.EmptyDataError: If the CSV file is empty.
            pd.errors.ParserError: If there's an error parsing the CSV file.
            Exception: For any unexpected errors during the reading process.

        Example Usage:
            from my_module import PandasCsvReader
            # Example with default arguments
            reader = PandasCsvReader("/dbfs/mnt/data/data.csv")
            data = reader.read_data()
            print(data)
        # Example with additional keyword arguments
            reader = PandasCsvReader("/dbfs/mnt/data/data.csv")
            data = reader.read_data()
            print(data)
        # Example with storage options
            reader = PandasCsvReader(
                "/dbfs/mnt/data/data.csv",
                storage_options={
                    "account_name": account_name, "account_key": account_key})
            data = reader.read_data()
            print(data)

        # Example reading a sample of the CSV file
            sample = reader.read_sample_data(n=5)
        """
        try:
            log_message(
                "info",
                f"Attempting to read CSV data from {self.file_path}")

            # Use Pandas read_csv as the reader
            reader = pd.read_csv
            # Execute the reader to load the data
            if kwargs:
                validate_kwargs(
                    pd.read_csv,
                    kwargs)
            data = reader(
                self.file_path,
                storage_options=self.storage_options,
                **kwargs)
            log_message(
                "info",
                f"Successfully read CSV data from {self.file_path}")
            return data

        except FileNotFoundError:
            error_message = f"File not found: {self.file_path}"
            log_message(
                "error",
                error_message)
            raise FileNotFoundError(error_message)

        except pd.errors.EmptyDataError:
            error_message = f"CSV file is empty: {self.file_path}"
            log_message(
                "error",
                error_message)
            raise pd.errors.EmptyDataError(error_message)

        except pd.errors.ParserError as e:
            error_message = f"Parsing error in CSV file {self.file_path}: {e}"
            log_message(
                "error",
                error_message)
            raise pd.errors.ParserError(error_message) from e

        except Exception as e:
            error_message = (
                "Unexpected error while reading CSV data from " +
                f"{self.file_path}: {e}")
            log_message(
                "error",
                error_message)
            raise Exception(error_message) from e


class PandasAvroReader(DataReader):
    """
    Reader class for Avro files using Pandas.

    This class provides functionality to read full Avro datasets or sample rows
    while supporting cloud storage options.

    Attributes:
        file_path (str): Path to the Avro file to read.
        storage_options (dict): Storage configuration for reading files from
        cloud or remote locations.

    Example Usage:
        from my_module import PandasAvroReader
        # Reading a full Avro file
        reader = PandasAvroReader(
            "/dbfs/mnt/data/data.avro",
            storage_options={
                "account_name": account_name, "account_key": account_key})
        data = reader.read_data()

        # Reading a sample of the Avro file
        sample = reader.read_sample_data(n=5)
    """

    def __init__(
        self,
        file_path: str,
        storage_options: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize PandasAvroReader with the file path and storage options.

        Args:
            file_path (str): Path to the Avro file.
            storage_options (dict, optional): Configuration for remote storage,
            e.g., Azure, AWS. Defaults to {"anon": True}.
        """
        PandasValidationUtils.validate_is_non_empty_string(
            file_path)
        super().__init__(file_path)
        if storage_options:
            PandasValidationUtils.validate_is_non_empty_dict(
                storage_options)
        self.storage_options = storage_options
        PandasValidationUtils.log_init_arguments(self)

    def read_data(
        self,
        **kwargs
    ) -> pd.DataFrame:
        """
        Read the full Avro dataset with error handling and dynamic
        method application.

        Args:
            and their arguments to apply dynamically.
                Example: {"filter": {"items": ["desired_column"]}}
            **kwargs: Additional configurations for Avro reading.

        Returns:
            pd.DataFrame: Loaded Avro dataset as a Pandas DataFrame.

        Raises:
            FileNotFoundError: If the file path is invalid or the file is
            not found.
            ValueError: If the Avro file is empty or invalid.
            Exception: For any unexpected errors during the reading process.

        Example Usage:
        from my_module import PandasAvroReader
        # Example with default arguments
            reader = PandasAvroReader(
                "/dbfs/mnt/data/data.avro")
            data = reader.read_data()
            print(data)
        # Example with additional keyword arguments
            reader = PandasAvroReader(
                "/dbfs/mnt/data/data.avro")
            data = reader.read_data()
            print(data)
        # Example with storage options
            reader = PandasAvroReader(
                "/dbfs/mnt/data/data.avro",
                storage_options={
                    "account_name": account_name, "account_key": account_key})
            data = reader.read_data()
            print(data)
        """
        try:
            log_message(
                "info",
                f"Attempting to read Avro data from {self.file_path}")

            # Open and read the Avro file
            with fsspec.open(
                self.file_path, mode="rb",
                **self.storage_options,
                **kwargs
            ) as f:
                avro_reader = reader(f)
                avro_data = [record for record in avro_reader]

            # Convert to DataFrame
            data = pd.DataFrame(avro_data)

            log_message(
                "info",
                f"Successfully read Avro data from {self.file_path}")
            return data

        except FileNotFoundError:
            error_message = (
                f"File not found: {self.file_path}")
            log_message(
                "error",
                error_message)
            raise FileNotFoundError(error_message)

        except ValueError as e:
            error_message = (
                f"Invalid Avro file at {self.file_path}: {e}")
            log_message(
                "error",
                error_message)
            raise ValueError(error_message) from e

        except Exception as e:
            error_message = (
                "Unexpected error while reading Avro data from " +
                f"{self.file_path}: {e}")
            log_message(
                "error",
                error_message)
            raise Exception(error_message) from e


class PandasReaderFactory(ReaderFactory):
    """
    Factory class for creating Pandas-based readers.

    This class provides methods to instantiate concrete Pandas readers
    for various file formats,
    such as CSV, JSON, Avro, and Parquet.

    Methods:
        csv_reader(file_path, storage_options): Creates a reader for CSV files.
        json_reader(file_path, storage_options): Creates a reader for JSON
        files.
        avro_reader(file_path, storage_options): Creates a reader for Avro
        files.
        parquet_reader(file_path, storage_options): Creates a reader for
        Parquet files.

    Example Usage:
        from my_module import PandasReaderFactory

        factory = PandasReaderFactory()

        # Creating a CSV reader
        csv_reader = factory.csv_reader("/dbfs/mnt/data/data.csv")
        data = csv_reader.read_data()

        # Creating a JSON reader
        json_reader = factory.json_reader("/dbfs/mnt/data/data.json")
        json_data = json_reader.read_data()

    """

    def csv_reader(
        self,
        file_path: str,
        storage_options: Optional[Dict[str, Any]] = None
    ) -> DataReader:
        """
        Create a CSV reader.

        Args:
            file_path (str): Path to the CSV file.
            storage_options (dict, optional): Configuration for remote storage.
            Defaults to None.

        Returns:
            PandasCsvReader: Instance of the CSV reader.

        Raises:
            Exception: If the reader instantiation fails.

        Example Usage:
        from my_module import PandasReaderFactory
        factory = PandasReaderFactory()
        csv_reader = factory.csv_reader("/dbfs/mnt/data/data.csv")
        data = csv_reader.read_data()

        """
        try:
            log_message(
                "info",
                f"Creating CSV reader for file: {file_path}")
            return PandasCsvReader(
                file_path=file_path,
                storage_options=storage_options)
        except Exception as e:
            error_message = (
                f"Failed to create CSV reader for file: {file_path} - {e}"
            )
            log_message(
                "error",
                error_message)
            raise Exception(error_message) from e

    def json_reader(
        self,
        file_path: str,
        storage_options: Optional[Dict[str, Any]] = None
    ) -> DataReader:
        """
        Create a JSON reader.

        Args:
            file_path (str): Path to the JSON file.
            storage_options (dict, optional): Configuration for remote storage.
            Defaults to None.

        Returns:
            PandasJsonReader: Instance of the JSON reader.

        Raises:
            Exception: If the reader instantiation fails.

        Example Usage:
        from my_module import PandasReaderFactory
        factory = PandasReaderFactory()
        json_reader = factory.json_reader("/dbfs/mnt/data/data.json")
        data = json_reader.read_data()

        """
        try:
            log_message(
                "info",
                f"Creating JSON reader for file: {file_path}")
            return PandasJsonReader(
                file_path=file_path,
                storage_options=storage_options)
        except Exception as e:
            error_message = (
                f"Failed to create JSON reader for file: {file_path} - {e}"
            )
            log_message(
                "error",
                error_message)
            raise Exception(error_message) from e

    def avro_reader(
        self,
        file_path: str,
        storage_options: Optional[Dict[str, Any]] = None
    ) -> DataReader:
        """
        Create an Avro reader.

        Args:
            file_path (str): Path to the Avro file.
            storage_options (dict, optional): Configuration for remote storage.
            Defaults to None.

        Returns:
            PandasAvroReader: Instance of the Avro reader.

        Raises:
            Exception: If the reader instantiation fails.

        Example Usage:
        from my_module import PandasReaderFactory
        factory = PandasReaderFactory()
        avro_reader = factory.avro_reader("/dbfs/mnt/data/data.avro")
        data = avro_reader.read_data()

        """
        try:
            log_message(
                "info",
                f"Creating Avro reader for file: {file_path}")
            return PandasAvroReader(
                file_path=file_path,
                storage_options=storage_options)
        except Exception as e:
            error_message = (
                f"Failed to create Avro reader for file: {file_path} - {e}"
            )
            log_message(
                "error",
                error_message)
            raise Exception(error_message) from e

    def parquet_reader(
        self,
        file_path: str,
        storage_options: Optional[Dict[str, Any]] = None
    ) -> DataReader:
        """
        Create a Parquet reader.

        Args:
            file_path (str): Path to the Parquet file.
            storage_options (dict, optional): Configuration for remote storage.
            Defaults to None.

        Returns:
            PandasParquetReader: Instance of the Parquet reader.

        Raises:
            Exception: If the reader instantiation fails.

        Example Usage:
        from my_module import PandasReaderFactory
        factory = PandasReaderFactory()
        parquet_reader = factory.parquet_reader("/dbfs/mnt/data/data.parquet")
        data = parquet_reader.read_data()

        """
        try:
            log_message(
                "info",
                f"Creating Parquet reader for file: {file_path}")
            return PandasParquetReader(
                file_path=file_path,
                storage_options=storage_options)
        except Exception as e:
            error_message = (
                f"Failed to create Parquet reader for file: {file_path} - {e}"
            )
            log_message(
                "error",
                error_message)
            raise Exception(error_message) from e


class PandasCloudReaderProvider(ReaderProvider):
    """
    Provider class for creating Pandas readers based on data type.

    This class facilitates the creation of specific Pandas-based readers
    (CSV, JSON, Avro, Parquet) by using the provided factory, data type,
    and connector. It dynamically resolves file paths and applies storage
    options for cloud-based storage.

    Attributes:
        factory (PandasReaderFactory): Factory instance for creating
            data readers.
        data_type (DataType): Data type for the reader
            (e.g., CSV, JSON, Avro, Parquet).
        connector (CloudConnector): Connector instance for resolving
            file paths and storage options.
        framework (str): Framework identifier (Pandas in this case).
        __storage_options (dict): Storage options resolved from the connector.

    Example Usage:
    ```python
        from my_cloud_connector import MyCloudConnector
        from my_data_type import DataType
        from my_pandas_reader_factory import PandasReaderFactory
        from my_pandas_reader_provider import PandasCloudReaderProvider

        connector = MyCloudConnector()
        factory = PandasReaderFactory()
        provider = PandasCloudReaderProvider(factory, DataType.CSV, connector)

        # Create a CSV reader
        reader = provider.create_reader("my_storage", "data.csv")
        data = reader.read_data()
    """

    def __init__(
        self,
        factory: PandasReaderFactory,
        data_type: DataType,
        connector: CloudConnector
    ):
        """
        Initialize the PandasCloudReaderProvider.

        Args:
            factory (PandasReaderFactory): Factory instance for
                creating data readers.
            data_type (DataType): Data type for the reader
                (e.g., CSV, JSON, Avro, Parquet).
            connector (CloudConnector): Connector instance for resolving
                file paths and storage options.
        """
        PandasValidationUtils.validate_inheritance(
            factory,
            ReaderFactory,
            'factory')
        PandasValidationUtils.validate_instance(
            data_type,
            DataType,
            "data_type")
        PandasValidationUtils.validate_inheritance(
            connector,
            CloudConnector,
            "connector")
        super().__init__(
            factory,
            data_type,
            connector)
        self.framework = Framework.PANDAS.value
        PandasValidationUtils.validate_is_non_empty_string(
            self.framework)
        self.__storage_options = self.connector.get_framework_config(
            self.framework)
        PandasValidationUtils.validate_is_non_empty_dict(
            self.__storage_options)
        PandasValidationUtils.log_init_arguments(self)

    def create_reader(
        self,
        storage_unit: str,
        object_name: str
    ):
        """
        Create a reader for Pandas using the data type, file identifier,
        and storage options.

        Args:
            storage_unit (str): The storage unit/container name.
            object_name (str): The name of the object/file to be read.

        Returns:
            DataReader: An instance of the appropriate Pandas reader for
            the specified data type.

        Raises:
            ValueError: If the specified data type is not supported.
            Exception: If any error occurs during the reader creation process.

        Example Usage:
        from my_module import PandasReaderFactory
        from my_module import PandasCloudReaderProvider
        from my_data_type import DataType
        from my_cloud_connector import MyCloudConnector

        connector = MyCloudConnector()
        factory = PandasReaderFactory()
        provider = PandasCloudReaderProvider(factory, DataType.CSV, connector)
        reader = provider.create_reader("my_storage", "data.csv")

        """
        try:
            # Resolve file path using the connector
            log_message(
                "info",
                f"Resolving file path for object: "
                f"{object_name} in storage unit: {storage_unit}",
            )
            file_path = self.connector.get_file_path(
                storage_unit, object_name, framework=self.framework
            )

            log_message(
                "info",
                f"Creating Pandas reader for file: "
                f"{file_path} with data type: {self.data_type.value}"
            )

            # Use the factory to create the appropriate reader
            match self.data_type:
                case DataType.CSV:
                    return self.factory.csv_reader(
                        file_path=file_path,
                        storage_options=self.__storage_options
                    )
                case DataType.JSON:
                    return self.factory.json_reader(
                        file_path=file_path,
                        storage_options=self.__storage_options
                    )
                case DataType.AVRO:
                    return self.factory.avro_reader(
                        file_path=file_path,
                        storage_options=self.__storage_options
                    )
                case DataType.PARQUET:
                    return self.factory.parquet_reader(
                        file_path=file_path,
                        storage_options=self.__storage_options
                    )
                case _:
                    error_message = (
                        "Unsupported data type: " +
                        f"{self.data_type.value} for file: " +
                        f"{file_path}"
                    )
                    log_message(
                        "error",
                        error_message
                    )
                    raise ValueError(error_message)

        except Exception as e:
            error_message = (
                "Failed to create Pandas reader for object: " +
                f"{object_name} - {e}"
            )
            log_message(
                "error",
                error_message)
            raise Exception(error_message) from e


class PandasLocalReaderProvider(ReaderProvider):
    """
    Provider class for creating Pandas readers for local files.

    This class facilitates the creation of specific Pandas-based readers
    (CSV, JSON, Avro, Parquet)
    using the provided factory and data type. It is designed specifically
    for local files and
    does not rely on cloud-specific connectors or storage options.

    Attributes:
        factory (PandasReaderFactory): Factory instance for creating
            data readers.
        data_type (DataType): Data type for the reader
            (e.g., CSV, JSON, Avro, Parquet).
        framework (str): Framework identifier (Pandas in this case).

    Example Usage:
    ```python
    from my_data_type import DataType
    from my_pandas_reader_factory import PandasReaderFactory
    from my_pandas_reader_provider import PandasLocalReaderProvider

        factory = PandasReaderFactory()
        provider = PandasLocalReaderProvider(factory, DataType.CSV)

        # Create a CSV reader
        reader = provider.create_reader("path/to/local/data.csv")
        data = reader.read_data()
    """

    def __init__(
        self,
        factory: PandasReaderFactory,
        data_type: DataType
    ):
        """
        Initialize the PandasLocalReaderProvider.

        Args:
            factory (PandasReaderFactory): Factory instance for creating
                data readers.
            data_type (DataType): Data type for the reader
                (e.g., CSV, JSON, Avro, Parquet).
        """
        PandasValidationUtils.validate_instance(
            factory,
            PandasReaderFactory,
            'factory')
        PandasValidationUtils.validate_instance(
            data_type,
            DataType,
            'data_type')
        self.factory = factory
        self.data_type = data_type
        self.framework = Framework.PANDAS.value
        PandasValidationUtils.validate_is_non_empty_string(
            self.framework)
        PandasValidationUtils.log_init_arguments(self)

    def create_reader(self, file_path: str):
        """
        Create a reader for Pandas using the data type and file path.

        Args:
            file_path (str): The path to the local file.

        Returns:
            DataReader: An instance of the appropriate Pandas reader for the
            specified data type.

        Raises:
            ValueError: If the specified data type is not supported.
            Exception: If any error occurs during the reader creation process.

        Example Usage:
        from my_module import PandasReaderFactory
        from my_module import PandasLocalReaderProvider
        from my_data_type import DataType

        factory = PandasReaderFactory()
        provider = PandasLocalReaderProvider(factory, DataType.CSV)
        reader = provider.create_reader("path/to/local/data.csv")
        """
        try:
            log_message(
                "info",
                f"Creating Pandas reader for file: "
                f"{file_path} with data type: {self.data_type.value}"
            )

            # Use the factory to create the appropriate reader
            match self.data_type:
                case DataType.CSV:
                    return self.factory.csv_reader(file_path=file_path)
                case DataType.JSON:
                    return self.factory.json_reader(file_path=file_path)
                case DataType.AVRO:
                    return self.factory.avro_reader(file_path=file_path)
                case DataType.PARQUET:
                    return self.factory.parquet_reader(file_path=file_path)
                case _:
                    error_message = (
                        "Unsupported data type: " +
                        f"{self.data_type.value} for file: " +
                        f"{file_path}"
                    )
                    log_message(
                        "error",
                        "Unsupported data type: ",
                        error_message)
                    raise ValueError(error_message)

        except Exception as e:
            error_message = (
                "Failed to create Pandas reader for file: " +
                f"{file_path} - {e}"
            )
            log_message(
                "error",
                error_message)
            raise Exception(error_message) from e


class PandasParquetSaver(DataSaver):
    """
    Saver class for Parquet files using Pandas.

    This class provides functionality to save Pandas DataFrames as
    Parquet files,
    with support for dynamic method application and cloud storage options.

    Attributes:
            data (pd.DataFrame): Pandas DataFrame to save.
            file_path (str): Path to save the Parquet file.
            storage_options (dict): Storage configuration for reading files from
                cloud or remote locations. Defaults to an empty dictionary.

    Example Usage:
        # Saving a DataFrame to a Parquet file
        saver = PandasParquetSaver(
            data,
            "/dbfs/mnt/data/data.parquet",
            storage_options={
                "account_name": "my_account", "account_key": "my_key"})
        saver.save_data()
    """

    def __init__(
        self,
        data: pd.DataFrame,
        file_path: str,
        storage_options: Optional[Dict[str, Any]] = {}
    ):
        """
        Initialize the PandasParquetSaver with the file path and data to save.

        Args:
            data (pd.DataFrame): Pandas DataFrame to save.
            file_path (str): Path to save the Parquet file.
            storage_options (dict): Storage configuration for reading files from
                cloud or remote locations. Defaults to None.
        """
        PandasValidationUtils.validate_is_non_empty_string(
            file_path)
        PandasValidationUtils.validate_is_dataframe(
            data,
            'data')
        super().__init__(file_path)
        self.data = data
        PandasValidationUtils.log_init_arguments(self)
        if storage_options:
            PandasValidationUtils.validate_is_non_empty_dict(
                storage_options
            )
        self.storage_options = storage_options

    def save_data(
        self,
        **kwargs
    ):
        """
        Save a Pandas DataFrame to a Parquet file with dynamically
        applied options.

        Args:
            **kwargs: Additional options for Pandas' `to_parquet` method.

        Raises:
            ValueError: If the DataFrame is empty or invalid.
            Exception: For any unexpected errors during the saving process.

        Example Usage:
        # Saving a DataFrame to a Parquet file from cloud
            saver = PandasParquetSaver(data, "/dbfs/mnt/data/data.parquet")
            saver.save_data(
                storage_options={
                    "account_name": "my_account", "account_key": "my_key"})
        # Saving a DataFrame to a Parquet file locally
            saver = PandasParquetSaver(data, "/path/to/local/data.parquet")
            saver.save_data()

        """
        try:
            log_message(
                "info",
                f"Attempting to save DataFrame to Parquet at {self.file_path}")

            # Validate if the DataFrame is not empty
            if self.data.empty:
                raise ValueError("Cannot save an empty DataFrame to Parquet.")

            if kwargs:
                validate_kwargs(
                    self.data.to_parquet,
                    kwargs)
            self.data.to_parquet(
                self.file_path,
                storage_options=self.storage_options,
                **kwargs)
            log_message(
                "info",
                f"Successfully saved Parquet file to {self.file_path}")

        except ValueError as e:
            error_message = (
                f"ValueError while saving Parquet file: {e}"
            )
            log_message(
                "error",
                error_message)
            raise ValueError(error_message) from e

        except Exception as e:
            error_message = (
                f"Unexpected error while saving Parquet file: {e}"
            )
            log_message(
                "error",
                error_message)
            raise Exception(error_message) from e


class PandasJsonSaver(DataSaver):
    """
    Saver class for JSON files using Pandas.

    This class provides functionality to save Pandas DataFrames as JSON files,
    with support for dynamic method application and optional cloud storage
    configurations.

    Attributes:
        file_path (str): Path to save the JSON file.
        data (pd.DataFrame): DataFrame to save as a JSON file.

    Example Usage:
        # Saving a DataFrame to a JSON file
        saver = PandasJsonSaver(
            data,
            "/dbfs/mnt/data/data.json",
            storage_options={
                "account_name": "my_account", "account_key": "my_key"}
                )
        saver.save_data()
    """

    def __init__(
        self,
        data: pd.DataFrame,
        file_path: str,
        storage_options: Optional[Dict[str, Any]] = {}
    ):
        """
        Initialize the PandasJsonSaver with the file path and data to save.

        Args:
            data (pd.DataFrame): Pandas DataFrame to save.
            file_path (str): Path to save the JSON file.
            storage_options (dict): Storage configuration for reading files from
                cloud or remote locations. Defaults to an empty dictionary.
        """
        PandasValidationUtils.validate_is_non_empty_string(
            file_path)
        PandasValidationUtils.validate_is_dataframe(
            data,
            'data')
        super().__init__(file_path)
        self.data = data
        if storage_options:
            PandasValidationUtils.validate_is_non_empty_dict(
                storage_options)
        self.storage_options = storage_options
        PandasValidationUtils.log_init_arguments(self)

    def save_data(
        self,
        **kwargs
    ):
        """
        Save a Pandas DataFrame to a JSON file with dynamically applied
        options.

        Args:
            **kwargs: Additional options for Pandas' `to_json` method.

        Raises:
            ValueError: If the DataFrame is empty or invalid.
            Exception: For any unexpected errors during the saving process.

        Example Usage:
            # Saving a DataFrame to a JSON file
            saver = PandasJsonSaver(data, "/dbfs/mnt/data/data.json")

            saver.save_data(storage_options={
                "account_name": "my_account", "account_key": "my_key"})

            # Saving a DataFrame to a JSON file with additional options
                saver.save_data(orient='records', default_handler=str)

            # Saving a DataFrame to a local file
                saver.save_data(path='/local/path/data.json')

        """
        try:
            log_message(
                "info",
                f"Attempting to save DataFrame to JSON at {self.file_path}")

            # Validate if the DataFrame is not empty
            if self.data.empty:
                raise ValueError("Cannot save an empty DataFrame to JSON.")


            if kwargs:
                validate_kwargs(
                    self.data.to_json,
                    kwargs)
            self.data.to_json(
                self.file_path,
                storage_options=self.storage_options,
                **kwargs
                )

            log_message(
                "info",
                f"Successfully saved JSON file to {self.file_path}")

        except ValueError as e:
            error_message = (
                f"ValueError while saving JSON file: {e}"
            )
            log_message(
                "error",
                error_message)
            raise ValueError(error_message) from e

        except Exception as e:
            error_message = (
                f"Unexpected error while saving JSON file: {e}"
            )
            log_message(
                "error",
                error_message)
            raise Exception(error_message) from e


class PandasCsvSaver(DataSaver):
    """
    Saver class for CSV files using Pandas.

    This class provides functionality to save Pandas DataFrames as CSV files,
    with support for dynamic method application and optional cloud
    storage configurations.

    Attributes:
            data (pd.DataFrame): Pandas DataFrame to save.
            file_path (str): Path to save the CSV file.
            storage_options (dict): Storage configuration for reading files from
                cloud or remote locations. Defaults to None.

    Example Usage:
        # Saving a DataFrame to a CSV file
        saver = PandasCsvSaver(
            data,
            "/dbfs/mnt/data/data.csv",
            storage_options={
                "account_name": "my_account", "account_key": "my_key"}
                )
        saver.save_data()
    """

    def __init__(
        self,
        data: pd.DataFrame,
        file_path: str,
        storage_options: Optional[Dict[str, Any]] = {}
    ):
        """
        Initialize the PandasCsvSaver with the file path and data to save.

        Args:
            data (pd.DataFrame): Pandas DataFrame to save.
            file_path (str): Path to save the CSV file.
            storage_options (dict): Storage configuration for reading files from
                cloud or remote locations. Defaults to None.
        """
        PandasValidationUtils.validate_is_non_empty_string(
            file_path)
        PandasValidationUtils.validate_is_dataframe(
            data,
            'data')
        super().__init__(file_path)
        self.data = data
        if storage_options:
            PandasValidationUtils.validate_is_non_empty_dict(
                storage_options
            )
        self.storage_options = storage_options
        PandasValidationUtils.log_init_arguments(self)

    def save_data(
        self,
        **kwargs
    ):
        """
        Save a Pandas DataFrame to a CSV file with dynamically applied options.

        Args:
            **kwargs: Additional options for Pandas' `to_csv` method.

        Raises:
            ValueError: If the DataFrame is empty or invalid.
            Exception: For any unexpected errors during the saving process.

        Example Usage:
        # Saving a DataFrame to a CSV file
        saver = PandasCsvSaver(data, "/dbfs/mnt/data/data.csv")

        saver.save_data(storage_options={
            "account_name": "my_account", "account_key": "my_key"})

        # Saving a DataFrame to a CSV file with additional options
        saver.save_data(index=False)

        # Saving a DataFrame to a local file
        saver.save_data(path='/local/path/data.csv')
        """
        try:
            log_message(
                "info",
                f"Attempting to save DataFrame to CSV at {self.file_path}")

            # Validate if the DataFrame is not empty
            if self.data.empty:
                raise ValueError("Cannot save an empty DataFrame to CSV.")
            if kwargs:
                validate_kwargs(self.data.to_csv, kwargs)
            self.data.to_csv(
                self.file_path,
                storage_options=self.storage_options,
                **kwargs
            )

            log_message(
                "info",
                f"Successfully saved CSV file to {self.file_path}")

        except ValueError as e:
            error_message = (
                f"ValueError while saving CSV file: {e}"
            )
            log_message(
                "error",
                error_message)
            raise ValueError(error_message) from e

        except Exception as e:
            error_message = (
                f"Unexpected error while saving CSV file: {e}"
            )
            log_message(
                "error",
                error_message)
            raise Exception(error_message) from e


class PandasAvroSaver(DataSaver):
    """
    Saver class for Avro files using Pandas.

    This class provides functionality to save Pandas DataFrames as Avro
    files, with support for cloud storage configurations and dynamic
    schema generation.

    Attributes:
            data (pd.DataFrame): Pandas DataFrame to save.
            file_path (str): Path to save the AVRO file.
            storage_options (dict): Storage configuration for reading files from
                cloud or remote locations. Defaults to None.

    Example Usage:
        # Saving a DataFrame to an Avro file
        saver = PandasAvroSaver(
            data,
            "/dbfs/mnt/data/data.avro",
            storage_options={
                "account_name": "my_account", "account_key": "my_key"}
                )
        saver.save_data()
    """

    def __init__(
        self,
        data: pd.DataFrame,
        file_path: str,
        storage_options: Optional[Dict[str, Any]] = {}
    ):
        """
        Initialize the PandasAvroSaver with the file path, data,
        and storage options.

        Args:
            data (pd.DataFrame): Pandas DataFrame to save.
            file_path (str): Path to save the AVRO file.
            storage_options (dict): Storage configuration for reading files from
                cloud or remote locations. Defaults to None.
        """
        PandasValidationUtils.validate_is_non_empty_string(
            file_path)
        PandasValidationUtils.validate_is_dataframe(
            data,
            'data')
        super().__init__(file_path)
        self.data = data
        if storage_options:
            PandasValidationUtils.validate_is_non_empty_dict(
                storage_options
            )
        self.storage_options = storage_options
        PandasValidationUtils.log_init_arguments(self)

    def save_data(
        self,
        **kwargs
    ):
        """
        Save a Pandas DataFrame to an Avro file.

        Args:
            **kwargs: Additional options for `fastavro.writer`.

        Raises:
            ValueError: If the DataFrame is empty or invalid.
            Exception: For any unexpected errors during the saving process.

        Example Usage:
        # Saving a DataFrame to an Avro file
        saver = PandasAvroSaver(data, "/dbfs/mnt/data/data.avro")

        saver.save_data(storage_options={
            "account_name": "my_account", "account_key": "my_key"})

        # Saving a DataFrame to an Avro file with additional options
        saver.save_data(compression="gzip")

        # Saving a DataFrame to a local file
        saver.save_data(path='/local/path/data.avro')

        """
        try:
            log_message(
                "info",
                f"Attempting to save DataFrame to Avro at {self.file_path}")

            # Validate if the DataFrame is not empty
            if self.data.empty:
                raise ValueError("Cannot save an empty DataFrame to Avro.")

            records = self.data.to_dict(orient="records")

            # Generate Avro Schema
            schema = self.generate_schema(self.data)

            # Use provided storage options or default
            effective_storage_options = self.storage_options

            # Save the records to the Avro file
            from fastavro import writer
            import fsspec
            with fsspec.open(
                self.file_path,
                "wb",
                **effective_storage_options,
                **kwargs
            ) as out_file:
                writer(out_file, schema, records)

            log_message(
                "info",
                f"Successfully saved Avro file to {self.file_path}")

        except ValueError as e:
            error_message = (
                f"ValueError while saving Avro file: {e}"
            )
            log_message(
                "error",
                error_message)
            raise ValueError(error_message) from e

        except Exception as e:
            error_message = (
                f"Unexpected error while saving Avro file: {e}"
            )
            log_message(
                "error",
                error_message)
            raise Exception(error_message) from e

    def generate_schema(
        self,
        data: pd.DataFrame
    ) -> dict:
        """
        Generate an Avro schema based on the Pandas DataFrame's columns
        and data types.

        Args:
            data (pd.DataFrame): Pandas DataFrame to infer schema from.

        Returns:
            dict: Avro schema as a dictionary.

        Raises:
            ValueError: If the schema cannot be generated.
        """
        log_message(
            "info",
            "Generating Avro schema for DataFrame")

        try:
            PANDAS_TO_AVRO_TYPE = {
                "int64": "long",
                "int32": "int",
                "float64": "double",
                "float32": "float",
                "object": "string",
                "bool": "boolean",
                "datetime64[ns]": {
                    "type": "long", "logicalType": "timestamp-millis"},
                "datetime64[ns, UTC]": {
                    "type": "long", "logicalType": "timestamp-millis"},
                "category": "string",
                "timedelta64[ns]": {"type": "long", "logicalType": "duration"},
                "Int64": ["null", "long"],
                "Float64": ["null", "double"],
                "boolean": ["null", "boolean"]
            }

            # Generate schema fields based on DataFrame columns and types
            fields = [
                {
                    "name": col,
                    "type": PANDAS_TO_AVRO_TYPE.get(str(dtype), "string")}
                for col, dtype in data.dtypes.items()
            ]

            # Create the Avro schema
            schema = {
                "type": "record",
                "name": "PandasRecord",
                "fields": fields,
            }

            log_message(
                "info",
                "Successfully generated Avro schema")
            return schema

        except Exception as e:
            error_message = (
                f"Unexpected error while generating Avro schema: {e}"
            )
            log_message(
                "error",
                error_message)
            raise Exception(error_message) from e


class PandasSaverFactory(SaverFactory):
    """
    Factory class for creating Pandas-based savers.

    This class provides methods to instantiate concrete Pandas savers
    for various file formats, such as CSV, JSON, Avro, and Parquet.

    Methods:
        csv_saver(file_path, data): Creates a saver for CSV files.
        json_saver(file_path, data): Creates a saver for JSON files.
        avro_saver(file_path, data): Creates a saver for Avro files.
        parquet_saver(file_path, data): Creates a saver for Parquet files.

    Example Usage:
        from my_module import PandasSaverFactory

        # Creating a Pandas saver factory
            factory = PandasSaverFactory()

        # Creating a CSV saver
            csv_saver = factory.csv_saver(
                "/dbfs/mnt/data/output.csv", dataframe)
            csv_saver.save_data()
    """

    def csv_saver(
        self,
        data: pd.DataFrame,
        file_path: str,
        storage_options: Optional[Dict[str, Any]] = {}
    ) -> DataSaver:
        """
        Create a CSV saver.

        Args:
            file_path (str): Path to save the CSV file.
            data (pd.DataFrame): DataFrame to be saved.

        Returns:
            PandasCsvSaver: An instance of the CSV saver.

        Example Usage:
            from my_module import PandasSaverFactory
            saver = factory.csv_saver("/dbfs/mnt/data/output.csv", dataframe)
            saver.save_data()

        """
        logger = get_logger()
        try:
            logger.log(
                "info",
                f"Creating CSV saver for file: {file_path}")
            return PandasCsvSaver(
                data=data,
                file_path=file_path,
                storage_options=storage_options)
        except Exception as e:
            error_message = (
                "Error creating CSV saver: {e}"
            )
            logger.log(
                "error",
                error_message)
            raise Exception(error_message) from e

    def json_saver(
        self,
        data: pd.DataFrame,
        file_path: str,
        storage_options: Optional[Dict[str, Any]] = {}
    ) -> DataSaver:
        """
        Create a JSON saver.

        Args:
            file_path (str): Path to save the JSON file.
            data (pd.DataFrame): DataFrame to be saved.

        Returns:
            PandasJsonSaver: An instance of the JSON saver.

        Example Usage:
            from my_module import PandasSaverFactory
        # Create a Pandas saver factory
            saver = factory.json_saver("/dbfs/mnt/data/output.json", dataframe)
            saver.save_data()

        """
        logger = get_logger()
        try:
            logger.log(
                "info",
                f"Creating JSON saver for file: {file_path}")
            return PandasJsonSaver(
                data=data,
                file_path=file_path,
                storage_options=storage_options)
        except Exception as e:
            error_message = (
                "Error creating JSON saver: {e}"
            )
            logger.log(
                "error",
                error_message)
            raise Exception(error_message) from e

    def avro_saver(
        self,
        data: pd.DataFrame,
        file_path: str,
        storage_options: Optional[Dict[str, Any]] = {}
    ) -> DataSaver:
        """
        Create an Avro saver.

        Args:
            file_path (str): Path to save the Avro file.
            data (pd.DataFrame): DataFrame to be saved.

        Returns:
            PandasAvroSaver: An instance of the Avro saver.

        Example Usage:
            from my_module import PandasSaverFactory

        # Create a Pandas saver factory
            factory = PandasSaverFactory()
        # Creating a avro saver
            saver = factory.avro_saver("/dbfs/mnt/data/output.avro", dataframe)
            saver.save_data()

        """
        logger = get_logger()
        try:
            logger.log(
                "info",
                f"Creating Avro saver for file: {file_path}")
            return PandasAvroSaver(
                data=data,
                file_path=file_path,
                storage_options=storage_options)
        except Exception as e:
            error_message = (
                "Error creating Avro saver: {e}"
            )
            logger.log(
                "error",
                f"Error creating Avro saver: {e}")
            raise Exception(error_message) from e

    def parquet_saver(
        self,
        data: pd.DataFrame,
        file_path: str,
        storage_options: Optional[Dict[str, Any]] = {}
    ) -> DataSaver:
        """
        Create a Parquet saver.

        Args:
            file_path (str): Path to save the Parquet file.
            data (pd.DataFrame): DataFrame to be saved.

        Returns:
            PandasParquetSaver: An instance of the Parquet saver.

        Example Usage:
            from my_module import PandasSaverFactory
            # Create a Pandas saver factory
                factory = PandasSaverFactory()
            # Creating a Parquet saver
                saver = factory.parquet_saver(
                    "/dbfs/mnt/data/output.parquet", dataframe)
                saver.save_data()
        """
        logger = get_logger()
        try:
            logger.log(
                "info",
                f"Creating Parquet saver for file: {file_path}")
            return PandasParquetSaver(
                data=data,
                file_path=file_path,
                storage_options=storage_options)
        except Exception as e:
            error_message = (
                "Error creating Parquet saver: {e}"
            )
            logger.log(
                "error",
                error_message)
            raise Exception(error_message) from e


class PandasCloudSaverProvider(SaverProvider):
    """
    Provider class for creating Pandas-based savers dynamically.

    This class facilitates the creation of specific Pandas-based savers
    (CSV, JSON, Avro, Parquet) by using the provided factory, data type,
    and connector. It dynamically resolves file paths and applies
    storage options for cloud-based storage.

    Attributes:
        factory (PandasSaverFactory): Factory instance for creating data
        savers.
        data_type (DataType): Data type for the saver
            (e.g., CSV, JSON, Avro, Parquet).
        connector (CloudConnector): Connector instance for resolving file
            paths and storage options.
        framework (str): Framework identifier (Pandas in this case).
        __storage_options (dict): Storage options resolved from the connector.

    Example Usage:
    from my_module import MyCloudConnector, PandasSaverFactory, DataType
        connector = MyCloudConnector()
        factory = PandasSaverFactory()
        provider = PandasCloudSaverProvider(factory, connector)

        # Create a CSV saver
        saver = provider.create_saver(
            data, "my_storage", "output.csv", DataType.CSV)
        saver.save_data(index=False)
    """

    def __init__(
        self,
        factory: PandasSaverFactory,
        connector: CloudConnector
    ):
        """
        Initialize the PandasCloudSaverProvider.

        Args:
            factory (PandasSaverFactory): Factory instance for creating data
            savers.
            connector (CloudConnector): Connector instance for resolving file
                paths and storage options.
        """
        PandasValidationUtils.validate_inheritance(
            factory, SaverFactory,
            'factory')
        PandasValidationUtils.validate_inheritance(
            connector, CloudConnector,
            'connector')

        super().__init__(factory, connector)

        self.framework = Framework.PANDAS.value

        PandasValidationUtils.validate_is_non_empty_string(
            self.framework)
        self.__storage_options = self.connector.get_framework_config(
            self.framework)
        PandasValidationUtils.validate_is_non_empty_dict(
            self.__storage_options)

    def create_saver(
        self,
        data: pd.DataFrame,
        storage_unit: str,
        object_name: str,
        data_type: DataType,
    ):
        """
        Create a saver for Pandas using the data type, file identifier, and
        storage options.

        Args:
            data (pd.DataFrame): DataFrame to be saved.
            storage_unit (str): The storage unit/container name.
            object_name (str): The name of the object/file to be saved.
            data_type (DataType): Data type for the saver
            (e.g., CSV, JSON, Avro, Parquet).

        Returns:
            DataSaver: An instance of the appropriate Pandas saver for the
            specified data type.

        Raises:
            ValueError: If the specified data type is not supported.
            Exception: If any error occurs during the saver creation process.

        Example Usage:
            from my_module import (
                MyCloudConnector, PandasSaverFactory, DataType)

            connector = MyCloudConnector()
            factory = PandasSaverFactory()
            provider = PandasCloudSaverProvider(factory, connector)
            # Create a CSV saver
                saver = provider.create_saver(
                    data, "my_storage", "output.csv", DataType.CSV)
                saver.save_data(index=False)
        """
        PandasValidationUtils.validate_is_non_empty_string(
            storage_unit)
        PandasValidationUtils.validate_is_non_empty_string(
            object_name)
        PandasValidationUtils.validate_instance(
            data_type,
            DataType,
            "data_type")
        self.data_type = data_type
        try:
            # Resolve file path using the connector
            log_message(
                "info",
                f"Resolving file path for object: {object_name} "
                f"in storage unit: {storage_unit}"
            )
            file_path = self.connector.get_file_path(
                storage_unit, object_name, framework=self.framework
            )

            log_message(
                "info",
                f"Creating Pandas saver for file: {file_path} "
                f"with data type: {self.data_type.value}"
            )

            # Use the factory to create the appropriate saver
            match self.data_type:
                case DataType.CSV:
                    return self.factory.csv_saver(
                        data=data,
                        file_path=file_path,
                        storage_options=self.__storage_options
                    )
                case DataType.JSON:
                    return self.factory.json_saver(
                        data=data,
                        file_path=file_path,
                        storage_options=self.__storage_options
                    )
                case DataType.AVRO:
                    return self.factory.avro_saver(
                        data=data,
                        file_path=file_path,
                        storage_options=self.__storage_options
                    )
                case DataType.PARQUET:
                    return self.factory.parquet_saver(
                        data=data,
                        file_path=file_path,
                        storage_options=self.__storage_options
                    )
                case _:
                    error_message = (
                        f"Unsupported data type: {self.data_type.value} " +
                        f"for file: {file_path}"
                    )
                    log_message(
                        "error",
                        error_message)
                    raise ValueError(error_message)

        except Exception as e:
            error_message = (
                f"Failed to create Pandas saver for object: {object_name} " +
                f"- {e}"
            )
            log_message(
                "error",
                error_message)
            raise Exception(error_message) from e


class PandasLocalSaverProvider(SaverProvider):
    """
    Provider class for creating Pandas-based savers for local files.

    This class facilitates the creation of specific Pandas-based savers
    (CSV, JSON, Avro, Parquet) using the provided factory and data type.
    It is designed specifically for local files and does not rely on
    cloud-specific connectors or storage options.

    Attributes:
        factory (PandasSaverFactory): Factory instance for creating
            data savers.
        data_type (DataType): Data type for the saver
            (e.g., CSV, JSON, Avro, Parquet).
        framework (str): Framework identifier (Pandas in this case).

    Example Usage:
    from my_module import PandasSaverFactory, DataType
        factory = PandasSaverFactory()
        provider = PandasLocalSaverProvider(factory, DataType.CSV)

        # Create a CSV saver
        saver = provider.create_saver("output.csv", data)
        saver.save_data(index=False)
    """

    def __init__(
        self,
        factory: PandasSaverFactory
    ):
        """
        Initialize the PandasLocalSaverProvider.

        Args:
            factory (PandasSaverFactory): Factory instance for creating
                data savers.
                (e.g., CSV, JSON, Avro, Parquet).
        """
        PandasValidationUtils.validate_instance(
            factory,
            SaverFactory, "factory")
        self.factory = factory
        self.framework = Framework.PANDAS.value
        PandasValidationUtils.validate_is_non_empty_string(
            self.framework)
        PandasValidationUtils.log_init_arguments(self)

    def create_saver(
        self,
        data: pd.DataFrame,
        file_path: str,
        data_type: DataType
    ):
        """
        Create a saver for Pandas using the data type and file path.

        Args:
            data (pd.DataFrame): DataFrame to be saved.
            file_path (str): The path to the local file to save the data.
            data_type (DataType): Data type for the saver

        Returns:
            DataSaver: An instance of the appropriate Pandas saver for the
            specified data type.

        Raises:
            ValueError: If the specified data type is not supported.
            Exception: If any error occurs during the saver creation process.

        Example Usage:
            from my_module import PandasSaverFactory, DataType

            factory = PandasSaverFactory()
            provider = PandasLocalSaverProvider(factory)
            # Create a CSV saver
                saver = provider.create_saver(data, "output.csv", DataType.CSV)
                saver.save_data(index=False)
        """
        PandasValidationUtils.validate_is_non_empty_string(
            file_path)
        PandasValidationUtils.validate_is_dataframe(
            data,
            "data")
        PandasValidationUtils.validate_instance(
            data_type,
            DataType,
            "data_type")
        self.data_type = data_type
        try:
            log_message(
                "info",
                f"Creating Pandas saver for file: "
                f"{file_path} with data type: {self.data_type.value}"
            )

            # Use the factory to create the appropriate saver
            match self.data_type:
                case DataType.CSV:
                    return self.factory.csv_saver(
                        data=data,
                        file_path=file_path)
                case DataType.JSON:
                    return self.factory.json_saver(
                        data=data,
                        file_path=file_path)
                case DataType.AVRO:
                    return self.factory.avro_saver(
                        data=data,
                        file_path=file_path)
                case DataType.PARQUET:
                    return self.factory.parquet_saver(
                        data=data,
                        file_path=file_path)
                case _:
                    error_message = (
                        f"Unsupported data type: {self.data_type.value} " +
                        f"for file: {file_path}"
                    )
                    log_message(
                        "error",
                        error_message)
                    raise ValueError(error_message)

        except Exception as e:
            error_message = (
                f"Failed to create Pandas saver for file: {file_path} - {e}"
            )
            log_message(
                "error",
                error_message)
            raise Exception(error_message) from e


class PandasDBConnector(DBConnector):
    """
    Implementation of DBConnector for SQL Server using pyodbc and Pandas.

    Features:
        - Retry logic for connections.
        - Fetches query results as Pandas DataFrames.
        - Executes parameterized queries safely.
        - Supports automatic disconnection using a context manager.

    Example Usage:
        # Example of usage with a context manager
        with PandasDBConnector(
            host="myserver.database.windows.net",
            database="mydb",
            user="admin",
            password="password",
            driver="{ODBC Driver 17 for SQL Server}"
        ) as connector:
            # Fetch DataFrame
            query = "SELECT * FROM my_table WHERE id = ?"
            data = connector.fetch_data(query, params=(1,))
            print(data)

            # Execute query
            insert_query = "INSERT INTO my_table (id, name) VALUES (?, ?)"
            connector.execute_query(insert_query, params=(2, "New User"))
    """

    def __init__(
        self,
        host: str,
        database: str,
        user: str,
        password: str,
        driver="{SQL Server}",
        retries: int = 3
    ):
        """
        Initialize the PandasDBConnector.

        Args:
            host (str): Database server hostname or IP address.
            database (str): Name of the database.
            user (str): Username for authentication.
            password (str): Password for authentication.
            driver (str): ODBC driver for the database.
            `Defaults to "{SQL Server}".
            retries (int): Number of retry attempts for connection.
                Defaults to 3.
        """
        PandasValidationUtils.validate_is_non_empty_string(
            host)
        PandasValidationUtils.validate_is_non_empty_string(
            database)
        PandasValidationUtils.validate_is_non_empty_string(
            user)
        PandasValidationUtils.validate_is_non_empty_string(
            password)
        PandasValidationUtils.validate_is_non_empty_string(
            driver)
        PandasValidationUtils.validate_is_integer(
            retries,
            'retries')
        super().__init__(
            host,
            database,
            user,
            password)
        self.driver = driver
        self.retries = retries
        PandasValidationUtils.log_init_arguments(self)

    def connect(self):
        """
        Establish a connection to the database with retry logic.

        Raises:
            ConnectionError: If the connection fails after multiple retries.
        """
        for attempt in range(1, self.retries + 1):
            try:
                log_message(
                    "info",
                    f"Attempting to connect to database: {self.database} "
                    f"(Attempt {attempt})"
                )
                self.connection = pyodbc.connect(
                    f"DRIVER={self.driver};"
                    f"SERVER={self.host};DATABASE={self.database};"
                    f"UID={self.user};PWD={self.password}"
                )
                log_message(
                    "info",
                    "Successfully connected to the database.")
                return
            except Exception as e:
                log_message(
                    "error",
                    f"Connection attempt {attempt} failed: {e}")
                if attempt == self.retries:
                    error_message = (
                        "Failed to connect to database: {self.database} " +
                        f"after {self.retries} attempts."
                    )
                    log_message(
                        "error",
                        error_message)
                    raise ConnectionError(error_message) from e
                time.sleep(2)

    def fetch_data(self, query: str, params: dict = None) -> pd.DataFrame:
        """
        Fetch data from the database and return it as a Pandas DataFrame.

        Args:
            query (str): SQL SELECT query.
            params (dict, optional): Parameters for the query.
                Defaults to None.

        Returns:
            pd.DataFrame: Query results as a DataFrame.

        Raises:
            RuntimeError: If fetching data fails.

        Example Usage:
        from my_module import PandasDBConnector

        connector = PandasDBConnector(
            host="myserver.database.windows.net",
            database="mydb",
            user="admin",
            password="password",
            driver="{ODBC Driver 17 for SQL Server}",
            retries=3)

        query = "SELECT * FROM my_table WHERE id = ?"
        params = {"id": 1}
        data = connector.fetch_data(query, params)
        print(data)
        """
        try:
            log_message("info", f"Executing query: {query}")
            with self.connection.cursor() as cursor:
                cursor.execute(query, params or ())
                rows = cursor.fetchall()
                columns = [col[0] for col in cursor.description]
            log_message(
                "info",
                "Query executed successfully. Fetching results.")
            return pd.DataFrame.from_records(
                rows,
                columns=columns
            )
        except Exception as e:
            error_message = (
                "Failed to fetch data: {query} - {e}"
            )
            log_message(
                "error",
                error_message)
            raise RuntimeError(error_message) from e

    def execute_query(self, query: str, params: dict = None):
        """
        Execute non-SELECT queries (INSERT, UPDATE, DELETE).

        Args:
            query (str): SQL query to execute.
            params (dict, optional): Parameters for the query.
            Defaults to None.

        Raises:
            RuntimeError: If executing the query fails.

        Example Usage:
        from my_module import PandasDBConnector
        connector = PandasDBConnector(
            host="myserver.database.windows.net",
            database="mydb",
            user="admin",
            password="password",
            driver="{ODBC Driver 17 for SQL Server},
            retries=3)

        query = "INSERT INTO my_table (id, name) VALUES (?, ?)"
        params = {"id": 2, "name": "New User"}
        connector.execute_query(query, params)
        print("Query executed successfully.")

        """
        PandasValidationUtils.validate_is_non_empty_string(
            query)
        if params:
            PandasValidationUtils.validate_is_non_empty_dict(
                params)
        try:
            log_message("info", f"Executing query: {query}")
            with self.connection.cursor() as cursor:
                cursor.execute(query, params or ())
                self.connection.commit()
            log_message("info", "Query executed successfully.")
        except Exception as e:
            error_message = (
                "Failed to execute query: {query} - {e}"
            )
            log_message(
                "error",
                error_message)
            raise RuntimeError(error_message) from e

    def __enter__(self):
        """
        Context manager entry point.
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit point.
        """
        self.disconnect()


class PandasInferSchema(InferSchema):
    """
    Schema inference class for Pandas DataFrames.

    Infers schema from a Pandas DataFrame, including metadata such as:
    - Data type
    - Nullable columns
    - Unique values
    - Minimum and maximum values for numeric columns

    Attributes:
        config (dict): Optional configuration settings for schema inference.

    Example Usage:
        infer_schema = PandasInferSchema()
        data = pd.DataFrame({
            "col1": [1, 2, 3],
            "col2": ["a", "b", "c"],
            "col3": [None, 2.5, 3.1]
        })
        schema = infer_schema.infer(data)
    """

    def __init__(self, **kwargs):
        """
        Initialize PandasInferSchema with optional configurations.

        Args:
            **kwargs: Additional configurations for schema inference.
        """
        self.config = kwargs  # Store optional configurations
        PandasValidationUtils.log_init_arguments(self)

    def infer(self, data: pd.DataFrame, **kwargs):
        """
        Infer schema from a Pandas DataFrame.

        Args:
            data (pd.DataFrame): Input Pandas DataFrame.
            **kwargs: Additional configurations for schema inference.

        Returns:
            dict: Schema as a dictionary.

        Raises:
            ValueError: If the input DataFrame is empty.

        Example Usage:
        from my_module import PandasInferSchema
            infer_schema = PandasInferSchema()
            data = pd.DataFrame({
                "col1": [1, 2, 3],
                "col2": ["a", "b", "c"],
                "col3": [None, 2.5, 3.1]
            })
            schema = infer_schema.infer(data)
            print(schema)

        """
        PandasValidationUtils.validate_is_dataframe(data, 'data')

        log_message("info", "Inferring schema for the dataset")

        schema = {}
        for col in data.columns:
            schema[col] = {
                "dtype": str(data[col].dtype),
                "nullable": data[col].isnull().any(),
                "unique": data[col].is_unique,
                "min": data[col].min() if pd.api.types.is_numeric_dtype(
                    data[col]) else None,
                "max": data[col].max() if pd.api.types.is_numeric_dtype(
                    data[col]) else None,
            }

        log_message(
            "info",
            "Schema inference completed")
        return schema


class PandasInferSchemaFactory(InferSchemaFactory):
    """
    Factory class for creating schema inference instances for Pandas
    DataFrames.

    This factory supports:
    - Extensibility for different schema inference strategies
        (default, extended, etc.).
    - Dynamic configuration options to customize schema inference behavior.
    - Logging for factory operations to monitor creation and configuration
        changes.

    Attributes:
        schema_type (str): The type of schema inference to create
        (e.g., "default", "extended").
        schema_class (class): The schema inference class to instantiate.
        options (dict): Configuration options for schema inference.
        logger (DynamicLogger): Logger instance for monitoring factory
        operations.

    Example Usage:
        # Example 1: Create default PandasInferSchema
        factory = PandasInferSchemaFactory()
        infer_schema = factory.create_infer_schema()
        schema = infer_schema.infer(data)

        # Example 2: Create extended PandasInferSchema
        factory = PandasInferSchemaFactory(
            schema_type="extended", schema_class=PandasInferSchema)
        infer_schema = factory.create_infer_schema()
        schema = infer_schema.infer(data)

        # Example 3: Dynamically update options using set_options
        factory = PandasInferSchemaFactory()
        factory.set_options(
            {"custom_option": "example_value"})
        infer_schema = factory.create_infer_schema()
        schema = infer_schema.infer(data)

        # Example 4: Update schema type dynamically
        factory.schema_type = "extended"
        factory.schema_class = PandasInferSchema
        infer_schema = factory.create_infer_schema()
        schema = infer_schema.infer(data)
    """

    def __init__(
        self,
        schema_type: str = "default",
        schema_class=None,
        options: dict = None
    ):
        """
        Initialize the factory with schema type, schema class, and options.

        Args:
            schema_type (str, optional): Type of schema to create
                ("default", "extended"). Defaults to "default".
            schema_class (class, optional): Schema inference class to
                instantiate. Defaults to PandasInferSchema.
            options (dict, optional): Configuration options for schema
                inference. Defaults to None.
        """
        self.schema_type = schema_type
        self.schema_class = schema_class or PandasInferSchema
        self.options = options or {}

        # Validate schema_class compatibility
        PandasValidationUtils.validate_inheritance(
            self.schema_class,
            InferSchema,
            'schema_class')
        PandasValidationUtils.log_init_arguments(self)

    def set_options(self, new_options: dict):
        """
        Update the configuration options dynamically.

        Args:
            new_options (dict): New configuration options to merge with
            the existing ones.

        Example Usage:
        from my_module import PandasInferSchemaFactory

        factory = PandasInferSchemaFactory()
        factory.set_options({"custom_option": "example_value"})
        infer_schema = factory.create_infer_schema()
        schema = infer_schema.infer(data)

        """
        PandasValidationUtils.validate_is_non_empty_dict(
            new_options)
        self.options.update(new_options)
        log_message("info", f"Updated options: {new_options}")

    def create_infer_schema(self) -> InferSchema:
        """
        Create and return an instance of the specified schema class or type.

        Returns:
            InferSchema: An instance of the schema class.

        Raises:
            ValueError: If the schema type is unsupported or the schema
            class is not properly implemented.

        Example Usage:
        from my_module import PandasInferSchemaFactory

        factory = PandasInferSchemaFactory()
        infer_schema = factory.create_infer_schema()
        schema = infer_schema.infer(data)

        """
        try:
            log_message(
                "info",
                "Creating schema inference instance for " +
                f"schema_type={self.schema_type}")

            # Handle "default" schema type
            if self.schema_type == "default":
                return self.schema_class(**self.options)

            # Handle "extended" schema type
            elif self.schema_type == "extended":
                if 'PandasInferSchema' not in globals():
                    error_message = (
                        "The 'extended' schema type requires the " +
                        "'PandasInferSchema' class to be available. " +
                        "Please import it or provide an alternative."
                    )
                    log_message(
                        "error",
                        error_message)
                    raise ValueError(error_message)
                return PandasInferSchema(**self.options)

            # Unsupported schema type
            else:
                error_message = (
                    f"Unsupported schema type: {self.schema_type}"
                )
                log_message(
                    "error",
                    error_message)
                raise ValueError(error_message)

        except Exception as e:
            error_message = (
                "Error creating schema inference instance: {e}"
            )
            log_message(
                "error",
                error_message)
            raise Exception(error_message) from e


class PandasSchemaReader(SchemaReader):
    """
    Reader class for extracting and transforming schemas from a JSON file into
    a Pandas-compatible format.

    This class reads a JSON schema file, validates the specified source,
    and converts the schema fields into a Pandas-compatible dictionary
    of column names and data types.

    Attributes:
        DEFAULT_TYPE_MAPPING (dict): Default mapping from source schema
            types to Pandas-compatible data types.
        logger (DynamicLogger): Logger instance for logging operations.

    Example Usage:
        # Step 1: Initialize a JSON reader
        json_reader = PandasJsonReader("path/to/schema.json")

        # Step 2: Use PandasSchemaReader to read and transform schema
        schema_reader = PandasSchemaReader()
        pandas_schema = schema_reader.read_schema_json(
            json_reader,
            source_name="Aspen OEE",
            encoding="utf-8"  # Optional arguments for reading JSON
        )
        print(pandas_schema)

        # Step 3: Custom type mapping
        custom_mapping = {
            "StringType": "str", "DoubleType": "float", "IntegerType": "int"}
        schema_reader = PandasSchemaReader(type_mapping=custom_mapping)
        pandas_schema = schema_reader.read_schema_json(
            json_reader, source_name="Aspen OEE")
        print(pandas_schema)
    """

    DEFAULT_TYPE_MAPPING = {
        "StringType": "object",
        "DoubleType": "float64",
        "IntegerType": "int64",
        "BooleanType": "bool",
    }

    def __init__(self, type_mapping: dict = None):
        """
        Initialize the PandasSchemaReader with a logger and a type mapping.

        Args:
            type_mapping (dict, optional): Custom mapping for schema types
            to Pandas dtypes. Defaults to None.
        """
        self.type_mapping = type_mapping or self.DEFAULT_TYPE_MAPPING
        PandasValidationUtils.validate_is_non_empty_dict(
            self.type_mapping)
        PandasValidationUtils.log_init_arguments(
            self)

    def read_schema_json(self, data_reader, source_name: str, **kwargs):
        """
        Extract and transform the schema for the specified source to
        be compatible with a DataTypeValidator.

        Args:
            data_reader (PandasJsonReader): A reader object to read the
            JSON schema file.
            source_name (str): Name of the source (e.g., "Aspen OEE").
            **kwargs: Additional arguments for the JSON reader.

        Returns:
            dict: Transformed schema as a dictionary, with column names as
            keys and Pandas-compatible data types as values.

        Raises:
            ValueError: If the source name is not found in the schema or
            if the schema format is invalid.
            Exception: For unexpected errors during schema reading
            or transformation.

        Example Usage:
        from my_module import PandasJsonReader, PandasSchemaReader
        json_reader = PandasJsonReader("path/to/schema.json")
        schema_reader = PandasSchemaReader()
        pandas_schema = schema_reader.read_schema_json(
            json_reader,
            source_name="Aspen OEE",
            encoding="utf-8"  # Optional arguments for reading JSON
        )
        """
        PandasValidationUtils.validate_is_non_empty_string(
            source_name)
        try:
            log_message(
                "info",
                f"Reading schema for source '{source_name}' from JSON file")

            # Step 1: Read the schema file into a DataFrame
            schema_df = data_reader.read_data(**kwargs)

            # Step 2: Ensure the source name exists as a column
            if source_name not in schema_df.columns:
                error_message = (
                    f"Source '{source_name}' not found in the schema file."
                )
                log_message(
                    "error",
                    error_message)
                raise ValueError(error_message)

            # Step 3: Extract schema JSON for the given source
            source_schema_json = schema_df[source_name].iloc[0]
            log_message(
                "info",
                f"Schema for source '{source_name}' successfully extracted")

            # Step 4: Deserialize JSON if necessary
            if isinstance(source_schema_json, str):
                import json
                schema_dict = json.loads(source_schema_json)
            elif isinstance(source_schema_json, dict):
                schema_dict = source_schema_json
            else:
                error_message = (
                    f"Invalid schema format for source '{source_name}'. "
                    "Expected JSON or a dictionary."
                )
                log_message(
                    "error",
                    error_message)
                raise ValueError(error_message)

            # Step 5: Transform schema into a Pandas-compatible dictionary
            transformed_schema = {}
            for field in schema_dict["schema"]:
                field_name, field_type = field["name"], field["type"]
                if field_type not in self.type_mapping:
                    log_message(
                        "warning",
                        f"Unknown type '{field_type}' "
                        f"for field '{field_name}'. Defaulting to 'object'")
                transformed_schema[field_name] = self.type_mapping.get(
                    field_type, "object")

            log_message(
                "info",
                f"Schema transformation for source '{source_name}' completed")
            return transformed_schema

        except ValueError as e:
            error_message = f"Schema reading error: {e}"
            log_message(
                "error",
                error_message)
            raise ValueError(error_message) from e

        except Exception as e:
            error_message = (
                f"Unexpected error while reading schema: {e}"
            )
            log_message(
                "error",
                error_message)
            raise Exception(error_message) from e


class PandasMissingColumnsValidator(Validator):
    """
    Validator to ensure required columns are present in a Pandas DataFrame.

    Attributes:
        required_columns (list): A list of column names expected to be in
        the DataFrame.

    Example Usage:
        validator = PandasMissingColumnsValidator(
            required_columns=["col1", "col2", "col3"])
        data = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
        result = validator.validate(data)
        print(result)
        # Output:
        # {
        #     "validator": "PandasMissingColumnsValidator",
        #     "is_valid": False,
        #     "errors": [{
            # "error_type": "missing_columns",
            # "details": "Missing columns: ['col3']"}],
        #     "invalid_columns": ["col3"]
        # }
    """

    def __init__(self, required_columns: list):
        """
        Initialize the PandasMissingColumnsValidator.

        Args:
            required_columns (list): A list of column names expected to be
            in the DataFrame.
        """
        PandasValidationUtils.validate_is_non_empty_list(
            required_columns)
        self.required_columns = required_columns
        PandasValidationUtils.log_init_arguments(
            self)

    def validate(self, data: pd.DataFrame) -> dict:
        """
        Validate that the required columns are present in the DataFrame.

        Args:
            data (pd.DataFrame): The DataFrame to validate.

        Returns:
            dict: Validation result with the following keys:
                - "validator" (str): Name of the validator.
                - "is_valid" (bool): Whether the validation passed.
                - "errors" (list): List of errors, if any.
                - "invalid_columns" (list): List of missing columns.
        """
        log_message("info", "Validating presence of required columns.")

        missing_columns = PandasValidationUtils.check_missing_columns(
            data,
            self.required_columns)

        if missing_columns:
            log_message(
                "error",
                f"Missing columns detected: {missing_columns}")
            return {
                "validator": "PandasMissingColumnsValidator",
                "is_valid": False,
                "errors": [{
                    "error_type": "missing_columns",
                    "details": f"Missing columns: {missing_columns}"
                }],
                "invalid_columns": missing_columns
            }

        log_message(
            "info",
            "All required columns are present.")
        return {
            "validator": "PandasMissingColumnsValidator",
            "is_valid": True,
            "errors": [],
            "invalid_columns": []
        }


class PandasExtraColumnsValidator(Validator):
    """
    Validator to ensure no unexpected columns are present in a
    Pandas DataFrame.

    Attributes:
        allowed_columns (list): A list of allowed column names in
        the DataFrame.

    Example Usage:
        validator = PandasExtraColumnsValidator(
            allowed_columns=["col1", "col2", "col3"])
        data = pd.DataFrame(
            {"col1": [1, 2], "col2": [3, 4], "extra_col": [5, 6]})
        result = validator.validate(data)
        print(result)
        # Output:
        # {
        #     "validator": "PandasExtraColumnsValidator",
        #     "is_valid": False,
        #     "errors": [{
            # "error_type": "extra_columns",
            # "details": "Unexpected columns: ['extra_col']"}],
        #     "extra_columns": ["extra_col"]
        # }
    """

    def __init__(self, allowed_columns: list):
        """
        Initialize the PandasExtraColumnsValidator.

        Args:
            allowed_columns (list): A list of allowed column names in
            the DataFrame.
        """
        PandasValidationUtils.validate_is_non_empty_list(
            allowed_columns)
        self.allowed_columns = allowed_columns
        PandasValidationUtils.log_init_arguments(
            self)

    def validate(self, data: pd.DataFrame) -> dict:
        """
        Validate that no unexpected columns are present in the DataFrame.

        Args:
            data (pd.DataFrame): The DataFrame to validate.

        Returns:
            dict: Validation result with the following keys:
                - "validator" (str): Name of the validator.
                - "is_valid" (bool): Whether the validation passed.
                - "errors" (list): List of errors, if any.
                - "extra_columns" (list): List of unexpected columns.
        """
        PandasValidationUtils.validate_is_dataframe(data, 'data')
        log_message(
            "info",
            "Validating for unexpected columns.")

        # Step 1: Identify extra columns
        invalid_columns = list(set(data.columns) - set(self.allowed_columns))

        # Step 2: Log result and prepare output
        if invalid_columns:
            log_message(
                "error",
                f"Unexpected columns detected: {invalid_columns}")
            return {
                "validator": "PandasExtraColumnsValidator",
                "is_valid": False,
                "errors": [{
                    "error_type": "invalid_columns",
                    "details": f"Unexpected columns: {invalid_columns}"
                }],
                "invalid_columns": invalid_columns
            }

        log_message(
            "info",
            "No unexpected columns found.")
        return {
            "validator": "PandasExtraColumnsValidator",
            "is_valid": True,
            "errors": [],
            "invalid_columns": []
        }


class PandasDataTypeValidator(Validator):
    """
    Validator to ensure column data types match the expected schema in
    a Pandas DataFrame.

    Attributes:
        expected_schema (dict): Dictionary mapping column names to
        expected data types.

    Example Usage:
        validator = PandasDataTypeValidator(
            expected_schema={
                "col1": "int64", "col2": "float64", "col3": "object"}
        )
        data = pd.DataFrame({
            "col1": [1, 2],
            "col2": [3.5, 4.6],
            "col3": ["a", "b"]
        })
        result = validator.validate(data)
        print(result)
        # Output:
        # {
        #     "validator": "PandasDataTypeValidator",
        #     "is_valid": True,
        #     "errors": [],
        #     "invalid_columns": [],
        #     "missing_columns": []
        # }
    """

    def __init__(self, expected_schema: dict):
        """
        Initialize the PandasDataTypeValidator.

        Args:
            expected_schema (dict): A dictionary mapping column names to
            expected data types.
        """
        PandasValidationUtils.validate_is_non_empty_dict(
            expected_schema)
        self.expected_schema = expected_schema
        PandasValidationUtils.log_init_arguments(self)

    def validate(self, data: pd.DataFrame) -> dict:
        """
        Validate that column data types in the DataFrame match the
        expected schema.

        Args:
            data (pd.DataFrame): The DataFrame to validate.

        Returns:
            dict: Validation result with the following keys:
                - "validator" (str): Name of the validator.
                - "is_valid" (bool): Whether the validation passed.
                - "errors" (list): List of errors, if any.
                - "invalid_columns" (list): List of columns with incorrect
                    data types.
                - "missing_columns" (list): List of columns missing from
                    the dataset.
        """
        PandasValidationUtils.validate_is_dataframe(
            data,
            'data')
        log_message(
            "info",
            "Validating column data types against the expected schema.")

        # Step 1: Use PandasValidationUtils to check missing columns
        missing_columns = PandasValidationUtils.check_missing_columns(
            data,
            list(self.expected_schema.keys()))

        errors = []
        invalid_columns = []

        # Step 2: Log missing columns if any
        if missing_columns:
            for col in missing_columns:
                log_message(
                    "error",
                    f"Missing column: '{col}'")
                errors.append({
                    "error_type": "missing_column",
                    "details": f"Column '{col}' is missing from the dataset."
                })

        # Step 3: Use PandasValidationUtils for type validation
        for col, expected_type in self.expected_schema.items():
            if col in data.columns:
                actual_type = str(data[col].dtype)
                if not PandasValidationUtils.check_column_dtype(
                    data[col],
                    expected_type
                ):
                    log_message(
                        "error",
                        f"Type mismatch for column '{col}': "
                        f"Expected {expected_type}, Got {actual_type}")
                    errors.append({
                        "error_type": "type_mismatch",
                        "details": f"Column '{col}' has incorrect type. "
                        f"Expected: {expected_type}, Got: {actual_type}"
                    })
                    invalid_columns.append(col)

        # Prepare the validation result
        result = {
            "validator": "PandasDataTypeValidator",
            "is_valid": not bool(errors),
            "errors": errors,
            "invalid_columns": invalid_columns,
            "missing_columns": missing_columns
        }

        if errors:
            log_message(
                "error",
                f"Data type validation failed with {len(errors)} errors.")
        else:
            log_message(
                "info",
                "Data type validation passed successfully.")

        return result


class PandasNullValueValidator(Validator):
    """
    Validator to check for null or empty values in critical columns of
    a Pandas DataFrame.

    Attributes:
        critical_columns (list): List of critical columns to validate.
        null_values (list): List of values considered as null/empty.

    Example Usage:
        validator = PandasNullValueValidator(
            critical_columns=["col1", "col2"],
            null_values=[None, "", "NA"]
        )
        data = pd.DataFrame({
            "col1": [1, None, 3],
            "col2": ["a", "", "NA"],
            "col3": [5, 6, 7]
        })
        result = validator.validate(data)
        print(result)
    """

    def __init__(self, critical_columns: list, null_values: list = None):
        """
        Initialize the PandasNullValueValidator.

        Args:
            critical_columns (list): List of critical columns to validate.
            null_values (list): Values considered as null/empty.
                Defaults to [None, ""].
        """
        PandasValidationUtils.validate_is_non_empty_list(
            critical_columns)

        self.critical_columns = critical_columns
        if null_values:
            PandasValidationUtils.validate_is_non_empty_list(
                null_values)
        self.null_values = null_values or [None, "", pd.NA, np.nan]
        PandasValidationUtils.log_init_arguments(self)

    def validate(self, data: pd.DataFrame) -> dict:
        """
        Validate the DataFrame for null or empty values in critical columns.

        Args:
            data (pd.DataFrame): The DataFrame to validate.

        Returns:
            dict: Validation result with the following keys:
                - "validator" (str): Name of the validator.
                - "is_valid" (bool): Whether the validation passed.
                - "errors" (list): List of errors, if any.
                - "invalid_rows" (pd.DataFrame): Rows with null/empty values.
                - "missing_columns" (list): List of missing columns.
        """
        PandasValidationUtils.validate_is_dataframe(
            data,
            'data')
        log_message(
            "info",
            "Validating critical columns for null or empty values.")

        errors = []
        invalid_rows = pd.DataFrame()

        # Step 1: Check for missing columns
        missing_columns = PandasValidationUtils.check_missing_columns(
            data,
            self.critical_columns)
        for col in missing_columns:
            errors.append({
                "error_type": "missing_column",
                "details": f"Column '{col}' is missing from the dataset."
            })
            log_message(
                "error",
                f"Column '{col}' is missing from the dataset.")

        # Step 2: Validate null or empty rows for existing columns
        for col in set(self.critical_columns) - set(missing_columns):
            null_or_empty_rows = data[data[col].isin(self.null_values)]
            if not null_or_empty_rows.empty:
                errors.append({
                    "error_type": "null_values",
                    "details": f"Column '{col}' contains null/empty values."
                })
                log_message(
                    "error",
                    f"Column '{col}' contains null/empty values.")
                invalid_rows = PandasValidationUtils.concatenate_invalid_rows(
                    invalid_rows,
                    null_or_empty_rows)

        # Prepare the validation result
        result = {
            "validator": "PandasNullValueValidator",
            "is_valid": not bool(errors),
            "errors": errors,
            "invalid_rows": invalid_rows,
            "missing_columns": missing_columns
        }

        if errors:
            log_message(
                "error",
                f"Null value validation failed with {len(errors)} errors.")
        else:
            log_message(
                "info",
                "Null value validation passed successfully.")

        return result


class PandasRangeValidator(Validator):
    """
    Validator to ensure numerical values fall within specified ranges
    for columns in a Pandas DataFrame.

    Attributes:
        column_ranges (dict): Dictionary specifying the range for each column.
        inclusive (bool): If True, range boundaries are inclusive (default).
            If False, boundaries are exclusive.

    Example Usage:
        validator = PandasRangeValidator(
            column_ranges={"col1": (0, 100), "col2": (10, 50)},
            inclusive=False
        )
        data = pd.DataFrame({
            "col1": [0, 10, 20, 100, 150],
            "col2": [15, 5, 45, 50]
        })
        result = validator.validate(data)
        print(result)
    """

    def __init__(self, column_ranges: dict, inclusive: bool = True):
        """
        Initialize the PandasRangeValidator.

        Args:
            column_ranges (dict): Dictionary of column names and their
                allowed (min, max) ranges.
            inclusive (bool): If True, range boundaries are inclusive.
                Defaults to True.
        """
        PandasValidationUtils.validate_is_non_empty_dict(
            column_ranges)
        self.column_ranges = column_ranges
        PandasValidationUtils.validate_is_boolean(inclusive)
        self.inclusive = inclusive
        PandasValidationUtils.log_init_arguments(self)

    def validate(self, data: pd.DataFrame) -> dict:
        """
        Validate the DataFrame to ensure values in specified columns
        fall within defined ranges.

        Args:
            data (pd.DataFrame): The DataFrame to validate.

        Returns:
            dict: Validation result with the following keys:
                - "validator" (str): Name of the validator.
                - "is_valid" (bool): Whether the validation passed.
                - "errors" (list): List of errors, if any.
                - "invalid_rows" (pd.DataFrame): Rows with out-of-range values.
                - "missing_columns" (list): List of missing columns.
        """
        PandasValidationUtils.validate_is_dataframe(
            data,
            'data')
        log_message(
            "info",
            f"Starting range validation with inclusive={self.inclusive}.")

        # Handle empty DataFrame
        if data.empty:
            log_message(
                "error",
                "The input DataFrame is empty.")
            return {
                "validator": "PandasRangeValidator",
                "is_valid": False,
                "errors": [{"error_type": "empty_dataset",
                            "details": "The dataset is empty."}],
                "invalid_rows": data,
                "missing_columns": []
            }

        errors = []
        invalid_rows = pd.DataFrame()

        # Step 1: Check for missing columns using PandasValidationUtils
        missing_columns = PandasValidationUtils.check_missing_columns(
            data,
            list(self.column_ranges.keys()))
        for col in missing_columns:
            log_message(
                "error",
                f"Missing column: '{col}'")
            errors.append({
                "error_type": "missing_column",
                "details": f"Column '{col}' is missing from the dataset."
            })

        # Step 2: Validate value ranges for each column
        for col, (min_val, max_val) in self.column_ranges.items():
            if col not in missing_columns:
                # Ensure column data type is numeric before range check
                if not pd.api.types.is_numeric_dtype(data[col]):
                    log_message(
                        "error",
                        f"Column '{col}' is not numeric. " +
                        "Skipping range validation.")
                    errors.append({
                        "error_type": "invalid_data_type",
                        "details": f"Column '{col}' " +
                        "is not numeric. Expected numeric values."
                    })
                    continue

                # Perform range validation
                if self.inclusive:
                    out_of_range = ~data[col].between(
                        min_val,
                        max_val,
                        inclusive="both")
                else:
                    out_of_range = ~data[col].between(
                        min_val,
                        max_val,
                        inclusive="neither")

                out_of_range_rows = data.loc[out_of_range]

                if not out_of_range_rows.empty:
                    invalid_values = out_of_range_rows[col].unique().tolist()
                    boundary_type = (
                        "inclusive" if self.inclusive else "exclusive")
                    log_message(
                        "error",
                        f"Column '{col}' has values outside "
                        f"the {boundary_type} range ({min_val}, {max_val}). "
                        f"Invalid values: {invalid_values[:5]}..."
                    )
                    errors.append({
                        "error_type": "range_violation",
                        "details": (
                            f"Column '{col}' has values outside "
                            f"the {boundary_type} "
                            f"range ({min_val}, {max_val}). "
                            f"Invalid values: {invalid_values[:5]}...")
                    })
                    invalid_rows = pd.concat(
                        [invalid_rows, out_of_range_rows], ignore_index=True)

        # Prepare the validation result
        result = {
            "validator": "PandasRangeValidator",
            "is_valid": not bool(errors),
            "errors": errors,
            "invalid_rows": invalid_rows.drop_duplicates().reset_index(
                drop=True),
            "missing_columns": missing_columns
        }

        if errors:
            log_message(
                "error",
                f"Range validation failed with {len(errors)} errors.")
        else:
            log_message(
                "info",
                "Range validation passed successfully.")

        return result


class PandasUniquenessValidator(Validator):
    """
    Validator to ensure values in specified columns are unique in a
    Pandas DataFrame.

    Attributes:
        unique_columns (list): List of column names to check for uniqueness.

    Example Usage:
        validator = PandasUniquenessValidator(unique_columns=["col1", "col2"])
        data = pd.DataFrame({
            "col1": [1, 2, 2],
            "col2": ["a", "b", "a"],
            "col3": [10, 20, 30]
        })
        result = validator.validate(data)
        print(result)
    """

    def __init__(self, unique_columns: list):
        """
        Initialize the PandasUniquenessValidator.

        Args:
            unique_columns (list): List of column names to validate
            for uniqueness.
        """
        PandasValidationUtils.validate_is_non_empty_list(
            unique_columns)
        self.unique_columns = unique_columns
        PandasValidationUtils.log_init_arguments(
            self)

    def validate(
        self,
        data: pd.DataFrame
    ) -> dict:
        """
        Validate the DataFrame to ensure specified columns have unique values.

        Args:
            data (pd.DataFrame): The DataFrame to validate.

        Returns:
            dict: Validation result with the following keys:
                - "validator" (str): Name of the validator.
                - "is_valid" (bool): Whether the validation passed.
                - "errors" (list): List of errors, if any.
                - "invalid_rows" (pd.DataFrame): Rows with duplicate values.
                - "missing_columns" (list): List of missing columns.
        """
        PandasValidationUtils.validate_is_dataframe(data, 'data')
        log_message(
            "info",
            "Validating uniqueness for specified columns.")

        errors = []
        invalid_rows = pd.DataFrame()

        # Step 1: Check for missing columns
        missing_columns = PandasValidationUtils.check_missing_columns(
            data, self.unique_columns)
        for col in missing_columns:
            log_message(
                "error",
                f"Missing column: '{col}'")
            errors.append({
                "error_type": "missing_column",
                "details": f"Column '{col}' is missing from the dataset."
            })

        # Step 2: Check for duplicates in valid columns
        for col in set(self.unique_columns) - set(missing_columns):
            duplicate_rows = PandasValidationUtils.find_duplicates(data, col)
            if not duplicate_rows.empty:
                log_message(
                    "error",
                    f"Column '{col}' contains duplicate values.")
                errors.append({
                    "error_type": "duplicate_values",
                    "details": f"Column '{col}' contains duplicate values."
                })
                invalid_rows = pd.concat(
                    [invalid_rows, duplicate_rows],
                    ignore_index=True)

        # Prepare the validation result
        result = {
            "validator": "PandasUniquenessValidator",
            "is_valid": not bool(errors),
            "errors": errors,
            "invalid_rows": invalid_rows.drop_duplicates().reset_index(
                drop=True),
            "missing_columns": missing_columns
        }

        if errors:
            log_message(
                "error",
                f"Uniqueness validation failed with {len(errors)} errors.")
        else:
            log_message(
                "info",
                "Uniqueness validation passed successfully.")

        return result


class PandasRowCountValidator(Validator):
    """
    Validator to ensure the dataset meets a specified row count.

    This validator checks if the number of rows in a Pandas DataFrame
    falls within a defined range.

    Attributes:
        min_rows (int, optional): Minimum number of rows required.
        max_rows (int, optional): Maximum number of rows allowed.

    Example Usage:
        validator = PandasRowCountValidator(min_rows=5, max_rows=100)
        data = pd.DataFrame({"col1": [1, 2, 3, 4, 5]})
        result = validator.validate(data)
        print(result)
        # Output:
        # {
        #     "validator": "PandasRowCountValidator",
        #     "is_valid": True,
        #     "errors": [],
        #     "invalid_rows": pd.DataFrame()
        # }
    """

    def __init__(self, min_rows: int = None, max_rows: int = None):
        """
        Initialize the PandasRowCountValidator.

        Args:
            min_rows (int, optional): Minimum number of rows required.
                Defaults to None.
            max_rows (int, optional): Maximum number of rows allowed.
                Defaults to None.
        """
        PandasValidationUtils.validate_is_integer(
            min_rows,
            'min_rows')
        self.min_rows = min_rows
        PandasValidationUtils.validate_is_integer(
            max_rows,
            'max_rows')
        self.max_rows = max_rows
        if min_rows > max_rows:
            error_message = (
                "min_rows must be less than or equal to max_rows. "
            )
            log_message(
                "error",
                error_message)
            raise ValueError(error_message)
        PandasValidationUtils.log_init_arguments(self)

    def validate(self, data: pd.DataFrame) -> dict:
        """
        Validate the row count of the DataFrame.

        Args:
            data (pd.DataFrame): The DataFrame to validate.

        Returns:
            dict: Validation result with the following keys:
                - "validator" (str): Name of the validator.
                - "is_valid" (bool): Whether the validation passed.
                - "errors" (list): List of errors, if any.
                - "invalid_rows" (pd.DataFrame): Entire dataset if row count
                    validation fails.
        """
        PandasValidationUtils.validate_is_dataframe(
            data,
            'data')
        log_message(
            "info",
            "Validating row count.")

        row_count = len(data)
        errors = []

        # Perform row count validation using PandasValidationUtils
        PandasValidationUtils.validate_row_count(
            row_count,
            self.min_rows,
            self.max_rows,
            errors)

        # Prepare the result
        invalid_rows = data if errors else pd.DataFrame()
        result = {
            "validator": "PandasRowCountValidator",
            "is_valid": not bool(errors),
            "errors": errors,
            "invalid_rows": invalid_rows.reset_index(drop=True)
        }

        if errors:
            log_message(
                "error",
                f"Row count validation failed with {len(errors)} errors.")
        else:
            log_message(
                "info",
                "Row count validation passed successfully.")

        return result


class PandasNonEmptyValidator(Validator):
    """
    Validator to ensure the dataset is not empty.

    This validator checks if a Pandas DataFrame contains at least one row and
    one column.

    Example Usage:
        validator = PandasNonEmptyValidator()
        data = pd.DataFrame({"col1": [1, 2, 3]})
        result = validator.validate(data)
        print(result)
        # Output:
        # {
        #     "validator": "PandasNonEmptyValidator",
        #     "is_valid": True,
        #     "errors": [],
        #     "invalid_rows": pd.DataFrame()
        # }
    """

    def validate(self, data: pd.DataFrame) -> dict:
        """
        Validate if the DataFrame is not empty.

        Args:
            data (pd.DataFrame): The DataFrame to validate.

        Returns:
            dict: Validation result with the following keys:
                - "validator" (str): Name of the validator.
                - "is_valid" (bool): Whether the validation passed.
                - "errors" (list): List of errors, if any.
                - "invalid_rows" (pd.DataFrame): Entire dataset if it is empty.
        """
        logger = get_logger()
        PandasValidationUtils.validate_is_dataframe(
            data,
            'data')
        logger.log("info", "Validating if the dataset is non-empty.")

        # Use PandasValidationUtils to check if the DataFrame is empty
        errors = []
        PandasValidationUtils.validate_is_non_empty_dataset(data, errors)

        # Prepare the result
        result = {
            "validator": "PandasNonEmptyValidator",
            "is_valid": not bool(errors),
            "errors": errors,
            "invalid_rows": data if errors else pd.DataFrame()
        }

        if errors:
            logger.log("error", "Validation failed: The dataset is empty.")
        else:
            logger.log("info", "Validation passed: The dataset is not empty.")

        return result


class PandasValueValidator(Validator):
    """
    Validator to check for specific required or prohibited values in
    columns of a Pandas DataFrame.

    This validator ensures that column values either:
    - Only include the specified allowed values (`allow_only=True`).
    - Exclude the specified prohibited values (`allow_only=False`).

    Attributes:
        column_values (dict): A dictionary where keys are column names
            and values are lists of allowed/prohibited values.
        allow_only (bool): Whether to validate only allowed values (True)
            or disallowed values (False).

    Example Usage:
        data = pd.DataFrame({
            "col1": [1, 2, 3],
            "col2": ["A", "B", "C"]
        })
        # Allow only specific values in columns
        validator = PandasValueValidator(
            {"col1": [1, 2],
            "col2": ["A", "B"]},
            allow_only=True)
        result = validator.validate(data)
        print(result)
    """

    def __init__(
        self,
        column_values: dict,
        allow_only: bool = True
    ):
        """
        Initialize the PandasValueValidator.

        Args:
            column_values (dict): Dictionary of column names and their
                allowed/prohibited values.
            allow_only (bool): If True, validates that only specified
                values are allowed. Defaults to True.
        """
        PandasValidationUtils.validate_is_non_empty_dict(
            column_values)
        self.column_values = column_values
        PandasValidationUtils.validate_is_boolean(
            allow_only,
            "allow_only")
        self.allow_only = allow_only
        PandasValidationUtils.log_init_arguments(
            self)

    def validate(self, data: pd.DataFrame) -> dict:
        """
        Validate the DataFrame based on column value rules.

        Args:
            data (pd.DataFrame): The DataFrame to validate.

        Returns:
            dict: Validation result with the following keys:
                - "validator" (str): Name of the validator.
                - "is_valid" (bool): Whether the validation passed.
                - "errors" (list): List of errors, if any.
                - "invalid_rows" (pd.DataFrame): Rows with invalid values.
                - "missing_columns" (list): List of missing columns.
        """
        PandasValidationUtils.validate_is_dataframe(
            data,
            'data')
        log_message(
            "info",
            "Starting value validation for specified columns.")

        # Handle empty DataFrame
        if data.empty:
            log_message(
                "error",
                "The input DataFrame is empty.")
            return {
                "validator": "PandasValueValidator",
                "is_valid": False,
                "errors": [{
                    "error_type": "empty_dataset",
                    "details": "The dataset is empty."}],
                "invalid_rows": data,
                "missing_columns": []
            }

        # Initialize validation results
        errors = []
        invalid_rows = pd.DataFrame()
        missing_columns = []

        for col, values in self.column_values.items():
            if col in data.columns:
                # Type safety: Ensure column is compatible for comparison
                if not pd.api.types.is_scalar(values[0]):
                    log_message(
                        "error",
                        f"Column '{col}' contains incompatible data types.")
                    errors.append({
                        "error_type": "invalid_data_type",
                        "details": f"Column '{col}' has " +
                        "incompatible types for comparison."
                    })
                    continue

                invalid = None
                if self.allow_only:
                    invalid = ~data[col].isin(values)
                else:
                    invalid = data[col].isin(values)

                invalid_data = data.loc[invalid]

                if not invalid_data.empty:
                    invalid_values = invalid_data[col].unique().tolist()
                    log_message(
                        "error",
                        f"Column '{col}' contains disallowed values: "
                        f"{invalid_values[:5]}..."
                    )
                    errors.append({
                        "error_type": "value_violation",
                        "details": f"Column '{col}' contains "
                        "disallowed values. "
                        f"Invalid values: {invalid_values[:5]}..."
                    })
                    invalid_rows = pd.concat(
                        [invalid_rows, invalid_data],
                        ignore_index=True)
            else:
                # Log and append missing column error
                error_message = f"Column '{col}' is missing from the dataset."
                log_message(
                    "error",
                    error_message)
                missing_columns.append(col)
                errors.append({
                    "error_type": "missing_column",
                    "details": error_message
                })

        log_message(
            "info",
            f"Value validation completed with {len(errors)} errors.")

        result = {
            "validator": "PandasValueValidator",
            "is_valid": not bool(errors),
            "errors": errors,
            "invalid_rows": invalid_rows.drop_duplicates().reset_index(
                drop=True),
            "missing_columns": missing_columns
        }
        return result


class PandasReferentialIntegrityValidator(Validator):
    """
    Validator to ensure values in a column exist in a reference dataset.

    This validator checks that all values in a specified column of a DataFrame
    are present in a reference Pandas Series or list.

    Attributes:
        column (str): The name of the column to validate.
        reference_data (pd.Series): The reference dataset containing
        valid values.

    Example Usage:
        # Example DataFrame
        data = pd.DataFrame({
            "col1": [1, 2, 3, 4],
            "col2": ["A", "B", "C", "D"]
        })

        # Reference data
        reference = pd.Series(["A", "B", "C"])

        # Validate referential integrity
        validator = PandasReferentialIntegrityValidator(
            column="col2", reference_data=reference)
        result = validator.validate(data)

        print(result)
        # Output:
        # {
        #     "validator": "PandasReferentialIntegrityValidator",
        #     "is_valid": False,
        #     "errors": [
        #         {
        #             "error_type": "referential_integrity_violation",
        #             "details": "Column 'col2' contains values not in
        #                   the reference dataset."
        #         }
        #     ],
        #     "invalid_rows": ...  # DataFrame of invalid rows,
        #     "missing_columns": []
        # }
    """

    def __init__(self, column: str, reference_data: pd.Series):
        """
        Initialize the PandasReferentialIntegrityValidator.

        Args:
            column (str): The column to validate.
            reference_data (pd.Series): A reference Pandas Series or list with
                valid values.
        """
        if not isinstance(reference_data, (pd.Series, list)):
            error_message = (
                "Invalid type for reference_data. " +
                "Expected a Pandas Series or a list, got {}.".format(
                    type(reference_data).__name__)
            )
            log_message(
                "error",
                error_message)
            raise ValueError(error_message)
        self.reference_data = pd.Series(
            reference_data) if isinstance(
                reference_data, list) else reference_data
        PandasValidationUtils.validate_is_non_empty_string(column)
        self.column = column
        PandasValidationUtils.log_init_arguments(self)

    def validate(self, data: pd.DataFrame) -> dict:
        """
        Validate the column values against the reference dataset.

        Args:
            data (pd.DataFrame): The DataFrame to validate.

        Returns:
            dict: Validation result with the following keys:
                - "validator" (str): Name of the validator.
                - "is_valid" (bool): Whether the validation passed.
                - "errors" (list): List of errors, if any.
                - "invalid_rows" (pd.DataFrame): Rows with invalid values.
                - "missing_columns" (list): List of missing columns (if any).
        """
        PandasValidationUtils.validate_is_dataframe(
            data,
            'data')
        log_message(
            "info",
            "Starting referential integrity validation " +
            "for column '{self.column}'.")

        errors = []
        invalid_rows = pd.DataFrame()
        missing_columns = []

        if self.column in data.columns:
            invalid = ~data[self.column].isin(self.reference_data)
            invalid_data = data[invalid]

            if not invalid_data.empty:
                error_message = (
                    f"Column '{self.column}' " +
                    "contains values not in the reference dataset.")
                log_message("error", error_message)
                errors.append({
                    "error_type": "referential_integrity_violation",
                    "details": error_message
                })
                invalid_rows = pd.concat(
                    [invalid_rows, invalid_data],
                    ignore_index=True)
        else:
            error_message = (
                f"Column '{self.column}' " +
                "is missing from the dataset.")
            log_message(
                "error",
                error_message)
            missing_columns.append(self.column)
            errors.append({
                "error_type": "missing_column",
                "details": error_message
            })

        log_message(
            "info",
            f"Referential integrity validation completed with {len(errors)}" +
            " error(s).")

        result = {
            "validator": "PandasReferentialIntegrityValidator",
            "is_valid": not bool(errors),
            "errors": errors,
            "invalid_rows": invalid_rows.reset_index(drop=True),
            "missing_columns": missing_columns
        }
        return result


class PandasRegexValidator(Validator):
    """
    Validator to ensure column values match specific regex patterns.

    Attributes:
        column_patterns (dict): A dictionary where keys are column names
        and values are regex patterns.

    Example Usage:
        data = pd.DataFrame({
            "email": [
                "user1@example.com", "user2@example.com", "invalid_email"],
            "phone": ["123-456-7890", "987-654-3210", "invalid_phone"]
        })

        patterns = {
            "email": "^[\\w\\.\\-]+@[\\w\\.\\-]+\\.\\w+$",
            "phone": "^\\d{3}-\\d{3}-\\d{4}$"
        }


        validator = PandasRegexValidator(column_patterns=patterns)
        result = validator.validate(data)
        print(result)
    """

    def __init__(self, column_patterns: dict):
        """
        Initialize the PandasRegexValidator.

        Args:
            column_patterns (dict): Dictionary where keys are column names
            and values are regex patterns.
        """
        PandasValidationUtils.validate_is_non_empty_dict(
            column_patterns)
        self.column_patterns = column_patterns

        # Validate provided regex patterns
        for col, pattern in column_patterns.items():
            try:
                re.compile(pattern)  # Check if the pattern is valid
            except re.error as e:
                error_message = (
                    f"Invalid regex pattern for column '{col}': {e}"
                )
                log_message(
                    "error",
                    error_message)
                raise ValueError(
                    error_message)
        PandasValidationUtils.log_init_arguments(self)

    def validate(self, data: pd.DataFrame) -> dict:
        """
        Validate that column values match the specified regex patterns.

        Args:
            data (pd.DataFrame): The DataFrame to validate.

        Returns:
            dict: Validation result with the following keys:
                - "validator" (str): Name of the validator.
                - "is_valid" (bool): Whether the validation passed.
                - "errors" (list): List of errors, if any.
                - "invalid_rows" (pd.DataFrame): Rows with invalid values.
                - "missing_columns" (list): List of missing columns (if any).
        """
        PandasValidationUtils.validate_is_dataframe(data, 'data')
        log_message(
            "info",
            "Starting regex validation for specified columns.")

        # Handle empty DataFrame
        if data.empty:
            log_message(
                "error",
                "The input DataFrame is empty.")
            return {
                "validator": "PandasRegexValidator",
                "is_valid": False,
                "errors": [{"error_type": "empty_dataset",
                            "details": "The dataset is empty."}],
                "invalid_rows": data,
                "missing_columns": []
            }

        errors = []
        invalid_rows = pd.DataFrame()
        missing_columns = []

        for col, pattern in self.column_patterns.items():
            if col in data.columns:
                try:
                    if not pd.api.types.is_string_dtype(data[col]):
                        log_message(
                            "error",
                            f"Column '{col}' is not string-typed. " +
                            "Skipping regex validation.")
                        errors.append({
                            "error_type": "invalid_data_type",
                            "details": f"Column '{col}' is not string-typed." +
                            " Expected string values."
                        })
                        continue

                    # Identify invalid rows
                    invalid = ~data[col].astype(str).str.match(
                        pattern,
                        na=False)
                    invalid_data = data.loc[invalid]

                    if not invalid_data.empty:
                        invalid_values = invalid_data[col].unique().tolist()
                        log_message(
                            "error",
                            f"Column '{col}' contains invalid values: "
                            f"{invalid_values[:5]}...")
                        errors.append({
                            "error_type": "regex_violation",
                            "details": f"Column '{col}' contains values not "
                            f"matching the regex '{pattern}'. "
                            f"Invalid values: {invalid_values[:5]}..."
                        })
                        invalid_rows = pd.concat(
                            [invalid_rows, invalid_data],
                            ignore_index=True)
                except Exception as e:
                    log_message(
                        "error",
                        f"Regex validation failed for column '{col}': {e}")
                    errors.append({
                        "error_type": "validation_error",
                        "details": f"Failed to apply regex on column '{col}'. "
                        f"Error: {e}"
                    })
            else:
                error_message = f"Column '{col}' is missing from the dataset."
                log_message("error", error_message)
                missing_columns.append(col)
                errors.append({
                    "error_type": "missing_column",
                    "details": error_message
                })

        log_message(
            "info",
            f"Regex validation completed with {len(errors)} error(s).")

        result = {
            "validator": "PandasRegexValidator",
            "is_valid": not bool(errors),
            "errors": errors,
            "invalid_rows": invalid_rows.drop_duplicates().reset_index(
                drop=True),
            "missing_columns": missing_columns
        }
        return result


class PandasDuplicateRowsValidator(Validator):
    """
    Validator to check for duplicate rows in a Pandas DataFrame.

    This validator identifies duplicate rows and returns a detailed
    validation report.

    Attributes:
        subset (list, optional): List of column names to consider when
        identifying duplicates.If None, all columns are used.

    Example Usage:
        # Example DataFrame
        data = pd.DataFrame({
            "col1": [1, 2, 2, 3],
            "col2": ["a", "b", "b", "c"]
        })

        # Validate for duplicate rows
        validator = PandasDuplicateRowsValidator()
        result = validator.validate(data)
        print(result)
    """

    def __init__(self, subset: list = None):
        """
        Initialize the PandasDuplicateRowsValidator.

        Args:
            subset (list, optional): List of column names to consider when
            identifying duplicates. Defaults to None
            (checks for full row duplicates).
        """
        if subset:
            PandasValidationUtils.validate_is_non_empty_list(
                subset)
        self.subset = subset
        PandasValidationUtils.log_init_arguments(
            self)

    def validate(self, data: pd.DataFrame) -> dict:
        """
        Validate the dataset for duplicate rows.

        Args:
            data (pd.DataFrame): The DataFrame to validate.

        Returns:
            dict: Validation result with the following keys:
                - "validator" (str): Name of the validator.
                - "is_valid" (bool): Whether the validation passed.
                - "errors" (list): List of errors, if any.
                - "invalid_rows" (pd.DataFrame): DataFrame of duplicate rows.
        """
        PandasValidationUtils.validate_is_dataframe(data, 'data')
        log_message(
            "info",
            "Starting duplicate row validation. Subset: " +
            f"{self.subset or 'All columns'}")

        try:
            # Use PandasValidationUtils for duplicate detection
            duplicate_rows = PandasValidationUtils.detect_duplicates(
                data,
                subset=self.subset)
            if not duplicate_rows.empty:
                log_message(
                    "error",
                    f"Duplicate rows found: {len(duplicate_rows)} rows.")
                return {
                    "validator": "PandasDuplicateRowsValidator",
                    "is_valid": False,
                    "errors": [{
                        "error_type": "duplicate_rows",
                        "details": f"Found {len(duplicate_rows)} " +
                        "duplicate rows."
                    }],
                    "invalid_rows": duplicate_rows.reset_index(drop=True)
                }

            log_message("info", "No duplicate rows found.")
            return {
                "validator": "PandasDuplicateRowsValidator",
                "is_valid": True,
                "errors": [],
                "invalid_rows": pd.DataFrame()
            }

        except Exception as e:
            error_message = (
                f"Error during duplicate row validation: {e}"
            )
            log_message(
                "error",
                error_message)
            raise Exception(error_message) from e


class PandasColumnDependencyValidator(Validator):
    """
    Validator to ensure column dependencies are met in a Pandas DataFrame.

    This validator checks if the dependent column (`required_col`) is non-null
    or non-empty
    whenever the primary column (`col`) contains non-null values.

    Attributes:
        dependencies (dict): Dictionary where keys are columns and values
        are their required dependent columns.
        null_values (list): Values considered as null/empty.

    Example Usage:
        # Import required libraries
        import pandas as pd

        # Example DataFrame
        data = pd.DataFrame({
            "col1": [1, None, 3, 4],
            "col2": [None, "b", "", "d"]
        })

        # Define column dependencies
        dependencies = {"col1": "col2"}

        # Initialize the validator
        validator = PandasColumnDependencyValidator(dependencies)

        # Validate the DataFrame
        result = validator.validate(data)

        # Print validation results
        print("Validation Result:")
        print(result)
    """

    def __init__(self, dependencies: dict, null_values: list = ["", None]):
        """
        Initialize the PandasColumnDependencyValidator.

        Args:
            dependencies (dict): Dictionary where keys are columns and values
                are their required dependent columns.
            null_values (list): Values considered as null/empty.
                Defaults to ["", None].
        """
        PandasValidationUtils.validate_is_non_empty_dict(
            dependencies)
        self.dependencies = dependencies
        PandasValidationUtils.validate_is_non_empty_list(
            null_values)
        self.null_values = null_values
        PandasValidationUtils.log_init_arguments(self)

    def validate(self, data: pd.DataFrame) -> dict:
        """
        Validate the dataset for column dependencies.

        Args:
            data (pd.DataFrame): The dataset to validate.

        Returns:
            dict: Validation result with the following keys:
                - "validator" (str): Name of the validator.
                - "is_valid" (bool): Whether the validation passed.
                - "errors" (list): List of errors, if any.
                - "invalid_rows" (pd.DataFrame): DataFrame of rows violating
                    the dependencies.
                - "missing_columns" (list): List of missing columns.
        """
        PandasValidationUtils.validate_is_dataframe(
            data,
            'data')
        log_message(
            "info",
            "Starting column dependency validation.")
        errors = []
        invalid_rows = pd.DataFrame()
        missing_columns = []

        try:
            for col, required_col in self.dependencies.items():
                if col in data.columns and required_col in data.columns:
                    invalid = data[col].notnull() & data[required_col].isin(
                        self.null_values)
                    invalid_data = data[invalid]

                    if not invalid_data.empty:
                        errors.append({
                            "error_type": "dependency_violation",
                            "details": f"Column '{required_col}' "
                            f"is required when '{col}' is not null."
                        })
                        invalid_rows = pd.concat(
                            [invalid_rows, invalid_data],
                            ignore_index=True)
                else:
                    # Track missing columns
                    if col not in data.columns:
                        missing_columns.append(col)
                        errors.append({
                            "error_type": "missing_column",
                            "details": f"Column '{col}' is " +
                            "missing from the dataset."
                        })
                    if required_col not in data.columns:
                        missing_columns.append(required_col)
                        errors.append({
                            "error_type": "missing_column",
                            "details": f"Column '{required_col}' " +
                            "is missing from the dataset."
                        })

            # Prepare result
            result = {
                "validator": "PandasColumnDependencyValidator",
                "is_valid": not bool(errors),
                "errors": errors,
                "invalid_rows": invalid_rows.drop_duplicates().reset_index(
                    drop=True),
                "missing_columns": list(set(missing_columns))
            }

            if result["is_valid"]:
                log_message(
                    "info",
                    "Column dependency validation passed.")
            else:
                log_message(
                    "error",
                    "Column dependency validation failed: " +
                    f"{len(errors)} errors found.")

            return result

        except Exception as e:
            error_message = (
                f"Error during column dependency validation: {e}"
            )
            log_message(
                "error",
                error_message)
            raise Exception(error_message) from e


class PandasSchemaValidator(Validator):
    """
    Validator to ensure a Pandas DataFrame adheres to a predefined schema.

    This validator checks:
        - Presence of required columns.
        - Data types of specified columns.
        - Optional strict column order.
        - Allowance of extra columns.

    Attributes:
        schema (dict): A dictionary mapping column names to their expected
            Pandas dtypes.
        enforce_order (bool): Enforce the column order strictly
            (default: False).
        allow_extra_columns (bool): Allow extra columns not defined in schema
            (default: True).

    # Example Usage
    if __name__ == "__main__":
        # Step 1: Define schema
        schema = {
            "col1": "int64",
            "col2": "float64",
            "col3": "object"
        }

        # Step 2: Create sample data
        valid_data = pd.DataFrame({
            "col1": [1, 2, 3],
            "col2": [1.1, 2.2, 3.3],
            "col3": ["A", "B", "C"]
        })

        invalid_data = pd.DataFrame({
            "col1": [1, "wrong", 3],     # Wrong type in col1
            "col2": [1.1, 2.2, "oops"],  # Wrong type in col2
            "extra": [0, 1, 2]           # Extra column
        })

        # Step 3: Initialize the validator
        validator = PandasSchemaValidator(
            schema, enforce_order=True,
            allow_extra_columns=False)

        # Step 4: Validate valid data
        print("Valid Data Report:")
        valid_report = validator.validate(valid_data)
        print(valid_report)

        # Step 5: Validate invalid data
        print("\nInvalid Data Report:")
        invalid_report = validator.validate(invalid_data)
        display(invalid_report)

    """

    def __init__(
        self,
        schema: dict[str, str],
        enforce_order: bool = False,
        allow_extra_columns: bool = True
    ):
        """
        Initialize the schema validator.

        Args:
            schema (dict): A dictionary where keys are column names and values
                are Pandas data types.
            enforce_order (bool): If True, enforce exact column order.
                Defaults to False.
            allow_extra_columns (bool): If False, extra columns in the
                DataFrame trigger validation failure.
        """
        if not isinstance(schema, dict):
            error_message = (
                f"Invalid schema: {schema}. " +
                "Schema must be a dictionary of column names " +
                "and their expected data types."
            )
            log_message(
                "error",
                error_message)
            raise ValueError(error_message)
        self.schema = schema
        PandasValidationUtils.validate_is_boolean(
            enforce_order,
            'enforce_order')
        self.enforce_order = enforce_order
        PandasValidationUtils.validate_is_boolean(
            allow_extra_columns,
            'allow_extra_columns')
        self.allow_extra_columns = allow_extra_columns
        PandasValidationUtils.log_init_arguments(
            self)

    def validate(self, data: pd.DataFrame) -> dict[str, Any]:
        """
        Validate a DataFrame against the schema.

        Args:
            data (pd.DataFrame): The Pandas DataFrame to validate.

        Returns:
            dict: A validation report containing:
                - "validator" (str): Name of the validator.
                - "is_valid" (bool): Overall validation status.
                - "errors" (list): List of errors found during validation.
                - "invalid_columns" (list): Columns failing schema validation.
        """
        PandasValidationUtils.validate_is_dataframe(data, 'data')
        log_message(
            "info",
            "Starting schema validation.")

        errors = []
        invalid_columns = []

        # Step 1: Check for missing columns
        missing_columns = PandasValidationUtils.check_missing_columns(
            data,
            list(self.schema.keys()))
        if missing_columns:
            errors.append(
                {"error_type": "missing_columns",
                    "details": f"Missing columns: {missing_columns}"})
            invalid_columns.extend(missing_columns)

        # Step 2: Check for extra columns
        if not self.allow_extra_columns:
            extra_columns = [
                col for col in data.columns if col not in self.schema]
            if extra_columns:
                errors.append(
                    {"error_type": "extra_columns",
                        "details": f"Extra columns detected: {extra_columns}"})
                invalid_columns.extend(extra_columns)

        # Step 3: Check for data type mismatches
        for column, expected_type in self.schema.items():
            if column in data.columns:
                if not PandasValidationUtils.check_column_dtype(
                    data[column],
                    expected_type
                ):
                    errors.append({
                        "error_type": "type_mismatch",
                        "details": f"Column '{column}' has "
                        f"incorrect type '{data[column].dtype}'. "
                        f"Expected '{expected_type}'."
                    })
                    invalid_columns.append(column)

        # Step 4: Enforce column order (optional)
        if self.enforce_order:
            expected_order = list(self.schema.keys())
            actual_order = list(data.columns)
            if expected_order != actual_order:
                errors.append({
                    "error_type": "column_order",
                    "details": f"Column order mismatch. Expected: "
                    f"{expected_order}, Got: {actual_order}"
                })

        # Prepare final result
        result = {
            "validator": "PandasSchemaValidator",
            "is_valid": len(errors) == 0,
            "errors": errors,
            "invalid_columns": list(set(invalid_columns))
        }

        log_message(
            "info",
            f"Schema validation completed. Valid: {result['is_valid']}")
        return result


class PandasValidatorFactory(ValidatorFactory):
    """
    Factory class for creating various types of Pandas validators.

    Example Usage:
        # Initialize the factory
        factory = PandasValidatorFactory()

        # Create a Missing Columns Validator
        missing_columns_validator = factory.create_missing_columns_validator(
            required_columns=["col1", "col2"]
        )
        data = pd.DataFrame({
            "col1": [1, 2, 3],
            "col3": [4, 5, 6]
        })
        result = missing_columns_validator.validate(data)
        print(result)
        # Output:
        # {
        #     "validator": "PandasMissingColumnsValidator",
        #     "is_valid": False,
        #     "errors": [
        #         {"error_type": "missing_columns",
        # "details": "Missing columns: {'col2'}"}
        #     ],
        #     "invalid_columns": ["col2"]
        # }

        # Create a Range Validator
        range_validator = factory.create_value_range_validator(
            column_ranges={"col1": (0, 5)},
            inclusive=True
        )
        result = range_validator.validate(data)
        print(result)
        # Output:
        # {
        #     "validator": "PandasRangeValidator",
        #     "is_valid": True,
        #     "errors": [],
        #     "invalid_rows": pd.DataFrame(...),
        #     "missing_columns": []
        # }

    Methods:
        create_missing_columns_validator(required_columns: list) -> Validator
        create_extra_columns_validator(allowed_columns: list) -> Validator
        create_data_type_validator(schema: dict) -> Validator
        create_null_value_validator(
            critical_columns: list, null_values=None) -> Validator
        create_value_range_validator(
            column_ranges: dict, inclusive: bool = True) -> Validator
        create_uniqueness_validator(unique_columns: list) -> Validator
        create_rowCount_validator(
            min_rows: int = None, max_rows: int = None) -> Validator
        create_non_empty_validator() -> Validator
        create_value_validator(
            column_values: dict, allow_only: bool = True) -> Validator
        create_referential_integrity_validator(
            column: str, reference_data: pd.Series) -> Validator
        create_regex_validator(column_patterns: dict) -> Validator
        create_duplicate_row_validator() -> Validator
        create_column_dependency_validator(dependencies: dict) -> Validator
    """
    def __init__(self):
        """
        Initialize the PandasValidatorFactory.

        """

    def log_creation(self, validator_name: str, **params):
        """
        Log the creation of a validator.

        Args:
            validator_name (str): Name of the validator being created.
            params (dict): Parameters used to create the validator.
        """
        log_message(
            "info",
            f"Creating {validator_name} with parameters: {params}")

    def create_extra_columns_validator(
        self,
        allowed_columns: list
    ) -> Validator:
        self.log_creation(
            "PandasExtraColumnsValidator",
            allowed_columns=allowed_columns)
        if not isinstance(allowed_columns, list):
            error_message = (
                "allowed_columns must be a list.")
            log_message(
                "error",
                error_message)
            raise ValueError(error_message)
        return PandasExtraColumnsValidator(allowed_columns=allowed_columns)

    def create_missing_columns_validator(
        self,
        required_columns: list
    ) -> Validator:
        self.log_creation(
            "PandasMissingColumnsValidator",
            required_columns=required_columns)
        if not isinstance(required_columns, list):
            error_message = (
                "required_columns must be a list."
            )
            log_message(
                "error",
                error_message)
            raise ValueError(error_message)
        return PandasMissingColumnsValidator(required_columns)

    def create_data_type_validator(self, schema: dict) -> Validator:
        self.log_creation("PandasDataTypeValidator", schema=schema)
        if not isinstance(schema, dict):
            error_message = (
                "schema must be a dictionary."
            )
            log_message(
                "error",
                error_message)
            raise ValueError(error_message)
        return PandasDataTypeValidator(expected_schema=schema)

    def create_null_value_validator(
        self,
        critical_columns: list,
        null_values=None
    ) -> Validator:
        self.log_creation(
            "PandasNullValueValidator",
            critical_columns=critical_columns,
            null_values=null_values)
        return PandasNullValueValidator(
            critical_columns=critical_columns,
            null_values=null_values)

    def create_value_range_validator(
        self,
        column_ranges: dict,
        inclusive: bool = True
    ) -> Validator:
        self.log_creation(
            "PandasRangeValidator",
            column_ranges=column_ranges,
            inclusive=inclusive)
        return PandasRangeValidator(
            column_ranges=column_ranges,
            inclusive=inclusive)

    def create_uniqueness_validator(
        self,
        unique_columns: list
    ) -> Validator:
        self.log_creation(
            "PandasUniquenessValidator",
            unique_columns=unique_columns)
        return PandasUniquenessValidator(unique_columns=unique_columns)

    def create_rowCount_validator(
        self,
        min_rows: int = None,
        max_rows: int = None
    ) -> Validator:
        self.log_creation(
            "PandasRowCountValidator",
            min_rows=min_rows,
            max_rows=max_rows)
        return PandasRowCountValidator(min_rows=min_rows, max_rows=max_rows)

    def create_non_empty_validator(self) -> Validator:
        self.log_creation("PandasNonEmptyValidator")
        return PandasNonEmptyValidator()

    def create_value_validator(
        self,
        column_values: dict,
        allow_only: bool = True
    ) -> Validator:
        self.log_creation(
            "PandasValueValidator",
            column_values=column_values,
            allow_only=allow_only)
        return PandasValueValidator(
            column_values=column_values,
            allow_only=allow_only)

    def create_referential_integrity_validator(
        self,
        column: str,
        reference_data: pd.Series
    ) -> Validator:
        self.log_creation(
            "PandasReferentialIntegrityValidator",
            column=column,
            reference_data=reference_data)
        return PandasReferentialIntegrityValidator(
            column=column,
            reference_data=reference_data)

    def create_regex_validator(
        self,
        column_patterns: dict
    ) -> Validator:
        self.log_creation(
            "PandasRegexValidator",
            column_patterns=column_patterns)
        return PandasRegexValidator(column_patterns=column_patterns)

    def create_duplicate_row_validator(self) -> Validator:
        self.log_creation("PandasDuplicateRowsValidator")
        return PandasDuplicateRowsValidator()

    def create_column_dependency_validator(
        self,
        dependencies: dict
    ) -> Validator:
        self.log_creation(
            "PandasColumnDependencyValidator",
            dependencies=dependencies)
        return PandasColumnDependencyValidator(dependencies=dependencies)

    def create_schema_validator(
        self,
        schema: dict,
        enforce_order: bool = False,
        allow_extra_columns: bool = True
    ) -> Validator:
        self.log_creation(
            "PandasSchemaValidator",
            schema=schema,
            enforce_order=enforce_order,
            allow_extra_columns=allow_extra_columns)
        return PandasSchemaValidator(
            schema=schema,
            enforce_order=enforce_order,
            allow_extra_columns=allow_extra_columns)


class PandasValidatorProvider(ValidatorProvider):
    """
    Provider class to create Pandas validators dynamically based on the
    validation type.

    This class uses an instance of `PandasValidatorFactory` to create
    validators for different
    validation types as defined in the `ValidationType` enum.

    Example Usage:
        factory = PandasValidatorFactory()
        provider = PandasValidatorProvider(factory)

        # Example 1: Missing Columns Validation
        missing_validator = provider.create_validator(
            validation_type=ValidationType.MISSING_COLUMNS,
            required_columns=["col1", "col2"]
        )
        data = pd.DataFrame({"col1": [1, 2]})
        result = missing_validator.validate(data)
        print(result)

        # Example 2: Range Validation
        range_validator = provider.create_validator(
            validation_type=ValidationType.VALUE_RANGE,
            column_ranges={"col1": (0, 100)}
        )
        data = pd.DataFrame({"col1": [-1, 50, 101]})
        result = range_validator.validate(data)
        print(result)

    Methods:
        create_validator(
            validation_type: ValidationType, **options) -> Validator:
            Dynamically creates the appropriate validator based on the
            validation type and options.
    """

    def __init__(
        self,
        factory: PandasValidatorFactory
    ):
        """
        Initialize the PandasValidatorProvider.

        Args:
            factory (PandasValidatorFactory): An instance of the
                PandasValidatorFactory to create validators.
        """
        if factory:

            PandasValidationUtils.validate_inheritance(
                factory,
                ValidatorFactory,
                'factory')
        self.factory = factory or PandasValidatorFactory()

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
                    required_keys=["column", "reference_data"],
                    entity_type="validation",
                    entity_name="REFERENTIAL_INTEGRITY")
                return self.factory.create_referential_integrity_validator(
                    column=options["column"],
                    reference_data=options["reference_data"])

            case ValidationType.REGEX:
                validate_options(
                    options=options,
                    required_keys=["column_patterns"],
                    entity_type="validation",
                    entity_name="REGEX")
                return self.factory.create_regex_validator(
                    column_patterns=options["column_patterns"])

            case ValidationType.DUPLICATE_ROWS:
                return self.factory.create_duplicate_row_validator()

            case ValidationType.COLUMN_DEPENDENCY:
                validate_options(
                    options=options,
                    required_keys=["dependencies"],
                    entity_type="validation",
                    entity_name="COLUMN_DEPENDENCY")
                return self.factory.create_column_dependency_validator(
                    dependencies=options["dependencies"])

            case ValidationType.SCHEMA:
                validate_options(
                    options=options,
                    required_keys=[
                        "schema",
                        "enforce_order",
                        "allow_extra_columns"],
                    entity_type="validation",
                    entity_name="SCHEMA")
                return self.factory.create_schema_validator(
                    schema=options["schema"],
                    enforce_order=options["enforce_order"],
                    allow_extra_columns=options["allow_extra_columns"])

            case _:
                error_message = (
                    f"Unsupported validation type: {validation_type}"
                )
                log_message(
                    "error",
                    error_message)
                raise ValueError(error_message)


class PandasColumnRenamer(Transformer):
    """
    Transformer to rename columns in a Pandas DataFrame.

    Attributes:
        column_map (dict): A dictionary where keys are the current column
        names and values are the new column names.

    Example Usage:
        column_map = {"old_col1": "new_col1", "old_col2": "new_col2"}
        column_renamer = PandasColumnRenamer(column_map=column_map)
        transformed_data = column_renamer.transform(data)
    """

    def __init__(
        self,
        column_map: dict
    ):
        """
        Initialize the PandasColumnRenamer.

        Args:
            column_map (dict): A dictionary mapping current column names
            to new column names.

        Raises:
            ValueError: If column_map is not a dictionary or is empty.
        """
        PandasValidationUtils.validate_is_non_empty_dict(
            column_map)
        self.column_map = column_map
        PandasValidationUtils.log_init_arguments(
            self)

    def transform(
        self,
        data: pd.DataFrame,
        **kwargs
    ) -> pd.DataFrame:
        """
        Rename columns in the DataFrame.

        Args:
            data (pd.DataFrame): The input DataFrame.
            **kwargs: Additional parameters for DataFrame.rename()

        Returns:
            pd.DataFrame: The DataFrame with renamed columns.

        Raises:
            KeyError: If any column in the column_map does not exist in
            the DataFrame.
        """

        PandasValidationUtils.validate_is_dataframe(
            data,
            name="data")
        PandasValidationUtils.validate_columns_exist(
            data,
            list(self.column_map.keys()))

        # Validate kwargs for DataFrame.rename()
        validate_kwargs(data.rename, kwargs)

        log_message(
            "info",
            f"Renaming columns using column_map: {self.column_map}")
        return data.rename(columns=self.column_map, **kwargs)


class PandasColumnDropper(Transformer):
    """
    Transformer to drop specified columns from a Pandas DataFrame.

    Attributes:
        columns_to_drop (list): List of column names to drop.

    Example Usage:
        columns_to_drop = ["col1", "col2"]
        column_dropper = PandasColumnDropper(columns_to_drop=columns_to_drop)
        transformed_data = column_dropper.transform(data)
    """

    def __init__(self, columns_to_drop: list):
        """
        Initialize the PandasColumnDropper.

        Args:
            columns_to_drop (list): List of column names to drop.

        Raises:
            ValueError: If columns_to_drop is not a list or is empty.
        """
        PandasValidationUtils.validate_is_non_empty_list(
            columns_to_drop)
        self.columns_to_drop = columns_to_drop
        PandasValidationUtils.log_init_arguments(
            self)

    def transform(self, data: pd.DataFrame, **kwargs) -> pd.DataFrame:
        """
        Drop specified columns from the DataFrame.

        Args:
            data (pd.DataFrame): The input DataFrame.
            **kwargs: Additional parameters for DataFrame.drop()

        Returns:
            pd.DataFrame: The DataFrame with specified columns dropped.

        Raises:
            KeyError: If any column in columns_to_drop does not exist in
            the DataFrame.
        """
        PandasValidationUtils.validate_is_dataframe(
            data,
            name="data")
        # Validate columns to drop exist in the DataFrame
        PandasValidationUtils.validate_columns_exist(
            data,
            self.columns_to_drop)
        # Validate kwargs for DataFrame.drop()
        validate_kwargs(data.drop, kwargs)

        log_message(
            "info",
            f"Dropping columns: {self.columns_to_drop}")
        return data.drop(
            columns=self.columns_to_drop,
            **kwargs)


class PandasValueReplacer(Transformer):
    """
    Transformer to replace values in specified columns of a Pandas DataFrame.

    Attributes:
        value_map (dict): A dictionary where keys are column names, and values
            are dictionaries mapping old values to new values.

    Example Usage:
        value_replacer = PandasValueReplacer(
            value_map={
                "column1": {
                    "old_value1": "new_value1", "old_value2": "new_value2"},
                "column2": {"old_value3": "new_value3"}
            }
        )
        transformed_data = value_replacer.transform(data)
    """

    def __init__(
        self,
        value_map: dict
    ):
        """
        Initialize the PandasValueReplacer.

        Args:
            value_map (dict): Dictionary specifying columns and their
            respective value mappings.

        Raises:
            ValueError: If value_map is not a dictionary.
        """
        PandasValidationUtils.validate_is_non_empty_dict(value_map)
        self.value_map = value_map
        PandasValidationUtils.log_init_arguments(self)

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Replace values in the specified columns based on the value_map.

        Args:
            data (pd.DataFrame): Input DataFrame to transform.

        Returns:
            pd.DataFrame: Transformed DataFrame.

        Raises:
            KeyError: If any column in value_map is missing from the DataFrame.
        """
        PandasValidationUtils.validate_is_dataframe(data, "data")
        log_message("info", "Starting value replacement transformation.")
        transformed_data = data.copy()

        for column, replacements in self.value_map.items():
            if column not in transformed_data.columns:
                error_message = (
                    f"Column '{column}' not found in DataFrame. "
                )
                log_message(
                    "error",
                    error_message)
                raise KeyError(error_message)

            log_message(
                "info",
                f"Replacing values in column '{column}'.")
            transformed_data[column] = transformed_data[column].replace(
                replacements)

        log_message("info", "Value replacement transformation completed.")
        return transformed_data


class PandasColumnReorderer(Transformer):
    """
    Transformer to reorder columns in a Pandas DataFrame.

    Attributes:
        retain_unspecified (bool): If True, columns not in `column_order`
        are appended at the end.

    Example Usage:
        reorderer = PandasColumnReorderer(
            column_order=["Plant Name", "Process"],
            retain_unspecified=True
        )
        transformed_data = reorderer.transform(data)
    """

    def __init__(
        self,
        column_order: list,
        retain_unspecified: bool = False
    ):
        """
        Initialize the PandasColumnReorderer.

        Args:
            column_order (list): List specifying the desired order of columns.
            retain_unspecified (bool): Whether to retain columns not
            in `column_order`.

        Raises:
            ValueError: If column_order is not a list or is empty.
        """
        PandasValidationUtils.validate_is_non_empty_list(
            column_order)
        PandasValidationUtils.validate_is_boolean(
            retain_unspecified,
            'retain_unspecified')
        self.column_order = column_order
        self.retain_unspecified = retain_unspecified
        PandasValidationUtils.log_init_arguments(
            self)

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Reorder columns in the DataFrame.

        Args:
            data (pd.DataFrame): The input DataFrame.

        Returns:
            pd.DataFrame: The DataFrame with reordered columns.
        """
        PandasValidationUtils.validate_is_dataframe(
            data,
            name="data")
        # Validate that specified columns exist
        PandasValidationUtils.validate_columns_exist(
            data,
            self.column_order)
        # Determine the final column order
        existing_cols = [
            col for col in self.column_order if col in data.columns]
        if self.retain_unspecified:
            unspecified_cols = [
                col for col in data.columns if col not in self.column_order]
            final_order = existing_cols + unspecified_cols
        else:
            final_order = existing_cols

        log_message(
            "info",
            f"Final column order: {final_order}")
        return data[final_order]


class PandasColumnAdder(Transformer):
    """
    Transformer to add a new column to a Pandas DataFrame.

    This class supports:
    1. Static Value Assignment: Assign a single value to the new column.
    2. Column Copying: Copy values from an existing column to the new column.
    3. Expression-Based Computation: Compute the column using a Pandas
        `eval()` expression.
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
    Example:
        column_adder_non_static = PandasColumnAdderStatic(
        column_name="status",
        value = "default_value")

        column_adder = PandasColumnAdder(
            column_name="New Column",
            aggregation={"columns" : ["col1","col2"],
                        "agg_func":sum})
    """

    def __init__(
        self,
        column_name: str,
        value: Any = None,
        aggregation: dict = None
    ):
        """
        Initialize the PandasColumnAdder.

        Args:
            column_name (str): The name of the new column to be added.
            value (Any or Callable or str, optional): Specifies the values
            for the new column.
            aggregation (dict, optional): Settings for column aggregation:
                - columns (list): List of column names to aggregate.
                - agg_func (Callable): Aggregation function (e.g., sum, mean).

        Raises:
            ValueError: If both `value` and `aggregation` are None.
            ValueError: If aggregation is provided but improperly defined.
        """

        if value is None and aggregation is None:
            error_message = (
                "Both value and aggregation are None. " +
                "Either value or aggregation must be provided."
            )
            log_message(
                "error",
                error_message)
            raise ValueError(error_message)

        if aggregation:
            if not isinstance(aggregation, dict) or "columns" not in (
                    aggregation) or "agg_func" not in aggregation:
                error_message = (
                    "Aggregation must be a dictionary with "
                    "keys 'columns' and 'agg_func'."
                )
                log_message(
                    "error",
                    error_message)
                raise ValueError(error_message)

        PandasValidationUtils.validate_is_non_empty_string(
            column_name)
        self.column_name = column_name
        self.value = value
        self.aggregation = aggregation
        PandasValidationUtils.log_init_arguments(
            self)

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Add the new column to the DataFrame.

        Args:
            data (pd.DataFrame): The input DataFrame.

        Returns:
            pd.DataFrame: The DataFrame with the new column added.
        """
        PandasValidationUtils.validate_is_dataframe(
            data,
            name="data")
        try:
            if self.aggregation:
                # Perform multi-column aggregation
                columns = self.aggregation.get("columns", [])
                agg_func = self.aggregation.get("agg_func", None)

                # Validate columns exist
                PandasValidationUtils.validate_columns_exist(
                    data,
                    columns)
                # Apply the aggregation function
                log_message(
                    "info",
                    f"Aggregating columns {columns} into "
                    f"'{self.column_name}' using {agg_func.__name__}."
                )
                data[self.column_name] = data[columns].apply(agg_func, axis=1)

            elif callable(self.value):
                # Compute column values dynamically using a callable
                log_message(
                    "info",
                    f"Computing column '{self.column_name}' using a callable.")
                data[self.column_name] = self.value(data)

            elif isinstance(
                    self.value, str) and self.value.strip() in data.columns:
                # Copy values from an existing column
                log_message(
                    "info",
                    f"Copying column '{self.value}' to '{self.column_name}'.")
                data[self.column_name] = data[self.value]

            elif isinstance(self.value, str):
                # Evaluate expression
                log_message(
                    "info",
                    f"Computing column '{self.column_name}' "
                    f"using expression: {self.value}.")
                data[self.column_name] = self.value

            else:
                # Assign static value
                log_message(
                    "info",
                    f"Assigning static value '{self.value}' "
                    f"to column '{self.column_name}'.")
                data[self.column_name] = self.value

            log_message(
                "info",
                f"Column '{self.column_name}' added successfully.")

        except Exception as e:
            error_message = (
                "Error while adding column " +
                f"'{self.column_name}': {e}")
            log_message(
                "error",
                error_message)
            raise Exception(error_message) from e

        return data


class PandasColumnNameStandardizer(Transformer):
    """
    Transformer to standardize column names in a Pandas DataFrame, with
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
        standardizer = PandasColumnNameStandardizer(case_style="snake_case",
        exclude_columns=["ID", "Date"])
        transformed_data = standardizer.transform(data)
    """

    def __init__(
        self,
        case_style: str = "snake_case",
        exclude_columns: list = None
    ):
        """
        Initialize the PandasColumnNameStandardizer.

        Args:
            case_style (str): The desired case style for column names.
            exclude_columns (list, optional): List of column names to exclude
                from standardization.

        Raises:
            ValueError: If an invalid `case_style` is provided.
        """
        valid_styles = ["snake_case",
                        "camelCase",
                        "PascalCase",
                        "lowercase",
                        "uppercase"]
        PandasValidationUtils.validate_is_non_empty_string(
            case_style)
        PandasValidationUtils.validate_case_style(
            case_style,
            valid_styles)
        self.case_style = case_style
        self.exclude_columns = exclude_columns
        PandasValidationUtils.log_init_arguments(
            self)

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize column names in the DataFrame, excluding specified columns.

        Args:
            data (pd.DataFrame): The input DataFrame.

        Returns:
            pd.DataFrame: The DataFrame with standardized column names.

        Raises:
            KeyError: If any columns in `exclude_columns` do not exist in the
            DataFrame.
        """

        PandasValidationUtils.validate_is_dataframe(
            data,
            name="data")

        # Validate excluded columns
        if self.exclude_columns is None:
            self.exclude_columns = []
        else:
            PandasValidationUtils.validate_columns_exist(
                data,
                self.exclude_columns)

        log_message(
            "info",
            "Standardizing column names.")
        new_columns = [
            col if col in self.exclude_columns else
            PandasValidationUtils.transform_column_name(col, self.case_style)
            for col in data.columns
        ]

        data.columns = new_columns
        log_message(
            "info",
            f"Column names standardized: {new_columns}")
        return data


class PandasColumnNamePrefixSuffix(Transformer):
    """
    Transformer to add a prefix or suffix to column names in a
    Pandas DataFrame, with support for excluding specific columns.

    Attributes:
        prefix (str): The prefix to add to column names. Defaults to an
            empty string.
        suffix (str): The suffix to add to column names. Defaults to an
            empty string.
        exclude_columns (list): List of column names to exclude from
            the transformation.

    Example Usage:
        prefixer = PandasColumnNamePrefixSuffix(
            prefix="prod_",
            exclude_columns=["ID", "Date"])
        transformed_data = prefixer.transform(data)
    """

    def __init__(
        self,
        prefix: str = "",
        suffix: str = "",
        exclude_columns: list = None
    ):
        """
        Initialize the PandasColumnNamePrefixSuffix.

        Args:
            prefix (str): The prefix to add to column names. Defaults to
                an empty string.
            suffix (str): The suffix to add to column names. Defaults to
                an empty string.
            exclude_columns (list, optional): List of column names to exclude
                from the transformation.

        Raises:
            ValueError: If `prefix` or `suffix` is not a string.
        """
        if prefix:
            PandasValidationUtils.validate_is_non_empty_string(
                prefix)
        if suffix:
            PandasValidationUtils.validate_is_non_empty_string(
                suffix)
        self.prefix = prefix
        self.suffix = suffix
        self.exclude_columns = exclude_columns
        PandasValidationUtils.log_init_arguments(
            self)

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Add a prefix or suffix to column names, excluding specified columns.

        Args:
            data (pd.DataFrame): The input DataFrame.

        Returns:
            pd.DataFrame: The DataFrame with updated column names.

        Raises:
            KeyError: If any columns in `exclude_columns` do not exist in
            the DataFrame.
        """
        PandasValidationUtils.validate_is_dataframe(
            data,
            name="data")
        # Validate excluded columns
        if self.exclude_columns is None:
            self.exclude_columns = []
        else:
            PandasValidationUtils.validate_columns_exist(
                data,
                self.exclude_columns)
        log_message(
            "info",
            f"Adding prefix '{self.prefix}' and suffix "
            f"'{self.suffix}' to column names.")
        updated_columns = [
            PandasValidationUtils.add_prefix_suffix_to_columns(
                col,
                self.prefix,
                self.suffix)
            if col not in self.exclude_columns else col
            for col in data.columns
        ]

        data.columns = updated_columns
        log_message(
            "info",
            f"Updated column names: {data.columns.tolist()}")
        return data


class PandasColumnNameRegexRenamer(Transformer):
    """
    Transformer to rename column names in a Pandas DataFrame using
    regex patterns, with support for excluding specific columns.

    Attributes:
        pattern (str): The regex pattern to search for in column names.
        replacement (str): The replacement string for matching patterns.
        exclude_columns (list): List of column names to exclude from
            the transformation.

    Example Usage:
        renamer = PandasColumnNameRegexRenamer(
            pattern=r"[^a-zA-Z0-9]", replacement="_",
            exclude_columns=["ID", "Date"])
        transformed_data = renamer.transform(data)
    """

    def __init__(
        self,
        pattern: str,
        replacement: str,
        exclude_columns: list = None
    ):
        """
        Initialize the PandasColumnNameRegexRenamer.

        Args:
            pattern (str): The regex pattern to search for.
            replacement (str): The string to replace matching patterns with.
            exclude_columns (list, optional): List of column names to
                exclude from transformation.

        Raises:
            ValueError: If `pattern` or `replacement` is not a string.
        """
        PandasValidationUtils.validate_is_non_empty_string(
            pattern)
        PandasValidationUtils.validate_is_non_empty_string(
            replacement)
        self.pattern = pattern
        self.replacement = replacement
        self.exclude_columns = exclude_columns
        PandasValidationUtils.log_init_arguments(
            self)

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Rename columns using regex patterns, excluding specified columns.

        Args:
            data (pd.DataFrame): The input DataFrame.

        Returns:
            pd.DataFrame: The DataFrame with updated column names.

        Raises:
            KeyError: If any columns in `exclude_columns` do not exist in
            the DataFrame.
        """
        PandasValidationUtils.validate_is_dataframe(
            data,
            name="data")
        # Validate excluded columns
        if self.exclude_columns is None:
            self.exclude_columns = []
        else:
            PandasValidationUtils.validate_columns_exist(
                data,
                self.exclude_columns)

        log_message(
            "info",
            f"Renaming columns using pattern "
            f"'{self.pattern}' with replacement '{self.replacement}'.")

        updated_columns = [
            PandasValidationUtils.rename_column_with_regex(
                col, self.pattern,
                self.replacement)
            if col not in self.exclude_columns else col
            for col in data.columns
        ]

        data.columns = updated_columns
        log_message(
            "info",
            f"Updated column names: {data.columns.tolist()}")
        return data


class PandasColumnAdderStatic(Transformer):
    """
    Transformer to add a column with a static value to a Pandas DataFrame.

    Attributes:
        column_name (str): The name of the new column.
        value (Any): The static value to assign to the new column.
        overwrite (bool): Whether to overwrite the column if it already exists.

    Example Usage:
        static_adder = PandasColumnAdderStatic(
            column_name="status", value="active", overwrite=False)
        transformed_data = static_adder.transform(data)
    """

    def __init__(self, column_name: str, value: Any, overwrite: bool = False):
        """
        Initialize the PandasColumnAdderStatic.

        Args:
            column_name (str): The name of the new column.
            value (Any): The static value to assign to the new column.
            overwrite (bool, optional): Whether to overwrite the column if
            it already exists. Defaults to False.

        Raises:
            ValueError: If `column_name` is not a string.
        """
        PandasValidationUtils.validate_is_non_empty_string(
            column_name)
        PandasValidationUtils.validate_is_boolean(
            overwrite,
            'overwrite')
        self.column_name = column_name
        self.value = value
        self.overwrite = overwrite
        PandasValidationUtils.log_init_arguments(
            self)

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Add a new column with a static value.

        Args:
            data (pd.DataFrame): The input DataFrame.

        Returns:
            pd.DataFrame: The DataFrame with the new column added.

        Raises:
            ValueError: If `column_name` already exists and
            `overwrite` is False.
        """
        PandasValidationUtils.validate_is_dataframe(
            data,
            name="data")
        if self.column_name in data.columns and not self.overwrite:
            log_message(
                "error",
                f"Column '{self.column_name}' " +
                "already exists and overwrite is set to False.")
            raise ValueError(
                f"Column '{self.column_name}' already exists. " +
                "Set overwrite=True to replace it.")

        try:
            if self.column_name in data.columns and self.overwrite:
                log_message(
                    "warning",
                    f"Overwriting existing column '{self.column_name}'.")
            data[self.column_name] = self.value
            log_message(
                "info",
                f"Successfully added column '{self.column_name}' "
                f"with static value: {self.value}")
        except Exception as e:
            error_message = (
                f"Error adding static column '{self.column_name}': {e}"
            )
            log_message(
                "error",
                error_message)
            raise Exception(error_message) from e
        return data


class PandasColumnPatternDropper(Transformer):
    """
    Transformer to drop columns from a Pandas DataFrame based on a
    regex pattern.

    Attributes:
        pattern (str): The regex pattern to match column names.
        exclude_columns (list): List of column names to exclude from
        being dropped.

    Example Usage:
        pattern_dropper = PandasColumnPatternDropper(
            pattern=r"temp_.*", exclude_columns=["temp_keep"])
        transformed_data = pattern_dropper.transform(data)
    """

    def __init__(
        self,
        pattern: str,
        exclude_columns: list = None
    ):
        """
        Initialize the PandasColumnPatternDropper.

        Args:
            pattern (str): The regex pattern to match column names.
            exclude_columns (list, optional): List of column names to exclude
            from dropping.

        Raises:
            ValueError: If `pattern` is not a string.
        """
        PandasValidationUtils.validate_is_non_empty_string(
            pattern)
        self.pattern = pattern
        self.exclude_columns = exclude_columns
        PandasValidationUtils.log_init_arguments(
            self)

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Drop columns matching the regex pattern.

        Args:
            data (pd.DataFrame): The input DataFrame.

        Returns:
            pd.DataFrame: The DataFrame with matching columns dropped.

        Raises:
            KeyError: If any columns in `exclude_columns` do not exist in
            the DataFrame.
        """
        PandasValidationUtils.validate_is_dataframe(
            data,
            name="data")
        if self.exclude_columns is None:
            self.exclude_columns = []
        else:
            PandasValidationUtils.validate_columns_exist(
                data,
                self.exclude_columns)
        # Identify columns matching the pattern
        matching_columns = PandasValidationUtils.get_columns_matching_pattern(
            data,
            self.pattern)
        log_message(
            "info",
            f"Columns matching pattern '{self.pattern}': {matching_columns}")

        # Exclude specified columns
        columns_to_drop = [
            col for col in matching_columns if col not in self.exclude_columns]
        log_message(
            "info",
            f"Columns to drop (after exclusions): {columns_to_drop}")

        # Drop matching columns
        return data.drop(columns=columns_to_drop, errors="ignore")


class PandasEmptyColumnDropper(Transformer):
    """
    Transformer to drop empty columns (all values are NaN) from a
    Pandas DataFrame.

    Attributes:
        exclude_columns (list): List of column names to exclude from
            being dropped.

    Example Usage:
        empty_dropper = PandasEmptyColumnDropper(
            exclude_columns=["important_column"])
        transformed_data = empty_dropper.transform(data)
    """
    def __init__(
        self,
        exclude_columns: list = None
    ):
        """
        Initialize the PandasEmptyColumnDropper.
        Args:
            exclude_columns (list, optional): List of column names to exclude
            from dropping.
        Raises:
            ValueError: If `exclude_columns` is not a list.
        """
        if exclude_columns:
            PandasValidationUtils.validate_is_non_empty_list(
                exclude_columns)
        self.exclude_columns = exclude_columns
        PandasValidationUtils.log_init_arguments(
            self)

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Drop columns where all values are NaN.

        Args:
            data (pd.DataFrame): The input DataFrame.

        Returns:
            pd.DataFrame: The DataFrame with empty columns dropped.

        Raises:
            KeyError: If any columns in `exclude_columns` do not exist in the
            DataFrame.
        """
        PandasValidationUtils.validate_is_dataframe(
            data,
            name="data")
        # Validate excluded columns
        if self.exclude_columns is None:
            self.exclude_columns = []
        else:
            PandasValidationUtils.validate_columns_exist(
                data,
                self.exclude_columns)
        # Identify empty columns
        empty_columns = PandasValidationUtils.get_empty_columns(data)
        log_message(
            "info",
            f"Empty columns identified: {empty_columns}")

        # Exclude specified columns
        columns_to_drop = [
            col for col in empty_columns if col not in self.exclude_columns]
        log_message(
            "info",
            f"Columns to drop (after exclusions): {columns_to_drop}")

        # Drop empty columns
        return data.drop(columns=columns_to_drop, errors="ignore")


class PandasColumnTypeDropper(Transformer):
    """
    Transformer to drop columns of specific data types from a Pandas DataFrame.

    Attributes:
        data_types (list): List of data types to drop
        (e.g., ["float64", "int64"]).
        exclude_columns (list): List of column names to exclude from
        being dropped.

    Example Usage:
        type_dropper = PandasColumnTypeDropper(
            data_types=["float64"], exclude_columns=["numeric_column"])
        transformed_data = type_dropper.transform(data)
    """

    def __init__(
        self,
        data_types: list,
        exclude_columns: list = None
    ):
        """
        Initialize the PandasColumnTypeDropper.

        Args:
            data_types (list): List of data types to drop
                (e.g., ["float64", "int64"]).
            exclude_columns (list, optional): List of column names to exclude
                from dropping.
        Raises:
            ValueError: If `data_types` is not a non-empty list.
        """
        PandasValidationUtils.validate_is_non_empty_list(
            data_types)
        self.data_types = data_types
        if exclude_columns:
            PandasValidationUtils.validate_is_non_empty_list(
                exclude_columns)
        self.exclude_columns = exclude_columns
        PandasValidationUtils.log_init_arguments(
            self)

    def transform(
        self,
        data: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Drop columns of specified data types.

        Args:
            data (pd.DataFrame): The input DataFrame.

        Returns:
            pd.DataFrame: The DataFrame with specified columns dropped.

        Raises:
            KeyError: If any columns in `exclude_columns` do not exist in
            the DataFrame.
        """
        PandasValidationUtils.validate_is_dataframe(
            data,
            name="data")
        # Validate excluded columns
        if self.exclude_columns is None:
            self.exclude_columns = []
        else:
            PandasValidationUtils.validate_columns_exist(
                data,
                self.exclude_columns)
        # Identify columns of specified data types
        columns_by_dtype = PandasValidationUtils.get_columns_by_dtypes(
            data,
            self.data_types)
        log_message(
            "info",
            f"Columns with data types {self.data_types}: {columns_by_dtype}")

        # Exclude specified columns
        columns_to_drop = [
            col for col in columns_by_dtype if col not in self.exclude_columns]
        log_message(
            "info",
            f"Columns to drop (after exclusions): {columns_to_drop}")

        # Drop specified columns
        return data.drop(columns=columns_to_drop, errors="ignore")


class PandasNullRatioColumnDropper(Transformer):
    """
    Transformer to drop columns with a high percentage of null values from a
    Pandas DataFrame.

    Attributes:
        threshold (float): The maximum null ratio allowed
            (e.g., 0.5 for 50% nulls).
        exclude_columns (list): List of column names to exclude from being
        dropped.

    Example Usage:
        null_ratio_dropper = PandasNullRatioColumnDropper(
            threshold=0.5, exclude_columns=["important_column"])
        transformed_data = null_ratio_dropper.transform(data)
    """

    def __init__(
        self,
        threshold: float,
        exclude_columns: list = None
    ):
        PandasValidationUtils.validate_float(
            threshold,
            'threshold')
        if not (0 <= threshold <= 1):
            error_message = (
                f"threshold must be between 0 and 1, but got {threshold}.")
            log_message(
                "error",
                error_message)
            raise ValueError(error_message)
        self.threshold = threshold
        self.exclude_columns = exclude_columns
        PandasValidationUtils.log_init_arguments(
            self)

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Drop columns with null ratios exceeding the threshold.

        Args:
            data (pd.DataFrame): The input DataFrame.

        Returns:
            pd.DataFrame: The DataFrame with columns dropped based on
            null ratio.
        """
        PandasValidationUtils.validate_is_dataframe(
            data,
            name="data")

        if self.exclude_columns is None:
            self.exclude_columns = []
        else:
            PandasValidationUtils.validate_is_non_empty_list(
                self.exclude_columns)
        columns_to_drop = [
            col for col in data.columns
            if data[col].isna().mean() > self.threshold and col not in
            self.exclude_columns
        ]
        log_message(
            "info",
            f"Columns to drop (based on null ratio): {columns_to_drop}")
        return data.drop(columns=columns_to_drop, errors="ignore")


class PandasColumnSplitter(Transformer):
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
        splitter = PandasColumnSplitter(
            column="full_name",
            pattern=" ",
            regex=False
        )
        transformed_data = splitter.transform(data)
    """

    def __init__(
        self,
        column: str,
        pattern: str,
        regex: bool = False,
        new_columns: list = None
    ):
        """
        Initialize the PandasColumnSplitter.

        Args:
            column (str): The column to split.
            pattern (str): The delimiter or regex pattern to use for splitting.
            regex (bool): Whether to treat the pattern as a regex. Defaults
                to False.
            new_columns (list, optional): List of new column names for
                the split columns.
        """
        PandasValidationUtils.validate_is_non_empty_string(
            column)
        PandasValidationUtils.validate_is_non_empty_string(
            pattern)
        PandasValidationUtils.validate_is_boolean(
            regex,
            'regex')
        if new_columns:
            PandasValidationUtils.validate_is_non_empty_list(
                new_columns)
        self.column = column
        self.pattern = pattern
        self.regex = regex
        self.new_columns = new_columns
        PandasValidationUtils.log_init_arguments(
            self)

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Split a column into multiple columns.

        Args:
            data (pd.DataFrame): The input DataFrame.

        Returns:
            pd.DataFrame: The DataFrame with the column split into new columns.
        """
        PandasValidationUtils.validate_is_dataframe(
            data,
            name="data")
        log_message(
            "info",
            f"Splitting column '{self.column}' "
            f"using pattern '{self.pattern}' (regex={self.regex}).")
        PandasValidationUtils.validate_columns_exist(
            data,
            [self.column])
        # Replace None or NaN with empty string in the column
        if data[self.column].isna().any():
            log_message(
                "warning",
                f"Column '{self.column}' "
                f"contains NaN or None values. Replacing with empty string.")
            data[self.column] = data[self.column].fillna("")

        # Perform the split
        split_data = PandasValidationUtils.split_column(
            data,
            self.column,
            self.pattern)

        # Replace any remaining None values in split results with empty strings
        split_data = split_data.fillna("")

        # Dynamically assign column names if new_columns is not provided
        num_splits = split_data.shape[1]
        if not self.new_columns:
            log_message(
                "info",
                "No new_columns provided. Generating default column names.")
            self.new_columns = [
                f"{self.column}_split_{i}" for i in range(num_splits)]
        elif len(self.new_columns) != num_splits:
            error_message = (
                f"Number of new_columns ({len(self.new_columns)}) "
                f"does not match the number of splits ({num_splits})."
            )
            log_message(
                "error",
                error_message)
            raise ValueError(error_message)

        # Assign the column names
        split_data.columns = self.new_columns
        log_message(
            "info",
            f"Split columns: {split_data.columns.tolist()}")

        # Combine the split columns with the original DataFrame
        data = pd.concat([data, split_data], axis=1)

        # Drop the original column
        data = data.drop(columns=[self.column], errors="ignore")
        log_message(
            "info",
            f"Column '{self.column}' dropped after splitting.")
        return data


class PandasColumnMerger(Transformer):
    """
    Transformer to merge multiple columns into a single column.

    Attributes:
        columns (list): List of columns to merge.
        new_column (str): Name of the new merged column.
        separator (str): Separator to use between values.
        drop_originals (bool): Whether to drop the original columns
        after merging.

    Example Usage:
        merger = PandasColumnMerger(
            columns=["first_name", "last_name"],
            new_column="full_name",
            separator=" ",
            drop_originals=True
        )
        transformed_data = merger.transform(data)
    """

    def __init__(
        self,
        columns: list,
        new_column: str,
        separator: str = " ",
        drop_originals: bool = True
    ):
        """
        Initialize the PandasColumnMerger.

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
        PandasValidationUtils.validate_is_non_empty_list(
            columns)
        PandasValidationUtils.validate_is_non_empty_string(
            new_column)
        PandasValidationUtils.validate_is_non_empty_string(
            separator)
        PandasValidationUtils.validate_is_boolean(
            drop_originals,
            'drop_originals')
        self.columns = columns
        self.new_column = new_column
        self.separator = separator
        self.drop_originals = drop_originals
        PandasValidationUtils.log_init_arguments(self)

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Merge multiple columns into a single column.

        Args:
            data (pd.DataFrame): The input DataFrame.

        Returns:
            pd.DataFrame: The DataFrame with the new merged column.

        Raises:
            KeyError: If any of the specified columns do not exist in
            the DataFrame.
        """
        PandasValidationUtils.validate_is_dataframe(
            data,
            name="data")
        # Validate columns exist
        PandasValidationUtils.validate_columns_exist(
            data,
            self.columns)
        # Log the merging operation
        log_message(
            "info",
            f"Merging columns {self.columns} into '{self.new_column}' "
            f"with separator '{self.separator}'."
        )

        # Perform the merge
        try:
            data[self.new_column] = PandasValidationUtils.merge_columns(
                data,
                self.columns,
                separator=self.separator)
            log_message(
                "info",
                f"New column '{self.new_column}' created successfully.")
        except Exception as e:
            error_message = (
                f"Error while creating new column '{self.new_column}': {e}"
            )
            log_message(
                "error",
                error_message)
            raise Exception(error_message) from e

        # Drop the original columns if specified
        if self.drop_originals:
            data = data.drop(columns=self.columns, errors="ignore")
            log_message(
                "info",
                f"Original columns {self.columns} dropped after merging.")

        return data


class PandasRowFilter(Transformer):
    """
    Transformer to filter rows in a Pandas DataFrame based on a condition.

    Attributes:
        condition (Callable): A function that takes a DataFrame and returns a
        Boolean Series,where `True` indicates rows to keep and
        `False` indicates rows to drop.

    Example Usage:
        # Retain rows where column "value" is greater than 10
        row_filter = PandasRowFilter(condition=lambda df: df["value"] > 10)
        transformed_data = row_filter.transform(data)
    """

    def __init__(
        self,
        condition: callable
    ):
        """
        Initialize the PandasRowFilter.

        Args:
            condition (Callable): A function that takes a DataFrame and
            returns a Boolean Series.

        Raises:
            ValueError: If `condition` is not callable.
        """
        if isinstance(condition, str):
            # Convert string to callable
            try:
                self.condition = eval(condition)
            except Exception as e:
                error_message = (
                    f"Invalid condition string: {condition}. "
                    f"Error: {e}."
                )
                log_message(
                    "error",
                    error_message)
                raise ValueError(error_message)
        elif callable(condition):
            self.condition = condition
        else:
            raise ValueError("Condition must be a callable or a string.")
        log_message(
            "info",
            f"Row filter initialized with condition: {condition}")

    def transform(
        self,
        data: pd.DataFrame,
        **kwargs
    ) -> pd.DataFrame:
        """
        Filter rows based on the provided condition.

        Args:
            data (pd.DataFrame): The input DataFrame.
            **kwargs: Additional parameters for future filtering logic.

        Returns:
            pd.DataFrame: The filtered DataFrame.

        Raises:
            ValueError: If the condition does not return a Boolean Series.
        """
        PandasValidationUtils.validate_is_dataframe(
            data,
            name="data"
        )

        log_message(
            "info",
            "Applying row filter condition.")
        try:
            # Apply the condition
            mask = self.condition(data, **kwargs)
            if not isinstance(mask, pd.Series) or mask.dtype != bool:
                error_message = (
                    "Invalid condition: {self.condition}. "
                    "Expected a Boolean Series, but got {mask.dtype}."
                )
                log_message(
                    "error",
                    error_message)
                raise ValueError(error_message)

            # Filter rows based on the mask
            log_message(
                "info",
                f"Filtering rows: {mask.sum()} rows retained, "
                f"{len(mask) - mask.sum()} rows dropped.")
            return data[mask]
        except Exception as e:
            error_message = (
                f"Error applying row filter: {e}"
            )
            log_message(
                "error",
                error_message)
            raise Exception(error_message) from e


class PandasRowDeduplicator(Transformer):
    """
    Transformer to remove duplicate rows from a Pandas DataFrame.

    Attributes:
        subset (list, optional): List of column names to consider for
        identifying duplicates. If None, all columns are considered.
        keep (str, optional): Determines which duplicates to keep:
            - "first" (default): Keep the first occurrence.
            - "last": Keep the last occurrence.
            - False: Remove all duplicates.

    Example Usage:
        # Remove duplicates based on all columns, keeping the first occurrence
        deduplicator = PandasRowDeduplicator()
        transformed_data = deduplicator.transform(data)

        # Remove duplicates based on specific columns
        deduplicator = PandasRowDeduplicator(
            subset=["col1", "col2"], keep="last")
        transformed_data = deduplicator.transform(data)
    """

    def __init__(
        self,
        subset: list = None,
        keep: str = "first"
    ):
        """
        Initialize the PandasRowDeduplicator.

        Args:
            subset (list, optional): List of column names to consider for
                identifying duplicates.
            keep (str, optional): Determines which duplicates to keep.
                Options: "first", "last", False.

        Raises:
            ValueError: If `keep` is not one of "first", "last", or False.
        """
        PandasValidationUtils.validate_is_non_empty_string(keep)
        valid_keep_options = {"first", "last", False}
        if keep not in valid_keep_options:
            error_message = (
                "Invalid value for 'keep': {keep}. "
                f"Must be one of {valid_keep_options}."
            )
            log_message(
                "error",
                error_message)
            raise ValueError(error_message)
        if subset:
            PandasValidationUtils.validate_is_non_empty_list(
                subset)
        self.subset = subset
        self.keep = keep
        PandasValidationUtils.log_init_arguments(
            self)

    def transform(self, data: pd.DataFrame, **kwargs) -> pd.DataFrame:
        """
        Remove duplicate rows from the DataFrame.

        Args:
            data (pd.DataFrame): The input DataFrame.
            **kwargs: Additional parameters for `drop_duplicates()`.

        Returns:
            pd.DataFrame: The DataFrame with duplicates removed.

        Raises:
            ValueError: If the input data is not a Pandas DataFrame.
        """
        PandasValidationUtils.validate_is_dataframe(
            data,
            name="data")

        log_message(
            "info",
            "Identifying duplicates.")

        PandasValidationUtils.validate_columns_exist(
            data,
            self.subset)
        try:
            # Validate kwargs for drop_duplicates()
            validate_kwargs(data.drop_duplicates, kwargs)

            # Determine the number of duplicates
            num_duplicates = data.duplicated(
                subset=self.subset,
                keep=self.keep).sum()
            log_message(
                "info",
                f"Found {num_duplicates} duplicate rows.")

            # Remove duplicates
            deduplicated_data = data.drop_duplicates(
                subset=self.subset,
                keep=self.keep,
                **kwargs)
            log_message(
                "info",
                f"Duplicates removed. {len(data) - len(deduplicated_data)} "
                f"rows dropped.")

            return deduplicated_data
        except Exception as e:
            error_message = (
                f"Error during deduplication: {e}"
            )
            log_message(
                "error",
                error_message)
            raise Exception(error_message) from e


class PandasRowSorter(Transformer):
    """
    Transformer to sort rows in a Pandas DataFrame.

    Attributes:
        by (list): List of column names to sort by.
        ascending (bool or list): Sort ascending or descending.
            Defaults to True.
        na_position (str): How to handle `NaN` values. Options are "first"
            or "last". Defaults to "last".

    Example Usage:
        # Sort rows by a single column in ascending order
        row_sorter = PandasRowSorter(by=["value"], ascending=True)
        transformed_data = row_sorter.transform(data)

        # Sort rows by multiple columns
        row_sorter = PandasRowSorter(
            by=["category", "value"],ascending=[True, False])
        transformed_data = row_sorter.transform(data)
    """

    def __init__(
        self,
        by: list,
        ascending: Union[bool, list] = True,
        na_position: str = "last"
    ):
        """
        Initialize the PandasRowSorter.

        Args:
            by (list): List of column names to sort by.
            ascending (bool or list, optional): Sort ascending or descending.
                Defaults to True.
            na_position (str, optional): How to handle `NaN` values.
                Defaults to "last".

        Raises:
            ValueError: If `by` is not a non-empty list or `na_position`
                is invalid.
        """
        valid_na_positions = {"first", "last"}
        PandasValidationUtils.validate_is_non_empty_list(
            by)
        if na_position not in valid_na_positions:
            error_message = (
                "Invalid value for na_position: {na_position}. "
                f"Must be one of {valid_na_positions}."
            )
            log_message(
                "error",
                error_message)
            raise ValueError(error_message)
        self.by = by
        self.ascending = ascending
        PandasValidationUtils.validate_is_non_empty_string(
            na_position)
        self.na_position = na_position
        PandasValidationUtils.log_init_arguments(
            self)

    def transform(self, data: pd.DataFrame, **kwargs) -> pd.DataFrame:
        """
        Sort rows in the DataFrame.

        Args:
            data (pd.DataFrame): The input DataFrame.
            **kwargs: Additional parameters for `sort_values()`.

        Returns:
            pd.DataFrame: The sorted DataFrame.
        """
        PandasValidationUtils.validate_is_dataframe(
            data,
            name="data")
        # Validate column names
        PandasValidationUtils.validate_columns_exist(
            data,
            self.by)

        log_message(
            "info",
            f"Sorting rows by: {self.by}, ascending: "
            f"{self.ascending}, na_position: {self.na_position}")
        try:
            # Validate kwargs for sort_values()
            validate_kwargs(data.sort_values, kwargs)

            # Perform the sorting
            sorted_data = data.sort_values(
                by=self.by,
                ascending=self.ascending,
                na_position=self.na_position, **kwargs
            )
            log_message(
                "info",
                "Rows sorted successfully.")
            return sorted_data
        except Exception as e:
            error_message = (
                f"Error during sorting: {e}"
            )
            log_message(
                "error",
                error_message)
            raise Exception(error_message) from e


class PandasRowSplitter(Transformer):
    """
    Transformer to split rows in a Pandas DataFrame based on a column
    containing lists or delimited strings.

    Attributes:
        column (str): The column to split.
        delimiter (str, optional): The delimiter to split strings in the
            column. Defaults to None (expects lists).

    Example Usage:
        # Split rows based on a column with lists
        data = pd.DataFrame({
            "id": [1, 2, 3],
            "tags": [["A", "B"], ["C"], []],
            "category": ["X", "Y", "Z"]
        })

        row_splitter = PandasRowSplitter(column="tags")
        transformed_data = row_splitter.transform(data)
        print(transformed_data)
        # Output:
        #    id tags category
        # 0   1    A        X
        # 1   1    B        X
        # 2   2    C        Y
        # 3   3  NaN        Z

        # Split rows based on a column with delimited strings
        data = pd.DataFrame({
            "id": [1, 2],
            "tags": ["A,B,C", "D,E"],
            "category": ["X", "Y"]
        })

        row_splitter = PandasRowSplitter(column="tags", delimiter=",")
        transformed_data = row_splitter.transform(data)
        print(transformed_data)
    """

    def __init__(
        self,
        column: str,
        delimiter: str = None
    ):
        """
        Initialize the PandasRowSplitter.

        Args:
            column (str): The column to split.
            delimiter (str, optional): The delimiter to split strings in
            the column. Defaults to None.

        Raises:
            ValueError: If `column` is not a string or empty.
        """
        PandasValidationUtils.validate_is_non_empty_string(
            column)
        self.column = column
        PandasValidationUtils.validate_is_non_empty_string(
            delimiter)
        self.delimiter = delimiter
        PandasValidationUtils.log_init_arguments(
            self)

    def transform(self, data: pd.DataFrame, **kwargs) -> pd.DataFrame:
        """
        Split rows based on the specified column.

        Args:
            data (pd.DataFrame): The input DataFrame.
            **kwargs: Additional parameters for Pandas operations.

        Returns:
            pd.DataFrame: The DataFrame with rows split based on the column.

        Raises:
            KeyError: If the specified column does not exist in the DataFrame.
            ValueError: If the column values are not lists or strings with the
            specified delimiter.
        """
        PandasValidationUtils.validate_is_dataframe(
            data,
            'data')
        PandasValidationUtils.validate_columns_exist(
            data, [self.column])

        log_message(
            "info",
            f"Splitting rows based on column '{self.column}'.")
        try:
            # Validate kwargs for assign
            validate_kwargs(data.assign, kwargs)
            # Validate column values
            if self.delimiter:
                PandasValidationUtils.validate_column_contains_delimiter(
                    data,
                    self.column,
                    self.delimiter)
                expanded_data = data.assign(
                    **{self.column: data[self.column].str.split(
                        self.delimiter)}
                )
            else:
                PandasValidationUtils.validate_column_is_list_type(
                    data,
                    self.column)
                expanded_data = data

            # Explode the column to split rows
            result = expanded_data.explode(self.column, ignore_index=True)
            log_message(
                "info",
                f"Rows expanded. Original rows: {len(data)}, "
                f"New rows: {len(result)}")
            return result
        except Exception as e:
            error_message = (
                f"Error during row splitting: {e}"
            )
            log_message(
                "error",
                error_message)
            raise Exception(error_message) from e


class PandasRowAggregator(Transformer):
    """
    Transformer to aggregate rows in a Pandas DataFrame by grouping them based
    on specified columns.

    Attributes:
        group_by (list): List of columns to group by.
        agg_config (dict): Dictionary specifying the aggregation configuration.
            Keys are column names, and values are aggregation functions or
            lists of functions.

    Example Usage:
        # Aggregate rows by 'category' and compute the sum of 'value'
        row_aggregator = PandasRowAggregator(
            group_by=["category"],
            agg_config={"value": "sum"}
        )
        transformed_data = row_aggregator.transform(data)

        # Aggregate with multiple functions for the same column
        row_aggregator = PandasRowAggregator(
            group_by=["category"],
            agg_config={"value": ["sum", "mean"]}
        )
        transformed_data = row_aggregator.transform(data)
    """

    def __init__(
        self,
        group_by: list,
        agg_config: dict
    ):
        """
        Initialize the PandasRowAggregator.

        Args:
            group_by (list): List of columns to group by.
            agg_config (dict): Dictionary specifying the aggregation
            configuration.

        Raises:
            ValueError: If `group_by` is not a non-empty list or `agg_config`
            is not a dictionary.
        """
        PandasValidationUtils.validate_is_non_empty_list(
            group_by)
        PandasValidationUtils.validate_is_non_empty_dict(
            agg_config)
        self.group_by = group_by
        self.agg_config = agg_config
        PandasValidationUtils.log_init_arguments(
            self)

    def transform(
        self,
        data: pd.DataFrame,
        **kwargs
    ) -> pd.DataFrame:
        """
        Aggregate rows in the DataFrame.

        Args:
            data (pd.DataFrame): The input DataFrame.
            **kwargs: Additional parameters for Pandas `groupby()` and `agg()`.

        Returns:
            pd.DataFrame: The aggregated DataFrame.

        Raises:
            KeyError: If any columns in `group_by` or `agg_config` do not
            exist in the DataFrame.
        """
        # Validate data input
        PandasValidationUtils.validate_is_dataframe(
            data,
            name="data")
        # Validate group_by columns
        PandasValidationUtils.validate_columns_exist(
            data,
            self.group_by)
        # Validate aggregation columns
        PandasValidationUtils.validate_columns_exist(
            data, list(self.agg_config.keys()))

        log_message(
            "info",
            f"Aggregating rows grouped by: "
            f"{self.group_by} with configuration: {self.agg_config}")
        try:
            # Perform group-by and aggregation using utility
            aggregated_data = PandasValidationUtils.group_and_aggregate(
                data,
                self.group_by,
                self.agg_config,
                **kwargs
            )
            log_message(
                "info",
                "Aggregation completed successfully.")
            return aggregated_data
        except Exception as e:
            error_message = (
                f"Error during aggregation: {e}"
            )
            log_message(
                "error",
                error_message)
            raise Exception(error_message) from e


class PandasRowAppender(Transformer):
    """
    Transformer to append rows to a Pandas DataFrame.

    Attributes:
        rows (pd.DataFrame or list): Rows to append to the DataFrame.

    Example Usage:
        # Append static rows
        new_rows = pd.DataFrame([{"category": "D", "value": 60, "count": 3}])
        row_appender = PandasRowAppender(rows=new_rows)
        transformed_data = row_appender.transform(data)

        # Append rows prepared using other transformers
        filtered_rows = some_filtering_logic()
        row_appender = PandasRowAppender(rows=filtered_rows)
        transformed_data = row_appender.transform(data)
    """

    def __init__(
        self,
        rows: Union[pd.DataFrame, list]
    ):
        """
        Initialize the PandasRowAppender.

        Args:
            rows (pd.DataFrame or list): Rows to append to the DataFrame.

        Raises:
            ValueError: If `rows` is not a Pandas DataFrame or a list of
            dictionaries.
        """

        # Validate rows_
        PandasValidationUtils.validate_is_dataframe(
            rows,
            name="Rows")

        self.rows = rows
        log_message(
            "info",
            f"Initialized with rows to append: "
            f"{len(rows) if isinstance(rows, list) else rows.shape[0]}")

    def transform(self, data: pd.DataFrame, **kwargs) -> pd.DataFrame:
        """
        Append rows to the DataFrame.

        Args:
            data (pd.DataFrame): The input DataFrame.
            **kwargs: Additional parameters for Pandas operations.

        Returns:
            pd.DataFrame: The DataFrame with rows appended.

        Raises:
            ValueError: If appended rows have inconsistent columns.
        """
        # Validate data input in transform
        PandasValidationUtils.validate_is_dataframe(
            data,
            name="data")

        log_message(
            "info",
            "Appending rows to the DataFrame.")
        try:
            # Convert rows to DataFrame if necessary
            if isinstance(self.rows, list):
                self.rows = pd.DataFrame(self.rows)

            # Validate columns
            if set(self.rows.columns) != set(data.columns):
                error_message = (
                    "Appended rows must have the same columns as "
                    "the existing DataFrame."
                )
                log_message(
                    "error",
                    error_message)
                raise ValueError(error_message)

            # Append rows
            transformed_data = pd.concat([data, self.rows], ignore_index=True)
            error_message = (
                f"Rows appended successfully. Original rows: {len(data)}, " +
                f"New rows: {len(self.rows)}," +
                f"Final rows: {len(transformed_data)}"
                )
            log_message(
                "info",
                error_message)
            return transformed_data
        except Exception as e:
            error_message = (
                f"Error appending rows: {e}"
            )
            log_message(
                "error",
                error_message)
            raise Exception(error_message) from e


class PandasRowSampler(Transformer):
    """
    Transformer to sample rows from a Pandas DataFrame.

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
        # Random sampling
        sampler = PandasRowSampler(mode="random", frac=0.5, replace=False)
        transformed_data = sampler.transform(data)

        # Select the first 5 rows
        sampler = PandasRowSampler(mode="head", n=5)
        transformed_data = sampler.transform(data)

        # Select the last 3 rows
        sampler = PandasRowSampler(mode="tail", n=3)
        transformed_data = sampler.transform(data)
    """

    def __init__(
        self,
        mode: str,
        n: int = None,
        frac: float = None,
        replace: bool = False
    ):
        """
        Initialize the PandasRowSampler.

        Args:
            mode (str): Sampling mode. Options are "random", "head", "tail".
            n (int, optional): Number of rows to sample for "head" or "tail".
            frac (float, optional): Fraction of rows to sample for "random".
            replace (bool, optional): Whether to sample with replacement for
                "random". Defaults to False.

        Raises:
            ValueError: If invalid sampling parameters are provided.
        """
        valid_modes = {"random", "head", "tail"}
        if mode not in valid_modes:
            error_message = (
                f"Invalid mode: {mode}. Must be one of {valid_modes}."
            )
            log_message(
                "error",
                error_message)
            raise ValueError(error_message)
        PandasValidationUtils.validate_is_non_empty_string(mode)
        self.mode = mode
        PandasValidationUtils.validate_is_integer(
            n,
            'n')
        self.n = n
        PandasValidationUtils.validate_float(frac, 'frac')
        self.frac = frac
        PandasValidationUtils.validate_is_boolean(
            replace,
            'replace')
        self.replace = replace
        PandasValidationUtils.log_init_arguments(
            self)
        PandasValidationUtils.validate_sampling_parameters(
            mode=mode,
            n=n,
            frac=frac)

    def transform(self, data: pd.DataFrame, **kwargs) -> pd.DataFrame:
        """
        Sample rows from the DataFrame.

        Args:
            data (pd.DataFrame): The input DataFrame.
            **kwargs: Additional parameters for sampling.

        Returns:
            pd.DataFrame: The sampled DataFrame.
        """
        PandasValidationUtils.validate_is_dataframe(
            data,
            name="Input data")

        log_message(
            "info",
            f"Sampling rows with mode: {self.mode}, n: {self.n}, frac: "
            f"{self.frac}, replace: {self.replace}")
        try:
            if self.mode == "random":
                sampled_data = data.sample(
                    frac=self.frac,
                    replace=self.replace,
                    **kwargs)
            elif self.mode == "head":
                sampled_data = data.head(self.n)
            elif self.mode == "tail":
                sampled_data = data.tail(self.n)
            else:
                error_message = (
                    f"Unsupported sampling mode: {self.mode}"
                )
                log_message(
                    "error",
                    error_message)
                raise ValueError(error_message)

            # Log row count change using utility
            PandasValidationUtils.log_row_count_change(
                len(data),
                len(sampled_data),
                action="Sampling completed")
            return sampled_data
        except Exception as e:
            error_message = (
                f"Error sampling rows: {e}"
            )
            log_message(
                "error",
                error_message)
            raise Exception(error_message) from e


class PandasRowDuplicator(Transformer):
    """
    Transformer to duplicate rows in a Pandas DataFrame based on a condition.

    Attributes:
        condition (Callable): A function that takes a DataFrame and returns a
            Boolean Series, where `True` indicates rows to duplicate.
        times (int, optional): Number of times to duplicate the matching rows.
            Defaults to 1.

    Example Usage:
        # Duplicate rows where 'status' is 'Pending' 2 times
        row_duplicator = PandasRowDuplicator(
            condition=lambda df: df["status"] == "Pending",
            times=2
        )
        transformed_data = row_duplicator.transform(data)
    """

    def __init__(
        self,
        condition: callable,
        times: int = 1
    ):
        """
        Initialize the PandasRowDuplicator.

        Args:
            condition (Callable): A function that takes a DataFrame and
                returns a Boolean Series.
            times (int, optional): Number of times to duplicate rows.
                Defaults to 1.

        Raises:
            ValueError: If `condition` is not callable or `times` is not
            a positive integer.
        """
        if not isinstance(times, int) or times <= 0:
            error_message = (
                f"Invalid times: {times}. Must be a positive integer."
            )
            log_message(
                "error",
                error_message)
            raise ValueError(error_message)
        PandasValidationUtils
        self.condition = condition
        self.times = times
        PandasValidationUtils.validate_is_callable(
            condition,
            'condition')
        PandasValidationUtils.log_init_arguments(
            self)

    def transform(self, data: pd.DataFrame, **kwargs) -> pd.DataFrame:
        """
        Duplicate rows in the DataFrame based on the condition.

        Args:
            data (pd.DataFrame): The input DataFrame.
            **kwargs: Additional parameters for Pandas operations.

        Returns:
            pd.DataFrame: The DataFrame with duplicated rows.
        """
        PandasValidationUtils.validate_is_dataframe(
            data,
            name="data")
        try:
            # Validate condition output
            mask = PandasValidationUtils.validate_boolean_condition(
                self.condition,
                data)
            log_message(
                "info",
                f"{mask.sum()} rows match the condition for duplication.")

            # Extract rows to duplicate
            rows_to_duplicate = data[mask]

            # Duplicate the rows
            duplicated_rows = pd.concat(
                [rows_to_duplicate] * self.times,
                ignore_index=True)
            log_message(
                "info",
                f"Duplicated rows {self.times} times.")

            # Combine original and duplicated rows
            combined_data = pd.concat(
                [data, duplicated_rows],
                ignore_index=True)
            log_message(
                "info",
                f"Rows duplicated successfully. Original rows: {len(data)}, "
                f"Final rows: {len(combined_data)}"
            )
            return combined_data
        except Exception as e:
            error_message = (
                f"Error during row duplication: {e}"
            )
            log_message(
                "error",
                error_message)
            raise Exception(error_message) from e


class PandasRowExpander(Transformer):
    """
    Transformer to expand rows in a Pandas DataFrame based on a column value
    or logic.

    Attributes:
        expand_column (str): The column containing the number of times
        to repeat each row.

    Example Usage:
        # Expand rows based on the 'repeat_count' column
        data = pd.DataFrame({
            "id": [1, 2, 3],
            "value": [100, 200, 300],
            "repeat_count": [2, 3, 1]
        })

        row_expander = PandasRowExpander(expand_column="repeat_count")
        transformed_data = row_expander.transform(data)
        print(transformed_data)
    """

    def __init__(
        self,
        expand_column: str
    ):
        """
        Initialize the PandasRowExpander.

        Args:
            expand_column (str): The column containing the number of times
            to repeat each row.

        Raises:
            ValueError: If `expand_column` is not a string or empty.
        """
        PandasValidationUtils.validate_is_non_empty_string(
            expand_column)
        self.expand_column = expand_column
        PandasValidationUtils.log_init_arguments(
            self)

    def transform(
        self,
        data: pd.DataFrame,
        **kwargs
    ) -> pd.DataFrame:
        """
        Expand rows based on the specified column.

        Args:
            data (pd.DataFrame): The input DataFrame.
            **kwargs: Additional parameters for Pandas operations.

        Returns:
            pd.DataFrame: The DataFrame with expanded rows.

        Raises:
            KeyError: If the `expand_column` does not exist in the DataFrame.
            ValueError: If the `expand_column` contains invalid values
            (non-integer or negative).
        """
        PandasValidationUtils.validate_is_dataframe(
            data,
            name="data")
        PandasValidationUtils.validate_columns_exist(
            data,
            [self.expand_column])

        # Validate positive integer values in expand_column
        PandasValidationUtils.validate_positive_integers(
            data[self.expand_column], self.expand_column
        )

        log_message(
            "info",
            f"Expanding rows based on column '{self.expand_column}'.")
        try:
            # Expand rows
            expanded_data = data.loc[
                data.index.repeat(data[self.expand_column])].reset_index(
                    drop=True)
            log_message(
                "info",
                f"Rows expanded successfully. Original rows: {len(data)}, "
                f"Expanded rows: {len(expanded_data)}"
            )
            return expanded_data
        except Exception as e:
            error_message = (
                f"Error during row expansion: {e}"
            )
            log_message(
                "error",
                error_message)
            raise Exception(error_message) from e


class PandasTransformerFactory(TransformerFactory):
    """
    Concrete factory class for creating Pandas transformers.
    """

    def __init__(self):
        """
        Initialize the PandasTransformerFactory with a logger.
        """

    def log_creation(self, transformer_name: str, **params):
        """
        Log the creation of a transformer.
        """
        log_message(
            "info", f"Creating {transformer_name} with parameters: {params}"
        )

    def create_column_adder(
        self,
        column_name: str,
        value: Any,
        aggregation: dict = None
    ) -> PandasColumnAdder:
        self.log_creation(
            "PandasColumnAdder",
            column_name=column_name,
            value=value,
            aggregation=aggregation)
        return PandasColumnAdder(
            column_name=column_name,
            value=value,
            aggregation=aggregation)

    def create_column_adder_static(
        self,
        column_name: str,
        value: any,
        overwrite: bool = False
    ) -> PandasColumnAdderStatic:
        self.log_creation(
            "PandasColumnAdderStatic",
            column_name,
            value,
            overwrite
        )
        return PandasColumnAdderStatic(
            column_name=column_name,
            value=value,
            overwrite=overwrite
        )

    def create_column_dropper(
        self,
        columns_to_drop: list
    ) -> PandasColumnDropper:
        self.log_creation(
            "PandasColumnDropper",
            columns_to_drop=columns_to_drop)
        return PandasColumnDropper(
            columns_to_drop=columns_to_drop)

    def create_column_merger(
        self,
        columns: list,
        new_column: str,
        separator: str = " ",
        drop_originals: bool = True
    ) -> PandasColumnMerger:
        self.log_creation(
            "PandasColumnMerger",
            columns=columns,
            new_column=new_column,
            separator=separator,
            drop_originals=drop_originals
        )
        return PandasColumnMerger(
            columns=columns,
            new_column=new_column,
            separator=separator,
            drop_originals=drop_originals)

    def create_column_name_prefix_suffix(
        self,
        prefix: str = "",
        suffix: str = "",
        exclude_columns: list = None
    ) -> PandasColumnNamePrefixSuffix:
        self.log_creation(
            "PandasColumnNamePrefixSuffix",
            prefix=prefix,
            suffix=suffix,
            exclude_columns=exclude_columns
        )
        return PandasColumnNamePrefixSuffix(
            prefix=prefix,
            suffix=suffix,
            exclude_columns=exclude_columns)

    def create_column_name_regex_renamer(
        self,
        pattern: str,
        replacement: str,
        exclude_columns: list = None
    ) -> PandasColumnNameRegexRenamer:
        self.log_creation(
            "PandasColumnNameRegexRenamer",
            pattern=pattern,
            replacement=replacement,
            exclude_columns=exclude_columns
        )
        return PandasColumnNameRegexRenamer(
            pattern=pattern,
            replacement=replacement,
            exclude_columns=exclude_columns
        )

    def create_column_name_standardizer(
        self,
        case_style: str = "snake_case",
        exclude_columns: list = None
    ) -> PandasColumnNameStandardizer:
        self.log_creation(
            "PandasColumnNameStandardizer",
            case_style=case_style,
            exclude_columns=exclude_columns)
        return PandasColumnNameStandardizer(
            case_style=case_style,
            exclude_columns=exclude_columns
        )

    def create_column_pattern_dropper(
        self,
        pattern: str,
        exclude_columns: list = None
    ) -> PandasColumnPatternDropper:
        self.log_creation(
            "PandasColumnPatternDropper",
            pattern=pattern,
            exclude_columns=exclude_columns)
        return PandasColumnPatternDropper(
            pattern=pattern,
            exclude_columns=exclude_columns)

    def create_column_renamer(
        self,
        column_map: dict
    ) -> PandasColumnRenamer:
        self.log_creation(
            "PandasColumnRenamer",
            column_map=column_map)
        return PandasColumnRenamer(
            column_map=column_map)

    def create_column_reorderer(
        self,
        column_order: list,
        retain_unspecified: bool = False
    ) -> PandasColumnReorderer:
        self.log_creation(
            "PandasColumnReorderer",
            column_order=column_order,
            retain_unspecified=retain_unspecified)
        return PandasColumnReorderer(
            column_order=column_order,
            retain_unspecified=retain_unspecified
        )

    def create_column_splitter(
        self,
        column: str,
        pattern: str,
        regex: bool = False,
        new_columns: list = None
    ) -> PandasColumnSplitter:
        self.log_creation(
            "PandasColumnSplitter",
            column=column,
            pattern=pattern,
            regex=regex,
            new_columns=new_columns
        )
        return PandasColumnSplitter(
            column=column,
            pattern=pattern,
            regex=regex,
            new_columns=new_columns
        )

    def create_column_type_dropper(
        self,
        data_types: list,
        exclude_columns: list = None
    ) -> PandasColumnTypeDropper:
        self.log_creation(
            "PandasColumnTypeDropper",
            data_types=data_types,
            exclude_columns=exclude_columns)
        return PandasColumnTypeDropper(
            data_types=data_types,
            exclude_columns=exclude_columns)

    def create_empty_column_dropper(
        self,
        exclude_columns: list = None
    ) -> PandasEmptyColumnDropper:
        self.log_creation(
            "PandasEmptyColumnDropper",
            exclude_columns=exclude_columns)
        return PandasEmptyColumnDropper(
            exclude_columns=exclude_columns
        )

    def create_null_ratio_column_dropper(
        self,
        threshold: float,
        exclude_columns: list = None
    ) -> PandasNullRatioColumnDropper:
        self.log_creation(
            "PandasNullRatioColumnDropper",
            threshold=threshold,
            exclude_columns=exclude_columns
        )
        return PandasNullRatioColumnDropper(
            threshold=threshold,
            exclude_columns=exclude_columns)

    def create_row_aggregator(
        self,
        group_by: list,
        agg_config: dict
    ) -> PandasRowAggregator:
        self.log_creation(
            "PandasRowAggregator",
            group_by=group_by,
            agg_config=agg_config)
        return PandasRowAggregator(
            group_by=group_by,
            agg_config=agg_config
        )

    def create_row_appender(
        self,
        rows: Union[pd.DataFrame, list]
    ) -> PandasRowAppender:
        self.log_creation(
            "PandasRowAppender",
            rows=rows)
        return PandasRowAppender(
            rows=rows)

    def create_row_deduplicator(
        self,
        subset: list = None,
        keep: str = "first"
    ) -> PandasRowDeduplicator:
        self.log_creation(
            "PandasRowDeduplicator",
            subset=subset,
            keep=keep)
        return PandasRowDeduplicator(
            subset=subset,
            keep=keep
        )

    def create_row_duplicator(
        self,
        condition: callable,
        times: int = 1
    ) -> PandasRowDuplicator:
        self.log_creation(
            "PandasRowDuplicator",
            condition=condition,
            times=times)
        return PandasRowDuplicator(
            condition=condition,
            times=times
        )

    def create_row_expander(
        self,
        expand_column: str
    ) -> PandasRowExpander:
        self.log_creation(
            "PandasRowExpander",
            expand_column=expand_column)
        return PandasRowExpander(
            expand_column=expand_column
        )

    def create_row_filter(
        self,
        condition: callable
    ) -> PandasRowFilter:
        self.log_creation(
            "PandasRowFilter",
            condition=condition)
        return PandasRowFilter(
            condition=condition
        )

    def create_row_sampler(
        self,
        mode: str,
        n: int = None,
        frac: float = None,
        replace: bool = False
    ) -> PandasRowSampler:
        self.log_creation(
            "PandasRowSampler",
            mode=mode,
            n=n,
            frac=frac,
            replace=replace
        )
        return PandasRowSampler(
            mode=mode,
            n=n,
            frac=frac,
            replace=replace
        )

    def create_row_sorter(
        self,
        by: list,
        ascending: Union[bool, list] = True,
        na_position: str = "last"
    ) -> PandasRowSorter:
        self.log_creation(
            "PandasRowSorter",
            by=by,
            ascending=ascending,
            na_position=na_position
            )
        return PandasRowSorter(
            by=by,
            ascending=ascending,
            na_position=na_position
        )

    def create_row_splitter(
        self,
        column: str,
        delimiter: str = None
    ) -> PandasRowSplitter:
        self.log_creation(
            "PandasRowSplitter",
            column=column,
            delimiter=delimiter
            )
        return PandasRowSplitter(
            column=column,
            delimiter=delimiter
        )

    def create_value_replacer(
        self,
        value_map: dict
    ) -> PandasValueReplacer:
        self.log_creation(
            "PandasValueReplacer",
            value_map=value_map
        )
        return PandasValueReplacer(
            value_map=value_map
        )


class PandasTransformerProvider(TransformerProvider):
    """
    A provider class for creating Pandas transformers dynamically based on
    the transformer type and configuration options.

    This class integrates with a factory (`PandasTransformerFactory`) to
    dynamically instantiate transformers. It ensures that required parameters
    are validated before creating the transformers, leveraging a centralized
    validation utility.

    Example Usage:
    --------------
    from pandas import DataFrame
    from your_module import (
        PandasTransformerFactory, PandasTransformerProvider, TransformerType)

    # Initialize the factory and provider
    factory = PandasTransformerFactory()
    provider = PandasTransformerProvider(factory)

    # Example 1: Creating a COLUMN_ADDER transformer
    transformer = provider.create_validator(
        transformer_type=TransformerType.COLUMN_ADDER,
        column_name="new_col",
        value=42,
        aggregation="sum"
    )
    data = DataFrame({"col1": [1, 2, 3]})
    result = transformer.transform(data)
    print(result)
    # Output:
    #    col1  new_col
    # 0     1       42
    # 1     2       42
    # 2     3       42

    # Example 2: Creating a COLUMN_DROPPER transformer
    transformer = provider.create_validator(
        transformer_type=TransformerType.COLUMN_DROPPER,
        columns_to_drop=["col1"]
    )
    data = DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
    result = transformer.transform(data)
    print(result)
    # Output:
    #    col2
    # 0     4
    # 1     5
    # 2     6

    # Example 3: Creating a COLUMN_NAME_PREFIX_SUFFIX transformer
    transformer = provider.create_validator(
        transformer_type=TransformerType.COLUMN_NAME_PREFIX_SUFFIX,
        prefix="prefix_",
        suffix="_suffix",
        exclude_columns=["col2"]
    )
    data = DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
    result = transformer.transform(data)
    print(result)
    # Output:
    #    prefix_col1_suffix  col2
    # 0                  1     4
    # 1                  2     5
    # 2                  3     6

    Parameters
    ----------
    factory : PandasTransformerFactory
        An instance of the `PandasTransformerFactory` responsible for
        creating specific transformers.

    Methods
    -------
    create_validator(
        transformer_type: TransformerType, **options) -> Transformer
        Dynamically creates a transformer based on the specified type
        (`TransformerType`) and configuration options.

    Raises
    ------
    ValueError
        If the required options for the transformer type are not provided or
        are invalid.

    Notes
    -----
    - The `TransformerType` Enum defines all the valid transformer types
        supported by this provider.
    - All required parameters for each transformer type must be included
        in the `options` dictionary.
    - Use the centralized `validate_options` utility to ensure proper
        parameter validation.

    See Also
    --------
    PandasTransformerFactory : Factory class for creating individual
        transformers.
    TransformerType : Enum class for defining valid transformer types.
    """
    def __init__(self, factory: PandasTransformerFactory):
        """
        Initialize the PandasValidatorProvider.

        Args:
            factory (PandasTransformerFactory): An instance of the
                PandasTransformerFactory to create transformers.
        """
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
                        "retain_unspecified",
                        False))
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


class PandasDataWorkflow(BaseDataWorkflow):
    """
    Orchestrates data-related tasks for both local and cloud environments
    using Pandas.
    """

    def __init__(
        self,
        reader_factory=None,
        saver_factory=None
    ):
        """
        Initializes the workflow.

        Args:
            reader_factory (PandasReaderFactory, optional): Factory for
            reader providers.
                Defaults to PandasReaderFactory().
            connector (CloudConnector, optional): Connector for resolving
                cloud paths.
        """
        super().__init__()
        self.reader_factory = reader_factory or PandasReaderFactory()
        self.saver_factory = saver_factory or PandasSaverFactory()

    def get_reader_provider(self, dataset_config):
        """
        Dynamically resolves the appropriate provider for the dataset.

        Args:
            dataset_config (dict): Configuration for a specific dataset.

        Returns:
            ReaderProvider: The appropriate provider based on the source.
        """
        data_type = dataset_config["reader"]["data_type"]
        reader_config = dataset_config["reader"]

        # Handle local source
        if reader_config.get("local", {}).get("file_path"):
            return PandasLocalReaderProvider(
                self.reader_factory,
                DataType[data_type.upper()])

        # Handle cloud source
        elif reader_config.get(
            "cloud", {}).get("storage_unit") and reader_config.get(
                "cloud", {}).get("object_name"):
            if not self.data_connector:
                raise ValueError(
                    "A data_connector is required for cloud workflows.")
            return PandasCloudReaderProvider(
                self.reader_factory,
                DataType[data_type.upper()],
                self.data_connector
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
        # data_type = dataset_config["writer"]["data_type"]
        reader_config = dataset_config["writer"]

        # Handle local source
        if reader_config.get("local", {}).get("file_path"):
            return PandasLocalSaverProvider(
                self.saver_factory)

        # Handle cloud source
        elif reader_config.get(
            "cloud", {}).get(
                "storage_unit") and reader_config.get(
                    "cloud", {}).get("object_name"):
            if not self.data_connector:
                raise ValueError(
                    "A data_connector is required for cloud workflows.")
            return PandasCloudSaverProvider(
                self.saver_factory,
                self.data_connector
            )

        # Raise error if neither is valid
        raise ValueError(
            "Dataset configuration must include a valid " +
            "'local' or 'cloud' source with all required fields."
        )

    def _pre_save_hook(self, save_config, kwargs):
        """
        Add Pandas-specific storage options before saving.

        Args:
            save_config (dict): Configuration for saving the dataset.
            kwargs (dict): Existing parameters for the saver.

        Returns:
            dict: Modified kwargs with storage options.
        """
        kwargs["storage_options"] = self.save_connector.get_framework_config(
            "pandas")
        return kwargs
