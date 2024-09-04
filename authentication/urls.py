from . import views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register/',views.RegisterationView.as_view() ,name='register'),
    path('login/',views.LoginView.as_view() ,name='login'),
    path('logout/',views.LogoutView.as_view() ,name='logout'),
    path('profile/',views.ProfileView.as_view() ,name='profile'),
    path('delete-profile/',views.deleteProfile ,name='delete-profile'),
    path('username-validation/',csrf_exempt(views.UsernameValidationView.as_view()) ,name='username-validation'),
    path('email-validation/',csrf_exempt(views.EmailValidationView.as_view()) ,name='email-validation'),
]