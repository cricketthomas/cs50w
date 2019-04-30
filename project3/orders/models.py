from django.db import models

# Create your models here.


class Topping_option(models.Model):
    topping = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.topping}"


class Size_option(models.Model):
    size_options = (
        ('Small', 'Small'),
        ('Large', 'Large'),
    )
    size = models.CharField(
        max_length=5, choices=size_options)

    def __str__(self):
        return f"{self.size}"


class Pizza(models.Model):
    selected_topping = models.ManyToManyField(
        Topping_option, blank=True, related_name="toppings")
    selected_size = models.ForeignKey(
        Size_option, on_delete=models.CASCADE, related_name="sizes")
    specialty = models.BooleanField(default=False)

    def __str__(self):
        return f"A pizza: {self.selected_topping}"
