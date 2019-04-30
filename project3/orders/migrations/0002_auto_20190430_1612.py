# Generated by Django 2.0.3 on 2019-04-30 20:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pizza',
            name='selected_size',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='sizes', to='orders.Size_option'),
        ),
        migrations.AlterField(
            model_name='size_option',
            name='size',
            field=models.CharField(choices=[('SM', 'Small'), ('LG', 'Large')], max_length=1),
        ),
    ]
