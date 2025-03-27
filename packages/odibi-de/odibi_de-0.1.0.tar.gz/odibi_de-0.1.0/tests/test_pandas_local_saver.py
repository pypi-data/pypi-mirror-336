import pytest
import pandas as pd
from odibi_de import (
    PandasLocalSaverProvider,
    PandasSaverFactory,
    DataType
)
from odibi_de.pandas_engine import PandasCsvSaver

@pytest.fixture
def df_sample():
    return pd.DataFrame({"name": ["Alice"], "age": [30]})

@pytest.fixture
def saver_provider():
    factory = PandasSaverFactory()
    return PandasLocalSaverProvider(factory)  # ✅ fixed

def test_local_saver_creates_csv_saver(saver_provider, df_sample):
    saver = saver_provider.create_saver(df_sample, "test_output.csv", DataType.CSV)
    assert isinstance(saver, PandasCsvSaver)
    assert saver.file_path  == "test_output.csv"

def test_local_saver_can_save_csv(tmp_path, saver_provider, df_sample):
    output_file = tmp_path / "output.csv"
    saver = saver_provider.create_saver(df_sample, str(output_file), DataType.CSV)
    saver.save_data(index=False)

    assert output_file.exists()

    # Validate content
    df_loaded = pd.read_csv(output_file)
    assert df_loaded.equals(df_sample)
