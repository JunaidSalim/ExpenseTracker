from django.shortcuts import render, redirect
from preferences.models import UserPreference
from .models import Income, Source
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.views import View
from django.utils.decorators import method_decorator
import json
from django.db.models import Q, F
from django.http import JsonResponse
import datetime
from django.utils import timezone
from datetime import timedelta

# Create your views here.
@login_required(login_url='login')
def incomes(request):
    try:
        currency = UserPreference.objects.get(user = request.user).currency
    except:
        currency = ""
    incomes = Income.objects.filter(user = request.user).order_by('-date')
    paginator = Paginator(incomes, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        "currency": currency,
        "incomes": incomes,
        "page_obj":page_obj
        }
    return render(request,'incomes/incomes.html',context)

@method_decorator(login_required(login_url='login'), name='dispatch')
class addIncome(View):
    def get(self,request):
        sources = Source.objects.all()

        context = {
            'sources':sources,
            'values':request.POST
        }
        return render(request,'incomes/add-income.html',context)

    def post(self,request):
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['date']
        source_name = request.POST['source']
        source = Source.objects.get(name = source_name)
        user = request.user

        if not amount or not description:
            messages.error(request,'Fill all Fields')
            return redirect('add-income')
        else:
            Income.objects.create(amount = amount,description = description,date = date,source = source, user = user)
            messages.success(request,'Income Added Successfully')
            return redirect('incomes')

@login_required(login_url='login')
def editIncome(request,id):
    try:
        income = Income.objects.get(pk=id)
    except:
        messages.error(request,'Income does not Exist!')
        return redirect('incomes')
    sources = Source.objects.all()
    user = request.user
    if income.user == user:
        context = {
            'income':income,
            'sources':sources
        }
        if request.method=='GET':
            return render(request,'incomes/edit-income.html',context)
        else:
            amount = request.POST['amount']
            description = request.POST['description']
            date = request.POST['date']
            source_name = request.POST['source']
            source = Source.objects.get(name = source_name)

            if not amount or not description:
                messages.error(request,'Fill all Fields')
                return render(request,'incomes/edit-income.html',context)
            else:
                income.amount = amount
                income.description = description
                income.date = date
                income.source = source
                income.save()
                messages.success(request,'Income Updated Successfully')
                return redirect('incomes')
    else:
        messages.error(request,'Access Denied')
        return redirect('incomes')


@login_required(login_url='login')
def deleteIncome(request,id):
    try:
        income = Income.objects.get(pk=id)
    except:
        messages.error(request,'Income does not Exist!')
        return redirect('incomes')
    if income.user == request.user:
        income.delete()
        return redirect('incomes')
    else:
        messages.error(request,'Access Denied')
        return redirect('incomes')
    
def searchIncome(request):
    if request.method == 'POST':
        search = json.loads(request.body).get('search')
        
        incomes = Income.objects.filter(
            Q(amount__istartswith=search, user=request.user) | 
            Q(description__icontains=search, user=request.user) |  
            Q(source__name__icontains=search, user=request.user) |  
            Q(date__istartswith=search, user=request.user)
        ).values('amount', 'description', 'date', 'source__name')
        
        results = incomes.annotate(source=F('source__name')).values('amount', 'description', 'date', 'source')
        
        return JsonResponse(list(results), safe=False)

    else:
        return redirect('home')
    

@login_required(login_url='login')
def incomes_summary(request):
    today_date = datetime.date.today()
    month_ago = today_date - datetime.timedelta(days = 30)
    
    val = request.GET.get('value', 'all')
    if val=="all":
        incomes = Income.objects.filter(user = request.user)
    elif val=="last_30_days":
        incomes=  Income.objects.filter(user = request.user,date__gte = month_ago, date__lte = today_date)
    else:
        today = timezone.now().date()
        first_day_of_current_month = today.replace(day=1)
        last_day_of_last_month = first_day_of_current_month - timedelta(days=1)
        first_day_of_last_month = last_day_of_last_month.replace(day=1)
        incomes =Income.objects.filter(user = request.user,date__gte=first_day_of_last_month, 
date__lte=last_day_of_last_month)
    
    result = {}

    def get_catgeory(income):
        return income.source.name
    
    def get_income_source_amount(source):
        amount = 0
        filtered_by_source = incomes.filter(source__name = source)

        for item in filtered_by_source:
            amount+=item.amount
        
        return amount

    source_list = list(set(map(get_catgeory,incomes)))
    for x in incomes:
        for y in source_list:
            result[y] = get_income_source_amount(y)

    return JsonResponse({'income_source_data':result}, safe=False)

def stats(request):
    today = timezone.now().date()
    first_day_of_current_month = today.replace(day=1)
    last_day_of_last_month = first_day_of_current_month - timedelta(days=1)
    last_month_name = last_day_of_last_month.strftime('%B')
    return render(request,'incomes/stats.html',{"month":last_month_name})