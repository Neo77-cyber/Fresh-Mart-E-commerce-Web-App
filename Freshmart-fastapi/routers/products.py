from database.schemas import OrderResponse, ProductResponse, OrderCreateResponse, ProductCreateResponse
from database.models import User, Product, Order
from fastapi import APIRouter


router = APIRouter(prefix='/Products',
                   tags=['Products'])



@router.post("/create_products", response_model=ProductResponse,
                                description = 'Create Products and detail')
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


@router.get('/products', response_model=list[ProductResponse],
                            description = 'Retrieves a list of products in the cart')
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