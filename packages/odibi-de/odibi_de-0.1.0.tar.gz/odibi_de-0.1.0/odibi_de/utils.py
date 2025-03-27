from enum import Enum
import threading
from typing import Any, Callable
import pandas as pd
import logging
import re
import inspect
import importlib
import sys
from pyspark.sql import Column, DataFrame
from pyspark.sql.types import BooleanType, DataType
from pyspark.sql.window import Window
from pyspark.sql.functions import (
    col, lit, expr, instr, udf,
    concat_ws, split, size, count, when, isnan)


from odibi_de.core_types import (
    Framework, DataReader)


def resolve_function(function_path):
    """
    Resolve a function given its fully qualified path.

    Args:
        function_path (str): Fully qualified path of the function to resolve.

    Returns:
        callable: Resolved function.

    Raises:
        ImportError: If the module containing the function cannot be imported.
        AttributeError: If the function is not found in the module.
    """

    try:
        module_name, function_name = function_path.rsplit(".", 1)
        module = importlib.import_module(module_name)
        return getattr(module, function_name)
    except ImportError as e:
        raise ImportError(
            f"Module could not be imported: {function_path}") from e
    except AttributeError as e:
        raise AttributeError(f"Function not found: {function_path}") from e


def validate_options(
    options: dict,
    required_keys: list[str],
    entity_type: str,
    entity_name: str
):
    """
    Validate that all required keys exist in the options dictionary.

    Args:
        options (dict): Dictionary containing configuration options.
        required_keys (list): List of keys that must exist in the options.
        entity_type (str): Type of the entity
            (e.g., 'transformer', 'validator').
        entity_name (str): Name of the entity being validated.

    Raises:
        ValueError: If one or more required keys are missing from the options
        dictionary.
    """
    logger = get_logger()
    missing_keys = [
        key for key in required_keys if key not in options]
    if missing_keys:
        error_message = (
            f"{', '.join(missing_keys)} must be provided " +
            f"for {entity_name} {entity_type}"
        )
        logger.log("error", error_message)
        raise ValueError(error_message)


def get_data_type_from_file_extension(object_name):
    from Data_Engineering_Class_Enums_and_Abstract_Classes import DataType
    """
    Get the data type based on the file extension of the given object name.

    Args:
        object_name (str): Name of the object (e.g., 'data.csv').

    Returns:
        DataType: The data type corresponding to the file extension.
    """
    PandasValidationUtils.validate_is_non_empty_string(object_name)
    if object_name.endswith('.csv'):
        return DataType.CSV
    elif object_name.endswith('.json'):
        return DataType.JSON
    elif object_name.endswith('.avro'):
        return DataType.AVRO
    elif object_name.endswith('.parquet'):
        return DataType.PARQUET
    else:
        raise ValueError(
            f"Unsupported file extension for object: {object_name}")


def validate_kwargs(method: Callable, kwargs):
    """
    Validate that the provided kwargs are valid for the given method.

    Args:
        method (Callable): The Pandas method to validate against.
        kwargs (dict): The additional parameters to validate.

    Raises:
        ValueError: If any kwargs are not valid for the method.
    """
    logger = get_logger()
    valid_params = inspect.signature(method).parameters
    invalid_params = [key for key in kwargs if key not in valid_params]
    if invalid_params:
        error_message = (
            f"Invalid parameters for {method.__name__}: {invalid_params}"
        )
        logger.log(
            "error",
            error_message)
        raise ValueError(error_message)


def apply_methods(obj, methods_with_args):
    """
    Apply the specified methods to the given object with the provided
    arguments.

    Args:
        obj (Any): The object to apply the methods to.
        methods_with_args (dict): A dictionary mapping method names to their
            corresponding arguments.

    Returns:
        Any: The result of applying the methods to the object.

    Raises:
        ValueError: If the provided methods_with_args dictionary is not valid.
    """

    logger = get_logger()
    PandasValidationUtils.validate_is_non_empty_dict(methods_with_args)
    for method_name, args in methods_with_args.items():
        if hasattr(obj, method_name):
            method_to_call = getattr(obj, method_name)
            if isinstance(args, dict):
                obj = method_to_call(**args)
            elif isinstance(args, (list, tuple)):
                obj = method_to_call(*args)
            else:
                obj = method_to_call(args)
        else:
            # Log warning or skip unsupported attributes
            message = (
                f"The method '{method_name}'" +
                f" is not supported by {obj.__class__.__name__}. Skipping..."
            )
            logger.log(
                "warning",
                message)
    return obj


class MetadataManager:
    """
    A simple class to manage and provide metadata for logging.

    Attributes:
        metadata (dict): A dictionary holding metadata key-value pairs.
    """

    def __init__(self):
        """
        Initialize a MetadataManager instance with an empty
        metadata dictionary.
        """
        self.metadata = {}

    def update_metadata(self, clear_existing: bool = False, **kwargs):
        """
        Update the metadata dictionary.

        Args:
            clear_existing (bool): Whether to clear the existing metadata
            before updating.
            **kwargs: Key-value pairs of metadata to update.
        """
        if clear_existing:
            error_message = (
                "'clear_existing' must be a boolean."
            )
            if not isinstance(clear_existing, bool):
                print(error_message)
                raise ValueError(error_message)
            # Remove all existing keys
            self.metadata.clear()
        self.metadata.update(kwargs)

    def get_metadata(self):
        """
        Retrieve the current metadata dictionary.

        Returns:
            dict: The current metadata stored in the manager.
        """
        return self.metadata


class CapturingHandler(logging.Handler):
    """
    A custom logging handler that captures log records for programmatic access.

    Attributes:
        records (list): A list that stores formatted log messages.
    """

    def __init__(self):
        """
        Initialize the CapturingHandler with an empty records list.
        """
        super().__init__()
        self.records = []

    def emit(self, record):
        """
        Capture the log message when a log event occurs.

        Args:
            record (LogRecord): The log record to be captured.
        """
        self.records.append(self.format(record))

    def get_logs(self):
        """
        Retrieve the captured log messages.

        Returns:
            list: A list of formatted log messages.
        """
        return self.records

    def clear_logs(self):
        """
        Clear all captured log messages.
        """
        self.records.clear()


class DynamicLogger:
    """
    A dynamic logger class that supports metadata injection, console logging,
    and programmatic log capturing.

    The logger is designed to:
    - Dynamically include metadata in log messages using a MetadataManager.
    - Log messages to the console via a stream handler.
    - Capture log messages programmatically for further processing or saving.
    - Dynamically update metadata at runtime and reflect changes in
        subsequent logs.

    Attributes:
        metadata_manager (MetadataManager): The manager for dynamic metadata
            injection.
        logger (Logger): The Python logger instance.
        capturing_handler (CapturingHandler): The custom handler for capturing
            logs programmatically.

    Example Usage:
        # Step 1: Create a MetadataManager and update metadata
        metadata_manager = MetadataManager()
        metadata_manager.update_metadata(
            project_name="OEEAnalysis",operation="save", file_format="CSV")

        # Step 2: Initialize the DynamicLogger
        dynamic_logger = DynamicLogger(metadata_manager)

        # Step 3: Log messages with dynamic metadata
        dynamic_logger.log("info", "Starting the save operation")
        dynamic_logger.log(
            "error", "Save operation failed due to insufficient permissions")

        # Step 4: Retrieve captured logs programmatically
        captured_logs = dynamic_logger.get_logs()
        print("\nCaptured Logs:")
        for log in captured_logs:
            print(log)

        # Step 5: Clear logs if needed
        dynamic_logger.clear_logs()

        # Step 6: Dynamically update metadata and log more messages
        metadata_manager.update_metadata(
            operation="validate", file_format="JSON")
        dynamic_logger.log("debug", "Validation passed for the schema")

        # Step 7: Retrieve updated logs with new metadata
        captured_logs = dynamic_logger.get_logs()
        for log in captured_logs:
            # Save logs to a file, upload to cloud, etc.
            print(log)

    Notes:
        - Metadata fields like `project_name`, `operation`, and `file_format`
            are dynamically injected into log records.
        - Handlers (stream and capturing) are ensured to be added only once to
            avoid duplicate logs.
        - Use the `MetadataManager` to dynamically update metadata for
            different operations.
    """

    def __init__(
        self,
        metadata_manager: MetadataManager,
        logger_name: str = "DynamicLogger"
    ):
        """
        Initialize the DynamicLogger instance.

        Ensures that only one instance of each handler (console and capturing)
        is added to the logger.
        Also injects metadata dynamically into log messages.

        Args:
            metadata_manager (MetadataManager): An instance of MetadataManager
                to provide metadata for logging.
            logger_name (str): The name of the logger instance. Defaults to
                "DynamicLogger".
        """
        self.metadata_manager = metadata_manager
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False  # Prevent duplicate logs

        # Ensure handlers are added only once
        self.capturing_handler = self._ensure_handlers()

        # Clear existing filters to avoid duplicates
        self.logger.filters.clear()
        self.logger.addFilter(self._create_metadata_filter())
        # Add metadata filter if not already present
        if not any(
            isinstance(
                f, self._create_metadata_filter().__class__)
            for f in self.logger.filters
        ):
            self.logger.addFilter(self._create_metadata_filter())

    def _ensure_handlers(self):
        """
        Ensure that the logger has exactly one StreamHandler and one
        CapturingHandler.

        Returns:
            CapturingHandler: The capturing handler added to the logger.
        """
        # Check for existing CapturingHandler
        capturing_handler = None
        for handler in self.logger.handlers:
            if isinstance(handler, CapturingHandler):
                capturing_handler = handler
                break

        if not capturing_handler:
            # Add handlers only if not already present
            dynamic_formatter = self._dynamic_formatter()

            # Stream handler for console output
            if not any(
                isinstance(h, logging.StreamHandler)
                for h in self.logger.handlers
            ):
                stream_handler = logging.StreamHandler()
                stream_handler.setFormatter(dynamic_formatter)
                self.logger.addHandler(stream_handler)

            # Capturing handler for programmatic access
            capturing_handler = CapturingHandler()
            capturing_handler.setFormatter(dynamic_formatter)
            self.logger.addHandler(capturing_handler)

        return capturing_handler

    def _dynamic_formatter(self):
        """
        Create a formatter that dynamically includes metadata fields in log
        messages.

        Returns:
            logging.Formatter: A formatter that dynamically formats log
            messages with metadata.
        """
        class DynamicFormatter(logging.Formatter):
            def format(self, record):
                metadata = getattr(record, "metadata", {})
                metadata_str = " - ".join(
                    f"{key}={value}" for key, value in metadata.items())
                record.msg = f"{metadata_str} - {record.msg}"
                return super().format(record)

        return DynamicFormatter("%(asctime)s - %(levelname)s - %(message)s")

    def _create_metadata_filter(self):
        """
        Create a metadata filter that injects metadata into log records.

        Returns:
            logging.Filter: A filter instance that attaches metadata to log
            records.
        """
        class MetadataFilter(logging.Filter):
            def __init__(self, metadata_manager: MetadataManager):
                super().__init__()
                self.metadata_manager = metadata_manager

            def filter(self, record):
                # Inject metadata into the record
                record.metadata = self.metadata_manager.get_metadata()
                return True

        return MetadataFilter(self.metadata_manager)

    def log(self, level: str, message: str):
        """
        Log a message at the specified level.

        Args:
            level (str): The log level (e.g., "info", "debug", "error").
            message (str): The log message.

        Raises:
            ValueError: If an invalid log level is provided.
        """
        logger = get_logger()
        log_method = getattr(self.logger, level.lower(), None)
        if log_method:
            log_method(message)
        else:
            error_message = f"Invalid log level: {level}"
            logger.log(
                "error",
                error_message)
            raise ValueError(error_message)

    def get_logs(self):
        """
        Retrieve all captured log messages.

        Returns:
            list: A list of captured log messages.
        """
        return self.capturing_handler.get_logs()

    def clear_logs(self):
        """
        Clear all captured log messages.
        """
        self.capturing_handler.clear_logs()

    def set_log_level(self, level: str):
        """
        Dynamically set the logging level.

        Args:
            level (str): The desired logging level
                (e.g., "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL").

        Raises:
            ValueError: If the provided level is invalid.
        """
        level = level.upper()
        if level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            error_message = f"Invalid logging level: {level}"
            self.log("error", error_message)
            raise ValueError(error_message)

        self.logger.setLevel(level)
        for handler in self.logger.handlers:
            handler.setLevel(level)
        self.log("info", f"Logging level set to {level}")


_logger_instance = None  # Global variable to store the logger instance
_logger_lock = threading.Lock()  # Ensure thread safety


def get_logger(metadata_manager=None):
    """
    Retrieve or initialize the singleton instance of DynamicLogger.

    If the logger instance has not been created, this function initializes it
    with the provided `metadata_manager` or a default one. Once initialized,
    the same logger instance is returned for subsequent calls.

    Args:
        metadata_manager (MetadataManager, optional):
            An optional MetadataManager instance to provide metadata for
                logging.
            If None, a default MetadataManager is created with
            `project_name="DefaultProject"` and `table_name="DefaultTable"`.

    Returns:
        DynamicLogger: The singleton logger instance.

    Example Usage:
        # Step 1: Create a logger with default metadata
        logger = get_logger()
        logger.log("info", "This is a log message.")

        # Step 2: Update metadata dynamically
        logger.metadata_manager.update_metadata(
            project_name="NewProject", table_name="NewTable")
        logger.log("info", "This log reflects updated metadata.")

        # Step 3: Retrieve the same logger instance
        same_logger = get_logger()
        same_logger.log("debug", "The logger remains the same instance.")
    """
    global _logger_instance

    # Use a lock to ensure thread-safe initialization
    with _logger_lock:
        if _logger_instance is None:
            if metadata_manager is None:
                # Create a default MetadataManager if none is provided
                metadata_manager = MetadataManager()
                metadata_manager.update_metadata(
                    project_name="DefaultProject", table_name="DefaultTable"
                )

            # Initialize the logger instance
            _logger_instance = DynamicLogger(metadata_manager)
    return _logger_instance


def refresh_logger(metadata_manager=None):
    """
    Force reinitialization of the singleton logger instance.

    This function clears the existing logger instance and creates a new one
    with the provided `metadata_manager` or a default one. Use this function
    when you need to reset the logger or update its metadata manager globally.

    Args:
        metadata_manager (MetadataManager, optional):
            An optional MetadataManager instance to provide metadata for
            logging.
            If None, a new MetadataManager is created with
            `project_name="DefaultProject"` and `table_name="DefaultTable"`.

    Returns:
        DynamicLogger: The refreshed logger instance.

    Example Usage:
        # Step 1: Refresh the logger with new metadata
        new_metadata_manager = MetadataManager()
        new_metadata_manager.update_metadata(
            project_name="RefreshedProject", table_name="RefreshedTable")
        logger = refresh_logger(new_metadata_manager)

        # Step 2: Log messages with the refreshed logger
        logger.log("info", "This log reflects refreshed metadata.")

        # Step 3: Confirm the logger was refreshed
        refreshed_logger = get_logger()
        refreshed_logger.log("debug", "This is the same refreshed instance.")
    """
    global _logger_instance
    # Use a lock to ensure thread-safe refresh
    with _logger_lock:
        print("Refreshing logger instance.")
        _logger_instance = None
    return get_logger(metadata_manager)


def log_message(level: str, message: str):
    """
    Utility function to log messages at a specified level.

    Args:
        level (str): The log level (e.g., "info", "debug", "warning", "error").
        message (str): The log message.

    Raises:
        ValueError: If an invalid log level is provided.
    """
    logger = get_logger()
    valid_levels = {"debug", "info", "warning", "error", "critical"}

    if level.lower() in valid_levels:
        logger.log(level.lower(), message)
    else:
        raise ValueError(f"Invalid log level: {level}")


# Specific log level functions for convenience
def log_info(message: str):
    """Utility function to log info messages."""
    log_message("info", message)


def log_debug(message: str):
    """Utility function to log debug messages."""
    log_message("debug", message)


def log_warning(message: str):
    """Utility function to log warning messages."""
    log_message("warning", message)


def log_error(message: str):
    """Utility function to log error messages."""
    log_message("error", message)


