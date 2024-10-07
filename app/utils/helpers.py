import requests
from .environment import EMBEDDINGS_USERNAME, EMBEDDINGS_PASSWORD


def get_embedding_token() -> str:
    login_url = "https://llm.enkai.id.vn/token"
    login_data = {
        "username": EMBEDDINGS_USERNAME,
        "password": EMBEDDINGS_PASSWORD
    }
    login_response = requests.post(login_url, json=login_data)

    if login_response.status_code == 200:
        token = login_response.json().get("access_token")
        return token
    return ValueError(f"Failed to get token from LLM: {login_response.text}")

def generate_embeddings(sentence: str) -> dict[str, list]:
    embeddings_url = "https://llm.enkai.id.vn/embeddings/create/"
    token = get_embedding_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    embeddings_response = requests.post(embeddings_url, headers=headers, json={"sentence": sentence})
    return embeddings_response.json()