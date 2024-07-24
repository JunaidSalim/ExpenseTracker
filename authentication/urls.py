from . import views
from django.urls import path

urlpatterns = [
    path('register/',views.RegisterationView.as_view() ,name='register'),
]