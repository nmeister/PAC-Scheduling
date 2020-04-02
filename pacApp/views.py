from django.shortcuts import render, redirect
from django.http import HttpResponse 
from django.template.loader import render_to_string 
from django.conf.urls.static import static
from . import models
from .models import TimeSlot


# Create your views here.

def index(request):
	#return HttpResponse("Hello, World")
	html = render_to_string('templates/pacApp/home.html')
	return HttpResponse(html)

def schedule(request):
	# t1 = models.TimeSlot(company_name="Sympoh", time_start=5, time_end=7,
		# studio="Wilcox")
	# context = {t1.company_name:t1}
	context = {'space_list' : TimeSlot.objects.all()}
	return render(request, "templates/pacApp/home2.html", context)

def insert_space_item(request: HttpResponse):
	timeSlot = TimeSlot(company_name = request.POST['company_name'], time_start = request.POST['time_start'],
						time_end = request.POST['time_end'], studio = request.POST['studio'])
	timeSlot.save()
	return redirect('/schedule')