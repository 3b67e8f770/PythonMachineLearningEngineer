#!/usr/bin/env python
import pandas as pd
import numpy as np

def generate_mock_data(filename="raw_transactions.csv"):
    data = {
        "transaction_id": [f"TXN_{i}" for i in range(100)],
        "store_id": np.random.choice(["LDN_01", "MAN_02", "LIV_03"], 100),
        "product_id": np.random.randint(1000, 1100, 100),
        "price": np.random.uniform(0.5, 50.0, 100),
        "timestamp": pd.date_range(start='2024-01-01', periods=100, freq='h')
    }
    df = pd.DataFrame(data)
    
    # Wprowadzanie błędów (Data Quality issues)
    df.loc[0:5, "price"] = -10.0  # Ujemna cena
    df.loc[10:15, "transaction_id"] = None  # Brakujące ID
    df.loc[20:22, "price"] = np.nan  # Null w cenie
    
    df.to_csv(filename, index=False)
    print(f"✅ Wygenerowano dane: {filename}")

if __name__ == "__main__":
    generate_mock_data()