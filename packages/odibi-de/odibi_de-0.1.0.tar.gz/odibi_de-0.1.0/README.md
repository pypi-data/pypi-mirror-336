# odibi_de

Odibi’s personal data engineering framework for scalable, modular, and testable data pipelines using **Pandas**, **Spark**, and **Azure**.

---

## 🚀 Features

- 🔄 Readers & Savers for Pandas and Spark
- ☁️ Supports both Cloud (Azure Blob Storage) and Local file systems
- 📦 Built-in connectors for blob storage and SQL databases
- 📊 Handles CSV, JSON, Parquet, Avro, and Delta formats
- 🧱 Structured using SOLID principles and extensible factory patterns
- 🧠 Validations, transformations, and logging included (optional to use)

---

## 📦 Installation

Clone the repo and install locally in **editable mode**:

```bash
git clone https://github.com/your-username/odibi_de_project.git
cd odibi_de_project
pip install -e .

```
## 🛠️ Usage

### ✅ Reading Local CSV File with Pandas

```python
from odibi_de import PandasReaderFactory, DataType

factory = PandasReaderFactory()
reader = factory.csv_reader("data.csv")
df = reader.read_data()

```
### ☁️ Reading JSON from Azure Blob with Spark
```python
from pyspark.sql import SparkSession
from odibi_de import AzureBlobConnector, SparkReaderFactory, SparkCloudReaderProvider, DataType

spark = SparkSession.builder.appName("MyApp").getOrCreate()

connector = AzureBlobConnector("myaccount", "mykey")
factory = SparkReaderFactory()

provider = SparkCloudReaderProvider(factory, DataType.JSON, connector, spark)
reader = provider.create_reader("my-container", "path/to/data.json")
df = reader.read_data()
df.show()
```

### 💾 Saving to Azure Blob Storage with Pandas

```python
from odibi_de import AzureBlobConnector, PandasSaverFactory, PandasCloudSaverProvider, DataType
import pandas as pd

data = pd.DataFrame({"name": ["Alice"], "age": [30]})
connector = AzureBlobConnector("myaccount", "mykey")
factory = PandasSaverFactory()
provider = PandasCloudSaverProvider(factory, connector)

saver = provider.create_saver(data, "my-container", "output.json", DataType.JSON)
saver.save_data(index=False)
```
### ☁️ Reading JSON from Azure Blob with Spark
```python
from pyspark.sql import SparkSession
from odibi_de import AzureBlobConnector, SparkReaderFactory, SparkCloudReaderProvider, DataType

spark = SparkSession.builder.appName("MyApp").getOrCreate()

connector = AzureBlobConnector("myaccount", "mykey")
factory = SparkReaderFactory()

provider = SparkCloudReaderProvider(factory, DataType.JSON, connector, spark)
reader = provider.create_reader("my-container", "path/to/data.json")
df = reader.read_data()
df.show()

```

## 📁 Project Structure
odibi_de_project/
│
├── odibi_de/
│   ├── __init__.py
│   ├── pandas_engine.py
│   ├── spark_engine.py
│   ├── core_types.py
│   ├── ...
│
├── tests/
│   ├── test_pandas_factory.py
│   ├── test_azure_connector.py
│   └── ...
│
├── setup.py
├── README.md
└── requirements.txt (optional)


## 🧭 Future Plans
- 📚 Add full documentation using Sphinx or Docusaurus

- 🌩️ Add support for AWS S3 and Google Cloud Storage

- ⚙️ CLI interface for quick ingestion and transformation jobs

- 🧬 Library of pre-built transformations and schema validators

- ✅ Optional integration with Great Expectations or similar tools

## 🙌 Acknowledgments
Created and maintained by Henry Odibi to empower data engineers and analysts with scalable, clean, and modular tooling.
    "Do it right, and do it every day." 💪