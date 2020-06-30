from django.shortcuts import render, redirect
from . import models
from .forms import UserForm, RegisterForm
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.auth import login,logout

# Create your views here.


def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == "POST":
        login_form = UserForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = auth.authenticate(username=username,password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return redirect('/movie/movie_display/')
            else:
                messages.error(request,'用户名或密码错误!')
            return render(request, 'login.html')
    else:
        login_form = UserForm()
        return render(request,'login.html',locals())


def register(request):
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                messages.error(request, '两次输入的密码不同！')
                return render(request, 'register.html')
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    messages.error(request, '用户已经存在!')
                    return render(request, 'register.html')
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    messages.error(request, '该邮箱地址已被注册!！')
                    return render(request, 'register.html')
            # 当一切都OK的情况下，创建新用户
            User.objects.create_user(username=username, password=password1, email=email)
            return redirect('/user/login/')  # 自动跳转到登录页面

    register_form = RegisterForm()
    return render(request, 'register.html', locals())


def logout_view(request):
    logout(request)
    return redirect('/user/login/')