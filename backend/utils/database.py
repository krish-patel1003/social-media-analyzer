from astrapy import DataAPIClient
from ..config import settings

async def get_database():
    client = DataAPIClient()
    async_db = client.get_async_database(
        settings.ASTRA_DB_ENDPOINT, 
        token=settings.ASTRA_DB_APPLICATION_TOKEN
    )
    return async_db
