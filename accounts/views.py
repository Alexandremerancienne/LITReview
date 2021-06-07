from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import (
    logout as django_logout,
)
from django.contrib.auth.decorators import login_required
from itertools import chain
from django.db.models import CharField, Value
from blog.models import Review, Ticket, UserFollows


# Create your views here.


@login_required
def homepage(request):
    user = request.user
    user_tickets = user.ticket_set.all()
    user_reviews = user.review_set.all()
    reviews = user_reviews.annotate(content_type=Value("REVIEW", CharField()))
    user_responses = Review.objects.filter(ticket__in=user_tickets)
    responses = user_responses.annotate(content_type=Value("RESPONSE",
                                                           CharField()))
    followed_users = [
        relation.followed_user
        for relation in UserFollows.objects.filter(user=request.user)
    ]
    followed_tickets = [
        ticket for ticket in Ticket.objects.filter(user__in=followed_users)
    ]
    reviews_tickets = [review.ticket for review in Review.objects.all()]
    user_unanswered = [
        ticket for ticket in user_tickets if ticket not in reviews_tickets
    ]
    unanswered_followed = [
        ticket for ticket in followed_tickets
        if ticket not in reviews_tickets
    ]
    unanswered_followed.extend(user_unanswered)
    unanswered_followed_tickets = Ticket.objects.filter(
        title__in=unanswered_followed
    )
    unanswered = unanswered_followed_tickets.annotate(
        content_type=Value("UNANSWERED_TICKET", CharField())
    )
    new_user_tickets = user_tickets.exclude(title__in=user_unanswered)
    tickets = new_user_tickets.annotate(content_type=Value("TICKET",
                                                           CharField()))


    user_reviews_tickets = [review.ticket for review in user_reviews]
    answered_tickets = [
        ticket for ticket in followed_tickets
        if ticket in user_reviews_tickets
    ]
    followed_answered = Ticket.objects.filter(title__in=answered_tickets)
    answered = followed_answered.annotate(
        content_type=Value("ANSWERED_TICKET", CharField())
    )





    followed_users_reviews = Review.objects.filter(user__in=followed_users)
    followed_reviews = followed_users_reviews.annotate(
        content_type=Value("FOLLOWED_REVIEW", CharField())
    )
    posts = sorted(
        chain(
            reviews,
            tickets,
            responses,
            unanswered,
            answered,
            followed_reviews,
        ),
        key=lambda post: post.time_created,
        reverse=True,
    )
    context = {
        "user": user,
        "posts": posts,
        "responses": responses,
        "unanswered_tickets": unanswered,
        "answered_tickets": answered,
        "followed_reviews": followed_reviews,
    }
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
