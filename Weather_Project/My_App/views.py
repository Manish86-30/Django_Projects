from django.shortcuts import render
from django.http import HttpResponse
import requests
import datetime


def home(request):
    weather_data = {}
    if 'city' in request.GET:
        city = request.GET['city']
        api_key = "6e9f8f2fa9663aab1a8b1a3719ab0717"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url).json()

        if response.get('cod') == 200:
            weather_data = {
                'city': city,
                'temperature': response['main']['temp'],
                'description': response['weather'][0]['description'],
                'icon': response['weather'][0]['icon'],
                'humidity': response['main']['humidity'],
                'wind': response['wind']['speed'],
                'feels_like': response['main']['feels_like'],
                'pressure': response['main']['pressure'],
                'clouds': response['clouds']['all']
            }
        else:
            weather_data = {'error': 'City not found!'}
    return render(request, 'home.html', {'weather_data': weather_data})