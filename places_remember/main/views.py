from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from .forms import MemoryForm
from .models import Memory


# Create your views here.

def home(request):
    return render(request, 'home.html')


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def profile(request):
    memories = Memory.objects.filter(user=request.user)
    return render(request, 'profile.html', {'memories': memories})


@login_required
def add_memory(request):
    if request.method == 'POST':
        form = MemoryForm(request.POST)
        if form.is_valid():
            memory = form.save(commit=False)
            memory.user = request.user
            memory.save()
            return redirect('profile')
    else:
        form = MemoryForm()
    return render(request, 'add_memory.html', {'form': form})
