import json

def cache_results(data: dict, filename: str):
    """Salva os dados em um arquivo JSON como cache."""
    with open(filename, 'w') as f:
        json.dump(data, f)

def load_cache(filename: str) -> dict:
    """Carrega os dados de um arquivo JSON se existir."""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
