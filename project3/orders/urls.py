from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("accounts/login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("menu", views.menu_view, name="menu"),
    #path("order", views.order, name="order"),
]

# <form action="{% url 'order' pizza.id %}" method="post">
# <select name = "pizzas" >
#   {% for pizza in pizzas % }
#    <option value = "{{ pizza.id }}" > {{pizza}} < /option >
#     {% endfor % }
#  </select >
#   <input type = "submit" value = "Order" />
# </form >
