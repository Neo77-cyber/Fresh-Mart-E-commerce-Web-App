# Generated by Django 4.2.1 on 2023-07-13 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlinestore', '0020_sellonfreshmart'),
    ]

    operations = [
        migrations.AddField(
            model_name='sellonfreshmart',
            name='phone_number',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
    ]
