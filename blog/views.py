import operator

from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewTicketForm, NewReviewForm, SearchUserForm
from .models import Ticket, Review, UserFollows
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
        context = {"form": form}
        return render(request, "blog/add_ticket.html", context)
    elif request.method == "POST":
        form = NewTicketForm(request.POST, request.FILES)
        if form.is_valid():
            new_ticket = form.save(commit=False)
            new_ticket.user = request.user
            new_ticket.save()
            return redirect("/")


def add_review(request, id_review=None, id_ticket=None):
    review_instance = (
        Review.objects.get(pk=id_review) if id_review is not None else None
    )
    ticket_instance = (
        Ticket.objects.get(pk=id_ticket) if id_ticket is not None else None
    )
    if request.method == "GET":
        form = NewReviewForm(
            instance=review_instance, initial={"ticket": ticket_instance}
        )
        context = {"form": form}
        return render(request, "blog/add_review.html", context)
    elif request.method == "POST":
        form = NewReviewForm(request.POST, initial={"ticket": ticket_instance})
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.user = request.user
            new_review.save()
            return redirect("/")


def see_users(request):
    users = AppUser.objects.all().order_by("username")
    users_names = [user.username for user in users]
    relations = UserFollows.objects.filter(user=request.user)
    relations_users = [relation.followed_user.username
                       for relation in relations]
    form = SearchUserForm()
    if request.method == "POST":
        form = SearchUserForm(request.POST)
        followed_name = request.POST["user_name"]
        if followed_name == request.user.username:
            return redirect("/community/")
        elif relations_users.count(followed_name) > 0:
            return redirect("/community/")
        elif users_names.count(followed_name) == 0:
            return redirect("/community/")
        if form.is_valid():
            new_relation = UserFollows()
            new_relation.user = request.user
            followed_user = AppUser.objects.get(username=followed_name)
            new_relation.followed_user = followed_user
            new_relation.save()
    new_relations = UserFollows.objects.filter(user=request.user).order_by(
        "followed_user"
    )
    context = {"users": users, "form": form, "new_relations": new_relations}
    return render(request, "blog/community.html", context)


def unfollow_user(request, id_user):
    followed_user = get_object_or_404(AppUser, id=id_user)
    context = {"followed_user": followed_user}
    return render(request, "blog/unfollow_user.html", context)


def confirm_unfollow(request, id_user):
    followed_user = get_object_or_404(AppUser, id=id_user)
    relation = UserFollows.objects.filter(
        user=request.user, followed_user=followed_user
    )
    relation.delete()
    return redirect("/community/")


def edit_publications(request):
    context = {}
    return render(request, "blog/edit_publications.html", context)


def edit_reviews(request):
    user = request.user
    user_reviews = user.review_set.all()
    ordered_reviews = sorted(user_reviews,
                             key=operator.attrgetter('time_created'),
                             reverse=True)
    context = {"user": user, "user_reviews": ordered_reviews}
    return render(request, "blog/edit_reviews.html", context)


def edit_tickets(request):
    user = request.user
    user_tickets = user.ticket_set.all()
    user_reviews = user.review_set.all()
    user_reviews_tickets = [review.ticket for review in user_reviews]
    answered_tickets = [
        ticket for ticket in user_tickets
        if ticket in user_reviews_tickets
    ]
    uncommented_user_tickets = user_tickets.exclude(title__in=answered_tickets)
    commented_user_tickets = user_tickets.filter(title__in=answered_tickets)
    ordered_tickets = sorted(user_tickets,
                             key=operator.attrgetter('time_created'),
                             reverse=True)
    context = {"user": user, "user_tickets": ordered_tickets,
               "uncommented_tickets": uncommented_user_tickets,
               "commented_tickets": commented_user_tickets}
    return render(request, "blog/edit_tickets.html", context)


def delete_review(request, id_review):
    review = get_object_or_404(Review, id=id_review)
    context = {"review": review}
    return render(request, "blog/delete_review.html", context)


def confirm_delete_review(request, id_review):
    review = get_object_or_404(Review, id=id_review)
    review.delete()
    return redirect("/edit_reviews/")


def delete_ticket(request, id_ticket):
    ticket = get_object_or_404(Ticket, id=id_ticket)
    context = {"ticket": ticket}
    return render(request, "blog/delete_ticket.html", context)


def confirm_delete_ticket(request, id_ticket):
    ticket = get_object_or_404(Ticket, id=id_ticket)
    ticket.delete()
    return redirect("/edit_tickets/")


def edit_ticket(request, id_ticket):
    instance_ticket = get_object_or_404(Ticket, id=id_ticket)
    form = NewTicketForm(instance=instance_ticket)
    if request.method == "POST":
        form = NewTicketForm(request.POST, request.FILES,
                             instance=instance_ticket)
        if form.is_valid():
            edited_ticket = form.save(commit=False)
            edited_ticket.user = request.user
            edited_ticket.save()
            return redirect("/edit_tickets/")
    context = {"form": form}
    return render(request, "blog/edit_ticket.html", context)


def edit_review(request, id_review):
    instance_review = get_object_or_404(Review, id=id_review)
    form = NewReviewForm(instance=instance_review)
    if request.method == "POST":
        form = NewReviewForm(request.POST, instance=instance_review)
        if form.is_valid():
            edited_review = form.save(commit=False)
            edited_review.user = request.user
            edited_review.save()
            return redirect("/edit_reviews/")
    context = {"form": form}
    return render(request, "blog/edit_review.html", context)
