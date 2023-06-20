from pydantic import BaseModel



class ProductCreateResponse(BaseModel):
    name: str
    price: int
    sales_price: int
    detail: str


class ProductResponse(BaseModel):
    product_id: int
    name: str
    price: int
    sales_price: int
    detail: str


class OrderCreateResponse(BaseModel):
    product_id: int
    quantity: int
    is_ordered: bool


class OrderResponse(BaseModel):
    product_id: int
    user: str
    quantity: int
    is_ordered: bool