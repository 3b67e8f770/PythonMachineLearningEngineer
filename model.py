# model.py
class FraudDetectionModel:
    def __init__(self):
        # Symulacja ładowania wag z pliku
        self.version = "1.0.0"

    def predict(self, amount: float, total_amount: float, moving_avg_3: float) -> float:
        # Bardzo prosta (udawana) logika modelu ML
        risk_score = (amount / moving_avg_3) if moving_avg_3 > 0 else 0
        if total_amount > 1000:
            risk_score += 0.2
        
        # Zwracamy prawdopodobieństwo od 0.0 do 1.0
        return min(max(risk_score * 0.1, 0.0), 1.0)