#! /usr/bin/env python
import os
from typing import Optional
from pyspark.sql import SparkSession, DataFrame, types
from pyspark.sql import functions as F

os.environ["HADOOP_HOME"] = r'D:\Python\hadoop'
os.environ["PATH"] += os.pathsep +os.path.join(os.environ['HADOOP_HOME'], 'bin')

#2.1 Spark inicialization
spark = SparkSession.builder.appName("Process_transation").getOrCreate()

schema = types.StructType([
    types.StructField("transaction_id", types.StringType(), True),
    types.StructField("store_id", types.StringType(), True),
    types.StructField("product_id", types.IntegerType(), True),
    types.StructField("price", types.DoubleType(), True),
    types.StructField("timestamp",types.TimestampType(), True)
    
    ])
    # dopasuj format do swoich danych       
df_spark = spark.read \
    .format("csv") \
    .option("header", "true") \
    .schema(schema) \
    .load("raw_transactions.csv") 


df_spark = df_spark.withColumn("Error",
    F.when(F.col("transaction_id").isNull(), "transaction_id is Null") \
     .when(F.col("price").isNull(), "price is Null") \
     .when(F.col("price") < 0, "Price was below 0") \
     .otherwise("ok")
)


path_to_good_data = 'D:/Python/prepering4battle/FRBS/2026_05_11/test/'
df_spark.filter(F.col("error") == "ok") \
    .withColumn("date", F.to_date("timestamp")) \
    .drop("error").write \
    .partitionBy("date") \
    .mode("overwrite")  \
    .parquet(path_to_good_data) 
