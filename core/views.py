from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import Category, Expense
from django.utils.decorators import method_decorator
from django.contrib import messages

# Create your views here.

@login_required(login_url='auth/login')
def index(request):
    return render(request,'base.html')

@method_decorator(login_required(login_url='login'), name='dispatch')
class addExpense(View):
    def get(self,request):
        categories = Category.objects.all()

        context = {
            'categories':categories,
            'values':request.POST
        }
        return render(request,'core/add-expense.html',context)

    def post(self,request):
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['date']
        category_name = request.POST['category']
        category = Category.objects.get(name = category_name)
        user = request.user

        if not amount or not description:
            messages.error(request,'Fill all Fields')
            return redirect('add-expense')
        else:
            Expense.objects.create(amount = amount,description = description,date = date,category = category, user = user)
            messages.success(request,'Expense Added Successfully')
            return redirect('home')
        


@login_required(login_url='login')
def expenses(request):
    return render(request,'core/expenses.html')