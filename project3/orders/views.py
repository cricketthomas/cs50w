from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import PizzaForm, SubForm, PastaForm, SaladForm, PlatterForm, OrderForm

# import models
from .models import Pizza, Pasta, Salad, Sub, Dinner_platter, Topping_option, Sub_extra, Size_option, Sub_option


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None})
    context = {
        "user": request.user
    }
    return render(request, "orders/user.html", context)


def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "orders/login.html", {"message": "Invalid credentials."})


def logout_view(request):
    logout(request)
    return render(request, "orders/login.html", {"message": "Logged out."})


def register_view(request):
    username = None
    email = None
    password = None
    first_name = None
    last_name = None
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        if User.objects.filter(username=username).exists():
            return render(request, "orders/register.html", {"message": "Username exists."})
        else:
            user = User.objects.create_user(
                username=username, password=password, email=email)
            user.first_name = first_name
            user.last_name = last_name

            user.save()
            user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
            # return render(request, "orders/login.html", {"message": "Invalid credentials."})
    return render(request, "orders/register.html")


def menu_view(request):
    context = {
        "pizzas": Pizza.objects.all(),
        "subs": Sub.objects.all(),
        "pastas": Pasta.objects.all(),
        "salads": Salad.objects.all(),
        "dinner_platters": Dinner_platter.objects.all(),


    }

    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"message": None})
    return render(request, "orders/menu.html", context)


def showform(request):
    pizza_form = PizzaForm(request.POST or None)
    sub_form = SubForm(request.POST or None)
    pasta_form = PastaForm(request.POST or None)
    platter_form = PlatterForm(request.POST or None)
    salad_form = SaladForm(request.POST or None)
    order_form = OrderForm(request.POST or None)

    context = {'PizzaForm': pizza_form,
               'PastaForm': pasta_form,
               'SubForm': sub_form,
               'SaladForm': salad_form,
               'PlatterForm': platter_form,
               'OrderForm': order_form
               }

    if order_form.is_valid():
        order_form.save()

        return render(request, "orders/user.html", {"message": "order form submitted."})
    return render(request, "orders/menu.html", context)
