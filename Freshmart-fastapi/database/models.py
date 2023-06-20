from tortoise import fields
from tortoise.models import Model
from database.secrets import password_context





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