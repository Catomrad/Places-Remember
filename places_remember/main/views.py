from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .forms import MemoryForm
from .models import Memory, User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
import requests
import json
# Create your views here.


def home(request):
    return render(request, 'home.html')


def logout_view(request):

    request.session.flush()
    logout(request)
    return redirect('/')


def profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/')  

    user = get_object_or_404(User, pk=user_id)
    memories = user.memories.all()
    return render(request, 'profile.html', {'user': user, 'memories': memories})


def add_memory(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/')

    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        form = MemoryForm(request.POST)
        if form.is_valid():
            memory = form.save(commit=False)
            memory.user = user
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


def edit_memory(request, memory_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/')

    user = get_object_or_404(User, pk=user_id)
    memory = get_object_or_404(Memory, id=memory_id)

    # Проверка, является ли текущий пользователь владельцем воспоминания
    if memory.user != user:
        return HttpResponseForbidden("You are not allowed to edit this memory.")

    if request.method == 'POST':
        form = MemoryForm(request.POST, instance=memory)
        if form.is_valid():
            memory = form.save(commit=False)
            memory.user = user

            # Обновляем координаты
            memory.latitude = form.cleaned_data['latitude']
            memory.longitude = form.cleaned_data['longitude']

            memory.save()
            return redirect('profile')
    else:
        form = MemoryForm(instance=memory)

    return render(request, 'edit_memory.html', {'form': form, 'memory': memory})


def delete_memory(request, memory_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/login/')

    user = get_object_or_404(User, pk=user_id)
    memory = get_object_or_404(Memory, id=memory_id)

    # Проверка, является ли текущий пользователь владельцем воспоминания
    if memory.user != user:
        return HttpResponseForbidden("You are not allowed to delete this memory.")

    if request.method == 'POST':
        memory.delete()
        return redirect('profile')
    return redirect('profile')


@csrf_exempt
def exchange_silent_token(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        silent_token = data.get('silent_token')
        uuid = data.get('uuid')
        service_token = settings.VK_SERVICE_TOKEN

        # Запрос к VK API для обмена silent_token на access_token
        response = requests.post('https://api.vk.com/method/auth.exchangeSilentAuthToken', data={
            'v': '5.131',
            'token': silent_token,
            'access_token': service_token,
            'uuid': uuid,
        })

        response_data = response.json()
        if 'response' in response_data:
            access_token = response_data['response']['access_token']
            user_id = response_data['response']['user_id']

            # Запрос к VK API для получения информации о пользователе
            profile_response = requests.get('https://api.vk.com/method/account.getProfileInfo', params={
                'v': '5.131',
                'access_token': access_token
            })

            profile_data = profile_response.json()

            if 'response' in profile_data:
                user_info = profile_data['response']
                avatar = data.get('user', {}).get('avatar')

                if not avatar:
                    # Если аватара нет в silent_token, сделаем запрос к users.get для получения фото
                    user_response = requests.get('https://api.vk.com/method/users.get', params={
                        'user_ids': user_id,
                        'fields': 'photo_200',
                        'v': '5.131',
                        'access_token': access_token
                    })

                    user_data = user_response.json()
                    if 'response' in user_data:
                        avatar = user_data['response'][0].get('photo_200')

                user_info['avatar'] = avatar

                # Сохраните или обновите информацию о пользователе в базе данных
                user, created = User.objects.update_or_create(
                    vk_id=user_id,
                    defaults={
                        'first_name': user_info['first_name'],
                        'last_name': user_info['last_name'],
                        'avatar': avatar,
                        'phone': user_info.get('phone')
                    }
                )

                request.session['user_id'] = user.id
                return JsonResponse({'access_token': access_token, 'user_info': user_info})
            else:
                return JsonResponse({'error': profile_data.get('error')}, status=400)
        else:
            return JsonResponse({'error': response_data.get('error')}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

