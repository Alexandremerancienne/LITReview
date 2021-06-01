from django.urls import path
from blog import views

urlpatterns = [
    path("addticket/", views.add_ticket, name="add_ticket"),
    path("addticket/<int:id_ticket>", views.add_ticket, name="add_ticket"),
    path("addreview/", views.add_review, name="add_review"),
    path("community/", views.see_users, name="see_users"),
    path("unfollow_user/<int:id_user>/", views.unfollow_user, name="unfollow_user"),
    path("delete_user/<int:id_user>/", views.confirm_unfollow, name="confirm_unfollow"),
    path("edit_publications/", views.edit_publications, name="edit_publications"),
    path("edit_reviews/", views.edit_reviews, name="edit_reviews"),
    path("edit_tickets/", views.edit_tickets, name="edit_tickets"),
    path("delete_review/<int:id_review>/", views.delete_review, name="delete_review"),
    path("confirm_delete_review/<int:id_review>/", views.confirm_delete_review, name="confirm_delete_review"),
    path("delete_ticket/<int:id_ticket>/", views.delete_ticket, name="delete_ticket"),
    path("confirm_delete_ticket/<int:id_ticket>/", views.confirm_delete_ticket, name="confirm_delete_ticket"),
    path("edit_ticket/<int:id_ticket>/", views.edit_ticket, name="edit_ticket"),
    path("edit_review/<int:id_review>/", views.edit_review, name="edit_review"),
]