class PandasValidationUtils:
    """
    Class for utility functions related to Pandas DataFrame validation.
    """
    @staticmethod
    def check_missing_columns(
        data: pd.DataFrame,
        required_columns: list,
        validate: bool = True
    ) -> list:
        """
        Check for missing columns in the dataset.

        Args:
            data (pd.DataFrame): The input Pandas DataFrame.
            required_columns (list): List of required column names.
            validate (bool): Whether to validate the inputs (default is True).

        Returns:
            list: A list of missing column names.

        Example:
            import pandas as pd
            from my_module import (
                PandasValidationUtils
            )
            # Example DataFrame
            df = pd.DataFrame({
                'ColumnA': [1, 2, 3],
                'ColumnB': [4, 5, 6]
            })
            # Required columns
            required = ['ColumnA', 'ColumnB', 'ColumnC']
            # Check for missing columns
            missing_columns = PandasValidationUtils.check_missing_columns(
                df, required)
            print(missing_columns)  # Output: ['ColumnC']

            # Disable validation
            missing_columns = PandasValidationUtils.check_missing_columns(
                df, required, validate=False)
            print(missing_columns)  # Output: ['ColumnC']
        """
        if validate:
            # Validate that the input is a DataFrame
            PandasValidationUtils.validate_is_dataframe(
                data, "data")

            # Validate that required_columns is a list
            PandasValidationUtils.validate_is_non_empty_list(
                required_columns
            )

        # Find and return missing columns
        return list(set(required_columns) - set(data.columns))

    @staticmethod
    def concatenate_invalid_rows(
        current_invalid: pd.DataFrame,
        new_invalid: pd.DataFrame,
        validate: bool = True
    ) -> pd.DataFrame:
        """
        Concatenate invalid rows into a single DataFrame.

        Args:
            current_invalid (pd.DataFrame): DataFrame of invalid rows.
            new_invalid (pd.DataFrame): New DataFrame of invalid rows.
            validate (bool): Whether to validate the inputs (default is True).

        Returns:
            pd.DataFrame: Concatenated DataFrame of invalid rows.

        Example:
            ```python
            import pandas as pd
            from my_module import (
                PandasValidationUtils
            )

            # Current invalid rows
            current_invalid = pd.DataFrame({
                'ID': [1, 2],
                'Error': ['Missing value', 'Invalid format']
            })

            # New invalid rows
            new_invalid = pd.DataFrame({
                'ID': [2, 3],
                'Error': ['Invalid format', 'Out of range']
            })

            # Concatenate invalid rows
            concatenated = PandasValidationUtils.concatenate_invalid_rows(
                current_invalid, new_invalid
            )
            print(concatenated)
            # Output:
            #    ID           Error
            # 0   1   Missing value
            # 1   2  Invalid format
            # 2   3    Out of range
            ```
        """
        if validate:
            PandasValidationUtils.validate_is_dataframe(
                current_invalid,
                'current_invalid'
            )
            PandasValidationUtils.validate_is_dataframe(
                new_invalid,
                'new_invalid'
            )
        return pd.concat(
            [current_invalid, new_invalid], ignore_index=True
            ).drop_duplicates().reset_index(drop=True)

    @staticmethod
    def check_column_dtype(
        column: pd.Series,
        expected_type: str,
        validate: bool = True
    ) -> bool:
        """
        Validate if a column's dtype matches the expected type.

        Args:
            column (pd.Series): Pandas Series to validate.
            expected_type (str): Expected Pandas dtype as a string.
            validate (bool): Whether to validate the inputs (default is True).

        Returns:
            bool: True if dtype matches, otherwise False.

        Example:
            ```python
            import pandas as pd
            from my_module import (
                PandasValidationUtils
            )

            # Example column
            example_column = pd.Series([1, 2, 3, 4])

            # Check if dtype is 'int64'
            is_correct_dtype = PandasValidationUtils.check_column_dtype(
                example_column, 'int64'
            )
            print(is_correct_dtype)  # Output: True

            # Check if dtype is 'float64'
            is_correct_dtype = PandasValidationUtils.check_column_dtype(
                example_column, 'float64'
            )
            print(is_correct_dtype)  # Output: False
            ```
        """
        if validate:
            # Validate series
            PandasValidationUtils.validate_is_non_empty_series(
                column,
                'column'
            )
            # Validate string
            PandasValidationUtils.validate_is_non_empty_string(
                expected_type
            )
        return str(column.dtype) == expected_type

    @staticmethod
    def check_value_range(
        series: pd.Series,
        min_val: float,
        max_val: float,
        inclusive: bool = True,
        validate: bool = True
    ) -> pd.DataFrame:
        """
        Check if values in a series fall within the specified range.

        Args:
            series (pd.Series): The series to check.
            min_val (float): Minimum value of the range.
            max_val (float): Maximum value of the range.
            inclusive (bool): If True, include boundaries; otherwise,
                exclude them.
            validate (bool): Whether to validate the inputs (default is True).

        Returns:
            pd.DataFrame: A DataFrame of rows with out-of-range values.

        Example:
            ```python
            import pandas as pd
            from my_module import (
                PandasValidationUtils
            )

            # Example Series
            example_series = pd.Series([5, 10, 15, 20, 25])

            # Check values within the range 10 to 20 (inclusive)
            out_of_range = PandasValidationUtils.check_value_range(
                example_series, min_val=10.0, max_val=20.0, inclusive=True
            )
            print(out_of_range)
            # Output:
            #     0
            # 0   5
            # 4  25

            # Check values within the range 10 to 20 (exclusive)
            out_of_range = PandasValidationUtils.check_value_range(
                example_series, min_val=10.0, max_val=20.0, inclusive=False
            )
            print(out_of_range)
            # Output:
            #     0
            # 0   5
            # 1  10
            # 3  20
            # 4  25
            ```
        """
        if validate:
            PandasValidationUtils.validate_float(
                min_val,
                'min_val')
            PandasValidationUtils.validate_float(
                max_val,
                'max_val')

        if inclusive:
            return series[
                ~series.between(min_val, max_val, inclusive="both")].to_frame()
        else:
            return series[(series <= min_val) | (series >= max_val)].to_frame()

    @staticmethod
    def find_duplicates(
        data: pd.DataFrame,
        column: str,
        validate: bool = True

    ) -> pd.DataFrame:
        """
        Find duplicate rows in the specified column.

        Args:
            data (pd.DataFrame): The DataFrame to check.
            column (str): The column to identify duplicates.
            validate (bool): Whether to validate the inputs (default is True).

        Returns:
            pd.DataFrame: Rows with duplicate values in the specified column.

        Example:
            ```python
            import pandas as pd
            from my_module import (
                PandasValidationUtils
            )

            # Example DataFrame
            df = pd.DataFrame({
                'ID': [1, 2, 3, 2, 4, 1],
                'Name': ['Alice', 'Bob', 'Charlie', 'Bob', 'Eve', 'Alice']
            })

            # Find duplicates in the 'ID' column
            duplicates = PandasValidationUtils.find_duplicates(
                df, column='ID'
            )
            print(duplicates)
            # Output:
            #    ID     Name
            # 0   1    Alice
            # 1   2      Bob
            # 3   2      Bob
            # 5   1    Alice

            # Find duplicates in the 'Name' column
            duplicates = PandasValidationUtils.find_duplicates(
                df, column='Name'
            )
            print(duplicates)
            # Output:
            #    ID     Name
            # 0   1    Alice
            # 1   2      Bob
            # 3   2      Bob
            # 5   1    Alice
            ```
        """
        if validate:
            PandasValidationUtils.validate_is_dataframe(
                data,
                'data'
            )
            PandasValidationUtils.validate_is_non_empty_string(
                column
            )
        return data[data[column].duplicated(keep=False)]

    @staticmethod
    def validate_row_count(
        row_count: int,
        min_rows: int,
        max_rows: int,
        errors: list,
        validate: bool = True
    ):
        """
        Validate row count against specified minimum and maximum constraints.

        Args:
            row_count (int): The current row count of the dataset.
            min_rows (int): Minimum allowed row count.
            max_rows (int): Maximum allowed row count.
            errors (list): List to append error details if validation fails.
            validate (bool): Whether to validate the inputs (default is True).

        Example:
            ```python
            from my_module import (
                PandasValidationUtils
            )

            # Define row count
            current_row_count = 50

            # Define constraints
            min_rows = 30
            max_rows = 100

            # Initialize an empty list to capture errors
            errors = []

            # Validate row count
            PandasValidationUtils.validate_row_count(
                row_count=current_row_count,
                min_rows=min_rows,
                max_rows=max_rows,
                errors=errors
            )

            print(errors)  # Output: []

            # Example with failing validation
            current_row_count = 20
            PandasValidationUtils.validate_row_count(
                row_count=current_row_count,
                min_rows=min_rows,
                max_rows=max_rows,
                errors=errors
            )

            print(errors)
            # Output:
            # [
            #     {
            #         'error_type': 'row_count_violation',
            #         'details': 'Row count 20 is less than
            # the minimum required 30.'
            #     }
            # ]
            ```
        """
        logger = get_logger()
        if validate:
            PandasValidationUtils.validate_is_integer(
                row_count,
                'row_count'
            )
            PandasValidationUtils.validate_is_integer(
                min_rows,
                'min_rows'
            )
            PandasValidationUtils.validate_is_integer(
                max_rows,
                'max_rows'
            )
        if min_rows is not None and row_count < min_rows:
            logger.log(
                "error",
                f"Row count {row_count} "
                f"is less than the minimum required {min_rows}.")
            errors.append({
                "error_type": "row_count_violation",
                "details": f"Row count {row_count} "
                f"is less than the minimum required {min_rows}."
            })

        if max_rows is not None and row_count > max_rows:
            logger.log(
                "error",
                f"Row count {row_count} "
                f"exceeds the maximum allowed {max_rows}.")
            errors.append({
                "error_type": "row_count_violation",
                "details": f"Row count {row_count} "
                f"exceeds the maximum allowed {max_rows}."
            })

    @staticmethod
    def validate_is_non_empty_dataset(
        data: pd.DataFrame,
        errors: list,
        validate: bool = True
    ):
        """
        Check if the DataFrame is empty and update the errors list
        if validation fails.

        Args:
            data (pd.DataFrame): The DataFrame to validate.
            errors (list): List to append error details if validation fails.
            validate (bool): Whether to validate the inputs (default is True).

        Example:
            ```python
            import pandas as pd
            from my_module import (
                PandasValidationUtils
            )

            # Example with a non-empty DataFrame
            df = pd.DataFrame({
                'ColumnA': [1, 2, 3],
                'ColumnB': [4, 5, 6]
            })

            errors = []

            # Validate non-empty DataFrame
            PandasValidationUtils.validate_is_non_empty_dataset(df, errors)
            print(errors)  # Output: []

            # Example with an empty DataFrame
            empty_df = pd.DataFrame()

            PandasValidationUtils.validate_is_non_empty_dataset(
                empty_df, errors)
            print(errors)
            # Output:
            # [
            #     {
            #         "error_type": "empty_dataset",
            #         "details": "The dataset is empty (no rows or columns)."
            #     }
            # ]
            ```
        """
        logger = get_logger()
        if validate:
            PandasValidationUtils.validate_is_dataframe(
                data,
                'data'
            )
        if data.empty:
            logger.log("error", "The dataset is empty (no rows or columns).")
            errors.append({
                "error_type": "empty_dataset",
                "details": "The dataset is empty (no rows or columns)."
            })

    @staticmethod
    def validate_column_values(
        data: pd.DataFrame,
        column: str,
        values: list,
        allow_only: bool,
        errors: list,
        validate: bool = True
    ):
        """
        Validate column values against specified rules.

        Args:
            data (pd.DataFrame): The DataFrame to validate.
            column (str): Column name to validate.
            values (list): List of allowed or prohibited values.
            allow_only (bool): If True, validate only allowed values.
                            If False, validate prohibited values.
            errors (list): List to append error details if validation fails.
            validate (bool): Whether to validate the inputs (default is True).

        Returns:
            pd.DataFrame: DataFrame of rows with invalid values.

        Example:
            ```python
            import pandas as pd
            from my_module import (
                PandasValidationUtils
            )

            # Example DataFrame
            df = pd.DataFrame({
                'Category': ['A', 'B', 'C', 'D', 'E']
            })

            errors = []

            # Validate only allowed values
            allowed_values = ['A', 'B', 'C']
            invalid_rows = PandasValidationUtils.validate_column_values(
                data=df,
                column='Category',
                values=allowed_values,
                allow_only=True,
                errors=errors
            )
            print(invalid_rows)
            # Output:
            #   Category
            # 3       D
            # 4       E

            print(errors)
            # Output:
            # [
            #     {
            #         "error_type": "value_violation",
            #         "details": "Column 'Category' contains values
            #           not allowed: ['A', 'B', 'C']."
            #     }
            # ]

            # Validate prohibited values
            prohibited_values = ['D', 'E']
            invalid_rows = PandasValidationUtils.validate_column_values(
                data=df,
                column='Category',
                values=prohibited_values,
                allow_only=False,
                errors=errors
            )
            print(invalid_rows)
            # Output:
            #   Category
            # 3       D
            # 4       E

            print(errors)
            # Output:
            # [
            #     {
            #         "error_type": "value_violation",
            #         "details": "Column 'Category' contains values
            #           prohibited: ['D', 'E']."
            #     }
            # ]
            ```
        """
        logger = get_logger()
        if validate:
            PandasValidationUtils.validate_is_dataframe(
                data,
                'data'
            )
            PandasValidationUtils.validate_is_non_empty_string(
                column
            )
            PandasValidationUtils.validate_is_non_empty_list(
                values
            ),
            PandasValidationUtils.validate_is_boolean(
                allow_only,
                'data'
            ),
            PandasValidationUtils.validate_is_non_empty_list(
                errors
            )
        invalid = ~data[
            column].isin(values) if allow_only else data[column].isin(values)
        invalid_data = data[invalid]
        if not invalid_data.empty:
            validation_type = "allowed" if allow_only else "prohibited"
            error_message = (
                f"Column '{column}'" +
                f" contains values not {validation_type}: {values}.")
            logger.log("error", error_message)
            errors.append({
                "error_type": "value_violation",
                "details": error_message
            })
        return invalid_data

    @staticmethod
    def validate_column_regex(
        data: pd.DataFrame,
        column: str,
        pattern: str,
        errors: list,
        validate: bool = True
    ):
        """
        Validate column values against a regex pattern.

        Args:
            data (pd.DataFrame): The DataFrame to validate.
            column (str): Column name to validate.
            pattern (str): Regex pattern to match.
            errors (list): List to append error details if validation fails.
            validate (bool): Whether to validate the inputs (default is True).

        Returns:
            pd.DataFrame: DataFrame of rows with invalid values.

        Example:
            ```python
            import pandas as pd
            from my_module import (
                PandasValidationUtils
            )

            # Example DataFrame
            df = pd.DataFrame({
                'Email': [
                    'valid@example.com',
                    'invalid-email',
                    'test@domain.com',
                    'wrong@com']
            })

            errors = []

            # Validate column values against regex pattern
            email_pattern = r'^[
                a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
            invalid_rows = PandasValidationUtils.validate_column_regex(
                data=df,
                column='Email',
                pattern=email_pattern,
                errors=errors
            )
            print(invalid_rows)
            # Output:
            #             Email
            # 1  invalid-email
            # 3      wrong@com

            print(errors)
            # Output:
            # [
            #     {
            #         "error_type": "regex_violation",
            #         "details": "Column 'Email' contains values not matching
            #           `the regex pattern '^[
                #        a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'."
            #     }
            # ]
            ```
        """
        logger = get_logger()
        if validate:
            PandasValidationUtils.validate_is_dataframe(
                data,
                'data'
            )
            PandasValidationUtils.validate_is_non_empty_string(
                column
            )
            PandasValidationUtils.validate_is_non_empty_string(
                pattern
            ),
            PandasValidationUtils.validate_is_non_empty_list(
                errors
            )
        invalid = ~data[column].astype(str).str.match(pattern, na=False)
        invalid_data = data[invalid]
        if not invalid_data.empty:
            error_message = (
                f"Column '{column}' " +
                f"contains values not matching the regex pattern '{pattern}'.")
            logger.log("error", error_message)
            errors.append({
                "error_type": "regex_violation",
                "details": error_message
            })
        return invalid_data

    @staticmethod
    def detect_duplicates(
        data: pd.DataFrame,
        subset: list = None,
        validate: bool = True
    ) -> pd.DataFrame:
        """
        Detect duplicate rows in a DataFrame.

        Args:
            data (pd.DataFrame): The DataFrame to check for duplicates.
            subset (list, optional): List of column names to consider when
                identifying duplicates. If None, all columns are used.
            validate (bool): Whether to validate the inputs (default is True).

        Returns:
            pd.DataFrame: DataFrame containing duplicate rows.

        Example:
            ```python
            import pandas as pd
            from my_module import (
                PandasValidationUtils
            )

            # Example DataFrame
            df = pd.DataFrame({
                'ID': [1, 2, 3, 2, 4, 1],
                'Name': ['Alice', 'Bob', 'Charlie', 'Bob', 'Eve', 'Alice'],
                'Age': [25, 30, 35, 30, 40, 25]
            })

            # Detect duplicates considering all columns
            duplicates = PandasValidationUtils.detect_duplicates(df)
            print(duplicates)
            # Output:
            #    ID   Name  Age
            # 0   1  Alice   25
            # 1   2    Bob   30
            # 3   2    Bob   30
            # 5   1  Alice   25

            # Detect duplicates based on 'ID' column only
            duplicates = PandasValidationUtils.detect_duplicates(
                df, subset=['ID'])
            print(duplicates)
            # Output:
            #    ID     Name  Age
            # 0   1    Alice   25
            # 3   2      Bob   30
            # 5   1    Alice   25
            ```
        """
        if validate:
            PandasValidationUtils.validate_is_dataframe(
                data,
                'data'
            )
            if subset:
                PandasValidationUtils.validate_is_non_empty_list(
                    subset
                )
        return data[data.duplicated(keep=False, subset=subset)]

    @staticmethod
    def validate_column_dependency(
        data: pd.DataFrame,
        primary: str,
        dependent: str,
        validate: bool = True
    ) -> pd.DataFrame:
        """
        Validate dependency between two columns.

        Args:
            data (pd.DataFrame): Dataset to validate.
            primary (str): Primary column name. Non-null values in this column
                        require non-null values in the dependent column.
            dependent (str): Dependent column name.
            validate (bool): Whether to validate the inputs (default is True).

        Returns:
            pd.DataFrame: Rows violating the dependency.

        Example:
            ```python
            import pandas as pd
            from my_module import (
                PandasValidationUtils
            )

            # Example DataFrame
            df = pd.DataFrame({
                'OrderID': [1, 2, 3, 4],
                'CustomerName': ['Alice', 'Bob', None, 'Eve']
            })

            # Validate dependency between 'OrderID' and 'CustomerName'
            violations = PandasValidationUtils.validate_column_dependency(
                data=df,
                primary='OrderID',
                dependent='CustomerName'
            )
            print(violations)
            # Output:
            #    OrderID CustomerName
            # 2        3         None
            ```
        """
        if validate:
            PandasValidationUtils.validate_is_dataframe(
                data,
                'data'
            )
            PandasValidationUtils.validate_is_non_empty_string(
                primary
            )
            PandasValidationUtils.validate_is_non_empty_string(
                dependent
            )
        return data[
            data[primary].notnull() & (data[dependent].isnull() | (
                data[dependent] == ""))]

    @staticmethod
    def validate_case_style(
        case_style: str,
        valid_styles: list,
        validate: bool = True
    ) -> None:
        """
        Validate the provided case style against valid options.

        Args:
            case_style (str): The case style to validate.
            valid_styles (list): List of valid case styles.
            validate (bool): Whether to validate the inputs (default is True).

        Raises:
            ValueError: If the case style is invalid.

        Example:
            ```python
            from my_module import (
                PandasValidationUtils
            )

            # Define valid case styles
            valid_styles = [
                'snake_case',
                'camelCase',
                'PascalCase']

            # Valid case style
            PandasValidationUtils.validate_case_style(
                case_style='snake_case',
                valid_styles=valid_styles
            )  # No error raised

            # Invalid case style
            try:
                PandasValidationUtils.validate_case_style(
                    case_style='kebab-case',
                    valid_styles=valid_styles
                )
            except ValueError as e:
                print(e)
            # Output:
            # Invalid case style: kebab-case. Must be one of [
                # 'snake_case', 'camelCase', 'PascalCase'].
            ```
        """
        logger = get_logger()
        if validate:
            PandasValidationUtils.validate_is_non_empty_string(
                case_style
            )
            PandasValidationUtils.validate_is_non_empty_list(
                valid_styles
            )
        if case_style not in valid_styles:
            error_message = (
                "Invalid case style: " +
                f"{case_style}. Must be one of {valid_styles}."
            )
            logger.log(
                "error",
                error_message)
            raise ValueError(error_message)

    @staticmethod
    def transform_column_name(
        column_name: str,
        case_style: str,
        validate: bool = True
    ) -> str:
        """
        Transform a column name to the specified case style.

        Args:
            column_name (str): The column name to transform.
            case_style (str): The desired case style. Supported styles are:
                            - "snake_case"
                            - "camelCase"
                            - "PascalCase"
                            - "lowercase"
                            - "uppercase"
            validate (bool): Whether to validate the inputs (default is True).

        Returns:
            str: The transformed column name.

        Example:
            ```python
            from my_module import (
                PandasValidationUtils
            )

            # Transform to snake_case
            result = PandasValidationUtils.transform_column_name(
                column_name="My Column Name", case_style="snake_case"
            )
            print(result)  # Output: my_column_name

            # Transform to camelCase
            result = PandasValidationUtils.transform_column_name(
                column_name="My Column Name", case_style="camelCase"
            )
            print(result)  # Output: myColumnName

            # Transform to PascalCase
            result = PandasValidationUtils.transform_column_name(
                column_name="My Column Name", case_style="PascalCase"
            )
            print(result)  # Output: MyColumnName

            # Transform to lowercase
            result = PandasValidationUtils.transform_column_name(
                column_name="My Column Name", case_style="lowercase"
            )
            print(result)  # Output: my column name

            # Transform to uppercase
            result = PandasValidationUtils.transform_column_name(
                column_name="My Column Name", case_style="uppercase"
            )
            print(result)  # Output: MY COLUMN NAME
            ```
        """
        if validate:
            PandasValidationUtils.validate_is_non_empty_string(
                column_name
            )
            PandasValidationUtils.validate_is_non_empty_string(
                case_style
            )
        if case_style == "snake_case":
            return re.sub(
                r"(_|-|\s)+", " ", column_name).lower().replace(" ", "_")
        elif case_style == "camelCase":
            temp = re.sub(
                r"(_|-|\s)+", " ", column_name).title().replace(" ", "")
            return temp[0].lower() + temp[1:]
        elif case_style == "PascalCase":
            return re.sub(
                r"(_|-|\s)+", " ", column_name).title().replace(" ", "")
        elif case_style == "lowercase":
            return column_name.lower()
        elif case_style == "uppercase":
            return column_name.upper()
        return column_name

    @staticmethod
    def add_prefix_suffix_to_columns(
        column_name: str,
        prefix: str = "",
        suffix: str = "",
        validate: bool = True
    ) -> str:
        """
        Add a prefix and/or suffix to a column name.

        Args:
            column_name (str): The column name to update.
            prefix (str): The prefix to add. Defaults to an empty string.
            suffix (str): The suffix to add. Defaults to an empty string.
            validate (bool): Whether to validate the inputs (default is True).

        Returns:
            str: The updated column name with prefix and/or suffix.

        Example:
            ```python
            from my_module import (
                PandasValidationUtils
            )

            # Add a prefix to the column name
            result = PandasValidationUtils.add_prefix_suffix_to_columns(
                column_name="Sales", prefix="Total_"
            )
            print(result)  # Output: Total_Sales

            # Add a suffix to the column name
            result = PandasValidationUtils.add_prefix_suffix_to_columns(
                column_name="Revenue", suffix="_2023"
            )
            print(result)  # Output: Revenue_2023

            # Add both prefix and suffix to the column name
            result = PandasValidationUtils.add_prefix_suffix_to_columns(
                column_name="Profit", prefix="Annual_", suffix="_2023"
            )
            print(result)  # Output: Annual_Profit_2023

            # No prefix or suffix
            result = PandasValidationUtils.add_prefix_suffix_to_columns(
                column_name="Cost"
            )
            print(result)  # Output: Cost
            ```
        """
        if validate:
            PandasValidationUtils.validate_is_non_empty_string(
                column_name
            )
        return f"{prefix}{column_name}{suffix}"

    @staticmethod
    def rename_column_with_regex(
        column_name: str,
        pattern: str,
        replacement: str,
        validate: bool = True
    ) -> str:
        """
        Rename a column name using a regex pattern.

        Args:
            column_name (str): The column name to transform.
            pattern (str): The regex pattern to search for.
            replacement (str): The string to replace matching patterns with.
            validate (bool): Whether to validate the inputs (default is True).

        Returns:
            str: The transformed column name.

        Example:
            ```python
            import re
            from my_module import (
                PandasValidationUtils
            )

            # Example 1: Replace spaces with underscores
            result = PandasValidationUtils.rename_column_with_regex(
                column_name="Column Name With Spaces",
                pattern=r"\\s+",
                replacement="_"
            )
            print(result)  # Output: Column_Name_With_Spaces

            # Example 2: Remove numeric characters
            result = PandasValidationUtils.rename_column_with_regex(
                column_name="Column123Name456",
                pattern=r"\\d+",
                replacement=""
            )
            print(result)  # Output: ColumnName

            # Example 3: Replace hyphens with spaces
            result = PandasValidationUtils.rename_column_with_regex(
                column_name="Column-Name-With-Hyphens",
                pattern=r"-",
                replacement=" "
            )
            print(result)  # Output: Column Name With Hyphens
            ```
        """
        if validate:
            PandasValidationUtils.validate_is_non_empty_string(
                column_name
            )
            PandasValidationUtils.validate_is_non_empty_string(
                pattern
            )
        return re.sub(pattern, replacement, column_name)

    @staticmethod
    def get_columns_matching_pattern(
        data: pd.DataFrame,
        pattern: str,
        validate: bool = True
    ) -> list:
        """
        Get a list of columns matching a regex pattern.

        Args:
            data (pd.DataFrame): The input DataFrame.
            pattern (str): The regex pattern to match column names.
            validate (bool): Whether to validate the inputs (default is True).

        Returns:
            list: List of column names matching the pattern.

        Example:
            ```python
            import pandas as pd
            from my_module import (
                PandasValidationUtils
            )

            # Example DataFrame
            df = pd.DataFrame({
                'sales_2023': [100, 200],
                'profit_2023': [50, 70],
                'cost_2022': [30, 40],
                'revenue': [150, 270]
            })

            # Get columns matching the pattern for "2023"
            matching_columns = PandasValidationUtils\
                .get_columns_matching_pattern(
                data=df,
                pattern=r'.*_2023'
            )
            print(matching_columns)  # Output: ['sales_2023', 'profit_2023']

            # Get columns starting with 're'
            matching_columns = PandasValidationUtils.\
                get_columns_matching_pattern(
                data=df,
                pattern=r'^re.*'
            )
            print(matching_columns)  # Output: ['revenue']
            ```
        """
        if validate:
            PandasValidationUtils.validate_is_dataframe(
                data,
                'data'
            )
            PandasValidationUtils.validate_is_non_empty_string(
                pattern
            )
        return [col for col in data.columns if re.match(pattern, col)]

    @staticmethod
    def get_empty_columns(
        data: pd.DataFrame,
        validate: bool = True
    ) -> list:
        """
        Identify columns with all values as NaN.

        Args:
            data (pd.DataFrame): The input DataFrame.
            validate (bool): Whether to validate the inputs (default is True).

        Returns:
            list: List of column names where all values are NaN.

        Example:
            ```python
            import pandas as pd
            from my_module import (
                PandasValidationUtils
            )

            # Example DataFrame
            df = pd.DataFrame({
                'A': [1, 2, 3],
                'B': [None, None, None],
                'C': [5, None, 7],
                'D': [None, None, None]
            })

            # Get columns with all NaN values
            empty_columns = PandasValidationUtils.get_empty_columns(data=df)
            print(empty_columns)  # Output: ['B', 'D']
            ```
        """
        if validate:
            PandasValidationUtils.validate_is_dataframe(
                data,
                'data'
            )
        return [col for col in data.columns if data[col].isna().all()]

    @staticmethod
    def get_columns_by_dtypes(
        data: pd.DataFrame,
        data_types: list,
        validate: bool = True
    ) -> list:
        """
        Identify columns of specific data types.

        Args:
            data (pd.DataFrame): The input DataFrame.
            data_types (list): List of data types to filter (
                e.g., ["float64", "int64"]).
            validate (bool): Whether to validate the inputs (default is True).

        Returns:
            list: List of column names with specified data types.

        Example:
            ```python
            import pandas as pd
            from my_module import (
                PandasValidationUtils
            )

            # Example DataFrame
            df = pd.DataFrame({
                'A': [1, 2, 3],       # int64
                'B': [1.1, 2.2, 3.3], # float64
                'C': ['x', 'y', 'z'], # object
                'D': [True, False, True] # bool
            })

            # Get columns with numeric data types
            numeric_columns = PandasValidationUtils.get_columns_by_dtypes(
                data=df, data_types=["float64", "int64"]
            )
            print(numeric_columns)  # Output: ['A', 'B']

            # Get columns with boolean data type
            bool_columns = PandasValidationUtils.get_columns_by_dtypes(
                data=df, data_types=["bool"]
            )
            print(bool_columns)  # Output: ['D']

            # Get columns with object data type
            object_columns = PandasValidationUtils.get_columns_by_dtypes(
                data=df, data_types=["object"]
            )
            print(object_columns)  # Output: ['C']
            ```
        """
        if validate:
            PandasValidationUtils.validate_is_dataframe(
                data,
                'data'
            )
            PandasValidationUtils.validate_is_non_empty_list(
                data_types
            )
        return data.select_dtypes(include=data_types).columns.tolist()

    @staticmethod
    def split_column(
        data: pd.DataFrame,
        column: str,
        pattern: str,
        regex: bool = False,
        validate: bool = True
    ) -> pd.DataFrame:
        """
        Split a column into multiple columns based on a pattern or regex.

        Args:
            data (pd.DataFrame): The input DataFrame.
            column (str): The column to split.
            pattern (str): The delimiter or regex pattern to use for splitting.
            regex (bool): Whether to treat the pattern as a regex.
                Defaults to False.
            validate (bool): Whether to validate the inputs
                (default is True).

        Returns:
            pd.DataFrame: A DataFrame with the column split into
                multiple columns.

        Raises:
            KeyError: If the specified column is not found in the DataFrame.

        Example:
            ```python
            import pandas as pd
            from my_module import (
                PandasValidationUtils
            )

            # Example DataFrame
            df = pd.DataFrame({
                'FullName': ['John Doe', 'Jane Smith', 'Emily Davis']
            })

            # Split column based on space delimiter
            split_df = PandasValidationUtils.split_column(
                data=df,
                column='FullName',
                pattern=' ',
                regex=False
            )
            print(split_df)
            # Output:
            #         0       1
            # 0    John     Doe
            # 1    Jane   Smith
            # 2   Emily   Davis

            # Split column based on regex pattern (split on any whitespace)
            split_df = PandasValidationUtils.split_column(
                data=df,
                column='FullName',
                pattern=r'\\s+',
                regex=True
            )
            print(split_df)
            # Output:
            #         0       1
            # 0    John     Doe
            # 1    Jane   Smith
            # 2   Emily   Davis
            ```
        """
        logger = get_logger()
        if validate:
            PandasValidationUtils.validate_is_dataframe(
                data,
                'data'
            )
            PandasValidationUtils.validate_is_non_empty_string(
                column
            )
            PandasValidationUtils.validate_is_non_empty_string(
                pattern
            )
            PandasValidationUtils.validate_is_boolean(
                regex,
                'regex'
            )
        if column not in data.columns:
            error_message = f"Column '{column}' not found in DataFrame."
            logger.log(
                logging.ERROR,
                error_message)
            raise KeyError(error_message)
        if regex:
            return data[column].str.strip().str.split(pattern, expand=True)
        return data[column].str.strip().str.split(pattern, expand=True)

    @staticmethod
    def merge_columns(
        data: pd.DataFrame,
        columns: list,
        separator: str = " ",
        validate: bool = True
    ) -> pd.Series:
        """
        Merge multiple columns into a single column, excluding None or
        NaN values.

        Args:
            data (pd.DataFrame): The input DataFrame.
            columns (list): List of columns to merge.
            separator (str): Separator to use between values.
                Defaults to a single space.
            validate (bool): Whether to validate the inputs (default is True).

        Returns:
            pd.Series: A Pandas Series containing the merged column.

        Raises:
            KeyError: If any of the specified columns are missing from
            the DataFrame.

        Example:
            ```python
            import pandas as pd
            from my_module import (
                PandasValidationUtils
            )

            # Example DataFrame
            df = pd.DataFrame({
                'FirstName': ['John', 'Jane', None],
                'LastName': ['Doe', 'Smith', 'Brown'],
                'Age': [30, None, 45]
            })

            # Merge 'FirstName' and 'LastName' with a space separator
            merged = PandasValidationUtils.merge_columns(
                data=df,
                columns=['FirstName', 'LastName'],
                separator=" "
            )
            print(merged)
            # Output:
            # 0      John Doe
            # 1    Jane Smith
            # 2      None Brown
            # dtype: object

            # Merge 'FirstName', 'LastName', and 'Age' with a comma separator
            merged = PandasValidationUtils.merge_columns(
                data=df,
                columns=['FirstName', 'LastName', 'Age'],
                separator=", "
            )
            print(merged)
            # Output:
            # 0    John, Doe, 30
            # 1      Jane, Smith
            # 2      None, Brown, 45
            # dtype: object
            ```
        """
        logger = get_logger()
        if validate:
            PandasValidationUtils.validate_is_dataframe(
                data,
                'data'
            )
            PandasValidationUtils.validate_is_non_empty_list(
                columns
            )
            PandasValidationUtils.validate_is_non_empty_string(
                separator
            )
        PandasValidationUtils.check_missing_columns(
            data,
            columns,
            False
        )
        # if any(col not in data.columns for col in columns):
        # missing_cols = [col for col in columns if col not in data.columns]
        missing_cols = PandasValidationUtils.check_missing_columns(
            data,
            columns,
            False
        )
        if missing_cols:
            error_message = f"Missing columns: {missing_cols}"
            logger.log(
                "error",
                error_message)
            raise KeyError(error_message)
        # Exclude None or NaN values during the join
        return data[columns].apply(
            lambda row: separator.join(
                [str(val) for val in row if pd.notna(val)]),
            axis=1
        )

    @staticmethod
    def validate_column_is_list_type(
        data: pd.DataFrame,
        column: str,
        validate: bool = True
    ) -> None:
        """
        Ensure all values in the specified column are lists.

        Args:
            data (pd.DataFrame): The input DataFrame.
            column (str): The column name to check.
            validate (bool): Whether to validate the inputs (default is True).

        Raises:
            ValueError: If any value in the column is not a list.

        Example:
            ```python
            import pandas as pd
            from my_module import (
                PandasValidationUtils
            )

            # Example DataFrame
            df = pd.DataFrame({
                'Lists': [[1, 2], ['a', 'b'], [3.5, 4.5]],
                'Mixed': [[1, 2], 'not a list', None]
            })

            # Validate column with only lists
            PandasValidationUtils.validate_column_is_list_type(
                data=df,
                column='Lists'
            )  # No exception raised

            # Validate column with non-list values
            try:
                PandasValidationUtils.validate_column_is_list_type(
                    data=df,
                    column='Mixed'
                )
            except ValueError as e:
                print(e)
            # Output:
            # Column 'Mixed' must contain lists.
            ```
        """
        logger = get_logger()
        if validate:
            PandasValidationUtils.validate_is_dataframe(
                data,
                'data'
            )
            PandasValidationUtils.validate_is_non_empty_string(
                column
            )
        if not data[column].apply(lambda x: isinstance(x, list)).all():
            error_message = f"Column '{column}' must contain lists."
            logger.log(
                "error",
                error_message)
            raise ValueError(error_message)

    @staticmethod
    def validate_column_contains_delimiter(
        data: pd.DataFrame,
        column: str,
        delimiter: str,
        validate: bool = True,
    ) -> None:
        """
        Ensure all values in the specified column contain the given delimiter.

        Args:
            data (pd.DataFrame): The input DataFrame.
            column (str): The column name to check.
            delimiter (str): The delimiter to validate.
            validate (bool): Whether to validate the inputs (default is True).

        Raises:
            ValueError: If any value in the column does not contain
            the delimiter.

        Example:
            ```python
            import pandas as pd
            from my_module import (
                PandasValidationUtils
            )

            # Example DataFrame
            df = pd.DataFrame({
                'Emails': [
                    'user1@example.com',
                    'user2@example.com',
                    'invalid-email'],
                'Names': ['John Doe', 'Jane Smith', 'Emily Davis']
            })

            # Validate that all values in 'Emails' contain '@'
            try:
                PandasValidationUtils.validate_column_contains_delimiter(
                    data=df,
                    column='Emails',
                    delimiter='@'
                )
            except ValueError as e:
                print(e)
            # No exception for valid rows

            # Validate that all values in 'Names' contain a space
            try:
                PandasValidationUtils.validate_column_contains_delimiter(
                    data=df,
                    column='Names',
                    delimiter=' '
                )
            except ValueError as e:
                print(e)
            # No exception for valid rows

            # Example with invalid data
            df_invalid = pd.DataFrame(
                {'Column': ['value1', 'value2', 'invalidX'],})
            ```
        """
        logger = get_logger()
        if validate:
            PandasValidationUtils.validate_is_dataframe(
                data,
                'data'
            )
            PandasValidationUtils.validate_is_non_empty_string(
                column
            )
            PandasValidationUtils.validate_is_non_empty_string(
                delimiter
            )
        if not data[column].apply(lambda x: isinstance(
            x, str) and delimiter in x
                                ).any():
            error_message = (
                "Column '{column}' " +
                "must contain strings with the delimiter '{delimiter}'."
            )
            logger.log(
                "error",
                error_message)
            raise ValueError(error_message)

    @staticmethod
    def group_and_aggregate(
        data: pd.DataFrame,
        group_by: list,
        agg_config: dict,
        validate: bool = True,
        **kwargs
    ) -> pd.DataFrame:
        """
        Group rows by specified columns and apply aggregation functions.

        Args:
            data (pd.DataFrame): The input DataFrame.
            group_by (list): List of columns to group by.
            agg_config (dict): Aggregation configuration with column-function
                mappings. For example, {
                    'column1': 'sum', 'column2': ['mean', 'max']}.
            validate (bool): Whether to validate the inputs (default is True).
            **kwargs: Additional parameters for `groupby()` and `agg()`.

        Returns:
            pd.DataFrame: The grouped and aggregated DataFrame.

        Raises:
            Exception: If any errors occur during aggregation.

        Example:
            ```python
            import pandas as pd
            from my_module import (
                PandasValidationUtils
            )

            # Example DataFrame
            df = pd.DataFrame({
                'Category': ['A', 'B', 'A', 'B', 'C'],
                'SubCategory': ['X', 'X', 'Y', 'Y', 'Z'],
                'Value': [10, 20, 30, 40, 50]
            })

            # Group and aggregate configuration
            agg_config = {
                'Value': ['sum', 'mean']
            }

            # Group by 'Category' and 'SubCategory' and apply aggregation
            grouped_data = PandasValidationUtils.group_and_aggregate(
                data=df,
                group_by=['Category', 'SubCategory'],
                agg_config=agg_config
            )
            print(grouped_data)
            # Output:
            #   Category SubCategory  Value_sum  Value_mean
            # 0        A           X         10        10.0
            # 1        A           Y         30        30.0
            # 2        B           X         20        20.0
            # 3        B           Y         40        40.0
            # 4        C           Z         50        50.0
            ```
        """
        logger = get_logger()
        if validate:
            PandasValidationUtils.validate_is_dataframe(
                data,
                'data'
            )
            PandasValidationUtils.validate_is_non_empty_list(
                group_by
            )
            PandasValidationUtils.validate_is_non_empty_dict(
                agg_config
            )
        try:
            aggregated_data = data.groupby(
                group_by, **kwargs).agg(agg_config).reset_index()
            return aggregated_data
        except Exception as e:
            error_message = f"Error during group-and-aggregate: {e}"
            logger.log(
                "error",
                error_message)
            raise Exception(error_message)

    @staticmethod
    def validate_columns_exist(
        data: pd.DataFrame,
        columns: list,
        validate: bool = True
    ) -> None:
        """
        Validate that the specified columns exist in the DataFrame.

        Args:
            data (pd.DataFrame): The input DataFrame.
            columns (list): List of column names to validate.
            validate (bool): Whether to validate the inputs (default is True).

        Raises:
            KeyError: If any column is missing from the DataFrame.

        Example:
            ```python
            import pandas as pd
            from my_module import (
                PandasValidationUtils
            )

            # Example DataFrame
            df = pd.DataFrame({
                'ColumnA': [1, 2, 3],
                'ColumnB': [4, 5, 6],
                'ColumnC': [7, 8, 9]
            })

            # Validate existing columns
            PandasValidationUtils.validate_columns_exist(
                data=df,
                columns=['ColumnA', 'ColumnB']
            )  # No exception raised

            # Validate with missing columns
            try:
                PandasValidationUtils.validate_columns_exist(
                    data=df,
                    columns=['ColumnA', 'ColumnD']
                )
            except KeyError as e:
                print(e)
            # Output:
            # Columns not found in DataFrame: ['ColumnD']
            ```
        """
        logger = get_logger()
        if validate:
            PandasValidationUtils.validate_is_dataframe(
                data,
                'data'
            )
            PandasValidationUtils.validate_is_non_empty_list(
                columns
            )
        # Use check_missing_columns to identify missing columns
        missing_columns = PandasValidationUtils.check_missing_columns(
            data,
            columns)
        if missing_columns:
            error_message = (
                "Columns not found in DataFrame: {missing_columns}"
            )
            logger.log(
                "error",
                error_message)
            raise KeyError(error_message)

    @staticmethod
    def validate_is_dataframe(
        data: Any,
        name: str = "Input",
        validate: bool = True
    ) -> None:
        """
        Validate that the input is a Pandas DataFrame.

        Args:
            data (Any): The input to validate.
            name (str, optional): Name of the input for more descriptive error
                messages. Defaults to "Input".
            validate (bool): Whether to validate the inputs (default is True).

        Raises:
            ValueError: If the input is not a Pandas DataFrame.

        Example:
            ```python
            import pandas as pd
            from my_module import (
                PandasValidationUtils
            )

            # Example with a valid DataFrame
            df = pd.DataFrame({'A': [1, 2, 3]})
            PandasValidationUtils.validate_is_dataframe(
                data=df,
                name="MyDataFrame"
            )  # No exception raised

            # Example with an invalid input
            not_a_df = [1, 2, 3]
            try:
                PandasValidationUtils.validate_is_dataframe(
                    data=not_a_df,
                    name="NotADataFrame"
                )
            except ValueError as e:
                print(e)
            # Output:
            # NotADataFrame must be a Pandas DataFrame.
            ```
        """
        logger = get_logger()
        if validate:
            PandasValidationUtils.validate_is_non_empty_string(
                name
            )
        if not isinstance(data, pd.DataFrame):
            error_message = f"{name} must be a Pandas DataFrame."
            logger.log(
                "error",
                error_message)
            raise ValueError(error_message)

    @staticmethod
    def validate_sampling_parameters(
        mode: str,
        n: int = None,
        frac: float = None,
        validate: bool = True
    ) -> None:
        """
        Validate sampling parameters based on the sampling mode.

        Args:
            mode (str): Sampling mode. Options are "random", "head", "tail".
            n (int, optional): Number of rows for "head" or "tail".
            frac (float, optional): Fraction of rows for "random".
            validate (bool): Whether to validate the inputs (default is True).

        Raises:
            ValueError: If the parameters are invalid.

        Example:
            ```python
            from my_module import (
                PandasValidationUtils
            )

            # Example 1: Valid sampling parameters for "head"
            PandasValidationUtils.validate_sampling_parameters(
                mode="head",
                n=5,
                frac = 0.3
            )  # No exception raised
            ```
        """
        logger = get_logger()
        if validate:
            PandasValidationUtils.validate_is_non_empty_string(
                mode
            )
            PandasValidationUtils.validate_is_integer(
                n,
                'n'
            )
            PandasValidationUtils.validate_float(
                frac,
                'frac'
            )
        if mode in {"head", "tail"} and (
            n is None or not isinstance(n, int) or n <= 0
        ):
            if logger:
                error_message = (
                    "n must be a positive integer " +
                    "for 'head' or 'tail'.")
                logger.log(
                    "error",
                    error_message)
            raise ValueError(error_message)

        if mode == "random" and (frac is None or not (0 < frac <= 1)):
            if logger:
                error_message = (
                    "frac must be a float between " +
                    "0 and 1 for 'random'.")
                logger.log(
                    "error",
                    error_message)
            raise ValueError(error_message)

    @staticmethod
    def log_row_count_change(
        original_count: int,
        new_count: int,
        action: str = "Processed",
        validate: bool = True
    ):
        """
        Log the change in row count after an action.

        Args:
            original_count (int): Number of rows before the action.
            new_count (int): Number of rows after the action.
            action (str, optional): Description of the action.
                Defaults to "Processed".
            validate (bool): Whether to validate the inputs (default is True).

        Example:
            ```python
            from my_module import (
                PandasValidationUtils
            )

            # Example 1: Log a filtering action
            PandasValidationUtils.log_row_count_change(
                original_count=100,
                new_count=80,
                action="Filtered rows"
            )
            # Output (logged): Filtered rows. Original rows: 100,
            # Resulting rows: 80

            # Example 2: Log a transformation action
            PandasValidationUtils.log_row_count_change(
                original_count=100,
                new_count=100,
                action="Applied transformation"
            )
            # Output (logged): Applied transformation. Original rows: 100,
            # Resulting rows: 100
            ```
        """
        logger = get_logger()
        if validate:
            PandasValidationUtils.validate_is_integer(
                original_count,
                'original_count'
            )
            PandasValidationUtils.validate_is_integer(
                new_count,
                'new_count'
            )
            PandasValidationUtils.validate_is_non_empty_string(
                action
            )
        message = (
            f"{action}." +
            f"Original rows: {original_count}, Resulting rows: {new_count}")
        logger.log(
            "info", message)

    @staticmethod
    def validate_boolean_condition(
        condition: callable,
        data: pd.DataFrame,
        validate: bool = True
    ) -> pd.Series:
        """
        Validate that a condition returns a Boolean Series.

        Args:
            condition (Callable): A function that takes a DataFrame and
                                returns a Boolean Series.
            data (pd.DataFrame): The input DataFrame.
            validate (bool): Whether to validate the inputs (default is True).

        Returns:
            pd.Series: The Boolean Series resulting from the condition.

        Raises:
            ValueError: If the condition does not return a Boolean Series.

        Example:
            ```python
            import pandas as pd
            from my_module import (
                PandasValidationUtils
            )

            # Example DataFrame
            df = pd.DataFrame({
                'Age': [25, 30, 15, 45],
                'Name': ['John', 'Jane', 'Jake', 'Emily']
            })

            # Define a valid condition
            def is_adult(data):
                return data['Age'] > 18

            # Validate the condition
            boolean_mask = PandasValidationUtils.validate_boolean_condition(
                condition=is_adult,
                data=df
            )
            print(boolean_mask)
            # Output:
            # 0     True
            # 1     True
            # 2    False
            # 3     True
            # Name: Age, dtype: bool

            # Define an invalid condition (does not return Boolean Series)
            def invalid_condition(data):
                return data['Age'] + 5

            try:
                PandasValidationUtils.validate_boolean_condition(
                    condition=invalid_condition,
                    data=df
                )
            except ValueError as e:
                print(e)
            # Output:
            # Condition did not return a Boolean Series.
            ```
        """
        logger = get_logger()
        if validate:
            PandasValidationUtils.validate_is_callable(
                condition,
                'condition'
            )
            PandasValidationUtils.validate_is_dataframe(
                data,
                'data'
            )
        mask = condition(data)
        if not isinstance(mask, pd.Series) or mask.dtype != bool:
            error_message = (
                "Condition did not return a Boolean Series."
            )
            logger.log(
                "error",
                error_message)
            raise ValueError(error_message)
        return mask

    @staticmethod
    def validate_is_boolean(
        input_value: Any,
        input_name: str = "boolean_value",
        validate: bool = True
    ) -> None:
        """
        Validate that an input is a boolean value.

        Args:
            input_value (Any): The input to validate as a boolean.
            input_name (str, optional): The name of the input for
                logging purposes. Defaults to "boolean_value".
            validate (bool): Whether to validate the inputs (default is True).

        Raises:
            ValueError: If the input is not a boolean value.

        Example:
            ```python
            from my_module import (
                PandasValidationUtils
            )

            # Example 1: Valid boolean input
            PandasValidationUtils.validate_is_boolean(
                input_value=True,
                input_name="IsValid"
            )  # No exception raised

            # Example 2: Invalid boolean input
            try:
                PandasValidationUtils.validate_is_boolean(
                    input_value="NotABoolean",
                    input_name="IsValid"
                )
            except ValueError as e:
                print(e)
            # Output:
            # IsValid must be a boolean value. Got str.
            ```
        """
        logger = get_logger()
        if validate:
            PandasValidationUtils.validate_is_non_empty_string(
                input_name
            )
        if not isinstance(input_value, bool):
            error_message = (
                f"{input_name} " +
                f"must be a boolean value. Got {type(input_value).__name__}."
            )
            logger.log(
                "error",
                error_message)
            raise ValueError(error_message)

    @staticmethod
    def validate_float(
        input_value,
        input_name="float_value",
        validate: bool = True
    ) -> None:
        """
        Validate that an input is a float value.

        Args:
            input_value (Any): The input to validate as a float.
            input_name (str, optional): The name of the input for
                logging purposes. Defaults to "float_value".
            validate (bool): Whether to validate the inputs (default is True).

        Raises:
            ValueError: If the input is not a float value.

        Example:
            ```python
            from my_module import (
                PandasValidationUtils
            )

            # Example 1: Valid float input
            PandasValidationUtils.validate_float(
                input_value=3.14,
                input_name="PiValue"
            )  # No exception raised

            # Example 2: Invalid float input (integer)
            try:
                PandasValidationUtils.validate_float(
                    input_value=5,
                    input_name="IntegerValue"
                )
            except ValueError as e:
                print(e)
            # Output:
            # IntegerValue must be a float value. Got int.

            # Example 3: Invalid float input (string)
            try:
                PandasValidationUtils.validate_float(
                    input_value="NotAFloat",
                    input_name="StringValue"
                )
            except ValueError as e:
                print(e)
            # Output:
            # StringValue must be a float value. Got str.
            ```
        """
        logger = get_logger()
        if validate:
            PandasValidationUtils.validate_is_non_empty_string(
                input_name
            )
        if not isinstance(input_value, float):
            error_message = (
                f"{input_name} " +
                f"must be a float value. Got {type(input_value).__name__}."
            )
            logger.log(
                "error",
                error_message)
            raise ValueError(error_message)

    @staticmethod
    def validate_is_integer(
        input_value,
        input_name="integer_value",
        validate: bool = True
    ) -> None:
        """
        Validate that an input is an integer value.

        Args:
            input_value (Any): The input to validate as an integer.
            input_name (str, optional): The name of the input for
                logging purposes. Defaults to "integer_value".
            validate (bool): Whether to validate the inputs (default is True).

        Raises:
            ValueError: If the input is not an integer value.

        Example:
            ```python
            from my_module import (
                PandasValidationUtils
            )

            # Example 1: Valid integer input
            PandasValidationUtils.validate_is_integer(
                input_value=42,
                input_name="AnswerToEverything"
            )  # No exception raised, logs success

            # Example 2: Invalid integer input (float)
            try:
                PandasValidationUtils.validate_is_integer(
                    input_value=3.14,
                    input_name="PiValue"
                )
            except ValueError as e:
                print(e)
            # Output:
            # PiValue must be an integer value. Got float.

            # Example 3: Invalid integer input (string)
            try:
                PandasValidationUtils.validate_is_integer(
                    input_value="NotAnInteger",
                    input_name="StringValue"
                )
            except ValueError as e:
                print(e)
            # Output:
            # StringValue must be an integer value. Got str.
            ```
        """
        logger = get_logger()
        if validate:
            PandasValidationUtils.validate_is_non_empty_string(
                input_name
            )
        if not isinstance(input_value, int):
            error_message = (
                f"{input_name} " +
                f"must be an integer value. Got {type(input_value).__name__}."
            )
            logger.log(
                "error",
                error_message)
            raise ValueError(error_message)
        logger.log(
            "info",
            f"{input_name} validation successful. Value: {input_value}")

    @staticmethod
    def log_init_arguments(
        instance,
        exclude_private=True
    ):
        """
        Log the arguments passed to the __init__ method dynamically.

        Args:
            instance (object): The class instance.
            exclude_private (bool): Whether to exclude private attributes
                (e.g., starting with '_'). Defaults to True.

        Logs:
            A message listing the arguments and their values.

        Example:
            ```python
            import logging
            from my_module import (
                PandasValidationUtils
            )

            # Set up a logger for demonstration
            logging.basicConfig(level=logging.INFO)

            class ExampleClass:
                def __init__(self, param1, param2, _private_param):
                    PandasValidationUtils.log_init_arguments(
                        instance=self,
                        exclude_private=True
                    )
                    self.param1 = param1
                    self.param2 = param2
                    self._private_param = _private_param

            # Instantiate the class
            obj = ExampleClass(
                param1="value1", param2=42, _private_param="hidden")
            # Logs:
            # INFO:root:ExampleClass initialized with arguments: {
                # 'param1': 'value1', 'param2': 42}
            ```
        """
        # Retrieve the caller's frame and extract arguments
        frame = inspect.currentframe().f_back
        method_name = frame.f_code.co_name
        logger = get_logger()
        # Ensure it's used inside __init__
        if method_name != "__init__":
            logger.log(
                "warning",
                "log_init_arguments " +
                "should ideally be used within __init__ methods.")

        # Get arguments from the caller's local variables
        args = {k: v for k, v in frame.f_locals.items() if k != "self"}
        if exclude_private:
            args = {k: v for k, v in args.items() if not k.startswith("_")}

        # Log the extracted arguments
        logger.log(
            "info",
            f"{instance.__class__.__name__} " +
            f"initialized with arguments: {args}")

    @staticmethod
    def validate_positive_integers(
        column: pd.Series,
        column_name: str,
        validate: bool = True
    ) -> None:
        """
        Validate that a column contains only positive integers.

        Args:
            column (pd.Series): The column to validate.
            column_name (str): The name of the column for error messages.
            validate (bool): Whether to validate the inputs (default is True).

        Raises:
            ValueError: If the column contains non-integer or negative values.

        Example:
            ```python
            import pandas as pd
            from my_module import (
                PandasValidationUtils
            )

            # Example DataFrame
            df = pd.DataFrame({
                'PositiveInts': [1, 2, 3],
                'MixedValues': [1, -2, 3],
                'NonIntegers': [1.5, 2.0, 3.0]
            })

            # Validate a column with positive integers
            PandasValidationUtils.validate_positive_integers(
                column=df['PositiveInts'],
                column_name='PositiveInts'
            )  # No exception raised

            # Validate a column with negative values
            try:
                PandasValidationUtils.validate_positive_integers(
                    column=df['MixedValues'],
                    column_name='MixedValues'
                )
            except ValueError as e:
                print(e)
            # Output:
            # The 'MixedValues' column contains negative values.

            # Validate a column with non-integer values
            try:
                PandasValidationUtils.validate_positive_integers(
                    column=df['NonIntegers'],
                    column_name='NonIntegers'
                )
            except ValueError as e:
                print(e)
            # Output:
            # The 'NonIntegers' column must contain integer values.
            ```
        """
        logger = get_logger()
        if validate:
            PandasValidationUtils.validate_is_non_empty_series(
                column,
                'column'
            )
            PandasValidationUtils.validate_is_non_empty_string(
                column_name
            )
        if not pd.api.types.is_integer_dtype(column):
            error_message = (
                f"The '{column_name}' column must contain integer values.")
            logger.log(
                "error",
                error_message)
            raise ValueError(error_message)
        if (column < 0).any():
            error_message = (
                f"The '{column_name}' column contains negative values."
            )
            logger.log(
                "error",
                error_message)
            raise ValueError(error_message)

    @staticmethod
    def validate_is_non_empty_dict(
        input_dict: dict,
    ) -> None:
        """
        Validate that an input is a non-empty dictionary.

        Args:
            input_dict (dict): The dictionary to validate.

        Raises:
            ValueError: If the input is not a non-empty dictionary.

        Example:
            ```python
            from my_module import (
                PandasValidationUtils
            )

            # Example 1: Valid dictionary
            valid_dict = {'key1': 'value1', 'key2': 'value2'}
            PandasValidationUtils.validate_is_non_empty_dict(valid_dict)

            # Example 2: Empty dictionary
            try:
                empty_dict = {}
                PandasValidationUtils.validate_is_non_empty_dict(empty_dict)
            except ValueError as e:
                print(e)
            # Output:
            # input_dict must be a dictionary.

            # Example 3: Invalid input (not a dictionary)
            try:
                invalid_input = [1, 2, 3]
                PandasValidationUtils.validate_is_non_empty_dict(invalid_input)
            except ValueError as e:
                print(e)
            # Output:
            # input_dict must be a dictionary.
            ```
        """
        logger = get_logger()
        # Get the variable name of the input_dict using the inspect module
        caller_frame = inspect.currentframe().f_back
        input_name = next(
            (k for k, v in caller_frame.f_locals.items() if v is input_dict),
            "input_dict")

        if not isinstance(input_dict, dict) or not input_dict:
            error_message = f"{input_name} must be a dictionary."
            logger.log(
                "error",
                error_message)
            raise ValueError(error_message)

    @staticmethod
    def validate_is_non_empty_list(
        input_list: list
    ) -> None:
        """
        Validate that an input is a non-empty list.

        Args:
            input_list (list): The list to validate.

        Raises:
            ValueError: If the input is not a non-empty list.

        Example:
            ```python
            from my_module import (
                PandasValidationUtils
            )

            # Example 1: Valid non-empty list
            valid_list = [1, 2, 3]
            PandasValidationUtils.validate_is_non_empty_list(valid_list)

            # Example 2: Empty list
            try:
                empty_list = []
                PandasValidationUtils.validate_is_non_empty_list(empty_list)
            except ValueError as e:
                print(e)
            # Output:
            # input_list must be a list.

            # Example 3: Invalid input (not a list)
            try:
                invalid_input = {'key': 'value'}
                PandasValidationUtils.validate_is_non_empty_list(invalid_input)
            except ValueError as e:
                print(e)
            # Output:
            # input_list must be a list.
            ```
        """
        logger = get_logger()
        # Get the variable name of the input_list using the inspect module
        caller_frame = inspect.currentframe().f_back
        input_name = next(
            (k for k, v in caller_frame.f_locals.items() if v is input_list),
            "input_list")

        if not isinstance(input_list, list) or not input_list:
            error_message = f"{input_name} must be a list."
            logger.log(
                "error",
                error_message)
            raise ValueError(error_message)

    @staticmethod
    def validate_is_non_empty_string(
        input_string: str
    ) -> None:
        """
        Validate that an input is a non-empty string.

        Args:
            input_string (str): The string to validate.

        Raises:
            ValueError: If the input is not a non-empty string.

        Example:
            ```python
            from my_module import (
                PandasValidationUtils
            )

            # Example 1: Valid non-empty string
            valid_string = "Hello, World!"
            PandasValidationUtils.validate_is_non_empty_string(valid_string)
            # Example 2: Empty string
            try:
                empty_string = ""
                PandasValidationUtils.validate_is_non_empty_string(empty_string)
            except ValueError as e:
                print(e)
            # Output:
            # input_string must be a string.

            # Example 3: Invalid input (not a string)
            try:
                invalid_input = 12345
                PandasValidationUtils.validate_is_non_empty_string(invalid_input)
            except ValueError as e:
                print(e)
            # Output:
            # input_string must be a string.
            ```
    """
        logger = get_logger()
        # Get the variable name of the input_string using the inspect module
        caller_frame = inspect.currentframe().f_back
        input_name = next(
            (k for k, v in caller_frame.f_locals.items() if v is input_string),
            "input_string")

        if not isinstance(input_string, str) or not input_string:
            error_message = f"{input_name} must be a string."
            logger.log(
                "error",
                error_message)
            raise ValueError(error_message)

    @staticmethod
    def validate_is_non_empty_series(
        input_series: pd.Series,
        input_name: str
    ) -> None:
        """
        Validate that an input is a non-empty Pandas Series.

        Args:
            input_series (pd.Series): The series to validate.
            input_name (str): The name of the input for logging purposes.

        Raises:
            ValueError: If the input is not a non-empty Pandas Series.

        Example:
            ```python
            import pandas as pd
            from my_module import (
                PandasValidationUtils
            )

            # Example 1: Valid non-empty Series
            valid_series = pd.Series([1, 2, 3])
            PandasValidationUtils.validate_is_non_empty_series(
                input_series=valid_series,
                input_name="ValidSeries"
            )  # No exception raised

            # Example 2: Empty Series
            try:
                empty_series = pd.Series([], dtype=float)
                PandasValidationUtils.validate_is_non_empty_series(
                    input_series=empty_series,
                    input_name="EmptySeries"
                )
            except ValueError as e:
                print(e)
            # Output:
            # EmptySeries must be a Pandas Series.

            # Example 3: Invalid input (not a Series)
            try:
                invalid_input = [1, 2, 3]
                PandasValidationUtils.validate_is_non_empty_series(
                    input_series=invalid_input,
                    input_name="InvalidInput"
                )
            except ValueError as e:
                print(e)
            # Output:
            # InvalidInput must be a Pandas Series.
            ```
        """
        logger = get_logger()
        if not isinstance(input_series, pd.Series) or input_series.empty:
            error_message = f"{input_name} must be a Pandas Series."
            logger.log(
                "error",
                error_message)
            raise ValueError(error_message)

    @staticmethod
    def validate_is_callable(
        input_function,
        input_name="condition",
        validate: bool = True
    ) -> None:
        """
        Validate that an input is a callable function.

        Args:
            input_function (Any): The input to validate as a callable.
            input_name (str, optional): The name of the input for
                logging purposes. Defaults to "condition".
            validate (bool): Whether to validate the inputs (default is True).

        Raises:
            ValueError: If the input is not a callable function.

        Example:
            ```python
            from my_module import (
                PandasValidationUtils
            )

            # Example 1: Valid callable function
            def example_function(data):
                return data

            PandasValidationUtils.validate_is_callable(
                input_function=example_function,
                input_name="ExampleFunction"
            )  # No exception raised

            # Example 2: Invalid input (not callable)
            try:
                not_callable = "This is not a function"
                PandasValidationUtils.validate_is_callable(
                    input_function=not_callable,
                    input_name="NotCallable"
                )
            except ValueError as e:
                print(e)
            # Output:
            # NotCallable must be a callable function.
            ```
        """
        logger = get_logger()
        if validate:
            PandasValidationUtils.validate_is_non_empty_string(
                input_name
            )
        if not callable(input_function):
            error_message = f"{input_name} must be a callable function."
            logger.log(
                "error",
                error_message)
            raise ValueError(error_message)

    @staticmethod
    def validate_inheritance(
        subclass,
        parent_class,
        input_name="class",
    ) -> None:
        """
        Validate that a class or instance inherits from a specified
        parent class.

        Args:
            subclass (type or object): The class or instance to validate.
            parent_class (type): The parent class to check inheritance against.
            input_name (str, optional): The name of the class input for
            logging purposes. Defaults to "class".

        Raises:
            TypeError: If the subclass does not inherit from the parent_class.

        Example:
            ```python
            from my_module import (
                PandasValidationUtils
            )

            # Define parent and child classes
            class Parent:
                pass

            class Child(Parent):
                pass

            # Example 1: Valid inheritance (class)
            PandasValidationUtils.validate_inheritance(
                subclass=Child,
                parent_class=Parent,
                input_name="ChildClass"
            )  # Logs success, no exception raised

            # Example 2: Valid inheritance (instance)
            child_instance = Child()
            PandasValidationUtils.validate_inheritance(
                subclass=child_instance,
                parent_class=Parent,
                input_name="ChildInstance"
            )  # Logs success, no exception raised

            # Example 3: Invalid inheritance
            class Unrelated:
                pass

            try:
                PandasValidationUtils.validate_inheritance(
                    subclass=Unrelated,
                    parent_class=Parent,
                    input_name="UnrelatedClass"
                )
            except TypeError as e:
                print(e)
            # Output:
            # Invalid class: Unrelated does not inherit from Parent.
            ```
        """
        logger = get_logger()
        # Extract the class if an instance is passed
        if not isinstance(subclass, type):
            logger.log(
                "info",
                f"{input_name} " +
                "is an instance. Extracting its class for validation.")
            subclass = type(subclass)

        if not issubclass(subclass, parent_class):
            error_message = (
                f"Invalid {input_name}: {subclass.__name__} " +
                f"does not inherit from {parent_class.__name__}."
            )
            logger.log(
                "error",
                error_message)
            raise TypeError(error_message)

        logger.log(
            "info",
            f"{input_name} validation successful. " +
            f"{subclass.__name__} inherits from {parent_class.__name__}.")

    @staticmethod
    def validate_instance(
        input_value,
        expected_class,
        input_name="input",
        validate: bool = True
    ):
        """
        Validate that the given input is an instance of the expected class.

        Args:
            input_value: The input value to validate.
            expected_class (type): The class to validate against.
            input_name (str, optional): Name of the input for logging purposes.
                                        Defaults to "input".
            validate (bool): Whether to validate the inputs (default is True).

        Raises:
            TypeError: If the input is not an instance of the expected class.

        Example:
            ```python
            from my_module import (
                PandasValidationUtils
            )

            # Define an example class
            class ExampleClass:
                pass

            # Example 1: Valid instance
            instance = ExampleClass()
            PandasValidationUtils.validate_instance(
                input_value=instance,
                expected_class=ExampleClass,
                input_name="ExampleInstance"
            )  # Logs success, no exception raised

            # Example 2: Invalid instance
            try:
                PandasValidationUtils.validate_instance(
                    input_value=42,
                    expected_class=ExampleClass,
                    input_name="NotAnInstance"
                )
            except TypeError as e:
                print(e)
            # Output:
            # Invalid input: Expected instance of ExampleClass, but got int.
            ```
        """
        logger = get_logger()
        if validate:
            PandasValidationUtils.validate_is_non_empty_string(
                input_name
            )
        if not isinstance(input_value, expected_class):
            error_message = (
                f"Invalid {input_name}: " +
                f"Expected instance of {expected_class.__name__}, " +
                f"but got {type(input_value).__name__}."
            )
            logger.log(
                "error",
                error_message)
            raise TypeError(error_message)
        logger.log(
            "info",
            f"{input_name} validation successful: "
            f"{input_value} is an instance of {expected_class.__name__}.")

    @staticmethod
    def validate_data_type(
        data_type: str,
        valid_data_types: Enum,
        validate: bool = True
    ):
        """
        Validate that the provided data type is valid.

        Args:
            data_type (str): The data type to validate (e.g., "CSV", "JSON").
            valid_data_types (Enum): Enum containing valid data types
                                    (e.g., DataType).
            validate (bool): Whether to validate the inputs (default is True).

        Raises:
            ValueError: If the data type is invalid or not supported.

        Example:
            ```python
            from enum import Enum
            from my_module import (
                PandasValidationUtils
            )

            # Define a valid data types Enum
            class DataType(Enum):
                CSV = "csv"
                JSON = "json"
                PARQUET = "parquet"

            # Example 1: Valid data type
            PandasValidationUtils.validate_data_type(
                data_type="CSV",
                valid_data_types=DataType
            )  # Logs success, no exception raised

            # Example 2: Invalid data type
            try:
                PandasValidationUtils.validate_data_type(
                    data_type="XML",
                    valid_data_types=DataType
                )
            except ValueError as e:
                print(e)
            # Output:
            # Invalid data type 'XML'. Supported types:
            #   ['CSV', 'JSON', 'PARQUET']
            ```
        """
        logger = get_logger()
        if validate:
            PandasValidationUtils.validate_is_non_empty_string(
                data_type
            )
            PandasValidationUtils.validate_instance(
                valid_data_types,
                Enum,
                'valid_data_types'
            )
        if not isinstance(
            data_type, str
        ) or data_type.upper() not in valid_data_types.__members__:
            error_message = (
                f"Invalid data type '{data_type}'. " +
                "Supported types: " +
                f"{list(valid_data_types.__members__.keys())}")
            logger.log(
                "error",
                error_message)
            raise ValueError(error_message)
        logger.log(
            "info",
            f"Valid data type: {data_type}")

    @staticmethod
    def validate_dataset_in_workflow(
        dataset_name: str,
        datasets: dict,
        validate: bool = True
    ):
        """
        Validate that a dataset exists in the workflow.

        Args:
            dataset_name (str): The name of the dataset to validate.
            datasets (dict): The dictionary of loaded datasets.
            validate (bool): Whether to validate the inputs (default is True).

        Raises:
            ValueError: If the dataset does not exist in the workflow.

        Example:
            ```python
            from my_module import (
                PandasValidationUtils
            )

            # Example dictionary of datasets
            loaded_datasets = {
                "sales_data": "path/to/sales.csv",
                "inventory_data": "path/to/inventory.csv"
            }

            # Example 1: Validate an existing dataset
            PandasValidationUtils.validate_dataset_in_workflow(
                dataset_name="sales_data",
                datasets=loaded_datasets
            )  # No exception raised

            # Example 2: Validate a non-existing dataset
            try:
                PandasValidationUtils.validate_dataset_in_workflow(
                    dataset_name="customer_data",
                    datasets=loaded_datasets
                )
            except ValueError as e:
                print(e)
            # Output:
            # Dataset 'customer_data' not found in loaded datasets.
            ```
        """
        logger = get_logger()
        if validate:
            PandasValidationUtils.validate_is_non_empty_string(
                dataset_name
            )
            PandasValidationUtils.validate_is_non_empty_dict(
                datasets
            )
        if dataset_name not in datasets:
            error_message = (
                f"Dataset '{dataset_name}' not found in loaded datasets.")
            logger.log(
                "error",
                error_message)
            raise ValueError(
                error_message)
        else:
            return None

    @staticmethod
    def log_workflow_action(
        action: str,
        dataset_name: str,
        success: bool,
        error: Exception = None
    ):
        """
        Log success or failure of a workflow action.

        Args:
            action (str): Action performed (e.g., 'validate', 'transform').
            dataset_name (str): The name of the dataset the action was
                applied to.
            success (bool): Whether the action succeeded.
            error (Exception, optional): Exception raised if the action failed.

        Example:
            ```python
            from my_module import (
                PandasValidationUtils
            )

            # Example 1: Log a successful action
            PandasValidationUtils.log_workflow_action(
                action="validate",
                dataset_name="sales_data",
                success=True
            )
            # Logs: Successfully completed 'validate' for dataset 'sales_data'.

            # Example 2: Log a failed action
            try:
                # Simulate an error
                raise ValueError("Invalid column format")
            except Exception as e:
                PandasValidationUtils.log_workflow_action(
                    action="transform",
                    dataset_name="inventory_data",
                    success=False,
                    error=e
                )
            # Logs: Failed to 'transform' dataset 'inventory_data':
            # Invalid column format
            ```
        """
        logger = get_logger()
        if success:
            logger.log(
                "info",
                f"Successfully completed "
                f"'{action}' for dataset '{dataset_name}'.")
        else:
            logger.log(
                "error",
                f"Failed to '{action}' dataset '{dataset_name}': {error}")


