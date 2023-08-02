# Databricks notebook source
# MAGIC %md ##### Create Database (if not exists)

# COMMAND ----------

dbutils.widgets.text("database_name", "guanjie_db")
database_name = dbutils.widgets.get("database_name")

# COMMAND ----------

# MAGIC %sql CREATE DATABASE IF NOT EXISTS ${database_name}

# COMMAND ----------


