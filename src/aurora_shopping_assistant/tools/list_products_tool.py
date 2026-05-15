import requests
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
        """List all products available in the store."""
        try:
            response = requests.get("http://localhost:3333/products", timeout=30)
            if response.ok:
                return response.json()
            else:
                return {"error": f"API Error {response.status_code}: {response.text}"}
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
