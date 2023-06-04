from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.fastapi import register_tortoise
from pydantic import BaseModel
from datetime import datetime
from typing import Dict
from tortoise.exceptions import DoesNotExist

app = FastAPI()

SECRET_KEY = "RsKrje6KrCLwLe5neVGZLVNrQA4ttrYErHjR6X8iSZU"

ACCESS_TOKEN_EXPIRE_MINUTES = 1440

password_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=100)
    password_hash = fields.CharField(max_length=100)

    async def verify_password(self, plain_password):
        return password_context.verify(plain_password, self.password_hash)

    class PydanticMeta:
        exclude = ["password_hash"]

    class Meta:
        table = "user"


class Product(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    price = fields.IntField()
    sales_price = fields.IntField()
    detail = fields.CharField(max_length=100)

    class Meta:
        table = "product"


class Order(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="orders")
    product = fields.ForeignKeyField("models.Product", related_name="orders")
    quantity = fields.IntField(default=1)  
    is_ordered = fields.BooleanField(default=False)  

    class Meta:
        table = "order"


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


register_tortoise(
    app,
    db_url='sqlite:///Users/neo/Documents/Codez/FASTApipractice/ecommercefastapi/database.db',
    modules={'models': ['main']},
    generate_schemas=True,
    add_exception_handlers=True,
)


async def get_user(username: str):
    return await User.get_or_none(username=username)


def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)


def authenticate_user(user: User, password: str):
    if not user or not verify_password(password, user.password_hash):
        return False
    else:
        return user


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post('/register')
async def register(username: str, password: str):
    existing_user = await get_user(username)
    if existing_user:
        raise HTTPException(status_code=400, detail='Username already exists')
    hashed_password = password_context.hash(password)
    user = await User.create(username=username, password_hash=hashed_password)
    return {"message": "Registered successfully"}


@app.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user(form_data.username)
    if not user or not await user.verify_password(form_data.password):
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub": user.username}, access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        user = await get_user(username)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token.")
        return {"message": "Protected route accessed successfully."}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")


@app.post("/token")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user(form_data.username)
    if not user or not await user.verify_password(form_data.password):
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub": user.username}, access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/create_products", response_model=ProductResponse)
async def create_products(new_product: ProductCreateResponse):
    create_product = await Product.create(
        name=new_product.name,
        price=new_product.price,
        sales_price=new_product.sales_price,
        detail=new_product.detail
    )

    response = ProductResponse(
        product_id=create_product.id,
        name=create_product.name,
        price=create_product.price,
        sales_price=create_product.sales_price,
        detail=create_product.detail
    )
    return response


@app.get('/products', response_model=list[ProductResponse])
async def products():
    all_products = await Product.all()
    response = []
    for product in all_products:
        product_response = ProductResponse(
            product_id=product.id,
            name=product.name,
            price=product.price,
            sales_price=product.sales_price,
            detail=product.detail
        )
        response.append(product_response)
    return response


@app.post("/shop")
async def shop(
    product_id: int,
    token: str = Depends(oauth2_scheme)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        user = await get_user(username)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token.")

        product = await Product.get_or_none(id=product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found.")

        order, created = await Order.get_or_create(product=product, user=user)

        response = OrderResponse(
            product_id=product.id,
            user=user.username,
            quantity=order.quantity,
            is_ordered=order.is_ordered
        )
        return response
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")


@app.get('/cart/')
async def cart(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        user = await get_user(username)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token.")
        
        order_items = await Order.filter(user=user).prefetch_related("product")
        subtotal_list = [order_item.product.price * order_item.quantity for order_item in order_items]
        total = sum(subtotal_list)

        return {
            "order_items": order_items,
            "subtotal_list": subtotal_list,
            "total": total
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")

  
@app.put('/update_quantity/{order_id}', response_model=OrderResponse)
async def update_quantity(order_id: int, quantity: int, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        user = await get_user(username)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token.")
        
        order = await Order.get_or_none(id=order_id, user=user)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found.")
        
        order.quantity = quantity
        await order.save()
        
        response = OrderResponse(
            product_id=order.product_id,
            user=user.username,
            quantity=order.quantity,
            is_ordered=order.is_ordered
        )
        
        return response
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")


@app.delete('/delete/{order_id}')
async def delete_cart_item(order_id:int, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        user = await get_user(username)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token.")
        
        try:
            await Order.filter(user=user, id=order_id).delete()
            return {'messsage': 'order deleted'}
        except DoesNotExist:
            raise HTTPException(status_code=404, detail='Order not found')
               
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")
    






