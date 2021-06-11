import operator

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewTicketForm, NewReviewForm, SearchUserForm
from .forms import CreateReviewForm
from .models import Ticket, Review, UserFollows
from accounts.models import AppUser
from itertools import chain
from django.db.models import CharField, Value


@login_required
def main(request):

    """A function to render the main page"""

    context = {}
    return render(request, "blog/main.html", context)


@login_required
def add_ticket(request, id_ticket=None):

    """A function to create a ticket"""

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


@login_required
def choose_review(request):

    """A function to choose
    between the following options:

    - Create a ticket and a review answering to it;
    - Answer to an existing ticket"""

    context = {}
    return render(request, "blog/choose_review.html", context)


@login_required
def add_review(request, id_review=None, id_ticket=None):

    """A function to add a review
    in response to an existing ticket"""

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
        context = {"form": form, "ticket": ticket_instance}
        return render(request, "blog/add_review.html", context)
    elif request.method == "POST":
        form = NewReviewForm(request.POST, initial={"ticket": ticket_instance})
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.user = request.user
            new_review.save()
            return redirect("/")


@login_required
def see_users(request):

    """A function to:

    - See all the users of LITReview website;
    - Follow new users"""

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
            return redirect("/community/")
    new_relations = UserFollows.objects.filter(user=request.user).order_by(
        "followed_user"
    )
    context = {"users": users, "form": form, "new_relations": new_relations}
    return render(request, "blog/community.html", context)


@login_required
def unfollow_user(request, id_user):

    """A function to send request to unfollow a user"""

    followed_user = get_object_or_404(AppUser, id=id_user)
    context = {"followed_user": followed_user}
    return render(request, "blog/unfollow_user.html", context)


@login_required
def confirm_unfollow(request, id_user):

    """A function to confirm unfollow request
    and delete a user from followed users"""

    followed_user = get_object_or_404(AppUser, id=id_user)
    relation = UserFollows.objects.filter(
        user=request.user, followed_user=followed_user
    )
    relation.delete()
    return redirect("/community/")


@login_required
def edit_posts(request):

    """A function to display one's posts
    and allow their edition"""

    user = request.user
    user_reviews = user.review_set.all()
    user_tickets = user.ticket_set.all()
    user_posts = chain(user_reviews, user_tickets)
    user_reviews_tickets = [review.ticket for review in user_reviews]
    answered_tickets = [
        ticket for ticket in user_tickets
        if ticket in user_reviews_tickets
    ]
    uncommented_user_tickets = user_tickets.exclude(title__in=answered_tickets)
    commented_user_tickets = user_tickets.filter(title__in=answered_tickets)
    ordered_publications = sorted(user_posts,
                                  key=operator.attrgetter('time_created'),
                                  reverse=True)
    context = {"user": user, "user_posts": ordered_publications,
               "user_tickets": user_tickets, "user_reviews": user_reviews,
               "uncommented_tickets": uncommented_user_tickets,
               "commented_tickets": commented_user_tickets}
    return render(request, "blog/edit_posts.html", context)


@login_required
def edit_reviews(request):

    """A function to edit one's reviews on Post page"""

    user = request.user
    user_reviews = user.review_set.all()
    ordered_reviews = sorted(user_reviews,
                             key=operator.attrgetter('time_created'),
                             reverse=True)
    context = {"user": user, "user_reviews": ordered_reviews}
    return render(request, "blog/edit_reviews.html", context)


@login_required
def edit_tickets(request):

    """A function to edit one's tickets on Post page"""

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


@login_required
def delete_review(request, id_review):

    """A function to ask for the deletion of one's review"""

    review = get_object_or_404(Review, id=id_review)
    context = {"review": review}
    return render(request, "blog/delete_review.html", context)


@login_required
def confirm_delete_review(request, id_review):

    """A function to confirm the deletion of one's review"""

    review = get_object_or_404(Review, id=id_review)
    review.delete()
    return redirect("/edit_posts/")


@login_required
def delete_ticket(request, id_ticket):

    """A function to ask for the deletion of one's ticket"""

    ticket = get_object_or_404(Ticket, id=id_ticket)
    context = {"ticket": ticket}
    return render(request, "blog/delete_ticket.html", context)


@login_required
def confirm_delete_ticket(request, id_ticket):

    """A function to confirm the deletion of one's ticket"""

    ticket = get_object_or_404(Ticket, id=id_ticket)
    ticket.delete()
    return redirect("/edit_posts/")


@login_required
def edit_ticket(request, id_ticket):

    """A function to edit a particular ticket"""

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


@login_required
def edit_review(request, id_review):

    """A function to edit a particular review"""

    instance_review = get_object_or_404(Review, id=id_review)
    form = NewReviewForm(instance=instance_review)
    if request.method == "POST":
        form = NewReviewForm(request.POST, instance=instance_review)
        if form.is_valid():
            edited_review = form.save(commit=False)
            edited_review.user = request.user
            edited_review.save()
            return redirect("/edit_reviews/")
    context = {"form": form, "review": instance_review}
    return render(request, "blog/edit_review.html", context)


@login_required
def comment_ticket(request):

    """A function to create a review
    in response to a ticket"""

    user = request.user
    user_tickets = user.ticket_set.all()
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
        content_type=Value("UNANSWERED_TICKET", CharField()))
    posts = sorted(unanswered, key=lambda post: post.time_created,
                   reverse=True)
    context = {"unanswered_tickets": posts}
    return render(request, "blog/comment_ticket.html", context)


@login_required
def create_review(request, id_review=None, id_ticket=None):

    """A function to create a new review.

    The function first creates a ticket,
    then creates a review answering to the newly created ticket."""

    review_instance = (
        Review.objects.get(pk=id_review) if id_review is not None else None
    )
    ticket_instance = (
        Ticket.objects.get(pk=id_ticket) if id_ticket is not None else None
    )
    if request.method == "GET":
        ticket_form = NewTicketForm(instance=ticket_instance)
        review_form = CreateReviewForm(
            instance=review_instance, initial={"ticket": ticket_instance}
        )
        context = {"ticket_form": ticket_form, "review_form": review_form}
        return render(request, "blog/create_review.html", context)
    elif request.method == "POST":
        ticket_form = NewTicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            new_ticket = ticket_form.save(commit=False)
            new_ticket.user = request.user
            new_ticket.save()
            review_form = CreateReviewForm(request.POST)
            if review_form.is_valid():
                new_review = review_form.save(commit=False)
                new_review.user = request.user
                new_review.ticket = new_ticket
                new_review.save()
                return redirect("/")
