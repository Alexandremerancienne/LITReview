from django.urls import path
from blog import views

urlpatterns = [
    path("addticket/", views.add_ticket, name="add_ticket"),
    path("addticket/<int:id_ticket>", views.add_ticket, name="add_ticket"),
    path("addreview/", views.add_review, name="add_review"),
    path("community/", views.see_all_users, name="see_all_users"),
]