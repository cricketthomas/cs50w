# Generated by Django 2.0.3 on 2019-05-02 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0013_auto_20190502_1247'),
    ]

    operations = [
        migrations.CreateModel(
            name='Salad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salads', models.CharField(choices=[('Garden Salad', 'Garden Salad'), ('Greek Salad', 'Greek Salad'), ('Antipasto', 'Antipasto'), ('Salad w/Tuna', 'Salad w/Tuna')], max_length=25)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=4)),
            ],
        ),
    ]
