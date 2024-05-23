from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
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
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            if latitude is not None and longitude is not None:
                memory.latitude = latitude
                memory.longitude = longitude
                memory.save()
                return redirect('profile')
    else:
        form = MemoryForm()
    return render(request, 'add_memory.html', {'form': form})


@login_required
def edit_memory(request, memory_id):
    memory = get_object_or_404(Memory, id=memory_id)

    # Проверка, является ли текущий пользователь владельцем воспоминания
    if memory.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this memory.")

    if request.method == 'POST':
        form = MemoryForm(request.POST, instance=memory)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = MemoryForm(instance=memory)

    return render(request, 'edit_memory.html', {'form': form})


def delete_memory(request, memory_id):
    memory = get_object_or_404(Memory, id=memory_id)
    if request.method == 'POST':
        memory.delete()
        return redirect('profile')
    return redirect('profile')
