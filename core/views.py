from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import Category, Expense
from django.utils.decorators import method_decorator
from django.contrib import messages
from preferences.models import UserPreference
from django.core.paginator import Paginator
import json
from django.db.models import Q, F
from django.http import JsonResponse, HttpResponse
import datetime
import csv

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
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        "currency": currency,
        "expenses": expenses,
        "page_obj":page_obj
        }
    return render(request,'core/expenses.html',context)

def searchExpense(request):
    if request.method == 'POST':
        search = json.loads(request.body).get('search')
        
        expenses = Expense.objects.filter(
            Q(amount__istartswith=search, user=request.user) | 
            Q(description__icontains=search, user=request.user) |  
            Q(category__name__icontains=search, user=request.user) |  
            Q(date__istartswith=search, user=request.user)
        ).values('amount', 'description', 'date', 'category__name')
        
        results = expenses.annotate(category=F('category__name')).values('amount', 'description', 'date', 'category')
        
        return JsonResponse(list(results), safe=False)
    
    else:
        return redirect('home')
    
@login_required(login_url='login')
def expenses_summary(request):
    today_date = datetime.date.today()
    month_ago = today_date - datetime.timedelta(days = 30)
    expenses=  Expense.objects.filter(user = request.user,date__gte = month_ago, date__lte = today_date)
    result = {}

    def get_catgeory(expense):
        return expense.category.name
    
    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category__name = category)

        for item in filtered_by_category:
            amount+=item.amount
        
        return amount

    category_list = list(set(map(get_catgeory,expenses)))
    print(category_list)
    for x in expenses:
        for y in category_list:
            result[y] = get_expense_category_amount(y)

    return JsonResponse({'expense_category_data':result}, safe=False)

def stats(request):
    return render(request,'core/stats.html')

@login_required(login_url='login')
def exportCSV(request):
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'attachment;filename = Expenses_' + str(datetime.datetime.now()) + '.csv'
    writer = csv.writer(response)
    writer.writerow(['Amount','Description','Category','Date'])
    
    expenses = Expense.objects.filter(user = request.user)

    for expense in expenses:
        writer.writerow([expense.amount,expense.description,expense.category.name,expense.date.strftime('%d-%m-%Y')])
    
    return response
