from . import views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('',views.incomes ,name='incomes'),   
    path('add-income/',views.addIncome.as_view() ,name='add-income'),  
    path('edit-income/<int:id>',views.editIncome ,name='edit-income'),
    path('delete-income/<int:id>',views.deleteIncome ,name='delete-income'),
    path('search-income/',csrf_exempt(views.searchIncome) ,name='search-income'),
    path('income-summary/',views.incomes_summary ,name='income-summary'),
    path('income-stats/',views.stats ,name='income-stats'),
]