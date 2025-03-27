import requests

API_URL = "https://api.medications.com/v1"  # Exemplo de URL de API

def fetch_data(endpoint: str, params: dict) -> dict:
    """
    Faz uma chamada GET à API externa e retorna os dados como um dicionário.
    """
    response = requests.get(f"{API_URL}/{endpoint}", params=params)
    response.raise_for_status()  # Levanta exceções para status HTTP 4xx/5xx
    return response.json()
