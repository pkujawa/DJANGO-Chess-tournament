from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout

from .forms import UserLoginForm, UserRegisterForm


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/')

    return render(request, "chess_games/login.html", context={'form': form})


def register_view(request):
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        return redirect('/')

    return render(request, "chess_games/signup.html", context={'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')
