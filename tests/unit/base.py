import unittest
import warnings
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.types import *
from build_test_data import get_test_data


class SparkTest(unittest.TestCase):
    #
    # Fixtures
    #
    # Spark Session object
    spark = None
    test_data = None

    @classmethod
    def setUpClass(cls) -> None:
        # create and configure PySpark Session
        cls.spark = (
          SparkSession.builder.appName("unit-tests").master("local").getOrCreate()
        )
        cls.spark.conf.set("spark.sql.shuffle.partitions", "1")
        cls.spark.sparkContext.setLogLevel("ERROR")
        # filter out ResourceWarning messages
        warnings.filterwarnings("ignore", category=ResourceWarning)

    # @classmethod
    # def tearDownClass(cls) -> None:
    #     # shut down Spark
    #     cls.spark.stop()

    def setUp(self) -> None:
        schema, data = get_test_data()
        self.test_data = self.buildDF(data, schema)

    def tearDown(self) -> None:
        del self.test_data

    def buildDF(self, data, schema) -> DataFrame:
        return self.spark.createDataFrame(data, schema)
