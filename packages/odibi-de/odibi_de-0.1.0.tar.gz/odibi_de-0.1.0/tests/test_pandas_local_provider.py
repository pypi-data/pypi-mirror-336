import pytest
from odibi_de import (
    PandasReaderFactory,
    PandasLocalReaderProvider,
    DataType
)
from odibi_de.pandas_engine import PandasCsvReader

def test_local_provider_creates_csv_reader():
    factory = PandasReaderFactory()
    provider = PandasLocalReaderProvider(factory, DataType.CSV)

    reader = provider.create_reader("local/file.csv")

    assert isinstance(reader, PandasCsvReader)
    assert reader.file_path == "local/file.csv"
