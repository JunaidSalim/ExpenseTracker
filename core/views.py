from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'base.html')

def addExpense(request):
    return render(request,'core/add-expense.html')