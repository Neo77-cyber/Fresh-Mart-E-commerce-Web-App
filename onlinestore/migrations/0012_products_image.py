# Generated by Django 4.2.1 on 2023-05-22 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlinestore', '0011_order_is_ordered_delete_shippinginfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='product_images/'),
        ),
    ]
