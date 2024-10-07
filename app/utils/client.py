from astrapy import DataAPIClient
from .environment import ASTRADB_API_URL, ASTRADB_APPLICATION_TOKEB, astradb_collection_name
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from .environment import POSTGRES_DATABASE_URL
from sqlalchemy.orm import sessionmaker

# Initialize the client
client = DataAPIClient(ASTRADB_APPLICATION_TOKEB)
astra_db = client.get_database_by_api_endpoint(ASTRADB_API_URL)

astra_client = astra_db.get_collection(astradb_collection_name)



postgres_client = create_async_engine(POSTGRES_DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=postgres_client,
    class_=AsyncSession,
    expire_on_commit=False,
)