class SparkValidationUtils:
    @staticmethod
    def validate_is_non_empty_series(
        column: Column,
        validate: bool = True
    ) -> None:
        """
        Validate that the input is a valid, non-empty Spark Column.

        This utility ensures that the provided input is a Spark Column and
        performs a basic check for validity.

        Args:
            column (Column): The Spark Column to validate.
            validate (bool): Whether to perform the validation. If False,
                the method skips validation. Defaults to True.

        Raises:
            ValueError: If the input is not a valid Spark Column.

        Examples:
            # Example 1: Validating a non-empty Spark Column
            from pyspark.sql import SparkSession
            from pyspark.sql.functions import col

            spark = SparkSession.builder.appName(
                "ValidationExample").getOrCreate()

            # Sample DataFrame
            df = spark.createDataFrame([
                {"id": 1, "value": "A"},
                {"id": 2, "value": "B"}
            ])

            # Validate a column
            column = col("id")
            SparkValidationUtils.validate_is_non_empty_series(column)

            # Example 2: Invalid input (not a Spark Column)
            invalid_column = "id"
            try:
                SparkValidationUtils.validate_is_non_empty_series(invalid_column)
            except ValueError as e:
                print(f"Validation failed: {e}")
        """
        if validate:
            logger = get_logger()
            # Get the column name or expression dynamically
            column_name = column._jc.toString()

            # Ensure the input is a Spark Column
            if not isinstance(column, Column):
                error_message = (
                    f"Invalid input: {column_name} is not a Spark Column.")
                logger.log(
                    "error",
                    error_message)
                raise ValueError(error_message)

            logger.log(
                "info",
                "Validation successful: " +
                f"{column_name} is a valid Spark Column.")

    @staticmethod
    def validate_is_positive_integer(
        column_name: str,
        data: DataFrame
    ) -> None:
        """
        Validate that a Spark Column contains only positive integers.

        This utility checks whether the specified column in a Spark DataFrame
        contains only positive integers. If any non-integer or negative values
        are found, an exception is raised.

        Args:
            column (Column): The Spark Column to validate.
            column_name (str): The name of the column being validated.
            data (DataFrame): The Spark DataFrame containing the column.

        Raises:
            ValueError: If the column contains non-integer or negative values.

        Examples:
            # Example 1: Validating a column with positive integers
            from pyspark.sql import SparkSession
            from pyspark.sql.functions import col

            spark = SparkSession.builder.appName(
                "ValidationExample").getOrCreate()

            # Sample DataFrame
            df = spark.createDataFrame([
                {"id": 1, "value": 10},
                {"id": 2, "value": 20}
            ])

            # Validate the "value" column
            SparkValidationUtils.validate_positive_integers(
                col("value"), "value", df)

            # Example 2: Column with invalid values (negative integers)
            invalid_df = spark.createDataFrame([
                {"id": 1, "value": -10},
                {"id": 2, "value": 20}
            ])

            try:
                SparkValidationUtils.validate_positive_integers(
                    col("value"), "value", invalid_df)
            except ValueError as e:
                print(f"Validation failed: {e}")

            # Example 3: Column with non-integer values
            non_integer_df = spark.createDataFrame([
                {"id": 1, "value": "ten"},
                {"id": 2, "value": 20}
            ])

            try:
                SparkValidationUtils.validate_positive_integers(
                    col("value"), "value", non_integer_df)
            except ValueError as e:
                print(f"Validation failed: {e}")
        """

        logger = get_logger()

        # Check for non-integer values
        non_integer_count = data.filter(
            ~col(column_name).cast("int").isNotNull()).count()
        if non_integer_count > 0:
            error_message = (
                f"The '{column_name}' column must contain only integers."
            )
            logger.log(
                "error",
                error_message)
            raise ValueError(error_message)

        # Check for negative values
        negative_count = data.filter(col(column_name) < 0).count()
        if negative_count > 0:
            error_message = (
                f"The '{column_name}' column must not contain negative values."
            )
            logger.log(
                "error",
                error_message)
            raise ValueError(
                error_message)

        logger.log(
            "info",
            "Validation successful: " +
            "'{column_name}' contains only positive integers.")

    @staticmethod
    def validate_is_dataframe(
        data: Any,
        name: str = "Input",
        validate: bool = True
    ) -> None:
        """
        Validate that the input is a Spark DataFrame.

        This utility ensures that the provided input is a Spark DataFrame. If
        the input is not a DataFrame, an exception is raised with a detailed
        error message.

        Args:
            data (Any): The input to validate.
            name (str, optional): A descriptive name for the input, used in
                error messages. Defaults to "Input".
            validate (bool, optional): Whether to perform the validation.
                If False, the method skips validation. Defaults to True.

        Raises:
            ValueError: If the input is not a Spark DataFrame.

        Examples:
            # Example 1: Validating a Spark DataFrame
            from pyspark.sql import SparkSession

            spark = SparkSession.builder.appName(
                "ValidationExample").getOrCreate()

            # Create a valid DataFrame
            df = spark.createDataFrame([
                {"id": 1, "value": "A"},
                {"id": 2, "value": "B"}
            ])

            # Validate the DataFrame
            SparkValidationUtils.validate_is_dataframe(df, name="MyDataFrame")

            # Example 2: Invalid input (not a DataFrame)
            not_a_dataframe = [
                {"id": 1, "value": "A"}, {"id": 2, "value": "B"}]

            try:
                SparkValidationUtils.validate_is_dataframe(
                    not_a_dataframe, name="MyList")
            except ValueError as e:
                print(f"Validation failed: {e}")
        """
        logger = get_logger()
        if validate:
            # Reuse PandasValidationUtils to validate the name
            PandasValidationUtils.validate_is_non_empty_string(name)

        # Validate the input type
        if not isinstance(data, DataFrame):
            error_message = (
                f"The input '{name}' is not a Spark DataFrame."
            )
            logger.log(
                "error",
                error_message)
            raise ValueError(error_message)

        logger.log(
            "info",
            f"{name} validation successful: Input is a Spark DataFrame.")

    @staticmethod
    def validate_is_column(
        column: Any,
        name: str = "Input",
        validate: bool = True
    ) -> None:
        """
        Validate that the input is a Spark Column.

        This utility ensures that the provided input is a valid Spark Column.
        If the input is not a Column, an exception is raised with a detailed
        error message.

        Args:
            column (Any): The input to validate.
            name (str, optional): A descriptive name for the input, used in
                error messages. Defaults to "Input".
            validate (bool, optional): Whether to perform the validation.
                If False, the method skips validation. Defaults to True.

        Raises:
            ValueError: If the input is not a Spark Column.

        Examples:
            # Example 1: Validating a Spark Column
            from pyspark.sql import SparkSession
            from pyspark.sql.functions import col

            spark = SparkSession.builder.appName(
                "ValidationExample").getOrCreate()

            # Create a sample DataFrame
            df = spark.createDataFrame([
                {"id": 1, "value": "A"},
                {"id": 2, "value": "B"}
            ])

            # Validate a valid Spark Column
            column = col("id")
            SparkValidationUtils.validate_is_column(column, name="IDColumn")

            # Example 2: Invalid input (not a Spark Column)
            not_a_column = "id"

            try:
                SparkValidationUtils.validate_is_column(
                    not_a_column, name="InvalidColumn")
            except ValueError as e:
                print(f"Validation failed: {e}")
        """
        logger = get_logger()
        if validate:
            PandasValidationUtils.validate_is_non_empty_string(name)

        if not isinstance(column, Column):
            error_message = (
                f"The input '{name}' is not a Spark Column."
            )
            logger.log(
                "error",
                error_message)
            raise ValueError(error_message)

        logger.log(
            "info",
            f"{name} validation successful: Input is a Spark Column.")

    @staticmethod
    def validate_is_boolean_column(
        column: Column,
        data: DataFrame,
        name: str = "Input"
    ) -> None:
        """
        Validate that the given Spark Column is a Boolean column.

        This utility ensures that the specified column exists in the DataFrame
        and is of Boolean type. If the column is not Boolean or does not exist,
        an exception is raised with a detailed error message.

        Args:
            column (Column): The Spark Column to validate.
            data (DataFrame): The parent DataFrame containing the column.
            name (str, optional): A descriptive name for the column, used in
                error messages. Defaults to "Input".

        Raises:
            ValueError: If the column is not Boolean or does not exist
                in the DataFrame.

        Examples:
            # Example 1: Validating a Boolean column
            from pyspark.sql import SparkSession
            from pyspark.sql.types import StructType, StructField, BooleanType
            from pyspark.sql.functions import col

            spark = SparkSession.builder.appName(
                "ValidationExample").getOrCreate()

            # Create a sample DataFrame with a Boolean column
            schema = StructType([
                StructField("id", IntegerType(), True),
                StructField("is_active", BooleanType(), True)
            ])
            df = spark.createDataFrame([(1, True), (2, False)], schema=schema)

            # Validate the "is_active" column
            SparkValidationUtils.validate_is_boolean_column(
                col("is_active"), df, name="IsActiveColumn")

            # Example 2: Invalid column (not Boolean)
            try:
                SparkValidationUtils.validate_is_boolean_column(
                    col("id"), df, name="IDColumn")
            except ValueError as e:
                print(f"Validation failed: {e}")

            # Example 3: Non-existent column
            try:
                SparkValidationUtils.validate_is_boolean_column(
                    col("non_existent"), df, name="NonExistentColumn")
            except ValueError as e:
                print(f"Validation failed: {e}")
        """
        logger = get_logger()

        # Ensure the column exists in the DataFrame and is of type Boolean
        if not any(
            field.name == column._jc.toString()
                and field.dataType.simpleString() == "boolean"
                for field in data.schema.fields
        ):
            error_message = (
                f"{name} must be a Boolean Spark Column."
            )
            logger.log(
                "error",
                error_message)
            raise ValueError(error_message)

        logger.log(
            "info",
            f"{name} validation successful: Input is a Boolean Spark Column.")

    @staticmethod
    def validate_boolean_condition(
        condition: callable,
        data: DataFrame,
        validate: bool = True
    ) -> Column:
        """
        Validate that a condition returns a Boolean Spark Column.

        This utility ensures that a user-defined condition, when applied to
        a Spark DataFrame, results in a Boolean Spark Column. It validates
        both the condition's return type and that the resulting column
        is valid.

        Args:
            condition (callable): A function that takes a Spark DataFrame
            as input and returns a Boolean Spark Column.
            data (DataFrame): The Spark DataFrame to which the condition will
                be applied.
            validate (bool): Whether to perform the validation.
                Defaults to True.

        Returns:
            Column: The Boolean Spark Column resulting from the condition.

        Raises:
            ValueError: If the condition does not return a Boolean
                Spark Column.

        Examples:
            # Example 1: Valid condition returning a Boolean column
            from pyspark.sql import SparkSession
            from pyspark.sql.functions import col

            spark = SparkSession.builder.appName(
                "ValidationExample").getOrCreate()

            # Create a sample DataFrame
            df = spark.createDataFrame([
                {"id": 1, "value": 10},
                {"id": 2, "value": 20},
                {"id": 3, "value": 30}
            ])

            # Define a valid condition
            def is_value_greater_than_15(dataframe):
                return col("value") > 15

            # Validate the condition
            result = SparkValidationUtils.validate_boolean_condition(
                is_value_greater_than_15, df)
            print("Condition validated successfully!")

            # Example 2: Invalid condition returning a non-Boolean column
            def invalid_condition(dataframe):
                return col("value") + 5

            try:
                SparkValidationUtils.validate_boolean_condition(
                    invalid_condition, df)
            except ValueError as e:
                print(f"Validation failed: {e}")

            # Example 3: Condition raising an error
            def faulty_condition(dataframe):
                return col("non_existent_column") > 15

            try:
                SparkValidationUtils.validate_boolean_condition(
                    faulty_condition, df)
            except ValueError as e:
                print(f"Validation failed: {e}")
        """
        logger = get_logger()

        if validate:
            # Validate the condition is callable
            PandasValidationUtils.validate_is_callable(condition, "condition")

            # Validate the data is a Spark DataFrame
            SparkValidationUtils.validate_is_dataframe(data, "data")

        # Apply the condition to the DataFrame
        try:
            mask = condition(data)
        except Exception as e:
            error_message = f"Condition raised an error: {e}"
            logger.log(
                "error",
                error_message)
            raise ValueError(error_message)

        # Validate that the result is a Spark Column
        SparkValidationUtils.validate_is_column(mask, name="Condition result")

        # Validate that the Column is Boolean using the new utility
        SparkValidationUtils.validate_is_boolean_column(
            mask, data, name="Condition result")

        logger.log(
            "info",
            "Validation successful: Condition returns a Boolean Spark Column.")
        return mask

    @staticmethod
    def check_missing_columns(
        data: DataFrame,
        required_columns: list,
        validate: bool = True
    ) -> list:
        """
        Check for missing columns in the Spark DataFrame.

        This utility identifies which columns from a list of required columns
        are missing in the given Spark DataFrame.

        Args:
            data (DataFrame): The Spark DataFrame to check.
            required_columns (list): List of required column names to validate.
            validate (bool): Whether to perform input validation.
                Defaults to True.

        Returns:
            list: A list of missing column names. If all columns are present,
                returns an empty list.

        Raises:
            ValueError: If the inputs are invalid (e.g., data is not a
            DataFrame or required_columns is not a non-empty list).

        Examples:
            # Example 1: DataFrame with all required columns present
            from pyspark.sql import SparkSession

            spark = SparkSession.builder.appName(
                "ValidationExample").getOrCreate()

            # Create a sample DataFrame
            df = spark.createDataFrame([
                {"id": 1, "name": "Alice"},
                {"id": 2, "name": "Bob"}
            ])

            # Validate required columns
            required = ["id", "name"]
            missing = SparkValidationUtils.check_missing_columns(df, required)
            print(f"Missing columns: {missing}")  # Output: Missing columns: []

            # Example 2: DataFrame missing required columns
            required_with_extra = ["id", "name", "age"]
            missing = SparkValidationUtils.check_missing_columns(
                df, required_with_extra)
            print(f"Missing columns: {missing}")

            # Example 3: Invalid input (not a DataFrame)
            try:
                SparkValidationUtils.check_missing_columns([{"id": 1}], ["id"])
            except ValueError as e:
                print(f"Validation failed: {e}")

            # Example 4: Invalid input (empty required_columns list)
            try:
                SparkValidationUtils.check_missing_columns(df, [])
            except ValueError as e:
                print(f"Validation failed: {e}")
        """
        if validate:
            # Validate that the input is a DataFrame
            SparkValidationUtils.validate_is_dataframe(data, "data")

            # Validate that required_columns is a non-empty list
            PandasValidationUtils.validate_is_non_empty_list(required_columns)

        # Find and return missing columns
        missing_columns = list(set(required_columns) - set(data.columns))
        return missing_columns

    @staticmethod
    def validate_columns_exist(
        data: DataFrame,
        columns: list,
        validate: bool = True
    ) -> None:
        """
        Validate that the specified columns exist in the Spark DataFrame.

        This utility ensures that all the specified column names are present
        in the given Spark DataFrame. If any column is missing, an exception
        is raised with details about the missing columns.

        Args:
            data (DataFrame): The Spark DataFrame to validate.
            columns (list): List of column names to check for existence.
            validate (bool): Whether to perform input validation.
                Defaults to True.

        Raises:
            KeyError: If any of the specified columns are missing from
            the DataFrame.

        Examples:
            # Example 1: DataFrame with all required columns present
            from pyspark.sql import SparkSession

            spark = SparkSession.builder.appName(
                "ValidationExample").getOrCreate()

            # Create a sample DataFrame
            df = spark.createDataFrame([
                {"id": 1, "name": "Alice"},
                {"id": 2, "name": "Bob"}
            ])

            # Validate that all required columns exist
            required_columns = ["id", "name"]
            SparkValidationUtils.validate_columns_exist(
                df, required_columns)
            print("Validation passed!")

            # Example 2: DataFrame missing required columns
            missing_columns = ["id", "name", "age"]
            try:
                SparkValidationUtils.validate_columns_exist(
                    df, missing_columns)
            except KeyError as e:
                print(f"Validation failed: {e}")

            # Example 3: Invalid input (not a DataFrame)
            try:
                SparkValidationUtils.validate_columns_exist(
                    [{"id": 1}], ["id"])
            except ValueError as e:
                print(f"Validation failed: {e}")

            # Example 4: Invalid input (empty columns list)
            try:
                SparkValidationUtils.validate_columns_exist(df, [])
            except ValueError as e:
                print(f"Validation failed: {e}")
        """
        logger = get_logger()

        if validate:
            # Validate the inputs
            SparkValidationUtils.validate_is_dataframe(data, "data")
            PandasValidationUtils.validate_is_non_empty_list(columns)

        # Use check_missing_columns to identify missing columns
        missing_columns = SparkValidationUtils.check_missing_columns(
            data, columns)
        if missing_columns:
            error_message = (
                "Columns not found in DataFrame: {missing_columns}"
            )
            logger.log(
                "error",
                error_message)
            raise KeyError(error_message)

        logger.log(
            "info",
            "All specified columns exist in the DataFrame.")

    @staticmethod
    def group_and_aggregate(
        data: DataFrame,
        group_by: list,
        agg_config: dict,
        validate: bool = True,
        **kwargs
    ) -> DataFrame:
        """
        Group rows by specified columns and apply aggregation functions.

        This utility groups a Spark DataFrame by the specified columns and
        applies aggregation functions to other columns as defined in the
        `agg_config`. It also supports additional parameters for customizing
        the group-and-aggregate process.

        Args:
            data (DataFrame): The Spark DataFrame to group and aggregate.
            group_by (list): List of column names to group by.
            agg_config (dict): Aggregation configuration mapping column names
            to aggregation functions (e.g., {"col1": "sum", "col2": "avg"}).
            validate (bool): Whether to perform input validation.
                Defaults to True.
            **kwargs: Additional parameters for grouping and aggregation.

        Returns:
            DataFrame: The grouped and aggregated Spark DataFrame.

        Raises:
            ValueError: If inputs are invalid
                (e.g., missing or invalid group/aggregation
                columns, or invalid aggregation functions).

        Examples:
            # Example 1: Basic group-and-aggregate operation
            from pyspark.sql import SparkSession
            from pyspark.sql.functions import col

            spark = SparkSession.builder.appName(
                "ValidationExample").getOrCreate()

            # Create a sample DataFrame
            df = spark.createDataFrame([
                {"category": "A", "value": 10},
                {"category": "A", "value": 20},
                {"category": "B", "value": 30},
                {"category": "B", "value": 40},
            ])

            # Define group and aggregation configurations
            group_by_columns = ["category"]
            aggregation_config = {"value": "sum"}

            # Perform group-and-aggregate
            result = SparkValidationUtils.group_and_aggregate(
                df, group_by_columns, aggregation_config)
            result.show()

            # Output:
            # +--------+-----------+
            # |category|value_sum  |
            # +--------+-----------+
            # |   A    |    30     |
            # |   B    |    70     |
            # +--------+-----------+

            # Example 2: Invalid aggregation function
            invalid_aggregation_config = {"value": "invalid_function"}
            try:
                SparkValidationUtils.group_and_aggregate(
                    df, group_by_columns, invalid_aggregation_config)
            except Exception as e:
                print(f"Validation failed: {e}")

            # Example 3: Empty group_by or agg_config
            try:
                SparkValidationUtils.group_and_aggregate(df, [], {})
            except ValueError as e:
                print(f"Validation failed: {e}")
        """
        logger = get_logger()

        if validate:
            # Validate inputs
            SparkValidationUtils.validate_is_dataframe(data, "data")
            PandasValidationUtils.validate_is_non_empty_list(group_by)
            PandasValidationUtils.validate_is_non_empty_dict(agg_config)

        try:
            # Build aggregation expressions
            agg_expressions = [
                expr(f"{func}({col_name})").alias(f"{col_name}_{func}")
                for col_name, func in agg_config.items()
            ]
            print(agg_expressions)

            # Perform group-by and aggregation
            aggregated_data = data.groupBy(*group_by).agg(*agg_expressions)

            logger.log("info", "Group and aggregation successful.")
            return aggregated_data

        except Exception as e:
            error_message = (
                "Error during group-and-aggregate: {e}"
            )
            logger.log(
                "error",
                error_message)
            raise e(error_message)

    @staticmethod
    def validate_column_contains_delimiter(
        data: DataFrame,
        column: str,
        delimiter: str,
        validate: bool = True,
    ) -> None:
        """
        Ensure all values in the specified column contain the given delimiter.

        This utility checks whether all values in a specified column of a Spark
        DataFrame contain a given delimiter. If any value does not contain the
        delimiter, an exception is raised.

        Args:
            data (DataFrame): The Spark DataFrame to validate.
            column (str): The name of the column to check.
            delimiter (str): The delimiter to validate.
            validate (bool): Whether to perform input validation.
                Defaults to True.

        Raises:
            ValueError: If any value in the column does not contain
                the delimiter.

        Examples:
            # Example 1: Validating a column with all values containing
            # the delimiter
            from pyspark.sql import SparkSession

            spark = SparkSession.builder.appName(
                "ValidationExample").getOrCreate()

            # Create a sample DataFrame
            df = spark.createDataFrame([
                {"id": 1, "address": "123 Main St"},
                {"id": 2, "address": "456 Elm St"}
            ])

            # Validate that all values in the "address" column contain a space
            SparkValidationUtils.validate_column_contains_delimiter(
                df, "address", " ")

            # Example 2: Column with values missing the delimiter
            invalid_df = spark.createDataFrame([
                {"id": 1, "address": "123MainSt"},
                {"id": 2, "address": "456 Elm St"}
            ])

            try:
                SparkValidationUtils.validate_column_contains_delimiter(
                    invalid_df, "address", " ")
            except ValueError as e:
                print(f"Validation failed: {e}")

            # Example 3: Non-existent column
            try:
                SparkValidationUtils.validate_column_contains_delimiter(
                    df, "non_existent", " ")
            except KeyError as e:
                print(f"Validation failed: {e}")
        """
        logger = get_logger()

        if validate:
            # Validate the DataFrame
            SparkValidationUtils.validate_is_dataframe(data, "data")

            # Validate the column and delimiter are non-empty strings
            PandasValidationUtils.validate_is_non_empty_string(column)
            PandasValidationUtils.validate_is_non_empty_string(delimiter)

        # Check for any value in the column that does not contain the delimiter
        missing_delimiter_count = data.filter(
            instr(col(column), delimiter) == 0).count()

        if missing_delimiter_count > 0:
            error_message = (
                "Column '{column}' must contain strings with the delimiter " +
                f"'{delimiter}'."
            )
            logger.log(
                "error",
                error_message)
            raise ValueError(error_message)

        logger.log(
            "info",
            "Validation successful: All values in column " +
            f"'{column}' contain the delimiter '{delimiter}'."
        )

    @staticmethod
    def validate_column_is_list_type(
        data: DataFrame,
        column: str,
        validate: bool = True
    ) -> None:
        """
        Ensure all values in the specified column are lists.

        This utility checks whether all values in a specified column of a Spark
        DataFrame are of type list. If any value is not a list, an exception is
        raised.

        Note:
            PySpark requires columns to have a consistent type. If the column
            contains mixed types (e.g., strings and lists), you must define
            the schema explicitly (e.g., as StringType) when creating the
            DataFrame to avoid schema inference errors.

        Args:
            data (DataFrame): The Spark DataFrame to validate.
            column (str): The name of the column to check.
            validate (bool): Whether to perform input validation.
                Defaults to True.

        Raises:
            ValueError: If any value in the column is not a list.
            KeyError: If the specified column does not exist in the DataFrame.

        Examples:
            # Example 1: Validating a column where all values are lists
            from pyspark.sql import SparkSession

            spark = SparkSession.builder.appName(
                "ValidationExample").getOrCreate()

            # Create a sample DataFrame
            df = spark.createDataFrame([
                {"id": 1, "tags": ["spark", "data"]},
                {"id": 2, "tags": ["python", "ml"]}
            ])

            # Validate the "tags" column
            SparkValidationUtils.validate_column_is_list_type(df, "tags")

            # Example 2: Handling mixed-type columns with an explicit schema
            from pyspark.sql.types import (
                StructType, StructField, IntegerType,StringType)

            # Define schema for mixed types
            schema = StructType([
                StructField("id", IntegerType(), True),
                StructField("tags", StringType(), True)])

            # Create a DataFrame with mixed types
            invalid_df = spark.createDataFrame([
                {"id": 1, "tags": "not_a_list"},       # String
                {"id": 2, "tags": str(["python", "ml"])}
            ], schema=schema)

            # Run the validation
            try:
                SparkValidationUtils.validate_column_is_list_type(
                    invalid_df, "tags")
            except ValueError as e:
                print(f"Validation failed: {e}")
        """
        logger = get_logger()

        if validate:
            # Validate that the input is a DataFrame
            SparkValidationUtils.validate_is_dataframe(data, "data")

            # Validate that the column is a non-empty string
            PandasValidationUtils.validate_is_non_empty_string(column)

        # Define a UDF to check if a value is a list
        is_list_udf = udf(lambda x: isinstance(x, list), BooleanType())

        # Filter rows where the column value is not a list
        non_list_count = data.filter(~is_list_udf(col(column))).count()

        if non_list_count > 0:
            error_message = (
                "Column '{column}' must contain lists."
            )
            logger.log(
                "error",
                error_message)
            raise ValueError(error_message)

        logger.log(
            "info",
            "Validation successful: All values in column " +
            "'{column}' are lists."
        )

    @staticmethod
    def merge_columns(
        data: DataFrame,
        columns: list,
        separator: str = " ",
        validate: bool = True
    ) -> DataFrame:
        """
        Merge multiple columns into a single column, excluding None or
        NaN values.

        This utility concatenates values from multiple columns into a single
        column,separating values using the specified `separator`. If any
        value is None or NaN,it is excluded from the concatenation.
        A new column named "merged_column" is added to the DataFrame.

        Args:
            data (DataFrame): The input Spark DataFrame.
            columns (list): List of column names to merge.
            separator (str, optional): Separator to use between values.
                Defaults toV a single space.
            validate (bool): Whether to perform input validation.
                Defaults to True.

        Returns:
            DataFrame: A new Spark DataFrame with an additional column
                "merged_column".

        Raises:
            KeyError: If any column in `columns` is missing from the DataFrame.
            ValueError: If the inputs are invalid (e.g., empty column list).

        Examples:
            # Example 1: Merging columns with valid input
            from pyspark.sql import SparkSession

            spark = SparkSession.builder.appName(
                "ValidationExample").getOrCreate()

            # Create a sample DataFrame
            df = spark.createDataFrame([
                {"id": 1, "first_name": "John", "last_name": "Doe"},
                {"id": 2, "first_name": "Jane", "last_name": "Smith"}
            ])

            # Merge "first_name" and "last_name" into a single column
            merged_df = SparkValidationUtils.merge_columns(
                df, ["first_name", "last_name"], separator=" ")
            merged_df.show()

            # Output:
            # +---+----------+---------+-------------+
            # | id|first_name|last_name|merged_column|
            # +---+----------+---------+-------------+
            # |  1|      John|      Doe|    John Doe |
            # |  2|      Jane|    Smith|  Jane Smith |
            # +---+----------+---------+-------------+

            # Example 2: Handling missing columns
            try:
                SparkValidationUtils.merge_columns(
                    df, ["first_name", "middle_name", "last_name"])
            except KeyError as e:
                print(f"Validation failed: {e}")

            # Example 3: Empty column list
            try:
                SparkValidationUtils.merge_columns(df, [])
            except ValueError as e:
                print(f"Validation failed: {e}")
        """
        logger = get_logger()

        if validate:
            # Validate inputs
            SparkValidationUtils.validate_is_dataframe(data, "data")
            PandasValidationUtils.validate_is_non_empty_list(columns)
            PandasValidationUtils.validate_is_non_empty_string(separator)

        # Check for missing columns using the reusable method
        missing_columns = SparkValidationUtils.check_missing_columns(
            data, columns)
        if missing_columns:
            error_message = (
                "Missing columns: {missing_columns}"
            )
            logger.log(
                "error",
                error_message)
            raise KeyError(error_message)

        # Merge columns using concat_ws
        try:
            merged_column = concat_ws(separator, *[col(c) for c in columns])
            merged_data = data.withColumn("merged_column", merged_column)
            logger.log("info", "Successfully merged columns.")
            return merged_data
        except Exception as e:
            error_message = (
                "Error during column merge: {e}"
            )
            logger.log(
                "error",
                error_message)
            raise e(error_message)

    @staticmethod
    def split_column(
        data: DataFrame,
        column: str,
        pattern: str,
        regex: bool = False,
        validate: bool = True
    ) -> DataFrame:
        """
        Split a column into multiple columns based on a pattern or regex.

        This utility splits the values of a specified column into multiple
        columns, using a delimiter or a regular expression. The new columns
        are dynamically named as `<column>_part0`, `<column>_part1`,
        etc., based on the split.

        Args:
            data (DataFrame): The input Spark DataFrame.
            column (str): The name of the column to split.
            pattern (str): The delimiter or regex pattern to use for splitting.
            regex (bool, optional): Whether to treat the pattern as a regex.
                Defaults to False.
            validate (bool, optional): Whether to perform input validation.
                Defaults to True.

        Returns:
            DataFrame: A new Spark DataFrame with additional columns created by
            splitting the input column.

        Raises:
            KeyError: If the specified column does not exist in the DataFrame.
            ValueError: If the inputs are invalid (e.g., empty pattern).

        Examples:
            # Example 1: Splitting a column with a simple delimiter
            from pyspark.sql import SparkSession

            spark = SparkSession.builder.appName(
                "ValidationExample").getOrCreate()

            # Create a sample DataFrame
            df = spark.createDataFrame([
                {"id": 1, "full_name": "John Doe"},
                {"id": 2, "full_name": "Jane Smith"}
            ])

            # Split the "full_name" column into "first_name" and "last_name"
            split_df = SparkValidationUtils.split_column(df, "full_name", " ")
            split_df.show()

            # Output:
            # +---+----------+-----------+------------+
            # | id|full_name |full_name_part0|full_name_part1|
            # +---+----------+-----------+------------+
            # |  1| John Doe |      John  |     Doe   |
            # |  2|Jane Smith|      Jane  |    Smith  |
            # +---+----------+-----------+------------+

            # Example 2: Splitting a column with a regex pattern
            regex_df = spark.createDataFrame([
                {"id": 1, "data": "key1=value1,key2=value2"},
                {"id": 2, "data": "keyA=valueA,keyB=valueB"}
            ])
            split_regex_df = SparkValidationUtils.split_column(
                regex_df, "data", ",")
            split_regex_df.show()

            # Example 3: Handling non-existent column
            try:
                SparkValidationUtils.split_column(df, "non_existent", " ")
            except KeyError as e:
                print(f"Validation failed: {e}")

            # Example 4: Invalid pattern (empty string)
            try:
                SparkValidationUtils.split_column(df, "full_name", "")
            except ValueError as e:
                print(f"Validation failed: {e}")
        """
        logger = get_logger()

        if validate:
            # Validate inputs
            SparkValidationUtils.validate_is_dataframe(data, "data")
            PandasValidationUtils.validate_is_non_empty_string(column)
            PandasValidationUtils.validate_is_non_empty_string(pattern)
            PandasValidationUtils.validate_is_boolean(regex, "regex")

        # Check if the column exists
        if column not in data.columns:
            error_message = (
                "Column '{column}' not found in DataFrame."
            )
            logger.log(
                "error",
                error_message)
            raise KeyError(error_message)

        try:
            # Split the column
            split_col = split(col(column), pattern)

            # Find the maximum number of splits in the column
            max_splits = data.select(
                size(split_col).alias("split_size")).agg(
                    {"split_size": "max"}).collect()[0][0]

            # Dynamically create columns for each part
            split_data = data.select(
                *data.columns,
                *[
                    split_col.getItem(
                        i).alias(f"{column}_part{i}") for i in range(
                            max_splits)]
            )

            logger.log(
                "info",
                "Successfully split column " +
                f"'{column}' using pattern '{pattern}'.")
            return split_data
        except Exception as e:
            error_message = (
                "Error during column split: {e}")
            logger.log(
                "error",
                error_message)
            raise e(error_message)

    @staticmethod
    def get_columns_by_dtypes(
        data: DataFrame,
        data_types: list,
        validate: bool = True
    ) -> list:
        """
        Identify columns of specific data types in a Spark DataFrame.

        This utility filters the column names in a Spark DataFrame
        based on their data types. It returns a list of column names
        that match the specified Spark data types. Includes additional
        handling for common numeric types like LongType.

        Args:
            data (DataFrame): The input Spark DataFrame.
            data_types (list): List of Spark data types to filter
                (e.g., [IntegerType, StringType]).
            validate (bool): Whether to perform input validation.
                Defaults to True.

        Returns:
            list: A list of column names with the specified data types.

        Raises:
            ValueError: If the input validation fails
                (e.g., invalid data types).

        Examples:
            # Example: Identifying numeric columns
            from pyspark.sql import SparkSession
            from pyspark.sql.types import IntegerType, StringType

            spark = SparkSession.builder.appName(
                "ValidationExample").getOrCreate()

            # Create a sample DataFrame with schema
            from pyspark.sql.types import (
                StructType, StructField, IntegerType,StringType, LongType)
            schema = StructType([
                StructField("id", IntegerType(), True),
                StructField("name", StringType(), True),
                StructField("age", LongType(), True)
            ])

            df = spark.createDataFrame([
                {"id": 1, "name": "Alice", "age": 25},
                {"id": 2, "name": "Bob", "age": 30}
            ], schema)

            # Get columns with numeric types
            numeric_columns = SparkValidationUtils.get_columns_by_dtypes(
                df, [IntegerType, LongType])
            print(f"Numeric columns: {numeric_columns}")
        """
        if validate:
            # Validate inputs
            SparkValidationUtils.validate_is_dataframe(data, "data")
            PandasValidationUtils.validate_is_non_empty_list(data_types)

            # Ensure all provided data types are valid Spark types
            for dtype in data_types:
                if not (
                    isinstance(dtype, type)) or not (
                        issubclass(dtype, DataType)):
                    raise ValueError(
                        f"Invalid data type: {dtype}. " +
                        "Must be a valid Spark data type class.")

        # Filter columns by data types
        matching_columns = [
            field.name
            for field in data.schema.fields if isinstance(
                field.dataType, tuple(data_types))
        ]

        return matching_columns

    @staticmethod
    def get_empty_columns(
        data: DataFrame,
        validate: bool = True
    ) -> list:
        """
        Identify columns with all values as null in a Spark DataFrame.
        This utility checks each column in the provided Spark DataFrame
        and identifies columns where all values are null or missing.
        Returns a list of such column names.

        Args:
            data (DataFrame): The input Spark DataFrame.
            validate (bool): Whether to perform input validation.
                Defaults to True.

        Returns:
            list: A list of column names where all values are null.
            If no such columns exist, returns an empty list.

        Raises:
            ValueError: If the input validation fails
                (e.g., `data` is not a DataFrame).

        Examples:
            # Example 1: DataFrame with some empty columns
            from pyspark.sql import SparkSession
            from pyspark.sql.types import (
                StructType, StructField, IntegerType, StringType)

            spark = SparkSession.builder.appName(
                "ValidationExample").getOrCreate()

            # Create a sample DataFrame
            schema = StructType([
                StructField("id", IntegerType(), True),
                StructField("name", StringType(), True),
                StructField("age", IntegerType(), True)
            ])
            df = spark.createDataFrame([
                {"id": 1, "name": "Alice", "age": None},
                {"id": 2, "name": "Bob", "age": None},
                {"id": 3, "name": "Charlie", "age": None}
            ], schema)

            # Identify empty columns
            empty_columns = SparkValidationUtils.get_empty_columns(df)
            print(f"Empty columns: {empty_columns}")  # Output: ['age']

            # Example 2: DataFrame with no empty columns
            df_full = spark.createDataFrame([
                {"id": 1, "name": "Alice", "age": 25},
                {"id": 2, "name": "Bob", "age": 30},
                {"id": 3, "name": "Charlie", "age": 35}
            ], schema)

            empty_columns_full = SparkValidationUtils.get_empty_columns(
                df_full)
            print(f"Empty columns: {empty_columns_full}")  # Output: []

            # Example 3: Invalid input (not a DataFrame)
            try:
                SparkValidationUtils.get_empty_columns([{"id": 1}])
            except ValueError as e:
                print(f"Validation failed: {e}")
        """
        if validate:
            # Validate the input is a DataFrame
            SparkValidationUtils.validate_is_dataframe(data, "data")

        # Identify columns where all values are null
        empty_columns = []
        for column in data.columns:
            null_count = data.select(
                count(when(col(column).isNull(), column)).alias(
                    "null_count")).collect()[0]["null_count"]
            total_count = data.count()
            if null_count == total_count:
                empty_columns.append(column)

        return empty_columns

    @staticmethod
    def get_columns_matching_pattern(
        data: DataFrame,
        pattern: str,
        validate: bool = True
    ) -> list:
        """
        Get a list of columns matching a regex pattern in a Spark DataFrame.

        This utility identifies column names in the Spark DataFrame that match
        a specified regex pattern. Returns a list of matching column names.

        Args:
            data (DataFrame): The input Spark DataFrame.
            pattern (str): The regex pattern to match column names.
            validate (bool): Whether to perform input validation.
                Defaults to True.

        Returns:
            list: A list of column names matching the regex pattern.
            If no columns match, returns an empty list.

        Raises:
            ValueError: If the input validation fails
                (e.g., invalid pattern or DataFrame).

        Examples:
            # Example 1: Matching column names with a prefix
            from pyspark.sql import SparkSession

            spark = SparkSession.builder.appName(
                "ValidationExample").getOrCreate()

            # Create a sample DataFrame
            df = spark.createDataFrame([
                {"id": 1, "value_2021": 100,
                "value_2022": 200,
                "other_col": "A"},
                {"id": 2, "value_2021": 150,
                "value_2022": 250,
                "other_col": "B"}
            ])

            # Get columns starting with 'value_'
            matching_columns = (
                SparkValidationUtils.get_columns_matching_pattern(
                df, r"^value_"))
            print(f"Matching columns: {matching_columns}")

            # Example 2: No matching columns
            no_match_columns = (
                SparkValidationUtils.get_columns_matching_pattern(
                df, r"^nonexistent_"))
            print(f"No matching columns: {no_match_columns}")  # Output: []

            # Example 3: Invalid pattern
            try:
                SparkValidationUtils.get_columns_matching_pattern(df, "")
            except ValueError as e:
                print(f"Validation failed: {e}")

        """
        if validate:
            # Validate inputs
            SparkValidationUtils.validate_is_dataframe(data, "data")
            PandasValidationUtils.validate_is_non_empty_string(pattern)

        # Match column names using the regex pattern
        matching_columns = [
            col for col in data.columns if re.match(pattern, col)]
        return matching_columns

    @staticmethod
    def validate_column_dependency(
        data: DataFrame,
        primary: str,
        dependent: str,
        validate: bool = True
    ) -> DataFrame:
        """
        Validate dependency between two columns in a Spark DataFrame.

        This utility checks whether the `dependent` column has null or
        empty values when the `primary` column is non-null. It returns
        a DataFrame of rows violating this dependency, allowing further
        inspection or debugging.

        Args:
            data (DataFrame): The input Spark DataFrame.
            primary (str): The name of the primary column.
            dependent (str): The name of the dependent column.
            validate (bool): Whether to perform input validation.
                Defaults to True.

        Returns:
            DataFrame: A Spark DataFrame containing rows where the dependency
                is violated.

        Raises:
            KeyError: If either the primary or dependent column does not exist
            in the DataFrame.
            ValueError: If inputs are invalid (e.g., empty column names).

        Examples:
            # Example 1: Identifying dependency violations
            from pyspark.sql import SparkSession

            spark = SparkSession.builder.appName(
                "ValidationExample").getOrCreate()

            # Create a sample DataFrame
            df = spark.createDataFrame([
                {"id": 1, "parent": "A", "child": "B"},
                {"id": 2, "parent": "C", "child": None},
                {"id": 3, "parent": None, "child": None},
                {"id": 4, "parent": "D", "child": ""}
            ])

            # Validate dependency: 'child' must not be null or empty
            if 'parent' is non-null
            violations = SparkValidationUtils.validate_column_dependency(
                df, "parent", "child")
            violations.show()

            # Output:
            # +---+------+-----+
            # | id|parent|child|
            # +---+------+-----+
            # |  2|     C| null|
            # |  4|     D|     |
            # +---+------+-----+

            # Example 2: Handling non-existent columns
            try:
                SparkValidationUtils.validate_column_dependency(
                    df, "nonexistent", "child")
            except KeyError as e:
                print(f"Validation failed: {e}")
        """
        if validate:
            # Validate inputs
            SparkValidationUtils.validate_is_dataframe(data, "data")
            PandasValidationUtils.validate_is_non_empty_string(primary)
            PandasValidationUtils.validate_is_non_empty_string(dependent)

        # Ensure the specified columns exist in the DataFrame
        missing_columns = [
            col_name for
            col_name in [primary, dependent] if col_name not in data.columns]
        if missing_columns:
            raise KeyError(f"Missing columns: {missing_columns}")

        # Filter rows violating the dependency
        try:
            violating_rows = data.filter(
                (col(primary).isNotNull()) &
                (col(dependent).isNull() | (col(dependent) == "") | isnan(col(
                    dependent)))
            )
            return violating_rows
        except Exception as e:
            raise Exception(f"Error validating column dependency: {e}")

    @staticmethod
    def detect_duplicates(
        data: DataFrame,
        subset: list = None,
        validate: bool = True
    ) -> DataFrame:
        """
        Detect duplicate rows in a Spark DataFrame.

        This utility identifies duplicate rows in the provided Spark DataFrame.
        If a `subset` of columns is specified, duplicates are detected based on
        those columns. Otherwise, all columns are used for duplicate detection.

        Args:
            data (DataFrame): The Spark DataFrame to check for duplicates.
            subset (list, optional): List of column names to consider when
                identifying duplicates. If None, all columns are used.
                Defaults to None.
            validate (bool): Whether to perform input validation.
                Defaults to True.

        Returns:
            DataFrame: A Spark DataFrame containing duplicate rows.

        Raises:
            KeyError: If any column in `subset` is missing from the DataFrame.
            ValueError: If inputs are invalid (e.g., empty subset).

        Examples:
            # Example 1: Detect duplicates based on a subset of columns
            from pyspark.sql import SparkSession

            spark = SparkSession.builder.appName(
                "ValidationExample").getOrCreate()

            # Create a sample DataFrame
            df = spark.createDataFrame([
                {"id": 1, "name": "Alice", "age": 25},
                {"id": 2, "name": "Bob", "age": 30},
                {"id": 3, "name": "Alice", "age": 25},
                {"id": 4, "name": "Alice", "age": 25}
            ])

            # Detect duplicates based on a subset of columns
            subset_duplicates = SparkValidationUtils.detect_duplicates(
                df, subset=["name", "age"])
            subset_duplicates.show()

            # Output:
            # +---+-----+---+--------------+
            # | id| name|age|duplicate_count|
            # +---+-----+---+--------------+
            # |  1|Alice| 25|              3|
            # |  3|Alice| 25|              3|
            # |  4|Alice| 25|              3|
            # +---+-----+---+--------------+

            # Example 2: Detect duplicates using all columns
            unique_duplicates = SparkValidationUtils.detect_duplicates(df)
            unique_duplicates.show()

            # Example 3: Handling missing columns in subset
            try:
                SparkValidationUtils.detect_duplicates(
                    df, subset=["nonexistent_column"])
            except KeyError as e:
                print(f"Validation failed: {e}")
        """
        if validate:
            # Validate inputs
            SparkValidationUtils.validate_is_dataframe(data, "data")
            if subset:
                PandasValidationUtils.validate_is_non_empty_list(subset)

        # If no subset is specified, use all columns
        columns_to_check = subset if subset else data.columns

        # Ensure all specified columns exist
        missing_columns = [
            col_name for col_name in (
                columns_to_check) if col_name not in data.columns]
        if missing_columns:
            raise KeyError(f"Missing columns: {missing_columns}")

        # Add a count of duplicates for each row using a Window function
        window_spec = Window.partitionBy(*[col(c) for c in columns_to_check])
        duplicate_data = data.withColumn("duplicate_count", count("*").over(
            window_spec))

        # Filter rows where the duplicate count is greater than 1
        return duplicate_data.filter(
            col("duplicate_count") > 1).drop(
                "duplicate_count")

    @staticmethod
    def validate_column_regex(
        data: DataFrame,
        column: str,
        pattern: str,
        errors: list,
        validate: bool = True
    ) -> DataFrame:
        """
        Validate column values against a regex pattern in a Spark DataFrame.

        This utility checks whether all values in a specified column of a Spark
        DataFrame match a given regex pattern. Rows with invalid values are
        returned as a DataFrame for further inspection or debugging.
        Additionally, details of validation failures are appended to the
        provided `errors` list.

        Args:
            data (DataFrame): The Spark DataFrame to validate.
            column (str): The name of the column to validate.
            pattern (str): The regex pattern to match against column values.
            errors (list): A list to which validation errors will be appended.
            validate (bool): Whether to perform input validation.
                Defaults to True.

        Returns:
            DataFrame: A Spark DataFrame containing rows with invalid values.

        Raises:
            KeyError: If the specified column does not exist in the DataFrame.
            ValueError: If inputs are invalid (e.g., empty pattern).

        Examples:
            # Example 1: Validating email addresses
            from pyspark.sql import SparkSession

            spark = SparkSession.builder.appName(
                "ValidationExample").getOrCreate()

            # Create a sample DataFrame
            df = spark.createDataFrame([
                {"id": 1, "email": "valid.email@example.com"},
                {"id": 2, "email": "invalid-email"},
                {"id": 3, "email": "another.valid@example.org"}
            ])

            # Validate the "email" column against a regex for email addresses
            errors = []
            invalid_rows = SparkValidationUtils.validate_column_regex(
                df, "email", r"^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$", errors
            )
            invalid_rows.show()

            # Output:
            # +---+-------------+
            # | id|        email|
            # +---+-------------+
            # |  2| invalid-email|
            # +---+-------------+

            # Example 2: Non-existent column
            try:
                SparkValidationUtils.validate_column_regex(df, "nonexistent",
                r"^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$", errors)
            except KeyError as e:
                print(f"Validation failed: {e}")

            # Example 3: Invalid regex pattern
            try:
                SparkValidationUtils.validate_column_regex(
                    df, "email", "", errors)
            except ValueError as e:
                print(f"Validation failed: {e}")
        """
        logger = get_logger()

        if validate:
            # Validate inputs
            SparkValidationUtils.validate_is_dataframe(data, "data", False)
            PandasValidationUtils.validate_is_non_empty_string(column)
            PandasValidationUtils.validate_is_non_empty_string(pattern)
            PandasValidationUtils.validate_instance(errors, list)

        # Ensure the column exists
        if column not in data.columns:
            error_message = (
                f"Column '{column}' not found in DataFrame."
            )
            logger.log(
                "error",
                error_message)
            raise KeyError(error_message)

        # Add a flag for invalid rows based on the regex
        invalid_data = data.filter(~col(column).rlike(pattern))

        # Check if any invalid rows exist
        if invalid_data.count() > 0:
            error_message = (
                f"Column '{column}' contains values not " +
                "matching the regex pattern " +
                f"'{pattern}'."
            )
            logger.log("error", error_message)
            errors.append({
                "error_type": "regex_violation",
                "details": error_message
            })

        return invalid_data

    @staticmethod
    def validate_column_values(
        data: DataFrame,
        column: str,
        values: list,
        allow_only: bool,
        errors: list,
        validate: bool = True
    ) -> DataFrame:
        """
        Validate that all values in a specified column are within a set of
        allowed values.

        This utility checks whether all values in a specified column of a
        Spark DataFrame are within a provided list of allowed values.
        Rows with invalid values are returned as a DataFrame for further
        inspection or debugging. Additionally, validation errors are
        appended to the provided `errors` list.

        Args:
            data (DataFrame): The Spark DataFrame to validate.
            column (str): The name of the column to validate.
            allowed_values (list): A list of allowed values for the column.
            errors (list): A list to which validation errors will be appended.
            validate (bool): Whether to perform input validation.
            Defaults to True.

        Returns:
            DataFrame: A Spark DataFrame containing rows with invalid values.

        Raises:
            KeyError: If the specified column does not exist in the DataFrame.
            ValueError: If inputs are invalid (e.g., empty allowed_values).

        Examples:
            # Example 1: Validating column values against allowed values
            from pyspark.sql import SparkSession

            spark = SparkSession.builder.appName(
                "ValidationExample").getOrCreate()

            # Create a sample DataFrame
            df = spark.createDataFrame([
                {"id": 1, "status": "active"},
                {"id": 2, "status": "inactive"},
                {"id": 3, "status": "unknown"}
            ])

            # Validate that the "status" column contains only allowed values
            allowed_values = ["active", "inactive"]
            errors = ["some errors]
            invalid_rows = SparkValidationUtils.validate_column_values(
                df, "status", allowed_values, errors)
            invalid_rows.show()

            # Output:
            # +---+-------+
            # | id| status|
            # +---+-------+
            # |  3|unknown|
            # +---+-------+

            # Example 2: Non-existent column
            try:
                SparkValidationUtils.validate_column_values(
                    df, "nonexistent", allowed_values, errors)
            except KeyError as e:
                print(f"Validation failed: {e}")

            # Example 3: Empty allowed_values
            try:
                SparkValidationUtils.validate_column_values(
                    df, "status", [], errors)
            except ValueError as e:
                print(f"Validation failed: {e}")
        """
        logger = get_logger()

        if validate:
            # Validate inputs
            SparkValidationUtils.validate_is_dataframe(data, "data")
            PandasValidationUtils.validate_is_non_empty_string(column)
            PandasValidationUtils.validate_is_non_empty_list(values)
            PandasValidationUtils.validate_is_boolean(allow_only, "allow_only")
            PandasValidationUtils.validate_instance(errors, list)

        # Ensure the column exists
        if column not in data.columns:
            error_message = (
                f"Column '{column}' not found in DataFrame."
            )
            logger.log(
                "error",
                error_message)
            raise KeyError(error_message)

        # Determine invalid rows based on allow_only flag
        if allow_only:
            invalid_data = data.filter(~col(column).isin(values))
        else:
            invalid_data = data.filter(col(column).isin(values))

        # Check if any invalid rows exist
        if invalid_data.count() > 0:
            validation_type = "allowed" if allow_only else "prohibited"
            error_message = (
                f"Column '{column}' contains values " +
                f"{validation_type}: {values}."
            )
            logger.log("error", error_message)
            errors.append({
                "error_type": "value_violation",
                "details": error_message
            })

        return invalid_data

    @staticmethod
    def validate_is_non_empty_dataset(
        data: DataFrame,
        errors: list,
        validate: bool = True
    ):
        """
        Check if the Spark DataFrame is empty and update the errors
        list if validation fails.

        This utility ensures that the provided Spark DataFrame is not empty.
        If the DataFrame has no rows or columns, it appends an error message
        to the `errors` list for further handling or debugging.

        Args:
            data (DataFrame): The Spark DataFrame to validate.
            errors (list): A list to which validation errors will be appended.
            validate (bool): Whether to perform input validation.
            Defaults to True.

        Raises:
            ValueError: If the `errors` list is not a valid list.
            ValueError: If `data` is not a Spark DataFrame.

        Examples:
            # Example 1: Validating a non-empty DataFrame
            from pyspark.sql import SparkSession

            spark = SparkSession.builder.appName(
                "ValidationExample").getOrCreate()

            # Create a sample non-empty DataFrame
            df = spark.createDataFrame([
                {"id": 1, "name": "Alice"},
                {"id": 2, "name": "Bob"}
            ])

            # Validate the DataFrame
            errors = []
            SparkValidationUtils.validate_is_non_empty_dataset(df, errors)
            print(f"Errors: {errors}")  # Output: Errors: []

            # Example 2: Validating an empty DataFrame
            empty_df = spark.createDataFrame([], schema="id INT, name STRING")

            SparkValidationUtils.validate_is_non_empty_dataset(
                empty_df, errors)
            print(f"Errors: {errors}")

            # Example 3: Invalid input (not a DataFrame)
            try:
                SparkValidationUtils.validate_is_non_empty_dataset(
                    [{"id": 1}], errors)
            except ValueError as e:
                print(f"Validation failed: {e}")
        """
        logger = get_logger()

        if validate:
            # Validate inputs
            SparkValidationUtils.validate_is_dataframe(data, "data")
            PandasValidationUtils.validate_instance(errors, list)

        # Check if the DataFrame is empty (no rows or columns)
        if not data.columns or data.count() == 0:
            logger.log("error", "The dataset is empty (no rows or columns).")
            errors.append({
                "error_type": "empty_dataset",
                "details": "The dataset is empty (no rows or columns)."
            })

    @staticmethod
    def check_value_range(
        data: DataFrame,
        column: str,
        min_val: float,
        max_val: float,
        inclusive: bool = True,
        validate: bool = True
    ) -> DataFrame:
        """
        Check if values in a column fall within the specified range in a Spark
        DataFrame.

        This utility identifies rows where the values in a specified column
        fall outside the given range. If `inclusive` is set to True, the range
        boundaries are included in the validation; otherwise, they are
        excluded.

        Args:
            data (DataFrame): The Spark DataFrame containing the colum
            to check.
            column (str): The name of the column to validate.
            min_val (float): Minimum value of the range.
            max_val (float): Maximum value of the range.
            inclusive (bool): If True, include boundaries; otherwise,
                exclude them. Defaults to True.
            validate (bool): Whether to validate the inputs. Defaults to True.

        Returns:
            DataFrame: A Spark DataFrame containing rows with
                out-of-range values.

        Raises:
            KeyError: If the specified column does not exist in the DataFrame.
            ValueError: If inputs (e.g., min_val, max_val) are invalid.

        Examples:
            # Example 1: Checking values within a range (inclusive)
            from pyspark.sql import SparkSession

            spark = SparkSession.builder.appName(
                "ValidationExample").getOrCreate()

            # Create a sample DataFrame
            df = spark.createDataFrame([
                {"id": 1, "value": 10.5},
                {"id": 2, "value": 15.0},
                {"id": 3, "value": 20.0},
                {"id": 4, "value": 25.5}
            ])

            # Identify rows with values outside the range 10.0 to 20.0 (
                # inclusive)
            out_of_range = SparkValidationUtils.check_value_range(
                df, "value", 10.0, 20.0)
            out_of_range.show()

            # Output:
            # +---+-----+
            # | id|value|
            # +---+-----+
            # |  4| 25.5|
            # +---+-----+

            # Example 2: Excluding boundaries
            out_of_range_exclusive = SparkValidationUtils.check_value_range(
                df, "value", 10.0, 20.0, inclusive=False)
            out_of_range_exclusive.show()

            # Output:
            # +---+-----+
            # | id|value|
            # +---+-----+
            # |  1| 10.5|
            # |  3| 20.0|
            # |  4| 25.5|
            # +---+-----+

            # Example 3: Handling non-existent column
            try:
                SparkValidationUtils.check_value_range(
                    df, "nonexistent_column", 10.0, 20.0)
            except KeyError as e:
                print(f"Validation failed: {e}")
        """
        if validate:
            # Validate inputs
            SparkValidationUtils.validate_is_dataframe(data, "data")
            PandasValidationUtils.validate_is_non_empty_string(column)
            PandasValidationUtils.validate_float(min_val, "min_val")
            PandasValidationUtils.validate_float(max_val, "max_val")

        # Ensure the column exists
        if column not in data.columns:
            raise KeyError(f"Column '{column}' not found in DataFrame.")

        # Define the range filter
        if inclusive:
            out_of_range_filter = ~(
                (col(column) >= lit(min_val)) & (col(column) <= lit(max_val)))
        else:
            out_of_range_filter = (
                col(column) <= lit(min_val)) | (col(column) >= lit(max_val))

        # Filter rows with out-of-range values
        return data.filter(out_of_range_filter)

    @staticmethod
    def check_column_dtype(
        data: DataFrame,
        column: str,
        expected_type: DataType,
        validate: bool = True
    ) -> bool:
        """
        Validate if a Spark DataFrame column's data type matches the
        expected type.

        This utility checks whether the data type of a specified column
        in a Spark DataFrame matches the provided `expected_type`.
        Returns `True` if the types match, otherwise `False`.

        Args:
            data (DataFrame): The Spark DataFrame to validate.
            column (str): The name of the column to validate.
            expected_type (DataType): The expected Spark data type
                (e.g., IntegerType, StringType).
            validate (bool): Whether to perform input validation.
            Defaults to True.

        Returns:
            bool: True if the column's data type matches the expected type,
            otherwise False.

        Raises:
            KeyError: If the specified column is not found in the DataFrame.
            ValueError: If the `expected_type` is not a valid Spark data type.

        Examples:
            # Example 1: Validating column data type
            from pyspark.sql import SparkSession
            from pyspark.sql.types import IntegerType, StringType

            spark = SparkSession.builder.appName(
                "ValidationExample").getOrCreate()

            # Create a sample DataFrame
            df = spark.createDataFrame([
                {"id": 1, "name": "Alice"},
                {"id": 2, "name": "Bob"}
            ])

            # Validate the "id" column's data type
            is_valid = SparkValidationUtils.check_column_dtype(
                df, "id", IntegerType)
            print(f"ID column is IntegerType: {is_valid}")  # Output: True

            # Validate the "name" column's data type
            is_valid = SparkValidationUtils.check_column_dtype(
                df, "name", StringType)
            print(f"Name column is StringType: {is_valid}")  # Output: True

            # Example 2: Invalid data type
            is_valid = SparkValidationUtils.check_column_dtype(
                df, "id", StringType)
            print(f"ID column is StringType: {is_valid}")  # Output: False

            # Example 3: Non-existent column
            try:
                SparkValidationUtils.check_column_dtype(df, "age", IntegerType)
            except KeyError as e:
                print(f"Validation failed: {e}")
        """
        if validate:
            # Validate the inputs
            SparkValidationUtils.validate_is_dataframe(data, "data")
            PandasValidationUtils.validate_is_non_empty_string(column)

        # Ensure the column exists in the DataFrame
        if column not in data.columns:
            raise KeyError(f"Column '{column}' not found in DataFrame.")

        # Get the column's data type
        actual_type = next(
            (field.dataType for field in (
                data.schema.fields) if field.name == column),
            None
        )

        # Check if the column's type matches the expected type
        return isinstance(actual_type, expected_type)

    @staticmethod
    def concatenate_invalid_rows(
        current_invalid: DataFrame,
        new_invalid: DataFrame,
        validate: bool = True
    ) -> DataFrame:
        """
        Concatenate invalid rows into a single Spark DataFrame and remove
        duplicates.

        This utility merges two Spark DataFrames containing invalid rows
        into a single DataFrame while ensuring that duplicates are
        removed from the resulting DataFrame.

        Args:
            current_invalid (DataFrame): A Spark DataFrame containing
                previously identified invalid rows.
            new_invalid (DataFrame): A Spark DataFrame containing newly
                identified invalid rows.
            validate (bool): Whether to validate the inputs. Defaults to True.

        Returns:
            DataFrame: A concatenated Spark DataFrame of invalid rows with
            duplicates removed.

        Raises:
            ValueError: If either of the inputs is not a valid Spark DataFrame.
            Exception: If an error occurs during concatenation
            or deduplication.

        Examples:
            # Example 1: Concatenating invalid rows
            from pyspark.sql import SparkSession

            spark = SparkSession.builder.appName(
                "ValidationExample").getOrCreate()

            # Create a DataFrame of previously invalid rows
            current_invalid = spark.createDataFrame([
                {"id": 1, "reason": "Missing value"},
                {"id": 2, "reason": "Invalid format"}
            ])

            # Create a DataFrame of new invalid rows
            new_invalid = spark.createDataFrame([
                {"id": 2, "reason": "Invalid format"},
                {"id": 3, "reason": "Out of range"}
            ])

            # Concatenate the DataFrames and remove duplicates
            combined_invalid = SparkValidationUtils.concatenate_invalid_rows(
                current_invalid, new_invalid)
            combined_invalid.show()

            # Output:
            # +---+---------------+
            # | id|         reason|
            # +---+---------------+
            # |  1|  Missing value|
            # |  2| Invalid format|
            # |  3|   Out of range|
            # +---+---------------+

            # Example 2: Invalid input (non-DataFrame)
            try:
                SparkValidationUtils.concatenate_invalid_rows(
                    current_invalid, [{"id": 4, "reason": "Invalid type"}])
            except ValueError as e:
                print(f"Validation failed: {e}")
        """
        if validate:
            # Validate inputs
            SparkValidationUtils.validate_is_dataframe(
                current_invalid,
                "current_invalid")
            SparkValidationUtils.validate_is_dataframe(
                new_invalid,
                "new_invalid")

        # Concatenate and remove duplicates
        try:
            combined = current_invalid.union(new_invalid).dropDuplicates()
            return combined
        except Exception as e:
            raise Exception(f"Error during concatenation: {e}")


