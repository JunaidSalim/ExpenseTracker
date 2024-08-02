from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages

# Create your views here.
class UsernameValidationView(View):
    def post(self,request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({"username_error":"Username should only contain alphabets and numbers"},status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Sorry username in use,choose another one'}, status=409)
        return JsonResponse({"username_valid":True},status=400)

class EmailValidationView(View):
    def post(self,request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({"email_error":"Email is Invalid"},status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Sorry Email in use,choose another one'}, status=409)
        return JsonResponse({"email_valid":True},status=400)

class RegisterationView(View):
    def get(self,request):
        return render(request,'authentication/register.html')
    
    def post(self,request):
        messages.info(request,"Test Message")
        messages.success(request,"Test Message")
        messages.error(request,"Test Message")
        messages.warning(request,"Test Message")
        return render(request,'authentication/register.html')