from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import RegistrationForm

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import LedState
import json

# Ensure one row exists
def get_led():
    obj, _ = LedState.objects.get_or_create(id=1)
    return obj

def dashboard(request):
    # Simple HTML page with ON/OFF buttons
    return render(request, 'led_dashboard.html')

@csrf_exempt
def set_led(request, state):
    led = get_led()
    if state == "on":
        led.is_on = True
    elif state == "off":
        led.is_on = False
    else:
        return JsonResponse({"error": "use on/off"}, status=400)
    led.save()
    return JsonResponse({"status": led.is_on})

def get_led_status(request):
    led = get_led()
    return JsonResponse({"is_on": led.is_on})
# Create your views here.
def members(request):
    return HttpResponse("Hello world!")


@login_required
def index(request):
    return render(request, 'index.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('index')

    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('index')
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        next_url = request.POST.get('next') or request.GET.get('next')
        if next_url and url_has_allowed_host_and_scheme(next_url, {request.get_host()}):
            return redirect(next_url)
        return redirect('index')
    return render(request, 'login.html', {'form': form})