from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


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
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldvalues' : request.POST
        }
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password)<6:
                    messages.error(request,'Password too short')
                    return render(request,'authentication/register.html',context)
                
                user = User.objects.create_user(username=username,email=email)
                user.set_password(password)
                user.save()
                messages.success(request,'Account Successfully Created')
                return redirect('login')
            
        return render(request,'authentication/register.html')

class LoginView(View):
    def get(self,request):
        return render(request,'authentication/login.html') 
    
    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = authenticate(username=username,password=password)

            if user:
                if user.is_active:
                    login(request,user)
                    messages.success(request,'Welcome ' + user.username + ', Your are now logged in')
                    return redirect('home')
            else:
                messages.error(request,'Invalid Credentials')
                return render(request,'authentication/login.html')
        else:
            messages.error(request,'Please Fill all Fields')
            return render(request,'authentication/login.html')

class LogoutView(View):
    def get(self,request):
        logout(request)
        messages.success(request,'You have been logged out')
        return redirect('login')
    

class ProfileView(LoginRequiredMixin, View):
    login_url = 'login'  

    def get(self, request):
        user_id = request.user.id
        user = User.objects.get(id=user_id)

        context = {
            "user" : user
        }
        return render(request, 'authentication/profile.html',context)

    def post(self, request):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']

        user = User.objects.get(id=request.user.id)

        user.first_name = first_name
        user.last_name = last_name

        if password:
            if len(password)<6:
                messages.error(request,"Password Should be atleast 6 characters")
                return redirect('profile')
            else:
                user.set_password(password)

        user.save()
        messages.success(request,"Changes Saved Successfully")
        return redirect('profile')
    
@login_required(login_url='login')
def deleteProfile(request):
    try:
        user = User.objects.get(id=request.user.id)
        user.delete()
        messages.success(request,'Account Deleted Successfully')
        return redirect('register')
    except:
        messages.error(request,"User Doesnot Exist")
        return redirect('register')