def generate_validator_map(module=None):
    from Data_Engineering_Class_Enums_and_Abstract_Classes import Validator
    """
    Dynamically generate a validator map by scanning a module or notebook
    for classes inheriting from the base `Validator` class.

    Args:
        module (module, optional): The module to scan. If None,
        scans the current notebook scope.

    Returns:
        dict: A mapping of class names to their corresponding classes.

    Example:
        ```python
        from Data_Engineering_Class_Enums_and_Abstract_Classes import Validator
        from Data_Engineering_Class_Libraries_and_Utility_Functions import (
            generate_validator_map
        )
        import my_module

        # Define example validators inheriting from the Validator base class
        class ValidatorA(Validator):
            pass

        class ValidatorB(Validator):
            pass

        # Generate the validator map for the current module
        validator_map = generate_validator_map(my_module)
        print(validator_map)
        # Output:
        # {
        #     'ValidatorA': <class '__main__.ValidatorA'>,
        #     'ValidatorB': <class '__main__.ValidatorB'>
        # }
        ```

    Notes:
        - This function is particularly useful in dynamic validation systems,
        where validators are added programmatically without hardcoding them
        into a single map.
        - Ensure that the `Validator` base class is properly imported in the
        module being scanned.
    """
    # Default to scanning the current notebook scope
    if module is None:
        module = sys.modules[__name__]

    validator_map = {}
    for name, obj in inspect.getmembers(module, inspect.isclass):
        # Ensure the class inherits from Validator and is not the base class
        if issubclass(obj, Validator) and obj is not Validator:
            validator_map[name] = obj
    return validator_map


