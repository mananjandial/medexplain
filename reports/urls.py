from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_report, name='upload'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),
]
