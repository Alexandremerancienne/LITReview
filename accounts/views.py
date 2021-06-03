from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import (
    logout as django_logout,
)
from django.contrib.auth.decorators import login_required
from itertools import chain
from django.db.models import CharField, Value
from blog.models import *


# Create your views here.

@login_required
def homepage(request):
    user = request.user
    user_tickets = user.ticket_set.all()
    tickets = user_tickets.annotate(content_type=Value('TICKET', CharField()))
    user_reviews = user.review_set.all()
    reviews = user_reviews.annotate(content_type=Value('REVIEW', CharField()))
    user_responses = Review.objects.filter(ticket__in=tickets)
    responses = user_responses.annotate(content_type=Value('RESPONSE', CharField()))
    followed_users = [relation.followed_user for relation in UserFollows.objects.filter(user=request.user)]
    followed_tickets_list = [ticket for ticket in Ticket.objects.filter(user__in=followed_users)]
    reviews_tickets_list = [review.ticket for review in Review.objects.all()]

    answered_tickets_list = [ticket for ticket in followed_tickets_list if ticket in reviews_tickets_list]
    followed_answered_tickets = Ticket.objects.filter(title__in=answered_tickets_list)
    answered_tickets = followed_answered_tickets.annotate(content_type=Value('ANSWERED_TICKET', CharField()))

    my_unanswered_tickets = [ticket for ticket in user_tickets if ticket not in reviews_tickets_list]
    unanswered_followed_tickets = [ticket for ticket in followed_tickets_list if ticket not in reviews_tickets_list]
    unanswered_followed_tickets.extend(my_unanswered_tickets)
    followed_unanswered_tickets = Ticket.objects.filter(title__in=unanswered_followed_tickets)
    unanswered_tickets = followed_unanswered_tickets.annotate(content_type=Value('UNANSWERED_TICKET', CharField()))

    followed_users_reviews = Review.objects.filter(user__in=followed_users)
    followed_reviews = followed_users_reviews.annotate(content_type=Value('FOLLOWED_REVIEW', CharField()))
    posts = sorted(
        chain(reviews, tickets, responses, unanswered_tickets, answered_tickets, followed_reviews),
        key=lambda post: post.time_created,
        reverse=True
    )
    context = {"user": user, "posts": posts, "responses": responses, "unanswered_tickets": unanswered_tickets,
               "answered_tickets": answered_tickets, "followed_reviews": followed_reviews}
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






