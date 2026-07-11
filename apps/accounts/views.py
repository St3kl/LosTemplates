from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from apps.orders.models import Order
from apps.orders.models import OrderItem






def login_view(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user:
            login(request, user)

            next_url = (
                request.POST.get("next")
                or request.GET.get("next")
            )

            if next_url:
                return redirect(next_url)

            return redirect("products:product_list")

        messages.error(
            request,
            "Invalid username or password.",
        )

    return render(
        request,
        "accounts/login.html",
    )


def register_view(request):

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Validation
        if not username or not email or not password:
            messages.error(request, "All fields are required.")
            return redirect("register")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        login(request, user)

        messages.success(request, "Account created successfully!")

        return redirect("products:product_list")

    return render(request, "accounts/register.html")

def logout_view(request):

    logout(request)

    return redirect("products:product_list")

@login_required
def dashboard(request):

    orders = (
        Order.objects
        .filter(user=request.user, status="paid")
        .prefetch_related("items__product")
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
    
    
    
@login_required
def downloads_view(request):

    items = (
        OrderItem.objects
        .filter(
            order__user=request.user,
            order__status="paid",
            product__isnull=False
        )
        .select_related("product", "order")
    )

    return render(
        request,
        "accounts/downloads.html",
        {"items": items}
    ) 
# Create your views here.
