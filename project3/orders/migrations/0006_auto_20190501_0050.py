# Generated by Django 2.2 on 2019-05-01 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_pizza_specialty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='size_option',
            name='size',
            field=models.CharField(choices=[('Small Regular', 'Small Regular'), ('Small Sicilian', 'Small Sicilian'), ('Large Regular', 'Large Regular'), ('Large Sicilian', 'Large Sicilian')], max_length=5),
        ),
    ]
