from django.shortcuts import render, redirect
from django.http import HttpResponse 
from django.template.loader import render_to_string
from django.template.defaulttags import register
from django.conf.urls.static import static
from . import models, studio, hours
from .models import ADRequest, Booking
from .studio import Studio



# Create your views here.
# our home page 
def homepage(request):
	#return HttpResponse("Hello, World")
	html = render_to_string('templates/pacApp/home.html')
	return HttpResponse(html)

# displays the calendar schedule 


def schedule(request):
	# create bookings 
	book1 = Booking(studio_id=0,
					company_id=0,
					company_name='sympoh',
					start_time=18, 
					end_time=20, 
					week_day=5)
	book3 = Booking(studio_id=0,
					company_id=0,
					company_name='disiac',
					start_time=21, 
					end_time=24, 
					week_day=4)
	book4 = Booking(studio_id=0,
					company_id=0,
					company_name='bac',
					start_time=18, 
					end_time=20, 
					week_day=3)
	book2 = Booking(studio_id=1,
					company_id=0,
					company_name='pub',
					start_time=21, 
					end_time=24, 
					week_day=1)
	book5 = Booking(studio_id=2,
					company_id=0,
					company_name='sympoh',
					start_time=15, 
					end_time=17, 
					week_day=0)
	book6 = Booking(studio_id=4,
					company_id=0,
					company_name='bac',
					start_time=17, 
					end_time=20, 
					week_day=1)
	# each studio has a list which will be passed in together as a studio 
	wilcox = []
	wilcox.append(book1)
	wilcox.append(book3)
	wilcox.append(book4)
	bloomberg = []
	dilliondance = []
	dilliondance.append(book5)
	roberts = []
	roberts.append(book2)
	roberts.append(book6)
	# wilcox = [Booking1, Booking2]
	context = {'Wilcox': wilcox, 
	'Bloomberg': bloomberg, 
	'DillionDance': dilliondance,
	'Roberts': roberts}
	
	return render(request, "templates/pacApp/home.html",context)

def insert_space_item(request: HttpResponse):
	
	return redirect('/schedule')

def insert_ad_request(request: HttpResponse):
	
	ad_req = ADRequest(company_name = request.POST['name'], 
		company_day_1 = request.POST.get('company_day_1'),
		company_start_time_1 = request.POST['company_start_time_1'],
		company_end_time_1 = request.POST['company_end_time_1'],
		company_studio_1 = request.POST.get('company_studio_1'),
		company_day_2 = request.POST.get('company_day_2'),
		company_start_time_2 = request.POST['company_start_time_2'],
		company_end_time_2 = request.POST['company_end_time_2'],
		company_studio_2 = request.POST.get('company_studio_2'),
		company_day_3 = request.POST.get('company_day_3'),
		company_start_time_3 = request.POST['company_start_time_3'],
		company_end_time_3 = request.POST['company_end_time_3'],
		company_studio_3 = request.POST.get('company_studio_3'),
		rank_1 = request.POST.get('rank1s'), 
		rank_2 = request.POST.get('rank2s'), 
		rank_3 = request.POST.get('rank3s'),
		rank_4 = request.POST.get('rank4s'),
		rank_5 = request.POST.get('rank5s'),
		num_reho = request.POST['num_reho'],
		company_size = request.POST['num_members'])
	ad_req.save()
	return redirect('/adminForm')

@register.filter
# creates a function that can be called directly from the template 
def get_range(start,end):
	return range(start,end)

@register.filter
def get_duration(start,end):
	return end-start+1

def adminForm(request):
	context = {'all_requests' : ADRequest.objects.all()}
	for item in context['all_requests']:
		print(item.name)
	return render(request, "templates/pacApp/form/adminForm.html", context)

