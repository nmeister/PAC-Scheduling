from django.shortcuts import render
from django.http import HttpResponse 
from django.template.loader import render_to_string 

# Create your views here.

def index(request):
	#return HttpResponse("Hello, World")
	html = render_to_string('home.html')
	#return HttpResponse(html)
	return render(request, "home.html")