from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.models import User
from .models import Category, Expense
from django.utils.decorators import method_decorator
from django.contrib import messages
from preferences.models import UserPreference
from django.core.paginator import Paginator
import json
from django.db.models import Q, F, Sum
from django.http import JsonResponse, HttpResponse
import datetime
import csv
import xlwt
from xhtml2pdf import pisa
from django.template.loader import get_template
from incomes.models import Income
from preferences.models import UserPreference
from django.utils import timezone
from datetime import timedelta

# Create your views here.
@login_required(login_url='auth/login')
def index(request):

    total_expenses = Expense.objects.filter(user = request.user).aggregate(total=Sum('amount'))['total'] or 0
    total_incomes = Income.objects.filter(user = request.user).aggregate(total=Sum('amount'))['total'] or 0

    today = timezone.now().date()
    first_day_of_current_month = today.replace(day=1)
    last_day_of_last_month = first_day_of_current_month - timedelta(days=1)
    first_day_of_last_month = last_day_of_last_month.replace(day=1)
    last_month_name = last_day_of_last_month.strftime('%B')

    expenses_last_month =Expense.objects.filter(user = request.user,date__gte=first_day_of_last_month, 
date__lte=last_day_of_last_month).aggregate(total=Sum('amount'))['total'] or 0
    
    incomes_last_month = Income.objects.filter(user = request.user,date__gte=first_day_of_last_month, 
date__lte=last_day_of_last_month).aggregate(total=Sum('amount'))['total'] or 0


    thirty_days_ago = today - timedelta(days=30)

    expenses_last_30_days = Expense.objects.filter(user = request.user,date__gte=thirty_days_ago,date__lte=today).aggregate(total=Sum('amount'))['total'] or 0

    incomes_last_30_days = Income.objects.filter(user = request.user,date__gte=thirty_days_ago,date__lte=today).aggregate(total=Sum('amount'))['total'] or 0

    balance = (total_incomes or 0) - (total_expenses or 0)
    last_month_balance = (incomes_last_month or 0) - (expenses_last_month or 0)
    last_30_days_balance = (incomes_last_30_days or 0) - (expenses_last_30_days or 0)


    user = User.objects.get(id=request.user.id)
    try:
        currency = UserPreference.objects.get(user = user).currency
    except:
        currency = ""

    context = {
        'balance':balance,
        'currency':currency,
        'last_month_balance':last_month_balance,
        'last_30_days_balance':last_30_days_balance,
        'total_expenses':total_expenses,
        'total_incomes':total_incomes,
        'expenses_last_month':expenses_last_month,
        'incomes_last_month':incomes_last_month,
        'last_month_name':last_month_name,
        'expenses_last_30_days':expenses_last_30_days,
        'incomes_last_30_days':incomes_last_30_days,
    }
    return render(request,'dashboard.html',context)

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
    expenses = Expense.objects.filter(user = request.user).order_by('-date')
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

    val = request.GET.get('value', 'all')
    if val=="all":
        expenses = Expense.objects.filter(user = request.user)
    elif val=="last_30_days":
        expenses=  Expense.objects.filter(user = request.user,date__gte = month_ago, date__lte = today_date)
    else:
        today = timezone.now().date()
        first_day_of_current_month = today.replace(day=1)
        last_day_of_last_month = first_day_of_current_month - timedelta(days=1)
        first_day_of_last_month = last_day_of_last_month.replace(day=1)
        expenses =Expense.objects.filter(user = request.user,date__gte=first_day_of_last_month, 
date__lte=last_day_of_last_month)

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
    for x in expenses:
        for y in category_list:
            result[y] = get_expense_category_amount(y)

    return JsonResponse({'expense_category_data':result}, safe=False)

def stats(request):
    today = timezone.now().date()
    first_day_of_current_month = today.replace(day=1)
    last_day_of_last_month = first_day_of_current_month - timedelta(days=1)
    last_month_name = last_day_of_last_month.strftime('%B')
    return render(request,'core/stats.html',{"month":last_month_name})

@login_required(login_url='login')
def exportCSV(request):
    tab = request.GET['tab']
    response = HttpResponse(content_type = 'text/csv')
    if tab=='income':
        response['Content-Disposition'] = 'attachment;filename = Incomes_' + str(datetime.datetime.now()) + '.csv'
    else:
        response['Content-Disposition'] = 'attachment;filename = Expenses_' + str(datetime.datetime.now()) + '.csv'
        
    writer = csv.writer(response)
    if tab=='income':
        writer.writerow(['Amount','Description','Source','Date'])
        rows = Income.objects.filter(user = request.user)
        for income in rows:
            writer.writerow([income.amount,income.description,income.source.name,income.date.strftime('%d-%m-%Y')])
    else:
        writer.writerow(['Amount','Description','Category','Date'])
        rows = Expense.objects.filter(user = request.user)
        for expense in rows:
            writer.writerow([expense.amount,expense.description,expense.category.name,expense.date.strftime('%d-%m-%Y')])
    
    return response

@login_required(login_url='login')
def exportExcel(request):
    tab = request.GET['tab']
    response = HttpResponse(content_type = 'application/ms-excel')
    if tab=='income':        
        response['Content-Disposition'] = 'attachment;filename = Incomes_' + str(datetime.datetime.now()) + '.xls'
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet('Incomes')
    else:        
        response['Content-Disposition'] = 'attachment;filename = Expenses_' + str(datetime.datetime.now()) + '.xls'
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet('Expenses')

    
    
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    if tab=='income':        
        columns = ['Amount','Description','Source','Date']
    else:
        columns = ['Amount','Description','Category','Date']



    for col_num in range(len(columns)):
        worksheet.write(row_num,col_num,columns[col_num],font_style)

    rows = Expense.objects.filter(user = request.user).values_list('amount','description','category__name','date') if tab!='income' else Income.objects.filter(user = request.user).values_list('amount','description','source__name','date')

    fontStyle = xlwt.XFStyle()
    fontStyle.font.bold = False

    for row in rows:
        row_num+=1

        for col_num in range(len(row)):
            worksheet.write(row_num,col_num,str(row[col_num]),fontStyle)
    
    workbook.save(response)

    return response

@login_required(login_url='login')
def exportPDF(request):
    tab = request.GET['tab']
    response = HttpResponse(content_type = 'application/pdf')
    if tab=="income":
        response['Content-Disposition'] = 'inline;attachment;filename = Incomes_' + str(datetime.datetime.now()) + '.pdf'
    else:
        response['Content-Disposition'] = 'inline;attachment;filename = Expenses_' + str(datetime.datetime.now()) + '.pdf'

    data = Expense.objects.filter(user=request.user) if tab!='income' else Income.objects.filter(user=request.user)

    if UserPreference.objects.filter(user=request.user).exists():
        currency = UserPreference.objects.get(user = request.user).currency
    else:
        currency = ""
    context = {
        'data':data,
        'tab':tab,
        'currency':currency
        }
    template_path = 'pdf.html'    
  
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


    