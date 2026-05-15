import asyncio
import aiohttp
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


class GetProductInput(BaseModel):
    """Input schema for GetProduct tool."""
    product_id: str = Field(
        ...,
        description="ID of the product in UUID format."
    )


class GetProductTool(BaseTool):
    name: str = "Get Product"
    description: str = (
        "Retrieves details of a specific product by ID. "
        "MUST receive the 'product_id' parameter with the product UUID."
    )
    args_schema: Type[BaseModel] = GetProductInput

    def _run(self, product_id: str) -> dict:
        return asyncio.run(self._arun(product_id))

    async def _arun(self, product_id: str) -> dict:
        """Get a specific product by its ID (async)."""
        if not product_id or product_id.strip() == "":
            return {"error": "Parameter 'product_id' is required. Provide the product UUID in the 'product_id' field."}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"http://localhost:3333/products/{product_id}",
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.ok:
                        return await response.json()
                    elif response.status == 404:
                        return {"error": f"Product with ID {product_id} not found."}
                    else:
                        text = await response.text()
                        return {"error": f"API Error {response.status}: {text}"}
        except aiohttp.ClientError as e:
            return {"error": f"Request failed: {str(e)}"}


get_product_tool = GetProductTool()
