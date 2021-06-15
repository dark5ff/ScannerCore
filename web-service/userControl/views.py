from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .signForm import UserForm, LoginForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout as logout_

def signin(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('/chat/')
        else:
            return render(request, 'userControl/login.html', {'signin': 'T','message':'Login Fail'})
    else:
        form = LoginForm()
        return render(request, 'userControl/login.html', {'signin': 'T','message':'Login Fail'})


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            return redirect("/chat/")
    else:
        form = UserForm()
        return render(request, 'userControl/adduser.html', {'form': form,"message":"Error"})



def logout(request):
    logout_(request)
    return redirect('/')
