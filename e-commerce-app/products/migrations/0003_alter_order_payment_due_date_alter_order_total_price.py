# Generated by Django 4.2.6 on 2023-10-10 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_order_payment_due_date_alter_order_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_due_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
