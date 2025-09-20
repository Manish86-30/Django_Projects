from django.shortcuts import render, redirect, HttpResponse
from translate import Translator


def home(request):
    if request.method == 'POST':
        text = request.POST['translate']
        language = request.POST['language']
        translator = Translator(to_lang=language)
        translation = translator.translate(text)
        return HttpResponse(translation)
    return render(request, 'index.html')