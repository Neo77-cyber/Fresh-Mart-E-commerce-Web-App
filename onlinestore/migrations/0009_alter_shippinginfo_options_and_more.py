# Generated by Django 4.2.1 on 2023-05-14 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlinestore', '0008_shippinginfo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shippinginfo',
            options={'ordering': ['-date_created']},
        ),
        migrations.RemoveField(
            model_name='shippinginfo',
            name='additional_information',
        ),
        migrations.RemoveField(
            model_name='shippinginfo',
            name='city',
        ),
        migrations.RemoveField(
            model_name='shippinginfo',
            name='delivery_address',
        ),
        migrations.RemoveField(
            model_name='shippinginfo',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='shippinginfo',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='shippinginfo',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='shippinginfo',
            name='state',
        ),
        migrations.AddField(
            model_name='shippinginfo',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='shippinginfo',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='shippinginfo',
            name='ref',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='shippinginfo',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]
