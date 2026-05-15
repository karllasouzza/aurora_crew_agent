import requests
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


class GetOrderStatusInput(BaseModel):
    """Input schema for Get Order Status tool."""
    order_id: str = Field(
        ...,
        description="ID of the order in UUID format"
    )


class GetOrderStatusTool(BaseTool):
    name: str = "Get Order Status"
    description: str = (
        "Retrieves the status and items of an existing order by ID. "
        "MUST receive the 'order_id' parameter with the order UUID."
    )
    args_schema: Type[BaseModel] = GetOrderStatusInput

    def _run(self, order_id: str) -> dict:
        """Get order status by Order ID."""
        if not order_id or order_id.strip() == "":
            return {"error": "Parameter 'order_id' is required. Provide the order UUID in the 'order_id' field."}

        try:
            response = requests.get(f"http://localhost:3333/orders/{order_id}", timeout=30)
            if response.ok:
                return response.json()
            elif response.status_code == 404:
                return {"error": f"Order with ID {order_id} not found."}
            else:
                return {"error": f"API Error {response.status_code}: {response.text}"}
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
