from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
# Create your views here.

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username is taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email is taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save();
                print('user created')
                return redirect('register')
        else:
            print('password not matching..')
            return redirect('register')
    else:
        return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
            # Redirect to a success page.
            ...
        else:
            # Return an 'invalid login' error message.
            messages.info(request, 'Email or password not valid')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

        
def logout(request):
    logout(request)
