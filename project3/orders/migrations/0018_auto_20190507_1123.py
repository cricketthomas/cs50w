# Generated by Django 2.0.3 on 2019-05-07 15:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0017_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='pasta',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='orders.Pasta'),
        ),
        migrations.AddField(
            model_name='order',
            name='platter',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='orders.Dinner_platter'),
        ),
        migrations.AddField(
            model_name='order',
            name='salad',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='orders.Salad'),
        ),
        migrations.AddField(
            model_name='order',
            name='sub',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='orders.Sub'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='order',
            name='pizza',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='orders.Pizza'),
        ),
    ]