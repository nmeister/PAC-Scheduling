from django.shortcuts import render
from django.http import HttpResponse 
from django.template.loader import render_to_string 
from django.conf.urls.static import static

# Create your views here.

def index(request):
	#return HttpResponse("Hello, World")
	html = render_to_string('home.html')
	#return HttpResponse(html)

def schedule(request):
	return render(request, "home2.html")