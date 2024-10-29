from dotenv import load_dotenv
import os

load_dotenv()

ASTRADB_APPLICATION_TOKEB = os.getenv("ASTRADB_APPLICATION_TOKEB")
ASTRADB_API_URL = os.getenv("ASTRADB_API_URL")
astradb_collection_name = 'questions'
POSTGRES_DATABASE_URL = os.getenv("POSTGRES_DATABASE_URL")
EMBEDDINGS_TOKENS=os.getenv("EMBEDDINGS_TOKENS")
EMBEDDINGS_USERNAME=EMBEDDINGS_TOKENS.split(":")[0]
EMBEDDINGS_PASSWORD=EMBEDDINGS_TOKENS.split(":")[1]
viewd_id = []

