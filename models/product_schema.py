from pydantic import BaseModel
from typing import Optional


class Product(BaseModel):

    sku: Optional[str] = ""
    name: Optional[str] = ""
    description: Optional[str] = ""
    brand: Optional[str] = ""
    category: Optional[str] = ""
    color: Optional[str] = ""
    size: Optional[str] = ""
    material: Optional[str] = ""
    price: Optional[float] = 0.0
    image_url_1: Optional[str] = ""
    image_url_2: Optional[str] = ""
    image_url_3: Optional[str] = ""