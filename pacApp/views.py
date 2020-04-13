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
	#ook1 = Booking(studio_id=0, company_id=0, start_time=)
	book1 = Booking(studio_id=0,
					company_id=0,
					company_name='Sympoh',
					start_time=17, 
					end_time=19, 
					week_day=0)
	book3 = Booking(studio_id=0,
					company_id=0,
					company_name='Sympoh',
					start_time=21, 
					end_time=24, 
					week_day=0)
	book2 = Booking(studio_id=1,
					company_id=0,
					company_name='Sympoh',
					start_time=9, 
					end_time=12, 
					week_day=0)
	wilcox = []
	wilcox.append(book1)
	wilcox.append(book3)
	bloomberg = []
	bloomberg.append(book2)
	# wilcox = [Booking1, Booking2]
	context = {'Wilcox': wilcox, 'Bloomberg': bloomberg}
	return render(request, "templates/pacApp/home2.html",context)

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
def get_range(start,end):

	return range(start,end+1)

@register.filter
def get_duration(start,end):
	return end-start+1

def adminForm(request):
	context = {'all_requests' : ADRequest.objects.all()}
	for item in context['all_requests']:
		print(item.name)
	return render(request, "templates/pacApp/form/adminForm.html", context)

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