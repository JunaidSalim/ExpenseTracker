from django.contrib import admin
from .models import *

# Register your models here.
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('amount', 'description', 'user', 'source', 'date',)
    search_fields = ('description', 'source__name', 'date','amount')

    list_per_page = 10

admin.site.register(Income, IncomeAdmin)
admin.site.register(Source)