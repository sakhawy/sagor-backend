# Generated by Django 5.0.1 on 2024-05-07 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sagor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phsensorreading',
            name='value',
            field=models.DecimalField(decimal_places=5, max_digits=10),
        ),
        migrations.AlterField(
            model_name='pumpedfood',
            name='quantity',
            field=models.DecimalField(decimal_places=5, max_digits=10),
        ),
        migrations.AlterField(
            model_name='tempraturesensorreading',
            name='value',
            field=models.DecimalField(decimal_places=5, max_digits=10),
        ),
    ]
