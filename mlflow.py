import mlflow
import os

def train_mock_model():
    # Udajemy, że trenujemy model
    hyperparam_depth = 5
    model_accuracy = 0.89
    
    # Zapisujemy udawany model do pliku
    with open("dummy_model.txt", "w") as f:
        f.write("To jest nasz super model ML do wykrywania kradziezy")

    print("Rozpoczynam logowanie do MLflow...")
    
    
    with mlflow.start_run():
        mlflow.log_param("max_depth", hyperparam_depth) 
        mlflow.log_metric("accuracy", model_accuracy)
        mlflow.log_artifact("dummy_model.txt")
   
    print("✅ Eksperyment zapisany. Wpisz w terminalu 'mlflow ui', aby zobaczyć wyniki w przeglądarce!")

if __name__ == "__main__":
    # Ustawiamy nazwę eksperymentu
    mlflow.set_experiment("Loss_Prevention_Model_Trials")
    train_mock_model()