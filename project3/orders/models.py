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
        max_length=64, choices=size_options)

    def __str__(self):
        return f"{self.size}"


class Pizza(models.Model):
    selected_topping = models.ManyToManyField(
        Topping_option, blank=True, related_name="toppings")
    selected_size = models.ForeignKey(
        Size_option, on_delete=models.CASCADE, related_name="sizes")
    specialty = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=4, decimal_places=2, default=0)

    def __str__(self):

        if len(self.selected_topping.all()) >= 1:
            return f"A {self.selected_size} Specialty: {self.specialty}, pizza w/ {self.selected_topping.values_list('topping', flat=True)} {self.price}"
        else:
            return f"A {self.selected_size} Specialty: {self.specialty}, Cheese pizza. {self.price}"


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
    price = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    sub_size = (
        ('Small', 'Small Sub'),
        ('Large', 'Large Sub'),
    )
    sub_sizes = models.CharField(
        max_length=64, choices=sub_size)

    extras = models.ManyToManyField(
        Sub_extra, blank=True, related_name="extras")

    extra_cheese = models.BooleanField(default=False)

    def __str__(self):
        return f"A {self.sub_sizes} size {self.sub_options} Sub Sandwich w/ {self.extras.values_list('extra', flat=True)} {self.price}"


# Pasta
class Pasta(models.Model):
    pasta_option = (
        ('Mozzarella', 'Mozzarella'),
        ('Meatballs', 'Meatballs'),
        ('Chicken', 'Chicken'),
    )
    pastas = models.CharField(
        max_length=64, choices=pasta_option)
    price = models.DecimalField(max_digits=4, decimal_places=2, default=0)

    def __str__(self):
        return f"Baked Ziti w/ {self.pastas} {self.price}"


# Salad
class Salad(models.Model):
    salad_option = (
        ('Garden Salad', 'Garden Salad'),
        ('Greek Salad', 'Greek Salad'),
        ('Antipasto', 'Antipasto'),
        ('Salad w/Tuna', 'Salad w/Tuna'),
    )
    salads = models.CharField(
        max_length=64, choices=salad_option)
    price = models.DecimalField(max_digits=4, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.salads} {self.price}"

# Dinner platter
class Dinner_platter(models.Model):
    platter_size = (
        ('Small', 'Small'),
        ('Large', 'Large'),
    )
    platter_sizes = models.CharField(
        max_length=64, choices=platter_size)
    platters = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=4, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.platter_sizes} {self.platters} {self.price}"


# I need an orders model, 
# i might need to refractor the models, have a price for the toppings, sizes and options tracking strategy 
# then something to limit the topping unless its special pizza.