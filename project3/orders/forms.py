from django import forms
from .models import Pizza, Sub, Pasta, Salad, Dinner_platter, Order


class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = ["selected_topping", "selected_size", "specialty"]


class SubForm(forms.ModelForm):
    class Meta:
        model = Sub
        fields = ["sub_options", "sub_sizes", "extras", "extra_cheese"]


class PastaForm(forms.ModelForm):
    class Meta:
        model = Pasta
        fields = ["pastas"]


class SaladForm(forms.ModelForm):
    class Meta:
        model = Salad
        fields = ["salads"]


class PlatterForm(forms.ModelForm):
    class Meta:
        model = Dinner_platter
        fields = ["platter_sizes", "platters"]


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["user", "pizza", "sub", "platter", "salad", "pasta"]
