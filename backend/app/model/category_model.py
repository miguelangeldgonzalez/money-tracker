from beanie import Document
from pydantic import Field

class Category(Document):
    name: str = Field(..., description="Category name")

    class Settings:
        name = "category"
