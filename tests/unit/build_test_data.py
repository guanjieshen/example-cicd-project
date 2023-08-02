from datetime import datetime
from pyspark.sql.types import *
from typing import Tuple


def get_test_data() -> Tuple[StructType, list]:
    schema: StructType = StructType(
        [
            StructField("event_ts", TimestampType()),
            StructField("value_a", FloatType()),
        ]
    )

    data = [
        [datetime(year=2020, month=1, day=1, hour=10, minute=10, second=10), 349.21],
        [datetime(year=2020, month=1, day=2, hour=11, minute=11, second=11), 360.1],
        [datetime(year=2020, month=1, day=3, hour=12, minute=12, second=12), 361.1],
    ]

    return schema, data
