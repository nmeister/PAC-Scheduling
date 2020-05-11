from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.template.loader import render_to_string


def error_404(request, exception):
    data = {}
    return render(request, 'templates/pacApp/404.html', data)


def error_500(request):
    data = {}
    return render(request, 'templates/pacApp/404.html', data)