def generate_transformer_map(module=None):
    from Data_Engineering_Class_Enums_and_Abstract_Classes import Transformer
    """
    Dynamically generate a map of transformer names to their classes.

    Args:
        module (module, optional): The module to scan for transformers.
            Defaults to the current notebook scope.

    Returns:
        dict: A mapping of transformer class names to their corresponding
            classes.

    Example:
        ```python
        from Data_Engineering_Class_Enums_and_Abstract_Classes import (
            Transformer)
        from Data_Engineering_Class_Libraries_and_Utility_Functions import (
            generate_transformer_map
        )
        import my_module

        # Define example transformers inheriting from the Transformer
        #   base class
        class TransformerA(Transformer):
            pass

        class TransformerB(Transformer):
            pass

        # Generate the transformer map for the current module
        transformer_map = generate_transformer_map(my_module)
        print(transformer_map)
        # Output:
        # {
        #     'TransformerA': <class '__main__.TransformerA'>,
        #     'TransformerB': <class '__main__.TransformerB'>
        # }
        ```

    Notes:
        - This function is particularly useful in dynamic transformation
        systems where transformers are added programmatically without
        hardcoding them into a single map.
        - Ensure that the `Transformer` base class is properly imported in the
        module being scanned.
    """

    # Default to scanning the current notebook scope
    if module is None:
        module = sys.modules[__name__]

    transformer_map = {}
    for name, obj in inspect.getmembers(module, inspect.isclass):
        # Include only subclasses of Transformer, excluding the base class
        if issubclass(obj, Transformer) and obj is not Transformer:
            transformer_map[name] = obj
    return transformer_map


