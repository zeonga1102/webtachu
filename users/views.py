from django.shortcuts import render, redirect
from .models import UserModel
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.contrib.auth.decorators import login_required


# Create your views here.
def sign_up_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signup.html')
    elif request.method == 'POST':
        email = request.POST.get('email', None)
        first_name = request.POST.get('name', None)
        username = request.POST.get('id', None)
        password = request.POST.get('password', None)
        password2 = request.POST.get('password2', None)

        if password != password2:
            return render(request, 'user/signup.html')
        else:
            exist_user = get_user_model().objects.filter(username=username)
            if exist_user:
                return render(request, 'user/signup.html')
            else:
                print(email, username, password)
                UserModel.objects.create_user(email=email, username=username, password=password, first_name=first_name)
                return redirect('/sign-in')


def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('id', None)
        password = request.POST.get('password', None)
        me = auth.authenticate(request, username=username, password=password)
        if me is not None:
            auth.login(request, me)
            return redirect('/')
        else:
            return redirect('/')
    elif request.method == 'GET':
        return render(request, 'user/signin.html')


@login_required
def logout(request):
    auth.logout(request)
    return redirect("/")


def home(request):
    user = request.user.is_authenticated
    if user:
        return redirect('/mypage')
    else:
        return redirect('/sign-in')


def mypage(request):
    if request.method == 'GET':
        return render(request, 'user/mypage.html')