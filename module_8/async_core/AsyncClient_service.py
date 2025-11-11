from httpx import AsyncClient


class AuthorService:
    def __init__(self, base_url: str =  None):
        self.base_url = base_url
        self.client = AsyncClient()

    async def get_data(self):
        response = await self.client.get(self.base_url)
        return response
