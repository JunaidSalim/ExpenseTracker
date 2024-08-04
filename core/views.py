from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='auth/login')
def index(request):
    return render(request,'base.html')

@login_required(login_url='login')
def addExpense(request):
    return render(request,'core/add-expense.html')