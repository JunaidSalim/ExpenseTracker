from . import views
from django.urls import path

urlpatterns = [
    path('',views.preference.as_view() ,name='preference'),
]