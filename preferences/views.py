from django.shortcuts import render,redirect
import os
import json
from django.conf import settings
from django.views import View
from .models import UserPreference
from django.contrib import messages

# Create your views here.

class preference(View):
    def get(self,request):
        currency_data = []
        file_path = os.path.join(settings.BASE_DIR,'currencies.json')
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)

            for key,value in data.items():
                currency_data.append({'name': key,'value':value})
        
        
        if UserPreference.objects.filter(user=request.user).exists():
            currency = UserPreference.objects.get(user=request.user).currency
            context = {
                'currency' : currency_data,
                'currency_val' : currency
            }
        else:
            context = {
                'currency' : currency_data,
            }

        return render(request,'preferences/preference.html',context)
    
    def post(self,request):
        check = UserPreference.objects.filter(user=request.user).exists()
        currency = request.POST['currency']
        if check:
            user_preference = UserPreference.objects.get(user=request.user)
            user_preference.currency = currency
            user_preference.save()
        else:
            UserPreference.objects.create(user = request.user,currency = currency)
        messages.success(request,'Changes Saved Succssfully')
        return redirect('home')
    