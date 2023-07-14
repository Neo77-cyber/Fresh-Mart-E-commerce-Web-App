# Generated by Django 4.2.1 on 2023-07-07 09:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('onlinestore', '0008_remove_order_is_ordered_orderitem_is_ordered'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompletedOrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('is_ordered', models.BooleanField(default=False)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onlinestore.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onlinestore.products')),
            ],
        ),
    ]