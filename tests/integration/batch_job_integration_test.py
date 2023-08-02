# Databricks notebook source
# MAGIC %md ##### Install Dependencies

# COMMAND ----------

# MAGIC %pip install nutter

# COMMAND ----------

# MAGIC %md ##### Set up test fixures and run integration test.

# COMMAND ----------

dbutils.widgets.text("database_name", "guanjie_db")
dbutils.widgets.text("table_name", "people10m")
database_name = dbutils.widgets.get("database_name")
table_name = dbutils.widgets.get("table_name")

# COMMAND ----------

from runtime.nutterfixture import NutterFixture, tag


class BatchJobTestFixture(NutterFixture):
    def before_all(self):
        sqlContext.sql(f"CREATE DATABASE IF NOT EXISTS {database_name}_tmp")
        sqlContext.sql(
            f"CREATE OR REPLACE TABLE {database_name}_tmp.{table_name} SHALLOW CLONE {database_name}.{table_name}"
        )

    def run_batch_job_test(self):
        dbutils.notebook.run(
            "../../notebooks/batch_job",
            600,
            {"sink": f"{database_name}_tmp.{table_name}"},
        )

    def assertion_batch_job_test(self):
        some_tbl = sqlContext.sql(
            f"SELECT COUNT(*) AS total FROM {database_name}_tmp.{table_name}"
        )
        first_row = some_tbl.first()
        print(first_row)
        assert first_row[0] > 0

    def after_all(self):
        sqlContext.sql(f"DROP DATABASE {database_name}_tmp CASCADE")


result = BatchJobTestFixture().execute_tests()
print(result.to_string())
# Comment out the next line (result.exit(dbutils)) to see the test result report from within the notebook
# result.exit(dbutils)
# COMMAND ----------
if result.test_results.num_failures > 0:
    raise Exception("Integration tests did not pass.")
