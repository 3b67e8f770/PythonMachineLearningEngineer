#! /usr/bin/env python
import os
from typing import Optional
from pyspark.sql import SparkSession, DataFrame, types
from pyspark.sql import functions as F

def col_null(df_good: DataFrame, col_name: str, df_bad: Optional[DataFrame] = None) -> tuple[DataFrame, DataFrame]:
    if not col_name:
        return df_good, None
    df_to_split = df_good.cache()

    df_temp_bad = df_to_split.filter(F.col(col_name).isNull())
    df_temp_bad = df_temp_bad.withColumn("error_reason",F.lit(f'{col_name} is NULL'))
    df_good_filtered = df_to_split.filter(F.col(col_name).isNotNull())
    print(f'There were {df_temp_bad.F.length(col_name)} NULL rows in {col_name}')
    if df_bad is not None:
        df_bad = df_bad.unionByName(df_temp_bad)
    else:
        df_bad = df_temp_bad
    
    return df_good_filtered, df_bad

def col_negative(df_good: DataFrame, col_name: str, df_bad: Optional[DataFrame] = None) -> tuple[DataFrame, DataFrame]:
    if not col_name:
        return df_good, None
    df_temp_bad = df_good.filter((F.col(col_name) <0) | (F.col(col_name).isNull()) )
    df_temp_bad = df_temp_bad.withColumn("error_reason",F.lit(f'{col_name} - incorrect value'))
    print(f'There were {df_temp_bad.F.length(col_name)} broken rows s in {col_name}')
    df_good = df_good.filter(F.col(col_name)>= 0)
    
    
    if df_bad is not None:
        df_bad = df_bad.unionByName(df_temp_bad)
    else:
        df_bad = df_temp_bad
    return df_good, df_bad

    
def col_val(df_good: DataFrame, col_name: str, values: list, df_bad: Optional[DataFrame] = None) -> tuple[DataFrame, DataFrame]:
    if not col_name:
        return df_good, None
    
    df_temp_bad = df_good.filter(~F.col(col_name).isin(values))
    df_good = df_good.filter(F.col(col_name).isin(values))
    df_temp_bad = df_temp_bad.withColumn("error_reason",F.lit(f'{col_name} not in {values}'))

    if df_bad is not None:
        df_bad = df_bad.unionByName(df_temp_bad)
    else:
        df_bad = df_temp_bad
    return df_good, df_bad

def main():  
    os.environ["HADOOP_HOME"] = r'D:\Python\hadoop'
    os.environ["PATH"] += os.pathsep +os.path.join(os.environ['HADOOP_HOME'], 'bin')

    #2.1 Spark inicialization
    spark = SparkSession.builder.appName("Process_transation").getOrCreate()
    
    #2.2 load data
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
        .option("timestamp") \
        .schema(schema) \
        .load("raw_transactions.csv") 

    
    #.option("sep", ";"): Jeśli Twój plik nie jest rozdzielany przecinkiem, tylko np. średnikiem, musisz to dodać.
    
    #2.3 transaction_id != null
    df_spark, df_bad = col_null(df_spark,"transaction_id")
    
    df_spark, df_bad = col_negative(df_spark, "price", df_bad)
   
    values = ["LDN_01", "MAN_02", "LIV_03"]
    df_spark, df_bad = col_val(df_spark, "store_id", values, df_bad)


    good_path = 'D:/Python/prepering4battle/FRBS/2026_05_11/gold/transactions/'
    df_spark.withColumn("date", F.to_date("timestamp")).write \
    .mode("overwrite") \
    .partitionBy("date") \
    .parquet(good_path)

    bad_path = 'D:/Python/prepering4battle/FRBS/2026_05_11/quarantine/failed_records/'
    df_bad.withColumn("date", F.to_date("timestamp")).write \
    .mode("overwrite") \
    .partitionBy("date") \
    .parquet(bad_path)


if __name__ =="__main__":
    main()

    
