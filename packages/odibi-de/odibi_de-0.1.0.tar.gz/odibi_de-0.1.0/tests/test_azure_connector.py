import pytest
from odibi_de import AzureBlobConnector, Framework 
def test_connector_initialization():
    connector = AzureBlobConnector("fakeaccount", "fakekey")
    assert connector.account_name == "fakeaccount"
    assert connector.account_key == "fakekey"

def test_get_file_path_returns_correct_url():
    connector = AzureBlobConnector("fakeaccount", "fakekey")
    blob_url = connector.get_file_path("mycontainer", "data/file.csv", Framework.PANDAS.value)

    expected = "az://mycontainer/data/file.csv"
    assert blob_url == expected
