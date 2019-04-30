from django.db import models

# Create your models here.


class Topping_option(models.Model):
    topping = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.topping}"


class Size_option(models.Model):
    size_options = (
        ('SM', 'Small'),
        ('LG', 'Large'),
    )
    size = models.CharField(max_length=1, choices=size_options, default=None)

    def __str__(self):
        return f"{self.size}"


class Pizza(models.Model):
    selected_topping = models.ManyToManyField(
        Topping_option, blank=True, related_name="toppings")

    def __str__(self):
        return f"A pizza: {self.selected_topping}"
