from django.shortcuts import render, redirect
from django.http import HttpResponse 
from django.template.loader import render_to_string 
from django.conf.urls.static import static
from . import models, studio, hours
from .models import TimeSlot, Hours, ADRequest
from .studio import Studio



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

	#{'Wilcox': [t1, t2]} t1 = company name, time start, time end 
	# context = {'Wilcox': TimeSlot.objects.all(), 'Bloomberg': TimeSlot.objects.all()}
	# context['space_list'] = TimeSlot.objects.all()
	return render(request, "templates/pacApp/home2.html", context)

def insert_space_item(request: HttpResponse):
	timeSlot = TimeSlot(company_name = request.POST['company_name'], time_start = request.POST['time_start'],
						time_end = request.POST['time_end'], studio = request.POST['studio'])
	timeSlot.save()
	return redirect('/schedule')

def insert_ad_request(request: HttpResponse):
	ad_req = ADRequest(name = request.POST['name'], company_day = request.POST['company_day'], 
						company_start_time = request.POST['company_start_time'], company_end_time = request.POST['company_end_time'], 
						company_studio = request.POST['company_studio'], rank_1 = request.POST['rank_1'], rank_2 = request.POST['rank_2'],  rank_3 = request.POST['rank_3'],  
						rank_4 = request.POST['rank_4'], rank_5 = request.POST['rank_5'],  num_reho = request.POST['num_reho'], num_members = request.POST['num_members'])
	ad_req.save()
	return redirect('/fors')

def fors(request):
	context = {'all_requests' : ADRequest.objects.all()}
	return render(request, "templates/pacApp/fors.html", context)

def div(request):
	args = {}
	args['bac'] = [4,5,6]
	args['sympoh'] = [7,8,9]
	args['disiac'] = [9,10,11,12]
	wilcox = Studio('Wilcox', args)
	bloomberg = Studio('Bloomberg', args)
	studios = []
	studios.append(wilcox)
	studios.append(bloomberg)
	context = {'space_list' : studios}
	return render(request, "templates/pacApp/div.html", context)