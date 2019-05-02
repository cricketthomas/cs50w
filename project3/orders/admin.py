from django.contrib import admin

from .models import Pizza, Topping_option, Size_option, Sub, Sub_extra, Sub_option, Pasta, Salad, Dinner_platter


# Register your models here.

admin.site.register(Pizza)
admin.site.register(Sub)
admin.site.register(Pasta)
admin.site.register(Salad)

admin.site.register(Sub_option)
admin.site.register(Sub_extra)
admin.site.register(Topping_option)
admin.site.register(Size_option)
admin.site.register(Dinner_platter)
