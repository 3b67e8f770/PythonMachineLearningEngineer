# test_process.py
import pytest
from pyspark.sql import SparkSession
from process_transactions import col_negative

@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder.master("local[1]").appName("pytest").getOrCreate()

def test_col_negative_filters_properly(spark):
    # Tworzymy fałszywe dane: jedna cena dobra (10.0), jedna zła (-5.0)
    data = [("TXN_1", 10.0), ("TXN_2", -5.0)]
    df = spark.createDataFrame(data, ["transaction_id", "price"])
    
    # Uruchamiamy Twoją funkcję
    df_good, df_bad = col_negative(df, "price")
    
    # Sprawdzamy wyniki (powinien zostać 1 dobry i 1 zły rekord)
    assert df_good.count() == 1
    assert df_bad.count() == 1