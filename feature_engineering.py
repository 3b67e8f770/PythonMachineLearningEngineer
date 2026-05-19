#!/usr/bin/env python3
from pyspark.sql import functions as F
from pyspark.sql import SparkSession, Window, types
import os

os.environ['HADOOP_HOME'] = r'D:\Python\hadoop'
os.environ["PATH"] += os.pathsep + os.path.join(os.environ['HADOOP_HOME'], 'bin')


def main() -> None:
    spark = SparkSession.builder.appName("feature_engineering").getOrCreate()
    # wczytaj plik
    schema = types.StructType([
        types.StructField("timestamp", types.TimestampType(), True),
        types.StructField("store_id", types.StringType(), True),
        types.StructField("amount", types.DoubleType(), True)

    ])
    df_spark = spark.read \
    .format('csv') \
    .option("header", "true") \
    .schema(schema) \
    .load("store_traffic.csv")

    # Sumę wartości transakcji (amount) dla danego sklepu (store_id), rosnąco po czasie (timestamp).
    wind_sum = Window \
        .partitionBy("store_id") \
        .orderBy("timestamp")
    df_spark = df_spark.withColumn("total amound", F.sum("amount").over(wind_sum))
    
    #Średnia krocząca z 3 ostatnich transakcji: Średnią wartość transakcji (amount) dla danego sklepu, biorąc pod uwagę bieżącą transakcję oraz dwie poprzednie (użyj rowsBetween(-2, 0) w konfiguracji okna).
    window_moving_avg = Window.partitionBy("store_id").orderBy("timestamp").rowsBetween(-2, 0)
    wind_avg = Window \
        .partitionBy("store_id") \
        .orderBy("timestamp") \
        .rowsBetween(-2, 0)
    df_spark = df_spark.withColumn("moving_avg_3", F.avg("amount").over(wind_avg))
    
    #save
    df_spark.withColumn("date", F.to_date("timestamp")) \
    .write.partitionBy("date") \
    .mode("overwrite") \
    .parquet(r'D:\Python\prepering4battle\FRBS\2026_05_11\features_output')

if __name__ == "__main__":
    main()