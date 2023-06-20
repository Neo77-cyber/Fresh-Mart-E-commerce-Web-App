from database.schemas import OrderResponse
from database.models import User, Product, Order
from fastapi import APIRouter,Depends, HTTPException
from utils.token import get_user, password_context,oauth2_scheme, authenticate_token
from tortoise.exceptions import DoesNotExist


router = APIRouter(prefix='/Store',
                   tags=['Store'])



@router.post("/shop",
             description = 'Add a product to users cart')
async def shop( product_id: int,token: str = Depends(oauth2_scheme), user: User = Depends(authenticate_token) ):

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


@router.get('/cart/',
            description = 'Retrieves the cart items and products')
async def cart( user: User = Depends(authenticate_token)):
       
        order_items = await Order.filter(user=user).prefetch_related("product")
        subtotal_list = [order_item.product.price * order_item.quantity for order_item in order_items]
        total = sum(subtotal_list)

        return {
            "order_items": order_items,
            "subtotal_list": subtotal_list,
            "total": total
        }
    

@router.put('/update_quantity/{order_id}', response_model=OrderResponse,
            description = 'Update cart item quantity with an ID')
async def update_quantity(order_id: int, quantity: int, user: User = Depends(authenticate_token)):
    
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
    

@router.delete('/delete/{order_id}', 
               description = 'Delete a cart item with an ID ')
async def delete_cart_item(order_id:int, user: User = Depends(authenticate_token)):
        try:
            await Order.filter(user=user, id=order_id).delete()
            return {'messsage': 'order deleted'}
        except DoesNotExist:
            raise HTTPException(status_code=404, detail='Order not found')