from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import Category, Expense
from django.utils.decorators import method_decorator
from django.contrib import messages
from preferences.models import UserPreference

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
            return redirect('expenses')


@login_required(login_url='login')
def editExpense(request,id):
    try:
        expense = Expense.objects.get(pk=id)
    except:
        messages.error(request,'Expense does not Exist!')
        return redirect('expenses')
    categories = Category.objects.all()
    user = request.user
    if expense.user == user:
        context = {
            'expense':expense,
            'categories':categories
        }
        if request.method=='GET':
            return render(request,'core/edit-expense.html',context)
        else:
            amount = request.POST['amount']
            description = request.POST['description']
            date = request.POST['date']
            category_name = request.POST['category']
            category = Category.objects.get(name = category_name)

            if not amount or not description:
                messages.error(request,'Fill all Fields')
                return render(request,'core/edit-expense.html',context)
            else:
                expense.amount = amount
                expense.description = description
                expense.date = date
                expense.category = category
                expense.save()
                messages.success(request,'Expense Updated Successfully')
                return redirect('expenses')
    else:
        messages.error(request,'Access Denied')
        return redirect('expenses')

        
@login_required(login_url='login')
def deleteExpense(request,id):
    try:
        expense = Expense.objects.get(pk=id)
    except:
        messages.error(request,'Expense does not Exist!')
        return redirect('expenses')
    if expense.user == request.user:
        expense.delete()
        return redirect('expenses')
    else:
        messages.error(request,'Access Denied')
        return redirect('expenses')

    


@login_required(login_url='login')
def expenses(request):
    try:
        currency = UserPreference.objects.get(user = request.user).currency
    except:
        currency = ""
    expenses = Expense.objects.filter(user = request.user)
    context = {
        "currency": currency,
        "expenses": expenses
        }
    return render(request,'core/expenses.html',context)