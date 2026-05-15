import requests
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
        """Get a specific product by its ID."""
        if not product_id or product_id.strip() == "":
            return {"error": "Parameter 'product_id' is required. Provide the product UUID in the 'product_id' field."}

        try:
            response = requests.get(f"http://localhost:3333/products/{product_id}", timeout=30)
            if response.ok:
                return response.json()
            elif response.status_code == 404:
                return {"error": f"Product with ID {product_id} not found."}
            else:
                return {"error": f"API Error {response.status_code}: {response.text}"}
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
