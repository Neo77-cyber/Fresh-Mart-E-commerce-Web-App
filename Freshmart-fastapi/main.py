from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from routers import users, products, shop

app = FastAPI(
    description='A simple E-commerce project that displays product catalogue, cart management and a responsive system for users to process orders '
)


app.include_router(users.router)
app.include_router(products.router)
app.include_router(shop.router)






register_tortoise(
    app,
    db_url='sqlite:///Users/neo/Documents/Codez/FASTApipractice/ecommercefastapi/database.db',
    modules={'models': ['database.models']},
    generate_schemas=True,
    add_exception_handlers=True,
)












    


               
    
    






