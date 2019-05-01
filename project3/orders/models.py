from django.db import models

# Create your models here.


class Topping_option(models.Model):
    topping = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.topping}"


class Size_option(models.Model):
    size_options = (
        ('Small Regular', 'Small Regular'),
        ('Large Regular', 'Large Regular'),
        ('Small Sicilian', 'Small Sicilian'),
        ('Large Sicilian', 'Large Sicilian'),
    )
    size = models.CharField(
        max_length=25, choices=size_options)

    def __str__(self):
        return f"{self.size}"


class Pizza(models.Model):
    selected_topping = models.ManyToManyField(
        Topping_option, blank=True, related_name="toppings")
    selected_size = models.ForeignKey(
        Size_option, on_delete=models.CASCADE, related_name="sizes")
    specialty = models.BooleanField(default=False)

    def __str__(self):
        if len(self.selected_topping.all()) >= 1:
            return f"A {self.selected_size} Specialty: {self.specialty}, pizza w/ {self.selected_topping.values_list('topping', flat=True)}"
        else:
            return f"A {self.selected_size} Specialty: {self.specialty}, Cheese pizza."
