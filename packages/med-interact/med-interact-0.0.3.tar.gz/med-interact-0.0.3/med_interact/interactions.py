from .api_client import fetch_data

def check_interaction(med1: str, med2: str) -> dict:
    """
    Verifica as interações entre dois medicamentos.
    """
    endpoint = "interactions"
    params = {"med1": med1, "med2": med2}
    data = fetch_data(endpoint, params)
    return data
