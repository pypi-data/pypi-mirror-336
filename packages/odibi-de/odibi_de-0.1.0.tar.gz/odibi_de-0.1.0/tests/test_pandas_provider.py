import pytest
from odibi_de import (
    PandasReaderFactory,
    PandasCloudReaderProvider,
    AzureBlobConnector,
    DataType,
    Framework
)

def test_provider_creates_csv_reader():
    factory = PandasReaderFactory()
    connector = AzureBlobConnector("testaccount", "testkey")
    provider = PandasCloudReaderProvider(factory, DataType.CSV, connector)

    reader = provider.create_reader("mycontainer", "data.csv")

    assert reader is not None
    assert reader.file_path == "az://mycontainer/data.csv"
