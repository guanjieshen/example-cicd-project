# Databricks notebook source
pip install -r ../requirements.txt

# COMMAND ----------

# MAGIC %load_ext autoreload
# MAGIC %autoreload 2

# COMMAND ----------

from unittest import TestLoader, TestResult

test_loader = TestLoader()
test_result = TestResult()

test_directory = str('unit')

test_suite = test_loader.discover(test_directory, pattern='*_test.py')
test_suite.run(result=test_result)

if test_result.wasSuccessful():
  print("All Unit Tests have passed")
else:
  print(test_result.errors)

