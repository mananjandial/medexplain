from django.urls import path
from . import views

urlpatterns = [
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("profile/update/", views.update_profile, name="update_profile"),

]
