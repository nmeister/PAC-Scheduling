from django.shortcuts import render, redirect
from django.http import HttpResponse 
from django.template.loader import render_to_string
from django.template.defaulttags import register
from django.conf.urls.static import static
from . import models, studio, hours
from .models import ADRequest, Booking
from .studio import Studio
import datetime
from datetime import date, timedelta


# Create your views here.
# our home page 
def homepage(request):
	#return HttpResponse("Hello, World")
	# create bookings
	if request.GET.get('newdate') == None:
		startdate = date.today()
		endweek = startdate + timedelta(days=6)
	else: 
		retdate = request.GET.get('newdate').split('-')
		# print(retdate)
		startdate = datetime.date(int(retdate[0]),int(retdate[1]),int(retdate[2]))
		endweek = startdate + timedelta(days=6)
		
	studioList = {'wilcox':0, 'bloomberg':1, 'dilliondance':2, 'dillionmpr': 3, 'roberts': 4, 'murphy':5, 'ns': 6, 'forbes': 7, 'ellie': 8}
	# filter by date range, but not sure where the date should be coming from 
	context = {'Wilcox': Booking.objects.filter(studio_id=0).filter(booking_date__range=[startdate, endweek]),
			   'Bloomberg': Booking.objects.filter(studio_id=1).filter(booking_date__range=[startdate, endweek]),
			   'DillionDance': Booking.objects.filter(studio_id=2).filter(booking_date__range=[startdate, endweek]),
			   'DillionMPR': Booking.objects.filter(studio_id=3).filter(booking_date__range=[startdate, endweek]),
			   'Roberts': Booking.objects.filter(studio_id=4).filter(booking_date__range=[startdate, endweek]),
			   'Murphy': Booking.objects.filter(studio_id=5).filter(booking_date__range=[startdate, endweek]),
			   'NewSouth': Booking.objects.filter(studio_id=6).filter(booking_date__range=[startdate, endweek]), 
			   'Forbes': Booking.objects.filter(studio_id=7).filter(booking_date__range=[startdate, endweek]),
			   'Ellie': Booking.objects.filter(studio_id=8).filter(booking_date__range=[startdate, endweek])}

	return render(request, "templates/pacApp/home.html", context)
# displays the calendar schedule

def schedule(request):
	studioList = {'wilcox':0,
	'bloomberg':1, 
	'dilliondance':2,
	'dillionmpr': 3,
	'roberts':4,
	'murphy':5,
	'ns': 6,
	'forbes': 7,
	'ellie': 8}

	#Return the day of the week as an integer, where Monday is 0 and Sunday is 6.
	weekday = datetime.datetime.today().weekday()


	context = {'Wilcox': Booking.objects.filter(studio_id=0),
			   'Bloomberg': Booking.objects.filter(studio_id=1),
			   'DillionDance': Booking.objects.filter(studio_id=2),
			   'DillionMPR': Booking.objects.filter(studio_id=3),
			   'Roberts': Booking.objects.filter(studio_id=4),
			   'Murphy': Booking.objects.filter(studio_id=5),
			   'NewSouth': Booking.objects.filter(studio_id=6), 
			   'Forbes': Booking.objects.filter(studio_id=7),
			   'Ellie': Booking.objects.filter(studio_id=8),
			   'Weekday' : weekday}
	return render(request, "templates/pacApp/schedule.html",context)

def create_booking(request: HttpResponse):

	studioList = {'wilcox':0, 'bloomberg':1, 'dilliondance':2, 'dillionmpr': 3, 'roberts':4, 
	'murphy':5, 'ns': 6, 'forbes': 7, 'ellie': 8}
	if request.is_ajax and request.method == "GET":
		date = (request.GET.get('date')).split('-')
		# print('received date is' + date)
		book = Booking(studio_id=studioList[(request.GET.get('studio'))],
				company_id=0, 
				company_name=request.GET.get('name'),
				start_time=(request.GET.get('starttime')), 
				end_time=(request.GET.get('endtime')),
				week_day=(request.GET.get('day')),
				booking_date=(datetime.date(int(date[0]),int(date[1]),int(date[2]))))
		# print('booked date is ' + book.booking_date) 
		book.save()
	return redirect('/')

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

