from . import views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('',views.index ,name='home'),
    path('add-expense/',views.addExpense.as_view() ,name='add-expense'),
    path('edit-expense/<int:id>',views.editExpense ,name='edit-expense'),
    path('delete-expense/<int:id>',views.deleteExpense ,name='delete-expense'),
    path('search-expense/',csrf_exempt(views.searchExpense) ,name='search-expense'),
    path('expenses/',views.expenses ,name='expenses'),
    path('expense-summary/',views.expenses_summary ,name='expense-summary'),
    path('expense-stats/',views.stats ,name='expense-stats'),
    path('export-csv/',views.exportCSV ,name='export-csv'),
    path('export-excel/',views.exportExcel ,name='export-excel'),
    path('export-pdf/',views.exportPDF ,name='export-pdf'),
]