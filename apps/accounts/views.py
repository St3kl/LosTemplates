from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from apps.orders.models import Order


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect("product_list")

    return render(request, "accounts/login.html")


def register_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        if not User.objects.filter(username=username).exists():

            user = User.objects.create_user(
                username=username,
                password=password
            )

            login(request, user)
            return redirect("product_list")

    return render(request, "accounts/register.html")

def logout_view(request):

    logout(request)

    return redirect("product_list")

@login_required
def dashboard(request):

    orders = (
        Order.objects
        .filter(user=request.user, paid=True)
        .select_related("product")
        .order_by("-created_at")
    )

    context = {
        "orders": orders,
        "total_orders": orders.count(),
    }

    return render(
        request,
        "accounts/dashboard.html",
        context
    )
# Create your views here.
