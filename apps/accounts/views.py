from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme
from .forms import RegisterForm

from apps.orders.models import Order, OrderItem

from .forms import (
    LoginForm,
    RegisterForm,
)

from .forms import (
    LoginForm,
    RegisterForm,
    UserUpdateForm,
    ProfileUpdateForm,
)
from .models import UserProfile


def login_view(request):

    next_url = (
        request.POST.get("next")
        or request.GET.get("next")
    )

    if request.method == "POST":

        form = LoginForm(
            request=request,
            data=request.POST,
        )

        if form.is_valid():

            user = form.get_user()

            login(
                request,
                user,
            )

            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={
                    request.get_host(),
                },
                require_https=request.is_secure(),
            ):

                return redirect(
                    next_url,
                )

            return redirect(
                "products:product_list",
            )

    else:

        form = LoginForm()

    return render(
        request,
        "accounts/login.html",
        {
            "form": form,
            "next": next_url,
        },
    )


def register_view(request):

    if request.method == "POST":

        form = RegisterForm(
            request.POST,
        )

        if form.is_valid():

            user = form.save()

            login(
                request,
                user,
            )

            messages.success(
                request,
                "Account created successfully!",
            )

            return redirect(
                "products:product_list",
            )

    else:

        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form,
        },
    )


def logout_view(request):

    logout(
        request,
    )

    return redirect(
        "products:product_list",
    )


@login_required
def dashboard(request):

    orders = (
        Order.objects
        .filter(
            user=request.user,
            status="paid",
        )
        .prefetch_related(
            "items__product",
        )
        .order_by(
            "-created_at",
        )
    )

    context = {

        "orders": orders,

        "total_orders": orders.count(),

    }

    return render(
        request,
        "accounts/dashboard.html",
        context,
    )


@login_required
def downloads_view(request):

    items = (
        OrderItem.objects
        .filter(
            order__user=request.user,
            order__status="paid",
            product__isnull=False,
        )
        .select_related(
            "product",
            "order",
        )
    )

    return render(
        request,
        "accounts/downloads.html",
        {
            "items": items,
        },
    )
    
@login_required
def profile_view(request):

    profile, created = UserProfile.objects.get_or_create(
        user=request.user,
    )

    if request.method == "POST":

        user_form = UserUpdateForm(
            request.POST,
            instance=request.user,
        )

        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=profile,
        )

        if (
            user_form.is_valid()
            and profile_form.is_valid()
        ):

            user_form.save()

            profile_form.save()

            messages.success(
                request,
                "Your profile has been updated successfully.",
            )

            return redirect(
                "accounts:profile",
            )

    else:

        user_form = UserUpdateForm(
            instance=request.user,
        )

        profile_form = ProfileUpdateForm(
            instance=profile,
        )

    return render(
        request,
        "accounts/profile.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
        },
    )