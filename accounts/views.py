from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login as django_login,
    logout as django_logout,
)
from django.contrib.auth.decorators import login_required
from blog.models import *

# Create your views here.


@login_required
def homepage(request):
    user = request.user
    user_tickets = user.ticket_set.all()
    user_reviews = user.review_set.all()
    context = {"user": user, "user_tickets": user_tickets, "user_reviews": user_reviews}
    return render(request, "accounts/homepage.html", context)


@login_required
def logout(request):
    context = {}
    django_logout(request)
    return render(request, "accounts/logout.html", context)


def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get("username")
            messages.success(request, "Account created for " + user)
            return redirect("login")
    context = {"form": form}
    return render(request, "accounts/register.html", context)
