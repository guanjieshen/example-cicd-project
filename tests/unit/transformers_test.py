from pyspark.sql import DataFrame
from notebooks.utils.transformers import convertTimestampToDate, addETLMetadata
from base import SparkTest
from pyspark.sql.types import *
from datetime import datetime
from chispa.dataframe_comparer import *


class TransformersTests(SparkTest):
    def setUp(self) -> None:
        super().setUp()

    def test_convertTimestampToDate(self):
        """Test conversion of timestamp to date type."""

        expected_schema = StructType(
            [
                StructField("event_ts", DateType()),
                StructField("value_a", FloatType()),
            ]
        )
        expected_data = [
            [datetime(2020, 1, 1), 349.21],
            [datetime(2020, 1, 2), 360.1],
            [datetime(2020, 1, 3), 361.1],
        ]

        expected_df: DataFrame = self.buildDF(expected_data, expected_schema)
        actual_df: DataFrame = convertTimestampToDate(self.test_data, "event_ts")

        assert_df_equality(expected_df, actual_df, ignore_nullable=True)

    def test_addETLMetadata(self):
        """Test addition of ETL metadata"""

        expected_schema = StructType(
            [
                StructField("event_ts", TimestampType()),
                StructField("value_a", FloatType()),
                StructField("__source", StringType()),
                StructField("__processedTime", TimestampType()),
            ]
        )
        expected_data = [
            [
                datetime(year=2020, month=1, day=1, hour=10, minute=10, second=10),
                349.21,
                "test",
                datetime(year=2020, month=1, day=1, hour=10, minute=10, second=10),
            ],
            [
                datetime(year=2020, month=1, day=2, hour=11, minute=11, second=11),
                360.1,
                "test",
                datetime(year=2020, month=1, day=2, hour=11, minute=11, second=11),
            ],
            [
                datetime(year=2020, month=1, day=3, hour=12, minute=12, second=12),
                361.1,
                "test",
                datetime(year=2020, month=1, day=3, hour=12, minute=12, second=12),
            ],
        ]

        expected_df: DataFrame = self.buildDF(expected_data, expected_schema)
        actual_df: DataFrame = addETLMetadata(self.test_data, "test")

        assert_schema_equality(
            expected_df.schema, actual_df.schema, ignore_nullable=True
        )
        assert_df_equality(
            expected_df.drop("__processedTime"),
            actual_df.drop("__processedTime"),
            ignore_nullable=True,
        )