class DynamicValidatorFactory:
    """
    Factory for dynamically creating Pandas validators based on
    a configuration dictionary.

    This factory generates a `validator_map` dynamically by scanning
    the specified module or the current notebook's namespace.It
    supports both Python scripts (`.py`) and notebook environments (`.ipynb`).

    Attributes:
        validator_map (dict): A dictionary mapping validator type names
            to their corresponding classes.
        logger (DynamicLogger): Logger instance for tracking factory
        operations.

    Example Usage:
        Using in a Python script (.py):
        ------------------------------
        import Data_Engineering_Class_Pandas_Implementation
        from Data_Engineering_Class_Libraries_and_Utility_Functions import (
            generate_validator_map)

        # Initialize the factory
        factory = DynamicValidatorFactory(
            Data_Engineering_Class_Pandas_Implementation)

        # Example configuration
        config = {
            "type": "PandasRangeValidator",
            "options": {"column_ranges": {"col1": [0, 100]},
            "inclusive": False}
        }

        # Create the validator
        validator = factory.create_validator(config)
        print(validator)

        Using in a Notebook (.ipynb):
        -----------------------------
        # Define validators in the notebook
        class PandasRangeValidator(Validator):
            def validate(self, data):
                return {"is_valid": True}

        class PandasMissingColumnsValidator(Validator):
            def validate(self, data):
                return {"is_valid": True}

        # Initialize the factory (no module required)
        factory = DynamicValidatorFactory()

        # Example configuration
        config = {
            "type": "PandasRangeValidator",
            "options": {"column_ranges": {"col1": [0, 100]},
            "inclusive": False}
        }

        # Create the validator
        validator = factory.create_validator(config)
        print(validator)
    """

    def __init__(self, module=None):
        """
        Initialize the factory by dynamically generating the `validator_map`.

        Args:
            module (module, optional): The module to scan for validator
                classes. Defaults to None. If None, the factory scans the
                current notebook namespace.

        Notes:
            - If you're working in a `.py` file, pass the module where
            the validator classes are defined.
            Example:
                import Data_Engineering_Class_Pandas_Implementation
                factory = DynamicValidatorFactory(
                    Data_Engineering_Class_Pandas_Implementation)

            - If you're working in a notebook, no module is required.
                The factory will automatically detect classes defined
                in the current notebook scope.

        Raises:
            ValueError: If the `validator_map` is empty, indicating
            no validators were found.
        """
        # Fallback to the notebook's namespace if no module is provided
        self.validator_map = generate_validator_map(
            module or sys.modules[__name__])
        self.logger = get_logger()

        if not self.validator_map:
            error_message = (
                "No validators were found in the specified module " +
                "or notebook namespace. " +
                "Ensure that validator classes inherit from " +
                "the `Validator` base class."
            )
            self.logger.log(
                "error",
                error_message)
            raise ValueError(error_message)

    def create_validator(self, validator_config: dict):
        """
        Create a validator instance based on the provided configuration.

        Args:
            validator_config (dict): A dictionary containing:
                - 'type': The name of the validator class.
                - 'options': A dictionary of options to configure the
                validator.

        Returns:
            Validator: An instance of the specified validator class.

        Raises:
            ValueError:
                - If 'type' or 'options' is missing from the configuration.
                - If the specified validator type is not supported.

        Example:
            config = {
                "type": "PandasRangeValidator",
                "options": {
                    "column_ranges": {"col1": [0, 100]},
                    "inclusive": False}
            }
            factory = DynamicValidatorFactory()
            validator = factory.create_validator(config)
        """
        PandasValidationUtils.validate_is_non_empty_dict(
            validator_config)
        # Validate configuration structure
        if "type" not in validator_config or "options" not in validator_config:
            error_message = (
                "Each validator must have a 'type' and 'options' key."
            )
            self.logger.log(
                "error",
                error_message)
            raise ValueError(error_message)

        validator_type = validator_config["type"]
        options = validator_config["options"]

        # Log the validator creation attempt
        self.logger.log(
            "info",
            f"Attempting to create validator of type "
            f"'{validator_type}' with options: {options}")

        # Remove any redundant 'type' key inside options
        options = {k: v for k, v in options.items() if k != "type"}

        # Check if the validator type is supported
        if validator_type not in self.validator_map:
            valid_types = ", ".join(self.validator_map.keys())
            error_message = (
                f"Unsupported validator type: '{validator_type}'. " +
                f"Supported types: {valid_types}."
            )
            self.logger.log(
                "error",
                error_message)
            raise ValueError(error_message)

        # Log validator creation success
        validator_class = self.validator_map[validator_type]
        self.logger.log(
            "info",
            f"Successfully created validator of type '{validator_type}'.")
        # Return the validator instance
        return validator_class(**options)


