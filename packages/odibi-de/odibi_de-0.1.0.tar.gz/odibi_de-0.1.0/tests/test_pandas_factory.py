import pytest
from odibi_de import PandasReaderFactory
from odibi_de.pandas_engine import (
    PandasCsvReader,
    PandasJsonReader,
    PandasAvroReader,
    PandasParquetReader
)

@pytest.fixture
def factory():
    return PandasReaderFactory()

def test_create_csv_reader(factory):
    reader = factory.csv_reader("fake.csv")
    assert isinstance(reader, PandasCsvReader)

def test_create_json_reader(factory):
    reader = factory.json_reader("fake.json")
    assert isinstance(reader, PandasJsonReader)

def test_create_avro_reader(factory):
    reader = factory.avro_reader("fake.avro")
    assert isinstance(reader, PandasAvroReader)

def test_create_parquet_reader(factory):
    reader = factory.parquet_reader("fake.parquet")
    assert isinstance(reader, PandasParquetReader)
