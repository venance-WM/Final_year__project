from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as dj_login,logout
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        
        if password == password1 :
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email already used')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username already used,try new name...')
                return redirect('register')
            else:
                user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
                user.save()
                return redirect('login')
        else:
            messages.info(request,'Password doesnot match.')
            return redirect('register')
    else:
       return render(request,'registration/register.html')


def my_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            dj_login(request,user)
            return render(request,'home/index.html')
        else:
            messages.info(request,'Invalid username or password')
            return redirect('login')
           
    return render(request,'registration/login.html')

def my_logout(request):
    logout(request)
    return redirect('index')