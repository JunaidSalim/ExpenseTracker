from . import views
from django.urls import path

urlpatterns = [
    path('',views.index ,name='home'),
    path('add-expense/',views.addExpense.as_view() ,name='add-expense'),
    path('expenses/',views.expenses ,name='expenses'),
]