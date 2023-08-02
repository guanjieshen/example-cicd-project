import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import *


# Convert Timestamp Column to Date
def convertTimestampToDate(df, timestamp_col_name):
    return df.withColumn(timestamp_col_name, to_date(timestamp_col_name))


# Add ETL related metadata
def addETLMetadata(df, source):
    out_df = df.withColumn("__source", lit(source)).withColumn(
        "__processedTime", current_timestamp()
    )
    return out_df
