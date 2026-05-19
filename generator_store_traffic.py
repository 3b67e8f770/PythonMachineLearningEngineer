import pandas as pd
import numpy as np

def generate_traffic_data():
    np.random.seed(42)
    dates = pd.date_range(start='2026-05-18 08:00:00', end='2026-05-18 20:00:00', freq='5min')
    
    data = {
        "timestamp": np.random.choice(dates, 500),
        "store_id": np.random.choice(["LDN_01", "MAN_02"], 500),
        "amount": np.random.uniform(5.0, 150.0, 500)
    }
    
    df = pd.DataFrame(data).sort_values(by="timestamp")
    df.to_csv("store_traffic.csv", index=False)
    print("✅ Wygenerowano dane: store_traffic.csv")

if __name__ == "__main__":
    generate_traffic_data()