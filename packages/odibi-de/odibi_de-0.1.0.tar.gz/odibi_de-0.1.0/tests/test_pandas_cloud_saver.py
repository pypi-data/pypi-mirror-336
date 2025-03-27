import pytest
import pandas as pd
from odibi_de import (
    AzureBlobConnector,
    PandasSaverFactory,
    PandasCloudSaverProvider,
    DataType,
)

from odibi_de.pandas_engine import PandasCsvSaver

@pytest.fixture
def df_sample():
    return pd.DataFrame({"name": ["Alice"], "age": [30]})

@pytest.fixture
def saver_provider():
    factory = PandasSaverFactory()
    connector = AzureBlobConnector("testaccount", "testkey")
    return PandasCloudSaverProvider(factory, connector)

def test_cloud_saver_creates_csv_saver(df_sample, saver_provider):
    saver = saver_provider.create_saver(
        data=df_sample,
        storage_unit="mycontainer",  
        object_name="data.csv",      
        data_type=DataType.CSV
    )

    assert isinstance(saver, PandasCsvSaver)
    assert saver.file_path == "az://mycontainer/data.csv"
