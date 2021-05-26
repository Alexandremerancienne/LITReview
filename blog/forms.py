from django.forms import ModelForm
from blog.models import Ticket, Review, UserFollows


class NewTicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]


class NewReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["ticket", "headline", "rating", "body"]


class FollowUserForm(ModelForm):
    class Meta:
        model = UserFollows
        fields = ["followed_user"]
