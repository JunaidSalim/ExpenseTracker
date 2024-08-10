from django.contrib import admin
from .models import *

# Register your models here.
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('amount', 'description', 'user', 'category', 'date',)
    search_fields = ('description', 'category__name', 'date','amount')

    list_per_page = 10

admin.site.register(Category)
admin.site.register(Expense, ExpenseAdmin)