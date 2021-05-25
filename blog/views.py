from django.shortcuts import render, redirect
from .forms import NewTicketForm, NewReviewForm
from .models import Ticket, Review
from accounts.models import AppUser

# Create your views here.


def main(request):
    context = {}
    return render(request, "blog/main.html", context)


def add_ticket(request, id_ticket=None):
    ticket_instance = (
        Ticket.objects.get(pk=id_ticket) if id_ticket is not None else None
    )
    if request.method == "GET":
        form = NewTicketForm(instance=ticket_instance)
        return render(request, "blog/add_ticket.html", locals())
    elif request.method == "POST":
        form = NewTicketForm(request.POST)
        if form.is_valid():
            new_ticket = form.save(commit=False)
            new_ticket.user = request.user
            new_ticket.save()
            return redirect("/")


def add_review(request, id_review=None):
    review_instance = (
        Review.objects.get(pk=id_review) if id_review is not None else None
    )
    if request.method == "GET":
        form = NewReviewForm(instance=review_instance)
        return render(request, "blog/add_review.html", locals())
    elif request.method == "POST":
        form = NewReviewForm(request.POST)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.user = request.user
            new_review.save()
            return redirect("/")


def see_all_users(request):
    all_users = AppUser.objects.all()
    context = {"all_users":all_users}
    return render(request, "blog/community.html", context)