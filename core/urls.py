from . import views
from django.urls import path

urlpatterns = [
    path('',views.index ,name='home'),
    path('add-expense/',views.addExpense.as_view() ,name='add-expense'),
    path('edit-expense/<int:id>',views.editExpense ,name='edit-expense'),
    path('delete-expense/<int:id>',views.deleteExpense ,name='delete-expense'),
    path('expenses/',views.expenses ,name='expenses'),
]