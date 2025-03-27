# odibi_de/__init__.py

# 📦 Pandas classes
from .pandas_engine import (
    PandasReaderFactory,
    PandasCloudReaderProvider,
    PandasLocalReaderProvider,
    PandasSaverFactory,
    PandasCloudSaverProvider,
    PandasLocalSaverProvider,
    PandasDBConnector
)

# 📦 Spark classes
from .spark_engine import (
    SparkReaderFactory,
    SparkCloudReaderProvider,
    SparkLocalReaderProvider,
    SparkStreamReaderFactory,
    SparkCloudStreamReaderProvider,
    SparkLocalStreamReaderProvider,
    SparkSaverFactory,
    SparkCloudSaverProvider,
    SparkLocalSaverProvider,
    SparkStreamSaverFactory,
    SparkCloudStreamSaverProvider,
    SparkLocalStreamSaverProvider,
    SparkDBConnector
)

# ☁️ Cloud connectors
from .azure_cloud_connector import AzureBlobConnector

# 🧠 Core types and enums
from .core_types import (
    DataType,
    CloudService,
    Framework,
    ValidationType,
    TransformerType
)

# 🛠 Utilities
from .utils import (
    get_logger,
    PandasValidationUtils,
    SparkValidationUtils,
    generate_validator_map,
    generate_transformer_map
)

# 📌 Versioning
from .version import __version__

# 🧠 Future abstraction layer (commented for now)
# from .pandas_engine import PandasDataProvider
# from .spark_engine import SparkDataProvider

# 🌍 Explicit export control
__all__ = [
    # Pandas
    "PandasReaderFactory",
    "PandasCloudReaderProvider",
    "PandasLocalReaderProvider",
    "PandasSaverFactory",
    "PandasCloudSaverProvider",
    "PandasLocalSaverProvider",
    "PandasDBConnector",

    # Spark
    "SparkReaderFactory",
    "SparkCloudReaderProvider",
    "SparkLocalReaderProvider",
    "SparkStreamReaderFactory",
    "SparkCloudStreamReaderProvider",
    "SparkLocalStreamReaderProvider",
    "SparkSaverFactory",
    "SparkCloudSaverProvider",
    "SparkLocalSaverProvider",
    "SparkStreamSaverFactory",
    "SparkCloudStreamSaverProvider",
    "SparkLocalStreamSaverProvider",
    "SparkDBConnector",

    # Cloud
    "AzureBlobConnector",

    # Core types
    "DataType",
    "CloudService",
    "Framework",
    "ValidationType",
    "TransformerType",

    # Utilities
    "get_logger",
    "PandasValidationUtils",
    "SparkValidationUtils",
    "generate_validator_map",
    "generate_transformer_map",

    # Version
    "__version__"
]
