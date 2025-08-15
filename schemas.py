from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    price: int
    stock: int

class ProductOut(ProductBase):
    id: int
    class Config:
        orm_mode = True

class OrderCreate(BaseModel):
    product_id: int
    quantity: int

class OrderOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    status: str
    class Config:
        orm_mode = True
