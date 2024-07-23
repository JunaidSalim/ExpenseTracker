from . import views
from django.urls import path

urlpatterns = [
    path('',views.index ,name='home'),
    path('add-expense/',views.addExpense ,name='add-expense'),
]