class ValidatorRunner:
    """
    Runner to execute multiple validators dynamically on a DataFrame
    (Pandas or Spark).

    Attributes:
        validators (list): List of validator configurations or instances.
        logger (DynamicLogger): Logger for tracking execution progress.
    """

    def __init__(
        self,
        validator_configs: list,
        factory: DynamicValidatorFactory
    ):
        """
        Initialize the runner with validator configurations and a factory.

        Args:
            validator_configs (list): List of validator configurations.
            factory (DynamicValidatorFactory): Factory to create validators.
        """
        self.logger = get_logger()
        PandasValidationUtils.validate_instance(
            factory,
            DynamicValidatorFactory,
            "factory")
        self.factory = factory
        self.validators = [
            self.factory.create_validator(
                config) for config in validator_configs
        ]

    def run_validations(self, data):
        """
        Execute all validators on the provided DataFrame.

        Args:
            data (pd.DataFrame or pyspark.sql.DataFrame): Data to validate.

        Returns:
            ValidationReport: Consolidated validation report.
        """
        # Determine the framework
        if isinstance(data, pd.DataFrame):  # Pandas DataFrame
            validation_utils = PandasValidationUtils
        elif isinstance(data, DataFrame):  # Spark DataFrame
            validation_utils = SparkValidationUtils
        else:
            error_message = (
                "Unsupported DataFrame type."
            )
            self.logger.log(
                "error",
                error_message)
            raise ValueError(error_message)
        report_class = ValidationReport
        # Validate the input data
        validation_utils.validate_is_dataframe(data, 'data')

        validator_results = []
        combined_invalid_rows = pd.DataFrame()
        combined_invalid_columns = set()
        invalid_rows_by_validator = {}
        invalid_columns_by_validator = {}

        self.logger.log(
            "info",
            "Starting validation run.")
        for validator in self.validators:
            validator_name = validator.__class__.__name__
            self.logger.log(
                "info",
                f"Running validator: {validator_name}")
            try:
                result = validator.validate(data)
                validator_results.append({
                    "validator": validator_name,
                    "is_valid": result.get(
                        "is_valid", True),
                    "errors": result.get(
                        "errors",
                        [])
                })

                # Collect invalid rows and columns
                if not result.get(
                    "is_valid",
                    True
                ):
                    if "invalid_rows" in result:
                        invalid_rows = result.get("invalid_rows")
                        invalid_rows_by_validator[validator_name] = (
                            invalid_rows)
                        combined_invalid_rows = pd.concat(
                            [combined_invalid_rows, invalid_rows],
                            ignore_index=True
                        ).drop_duplicates().reset_index(drop=True)
                    if "invalid_columns" in result:
                        invalid_columns = result.get("invalid_columns", [])
                        invalid_columns_by_validator[validator_name] = (
                            invalid_columns)
                        combined_invalid_columns.update(invalid_columns)

            except Exception as e:
                self.logger.log(
                    "error",
                    f"Validator {validator_name} failed: {e}"
                )
                validator_results.append({
                    "validator": validator_name,
                    "is_valid": False,
                    "errors": [
                        {
                            "error_type": "runtime_error",
                            "details": str(e)}]
                })

        self.logger.log(
            "info",
            "Validation run completed.")

        return report_class(
            validator_results=validator_results,
            combined_invalid_rows=combined_invalid_rows,
            invalid_columns=list(combined_invalid_columns),
            invalid_rows_by_validator=invalid_rows_by_validator,
            invalid_columns_by_validator=invalid_columns_by_validator
        )


