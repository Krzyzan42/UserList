from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib import messages
from users.forms import LoginForm, EditProfileForm, RegisterForm

# Create your views here.


def home(request):
    users = User.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'users/home.html', context=context)


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f'Logged in as {username}')
                return redirect('home')
    else:
        form = LoginForm()

    if request.method == 'POST':
        messages.error(request, 'Invalid credentials')
    return render(request, "users/login.html", {"form": form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = User.objects.create_user(username, password=password)
            auth_login(request, user)
            messages.success(request, f'You have registered as {username}')
            return redirect('home')
    else:
        form = RegisterForm()

    if request.method == 'POST':
        messages.error(request, 'Registration failed. Correct yourself')
    return render(request, "users/register.html", {"form": form})


def logout(request):
    auth_logout(request)
    return render(request, 'users/logout.html')


def profile(request, username):
    user = User.objects.get(username=username)
    if user is None:
        return render(request, 'users/profile.html')
    if user.id != request.user.id:
        return render(request, 'users/profile.html', context={'viewed_user': user})

    # User views their own profile page
    if request.method == 'POST':
        form = EditProfileForm(data=request.POST, instance=user)
        if form.is_valid():
            print('form valid')
            form.save(commit=True)
            update_session_auth_hash(request, form.instance)
            return redirect('home')
    else:
        form = EditProfileForm(instance=user)

    context = {
        "viewed_user": User.objects.get(username=username),
        "form": form,
    }
    return render(request, 'users/profile.html', context)
