# Krok 1: Pobierz oficjalny, czysty obraz systemu z zainstalowanym Pythonem 3.10
FROM python:3.10-slim

# Krok 2: Ustaw folder roboczy wewnątrz kontenera
WORKDIR /app

# Krok 3: Kopiujemy NAJPIERW tylko plik requirements.txt (Wyjaśnienie poniżej)
COPY requirements.txt .

# Krok 4: Instalujemy biblioteki (Wykorzystujemy Docker Cache)
RUN pip install --no-cache-dir \
    --trusted-host pypi.org \
    --trusted-host files.pythonhosted.org \
    -r requirements.txt

# Krok 5: Dopiero teraz kopiujemy resztę kodu aplikacji
COPY app.py /app/app.py
COPY model.py /app/model.py

# Krok 6: Informacja o porcie
EXPOSE 8000

# Krok 7: Komenda startowa (Poprawiony port na końcu!)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]