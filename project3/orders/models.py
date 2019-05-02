from django.db import models

# Create your models here.

# Pizzas


class Topping_option(models.Model):
    topping = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.topping}"


class Size_option(models.Model):
    size_options = (
        ('SR', 'Small Regular'),
        ('LR', 'Large Regular'),
        ('SS', 'Small Sicilian'),
        ('LS', 'Large Sicilian'),
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


# Subs

class Sub_extra(models.Model):
    extra = models.CharField(max_length=64)

    def __str__(self):
        return self.extra


class Sub_option(models.Model):
    sub_option = models.CharField(max_length=64)

    def __str__(self):
        return self.sub_option


class Sub(models.Model):
    sub_options = models.ForeignKey(
        Sub_option, on_delete=models.CASCADE, related_name="Sub_options")

    sub_size = (
        ('S', 'Small Sub'),
        ('L', 'Large Sub'),
    )
    sub_sizes = models.CharField(
        max_length=25, choices=sub_size)

    extras = models.ManyToManyField(
        Sub_extra, blank=True, related_name="extras")

    extra_cheese = models.BooleanField(default=False)

    def __str__(self):
        return f"A {self.sub_sizes} size {self.sub_options} Sub Sandwich w/ {self.extras.values_list('extra', flat=True)}"
