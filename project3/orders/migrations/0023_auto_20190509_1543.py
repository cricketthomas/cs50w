# Generated by Django 2.0.3 on 2019-05-09 19:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0022_auto_20190509_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='platter',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='orders.Dinner_platter'),
        ),
    ]