from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth import logout
from django.views.decorators.cache import never_cache
from django.shortcuts import render
def home_view(request):
    return render(request, 'website/home.html')
@never_cache
@require_POST
def user_logout_view(request):
    logout(request)
    response = redirect('home')
    return response