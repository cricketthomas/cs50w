# Generated by Django 2.0.3 on 2019-04-30 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20190430_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='size_option',
            name='size',
            field=models.CharField(choices=[('Small', 'Small'), ('Large', 'Large')], max_length=5),
        ),
    ]