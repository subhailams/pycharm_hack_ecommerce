# Generated by Django 2.2.8 on 2020-08-24 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0008_auto_20200824_2128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='isordered',
            field=models.BooleanField(default=False),
        ),
    ]
