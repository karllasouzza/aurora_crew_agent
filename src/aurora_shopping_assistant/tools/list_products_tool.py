import asyncio
import aiohttp
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel


class ListProductsInput(BaseModel):
    """Input schema for ListProducts tool."""
    pass


class ListProductsTool(BaseTool):
    name: str = "List Products"
    description: str = (
        "Lists all available products in the store with id, name, price, and stock quantity."
    )
    args_schema: Type[BaseModel] = ListProductsInput

    def _run(self) -> dict:
        return asyncio.run(self._arun())

    async def _arun(self) -> dict:
        """List all products available in the store (async)."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "http://localhost:3333/products",
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.ok:
                        return await response.json()
                    else:
                        text = await response.text()
                        return {"error": f"API Error {response.status}: {text}"}
        except aiohttp.ClientError as e:
            return {"error": f"Request failed: {str(e)}"}


list_products_tool = ListProductsTool()
