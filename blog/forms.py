from django import forms
from django.forms import ModelForm

from blog.models import Ticket, Review, UserFollows


class NewTicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]


class NewReviewForm(ModelForm):
    RATING_CHOICE = (
        ("0", "0"),
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
    )
    rating = forms.ChoiceField(
        widget=forms.RadioSelect, choices=RATING_CHOICE, label="Rating"
    )

    class Meta:
        model = Review
        fields = ["ticket", "headline", "rating", "body"]


class FollowUserForm(ModelForm):
    class Meta:
        model = UserFollows
        fields = ["followed_user"]


class SearchUserForm(forms.Form):
    user_name = forms.CharField(label="Search User", max_length=100)

