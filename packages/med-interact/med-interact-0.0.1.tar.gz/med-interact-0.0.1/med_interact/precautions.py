from .api_client import fetch_data

def get_precautions(med1: str, med2: str) -> list:
    """
    Retorna precauções ao combinar dois medicamentos.
    """
    endpoint = "precautions"
    params = {"med1": med1, "med2": med2}
    data = fetch_data(endpoint, params)
    return data.get("precautions", [])
