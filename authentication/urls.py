from . import views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register/',views.RegisterationView.as_view() ,name='register'),
    path('username-validation/',csrf_exempt(views.UsernameValidationView.as_view()) ,name='username-validation'),
]