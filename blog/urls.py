from django.urls import path
from blog import views

urlpatterns = [
    path("addticket/", views.add_ticket, name="add_ticket"),
    path("addticket/<int:id_ticket>", views.add_ticket, name="add_ticket"),
    path("addreview/", views.add_review, name="add_review"),
    path("community/", views.see_users, name="see_users"),
    path("unfollow_user/<int:id_user>/", views.unfollow_user, name="unfollow_user"),
    path("delete_user/<int:id_user>/", views.confirm_unfollow, name="confirm_unfollow"),
]
