from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from myapp.models import Playersinfo, Debate, Follower
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
                messages.info(request, 'User created')
                return redirect('login')
        else:
            messages.info(request, 'Password is not matching')
            return redirect('register')
    else:
        return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
            # Redirect to a success page.
        else:
            # Return an 'invalid login' error message.
            messages.info(request, 'Email or password not valid')
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('/')

def profile(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        current_user = User.objects.get(pk=user_id)
        debates = Debate.objects.filter(user_id=user_id)
        following_ids = current_user.following.all()
        following = []
        for f in following_ids:
            following.append(User.objects.get(pk=f.following_id))

        other_users = User.objects.exclude(id = user_id)
    return render(request, 'profile.html',{'debates':debates, 'other_users':other_users, 'following':following})


def follow(request, user_id, u_id):
    user = User.objects.get(pk=user_id)
    following_user = User.objects.get(pk=u_id)
    Follower.objects.create(follower_id = user_id,following_id= u_id)
    print('%s is following %s'%(user, following_user))
    return redirect('/accounts/profile')

def unfollow(request, user_id, u_id):
    user = User.objects.get(pk=user_id)
    following_user = User.objects.get(pk=u_id)
    follow_obj = Follower.objects.get(follower_id = user_id,following_id= u_id)
    follow_obj.delete()
    print('%s stop following %s'%(user, following_user))
    return redirect('/accounts/profile')
