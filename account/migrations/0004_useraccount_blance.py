# Generated by Django 5.0.1 on 2024-01-28 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_useraddress_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='blance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
        ),
    ]
