import asyncio
import aiohttp
from crewai.tools import BaseTool
from typing import Type, List
from pydantic import BaseModel, Field


class OrderItemInput(BaseModel):
    """Input schema for order items in Create Order."""
    product_id: str = Field(..., description="Product ID in UUID format")
    quantity: int = Field(..., gt=0, description="Quantity to order (must be positive integer)")


class CreateOrderInput(BaseModel):
    """Input schema for Create Order tool."""
    products: List[OrderItemInput] = Field(
        ...,
        description="List of products to order with productId and quantity"
    )


class CreateOrderTool(BaseTool):
    name: str = "Create Order"
    description: str = (
        "Creates a new purchase order. Receives an array of items with productId and quantity.\n"
        "IMPORTANT: Before calling this tool, verify stock availability by querying the product via GetProduct. "
        "If there is not enough stock, DO NOT call this tool and inform the user about the limitation."
    )
    args_schema: Type[BaseModel] = CreateOrderInput

    def _run(self, products: List[dict]) -> dict:
        return asyncio.run(self._arun(products))

    async def _arun(self, products: List[dict]) -> dict:
        """Create a new order with the specified products (async)."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "http://localhost:3333/orders",
                    headers={"Content-Type": "application/json"},
                    json={"products": products},
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.ok:
                        return await response.json()
                    else:
                        text = await response.text()
                        return {"error": f"Could not create order: {response.status} - {text}"}
        except aiohttp.ClientError as e:
            return {"error": f"Could not create order: {str(e)}"}


create_order_tool = CreateOrderTool()