class ValidationReport:
    """
    Generalized class to aggregate, summarize, and export validation results
    for both Pandas and Spark DataFrames.
    """

    def __init__(
        self,
        validator_results: list,
        combined_invalid_rows,
        invalid_columns: list,
        invalid_rows_by_validator: dict = None,
        invalid_columns_by_validator: dict = None,
    ):
        self.logger = get_logger()

        if not isinstance(validator_results, list):
            error_message = (
                "validator_results must be a list.")
            self.logger.log(
                "error",
                error_message)
            raise ValueError(error_message)
        self.validator_results = validator_results
        if isinstance(combined_invalid_rows, pd.DataFrame):
            self.data_type = "pandas"
            self.combined_invalid_rows = combined_invalid_rows.drop_duplicates(
                ).reset_index(drop=True)
        elif isinstance(combined_invalid_rows, DataFrame):
            self.data_type = "spark"
            self.combined_invalid_rows = combined_invalid_rows.dropDuplicates()
        else:
            error_message = (
                "combined_invalid_rows must be a Pandas or Spark DataFrame.")
            self.logger.log(
                "error",
                error_message)
            raise ValueError(error_message)

        if not isinstance(
            invalid_columns,
            list
        ):
            error_message = (
                "invalid_columns must be a list of strings."
            )
            self.logger.log(
                "error",
                error_message)
            raise ValueError(error_message)

        self.invalid_columns = list(set(invalid_columns))
        self.invalid_rows_by_validator = invalid_rows_by_validator or {}
        self.invalid_columns_by_validator = invalid_columns_by_validator or {}

    def generate_summary(self) -> dict:
        """
        Generate a summary of the validation results.

        Returns:
            dict: Summary of the validation results.
        """
        invalid_rows_count = (
            len(self.combined_invalid_rows)
            if self.data_type == "pandas"
            else self.combined_invalid_rows.count()
        )

        summary = {
            "total_validators": len(self.validator_results),
            "failed_validators": sum(
                1 for result in (
                    self.validator_results) if not result["is_valid"]
            ),
            "invalid_rows_count": invalid_rows_count,
            "invalid_columns_count": len(self.invalid_columns),
        }
        return summary

    def get_combined_invalid_data(self) -> dict:
        """
        Retrieve combined invalid rows and columns.
        """
        return {
            "combined_invalid_rows": self.combined_invalid_rows,
            "invalid_columns": self.invalid_columns,
        }

    def get_invalid_rows_by_validator(self) -> dict:
        """
        Retrieve invalid rows by validator.
        """
        return self.invalid_rows_by_validator

    def get_invalid_columns_by_validator(self) -> dict:
        """
        Retrieve invalid columns by validator.
        """
        return self.invalid_columns_by_validator

    def get_summary_and_validator_results(self) -> dict:
        """
        Get the validation summary and details.
        """
        summary = self.generate_summary()
        return {
            "summary": summary,
            "details": self.validator_results,
        }


class DynamicTransformerFactory:
    """
    Factory for creating transformers dynamically using a transformer map.

    Attributes:
        transformer_map (dict): A mapping of transformer names to
            their classes.
        logger (DynamicLogger): Logger for tracking transformer creation.
    """
    def __init__(self, module=None):
        """
        Initialize the factory by generating the transformer map.

        Args:
            module (module, optional): Module to scan for transformers.
                Defaults to current notebook scope.
        """
        self.logger = get_logger()
        self.transformer_map = generate_transformer_map(module)
        if not self.transformer_map:
            error_message = (
                "No transformers found in the specified module or namespace."
            )
            self.logger.log(
                "error",
                error_message)
            raise ValueError(error_message)
        self.logger.log(
            "info",
            f"Loaded {len(self.transformer_map)} transformers.")

    def create_transformer(self, transformer_config: dict):
        """
        Create a transformer instance dynamically.

        Args:
            transformer_config (dict): Configuration for the transformer.
            Must include:
                - "type": Transformer class name.
                - "options": Parameters for initializing the transformer.

        Returns:
            Transformer: An instance of the specified transformer.

        Raises:
            ValueError: If the transformer type is unsupported or options
            are invalid.
        """
        PandasValidationUtils.validate_is_non_empty_dict(
            transformer_config)
        transformer_type = transformer_config.get("type")
        options = transformer_config.get("options", {})

        if not transformer_type or transformer_type not in (
            self.transformer_map
        ):
            available_types = ", ".join(self.transformer_map.keys())
            error_message = (
                "Unsupported transformer type: " +
                f"{transformer_type}. Available types: {available_types}"
            )
            self.logger.log(
                "error",
                error_message)
            raise ValueError(error_message)

        self.logger.log(
            "info",
            f"Creating transformer: "
            f"{transformer_type} with options: {options}")
        transformer_class = self.transformer_map[transformer_type]
        return transformer_class(**options)


class TransformerRunner:
    """
    Runner to execute a sequence of transformers dynamically on a
    DataFrame (Pandas, Spark, or other supported frameworks).

    Attributes:
        transformers (list): List of transformer configurations or instances.
        logger (DynamicLogger): Logger for tracking transformation progress.
        framework (Framework): The framework being used (e.g., PANDAS, SPARK).
    """
    def __init__(
        self,
        transformer_configs: list,
        factory: DynamicTransformerFactory,
        framework: Framework
    ):
        """
        Initialize the runner with transformer configurations, a factory,
        and a framework.

        Args:
            transformer_configs (list): List of transformer configurations.
            factory (DynamicTransformerFactory): Factory for creating
                transformer instances.
            framework (Framework): Enum value representing the framework
                (PANDAS, SPARK, etc.).

        Raises:
            ValueError: If an unsupported framework is specified.
        """
        self.logger = get_logger()
        PandasValidationUtils.validate_instance(
            factory,
            DynamicTransformerFactory,
            "factory")
        self.factory = factory

        # Use the framework to set the appropriate validation utility
        self.framework = framework
        match self.framework:
            case Framework.PANDAS:
                self.validation_utils = PandasValidationUtils
            case Framework.SPARK:
                self.validation_utils = SparkValidationUtils
            case _:
                error_message = (
                    "Unsupported framework: " +
                    f"{framework}. Supported: PANDAS, SPARK."
                )
                self.logger.log(
                    "error",
                    error_message)
                raise ValueError(error_message)

        # Create transformers using the factory
        self.transformers = [
            self.factory.create_transformer(
                config) for config in transformer_configs
        ]
        self.logger.log(
            "info",
            "TransformerRunner initialized for " +
            f"{self.framework.value} framework.")

    def execute(self, data, **kwargs):
        """
        Execute all transformers on the given DataFrame using
        chained transformations.

        Args:
            data: The DataFrame to transform (Pandas or Spark).
            **kwargs: Additional parameters for transformer execution.

        Returns:
            Transformed DataFrame (Pandas or Spark).
        """
        self.validation_utils.validate_is_dataframe(data, 'data')
        self.logger.log(
            "info",
            "Starting transformation runner with chaining.")

        # Apply transformations in a chained manner
        try:
            result = data
            for transformer in self.transformers:
                transformer_name = transformer.__class__.__name__
                self.logger.log(
                    "info",
                    f"Applying transformer: {transformer_name}")
                result = transformer.transform(result, **kwargs)
            self.logger.log(
                "info",
                "Transformation runner completed successfully.")
            return result
        except Exception as e:
            error_message = (
                f"An error occurred during transformation: {e}"
            )
            self.logger.log(
                "error",
                error_message)
            raise Exception(error_message)


class UnifiedConfigLoader:
    """
    Loader to parse a unified configuration file for datasets, readers,
    validators, and transformers.

    This class processes a single configuration file, ensuring that readers,
    validators, and transformers
    are correctly associated with their respective datasets.

    Methods:
        load_config(data_reader: DataReader, **kwargs) -> dict:
            Parses and validates the configuration file, returning a
            structured dictionary.
    """

    def __init__(self):
        self.logger = get_logger()

    def load_config(
        self,
        data_reader: DataReader,
        **kwargs
    ):
        """
        Load and validate the unified configuration file.

        Args:
            data_reader (DataReader): A data reader that provides
                the JSON configuration.
            **kwargs: Additional arguments for the data reader.

        Returns:
            dict: A dictionary containing parsed configurations
                for datasets, readers, validators, transformers, and writers.

        Raises:
            ValueError: If the configuration file is missing required keys
            or has an invalid structure.
        """
        PandasValidationUtils.validate_inheritance(
            data_reader,
            DataReader,
            "data_reader"
        )
        try:
            self.logger.log(
                "info",
                "Loading unified configuration using" +
                " the provided data reader.")
            raw_data = data_reader.read_data(**kwargs)

            if "datasets" not in raw_data:
                error_message = (
                    "Missing 'datasets' key in configuration file."
                )
                self.logger.log(
                    "error",
                    error_message)
                raise ValueError(error_message)

            datasets = []
            for dataset_config in raw_data["datasets"]:
                reader = self._process_reader(dataset_config)
                validators = self._process_section(
                    dataset_config,
                    "validators")
                transformers = self._process_section(
                    dataset_config,
                    "transformers")
                writer = self._process_writer(dataset_config)

                datasets.append({
                    "reader": reader,
                    "validators": validators,
                    "transformers": transformers,
                    "writer": writer
                })

            self.logger.log(
                "info",
                "Unified configuration successfully loaded.")
            return {"datasets": datasets}

        except Exception as e:
            error_message = (
                f"Failed to load unified configuration: {e}"
            )
            self.logger.log(
                "error",
                error_message)
            raise e(error_message)

    def _process_reader(self, dataset_config: dict):
        """
        Validate and extract the reader configuration from the dataset.

        Args:
            dataset_config (dict): Configuration for a specific dataset.

        Returns:
            dict: A dictionary containing the reader configuration.

        Raises:
            ValueError: If the reader section is missing or invalid.
        """
        if "reader" not in dataset_config:
            error_message = (
                "Missing 'reader' key in dataset configuration."
            )
            self.logger.log(
                "error",
                error_message)
            raise ValueError(error_message)

        reader_config = dataset_config["reader"]
        required_keys = [
            "local",
            "cloud",
            "data_type",
            "variable_name"]
        for key in required_keys:
            if key not in reader_config:
                error_message = (
                    f"Missing required key '{key}' in reader configuration."
                )
                self.logger.log(
                    "error",
                    error_message)
                raise ValueError(error_message)

        self.logger.log(
            "info",
            f"Reader configuration processed for file: "
            f"{reader_config['variable_name']}.")
        return reader_config

    def _process_writer(self, dataset_config: dict):
        """
        Validate and extract the writer configuration from the dataset.

        Args:
            dataset_config (dict): Configuration for a specific dataset.

        Returns:
            dict: A dictionary containing the writer configuration.

        Raises:
            ValueError: If the writer section is missing or invalid.
        """
        if "writer" not in dataset_config:
            error_message = (
                "Missing 'writer' key in dataset configuration."
            )
            self.logger.log(
                "error",
                error_message)
            raise ValueError(error_message)

        writer_config = dataset_config["writer"]
        required_keys = ["local", "cloud", "data_type"]
        for key in required_keys:
            if key not in writer_config:
                error_message = (
                    f"Missing required key '{key}' in writer configuration."
                )
                self.logger.log(
                    "error",
                    error_message)
                raise ValueError(error_message)

        self.logger.log(
            "info",
            f"Writer configuration processed for dataset: \
                {dataset_config['reader']['variable_name']}."
        )
        return writer_config

    def _process_section(self, dataset_config: dict, section_name: str):
        """
        Validate and extract a specific section (validators or transformers)
        from the dataset configuration.

        Args:
            dataset_config (dict): Configuration for a specific dataset.
            section_name (str): The name of the section to process
            (e.g., 'validators').

        Returns:
            list: A list of processed configurations for the section.

        Raises:
            ValueError: If the section is missing or has an invalid structure.
        """
        section = dataset_config.get(section_name, [])
        if not isinstance(section, list):
            error_message = (
                f"'{section_name}' must be a list in " +
                "the dataset configuration."
            )
            self.logger.log(
                "error",
                error_message)
            raise ValueError(error_message)

        self.logger.log(
            "info",
            f"Processing {len(section)} entries in the "
            f"'{section_name}' section.")
        return [
            {"type": entry.get("type"),
                "options": {k: v for k, v in entry.items() if k != "type"}}
            for entry in section
        ]


class ConfigValidator:
    """
    Validates configuration for datasets, readers, validators,
    and transformers.

    Methods:
        validate_config(unified_config: dict) -> None:
            Validates the unified configuration dictionary.
    """

    @staticmethod
    def validate_local_config(local_config, variable_name):
        """
        Validates a local configuration.

        Args:
            local_config (dict): Configuration for local datasets.
            variable_name (str): Name of the dataset being validated.

        Raises:
            ValueError: If validation fails.
        """
        if not local_config.get("file_path"):
            raise ValueError(
                f"Dataset '{variable_name}' requires a valid " +
                "'file_path' in local configuration."
            )

    @staticmethod
    def validate_cloud_config(cloud_config, variable_name):
        """
        Validates a cloud configuration.

        Args:
            cloud_config (dict): Configuration for cloud datasets.
            variable_name (str): Name of the dataset being validated.

        Raises:
            ValueError: If validation fails.
        """
        if not cloud_config.get(
            "storage_unit") or not cloud_config.get(
                "object_name"):
            raise ValueError(
                f"Dataset '{variable_name}' requires both " +
                "'storage_unit' and 'object_name' in cloud configuration."
            )

    @staticmethod
    def validate_dataset_config(dataset_config):
        """
        Validates the dataset configuration.

        Args:
            dataset_config (dict): Configuration for the dataset.

        Raises:
            ValueError: If neither 'local' nor 'cloud' config is valid.
        """
        variable_name = dataset_config["reader"]["variable_name"]
        local_config = dataset_config.get("reader", {}).get("local", {})
        cloud_config = dataset_config.get("reader", {}).get("cloud", {})

        if bool(local_config) == bool(cloud_config):  # Both or neither
            raise ValueError(
                f"Dataset '{variable_name}' must specify exactly one of " +
                "'local' or 'cloud' configuration."
            )

        if local_config:
            ConfigValidator.validate_local_config(local_config, variable_name)
        elif cloud_config:
            ConfigValidator.validate_cloud_config(cloud_config, variable_name)

    @staticmethod
    def validate_writer_config(writer_config, variable_name):
        """
        Validates the writer configuration.

        Args:
            writer_config (dict): Configuration for the dataset writer.
            variable_name (str): Name of the dataset being validated.

        Raises:
            ValueError: If neither 'local' nor 'cloud' config is valid.
        """
        local_config = writer_config.get("local", {})
        cloud_config = writer_config.get("cloud", {})

        if bool(local_config) == bool(cloud_config):  # Both or neither
            raise ValueError(
                f"Writer configuration for dataset '{variable_name}' " +
                "must specify exactly one of 'local' or 'cloud'."
            )

        if local_config:
            ConfigValidator.validate_local_config(local_config, variable_name)
        elif cloud_config:
            ConfigValidator.validate_cloud_config(cloud_config, variable_name)
