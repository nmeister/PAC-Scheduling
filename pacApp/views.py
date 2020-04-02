from django.shortcuts import render
from django.http import HttpResponse 
from django.template.loader import render_to_string 
from django.conf.urls.static import static
from . import models


# Create your views here.

def index(request):
	#return HttpResponse("Hello, World")
	html = render_to_string('templates/pacApp/home.html')
	return HttpResponse(html)

def schedule(request):
	t1 = models.TimeSlot(company_name="Sympoh", time_start=5, time_end=7,
		studio="Wilcox")
	context = {t1.company_name:t1}
	return render(request, "templates/pacApp/home2.html", context)