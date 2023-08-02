# Databricks notebook source
# MAGIC %md ##### 0. Get Job Parameters

# COMMAND ----------

dbutils.widgets.text(
    "source", "dbfs:/databricks-datasets/learning-spark-v2/people/people-10m.delta"
)
dbutils.widgets.text("sink", "guanjie_db.people10m")

source = dbutils.widgets.get("source")
sink = dbutils.widgets.get("sink")

# COMMAND ----------

# MAGIC %md ##### 1. Read Input Dataset

# COMMAND ----------

df = spark.read.format("delta").load(source)

# COMMAND ----------

display(df)

# COMMAND ----------

# MAGIC %md ##### 2. Apply Transformations

# COMMAND ----------

from utils.transformers import convertTimestampToDate, addETLMetadata


transformed_df = df.transform(
    lambda df: convertTimestampToDate(df, "birthDate")
).transform(lambda df: addETLMetadata(df, source))

# COMMAND ----------

# display(transformed_df)

# COMMAND ----------

print(transformed_df.count())

# COMMAND ----------

# MAGIC %md ##### 3. Write to Data Lake

# COMMAND ----------

transformed_df.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(sink)
