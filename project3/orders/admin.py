from django.contrib import admin

from .models import Pizza, Topping_option, Size_option

# Register your models here.
admin.site.register(Topping_option)
admin.site.register(Size_option)
admin.site.register(Pizza)
