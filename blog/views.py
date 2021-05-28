from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewTicketForm, NewReviewForm, FollowUserForm, SearchUserForm
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


def see_users(request):
    users = AppUser.objects.all().order_by("username")
    users_names = [user.username for user in users]
    relations = UserFollows.objects.filter(user=request.user)
    relations_users = [relation.followed_user.username for relation in relations]
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
    if request.method == "POST":
        relation = UserFollows.objects.filter(
            user=request.user, followed_user=followed_user
        )
        relation.delete()
        return redirect("/community/")
    context = {"followed_user": followed_user}
    return render(request, "blog/unfollow_user.html", context)
