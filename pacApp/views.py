from django.shortcuts import render, redirect
from django.http import HttpResponse 
from django.template.loader import render_to_string
from django.template.defaulttags import register
from django.contrib import messages
from django.conf.urls.static import static
from . import models, studio, hours
from .models import ADRequest, Booking
from .studio import Studio
import datetime
from datetime import date, timedelta
import pandas as pd
import numpy as np
import copy
import random
# import sweetify

# Create your views here.
# our home page 

def error_404(request, exception):
        data = {}
        return render(request,'templates/pacApp/404.html', data)

def error_500(request):
        data = {}
        return render(request,'templates/pacApp/404.html', data)

def createContext(startdate, endweek, newdate, groups, getGroups):
	actualdate = date.today()
	currday = 'None'
	week = {}
	for i in range(7):
		# week.append((startdate + timedelta(days=i)).strftime('%Y-%m-%d-%w'))
		week[(startdate + timedelta(days=i)).strftime('%w')] = (startdate + timedelta(days=i)).strftime('%Y-%m-%d')
		if (startdate + timedelta(days=i)).strftime('%Y-%m-%d') == actualdate.strftime('%Y-%m-%d'):
			currday = actualdate.strftime('%w')
	# print(week)

	studioList = {'bloomberg':0, 'dillondance':1, 'dillonmar':2, 'dillonmpr': 3, 'murphy': 4, 'ns':5,'nswarmup': 6, 'nstheatre': 7, 'whitman': 8, 'wilcox': 9}
	# filter by date range, but not sure where the date should be coming from 
	# creating context for each day of the week plus the data 
	if isinstance(newdate, str):
		print('str')
		formatdate = newdate.split('-')[0] + '-' + newdate.split('-')[1] + '-' + newdate.split('-')[2]
	else:
		print('date')
		# formatdate = str(newdate.year) + '-' + str(newdate.month) + '-' + str(newdate.day)
		formatdate = newdate.strftime('%Y-%m-%d')
	context = {'Bloomberg': Booking.objects.filter(studio_id=0).filter(booking_date__range=[startdate, endweek]),
			   'DillonDance': Booking.objects.filter(studio_id=1).filter(booking_date__range=[startdate, endweek]),
			   'DillonMAR': Booking.objects.filter(studio_id=2).filter(booking_date__range=[startdate, endweek]),
			   'DillonMPR': Booking.objects.filter(studio_id=3).filter(booking_date__range=[startdate, endweek]),
			   'Murphy': Booking.objects.filter(studio_id=4).filter(booking_date__range=[startdate, endweek]),
			   'NewSouth': Booking.objects.filter(studio_id=5).filter(booking_date__range=[startdate, endweek]),
			   'NSWarmup': Booking.objects.filter(studio_id=6).filter(booking_date__range=[startdate, endweek]), 
			   'NSTheatre': Booking.objects.filter(studio_id=7).filter(booking_date__range=[startdate, endweek]),
			   'Whitman': Booking.objects.filter(studio_id=8).filter(booking_date__range=[startdate, endweek]), 
			   'Wilcox': Booking.objects.filter(studio_id=9).filter(booking_date__range=[startdate, endweek]), 
			   'newdate': newdate, 'formatdate': formatdate, 'weekday': int(startdate.strftime('%w')), 'sun': week['0'], 
			   'currday':currday,
			   'mon': week['1'], 'tue': week['2'], 'wed': week['3'], 
			   'thu': week['4'], 'fri': week['5'], 'sat': week['6']}
	if getGroups == True:

		context['Bloomberg'] = context['Bloomberg'].filter(company_name__in=groups)
		context['DillonDance'] = context['DillonDance'].filter(company_name__in=groups)
		context['DillonMAR'] = context['DillonMAR'].filter(company_name__in=groups)
		context['DillonMPR'] = context['DillonMPR'].filter(company_name__in=groups)
		context['Murphy'] = context['Murphy'].filter(company_name__in=groups)
		context['NewSouth'] = context['NewSouth'].filter(company_name__in=groups)
		context['NSWarmup'] = context['NSWarmup'].filter(company_name__in=groups)
		context['NSTheatre'] = context['NSTheatre'].filter(company_name__in=groups)
		context['Whitman'] = context['Whitman'].filter(company_name__in=groups)
		context['Wilcox'] = context['Wilcox'].filter(company_name__in=groups)
	print(context['formatdate'])
	return context

def carouselAvailable():
	startdate = date.today()
	currenttime = int(datetime.datetime.now().time().hour)
	#print(currenttime)
	notfree = Booking.objects.filter(start_time__exact=currenttime).filter(booking_date__exact=startdate)

	studioList = [1,1,1,1,1,1,1,1,1,1]
	for i in notfree:
		studioList[i.studio_id] = 0

	#print(studioList)

	return studioList

# rendering the home page with today's date 
def homepage(request):
	
	startdate = date.today()
	print(startdate)
	endweek = startdate + timedelta(days=6)
	groups = None
	getGroups = False
	context = createContext(startdate, endweek, startdate.strftime('%Y-%m-%d'), groups, getGroups)
	context['currentdate'] = startdate.strftime('%Y-%m-%d')
	context['editable'] = False
	context['cursor'] = 'not'
	context['available'] = carouselAvailable()
	return render(request, "templates/pacApp/home.html", context)

# displays the calendar schedule
def schedule(request):
	# render with today's date 
	startdate = date.today()
	endweek = startdate + timedelta(days=6)
	groups = None
	getGroups = False
	context = createContext(startdate, endweek, startdate, groups, getGroups)
	context['currentdate'] = startdate.strftime('%Y-%m-%d')
	context['editable'] = True
	context['cursor'] = "pointer"
	return render(request, "templates/pacApp/schedule.html",context)

def create_booking(date, studio, name, starttime, endtime, day):
	studioList = {'bloomberg':0, 'dillondance':1, 'dillonmar':2, 'dillonmpr': 3, 'murphy': 4, 'ns':5,'nswarmup': 6, 'nstheatre': 7, 'whitman': 8, 'wilcox': 9}
	date = date.split('-')
		# print('received date is' + date)
	book = Booking(studio_id=studioList[studio],
			company_id=0, 
			company_name=name,
			start_time=starttime, 
			end_time=endtime,
			week_day=day,
			booking_date=(datetime.date(int(date[0]),int(date[1]),int(date[2]))))
		# print('booked date is ' + book.booking_date) 	
	book.save()
	return book.week_day

def update(request:HttpResponse):
	# if there is a booking involved
	print('update')
	weekday = None
	if (request.GET.get('studio') != None):
		weekday = create_booking(request.GET.get('date'), request.GET.get('studio'), request.GET.get('name'), request.GET.get('starttime'),
			request.GET.get('endtime'), request.GET.get('day'))
	retdate = request.GET.get('newdate').split('-')
	startdate = datetime.date(int(retdate[0]),int(retdate[1]),int(retdate[2]))
	print(startdate)
	endweek = startdate + timedelta(days=6)
	newdate = request.GET.get('newdate')
	print(newdate)
	groups = request.GET.get('selectgroups')
	if (groups == 'None' or groups == None):
		groups = None
		getGroups = False
	else: 
		groups = groups.split('-')
		groups.pop(-1)
		getGroups = True
	context = createContext(startdate, endweek, newdate, groups, getGroups)
	if weekday != None:
		context['weekday'] = weekday
	groupday = request.GET.get('groupday');
	print(weekday)
	print('groupday is')
	print(groupday)
	if weekday == None and groupday != None:
		context['weekday'] = groupday
	context['editable'] = True

	return render(request, "templates/pacApp/tableElements/table.html", context)



def insert_space_item(request: HttpResponse):
	return redirect('/schedule')

def insert_ad_request(request: HttpResponse):

	print(request.POST.get('rankone'))
	ad_req = ADRequest(company_name = request.POST['company_name'],
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
		num_reho = request.POST['num_reho'],
		company_size = request.POST['num_members'],
		rank_1 = request.POST.get('rank1s'),
		rank_2 = request.POST.get('rank2s'), 
		rank_3 = request.POST.get('rank3s'),
		rank_4 = request.POST.get('rank4s'),
		rank_5 = request.POST.get('rank5s'))
	ad_req.save()
	return redirect('/adminForm#')

@register.filter
# creates a function that can be called directly from the template 
def get_range(start,end):
	return range(start,end)

@register.filter
def get_duration(start,end):
	return end-start+1

def adminForm(request):
	context = {'all_requests' : ADRequest.objects.all()}
	#for item in context['all_requests']:
	#	print(item.name)
	return render(request, "templates/pacApp/form/adminForm.html", context)

# code for the scheduling algorithm
def scheduling_alg(request):
	all_requests = ADRequest.objects.all()
	df_request = pd.DataFrame(data=None, columns=['name', 'company_day', 'company_start_time', 'company_end_time', 'company_studio', 
								'rank_1', 'rank_2',  'rank_3',  'rank_4', 'rank_5',  'num_reho', 'num_members'])

	for group in all_requests:
		group_request = pd.DataFrame(data={'name': [group.company_name], 'company_day': [group.company_day_1], 'company_start_time': [group.company_start_time_1], 'company_end_time': [group.company_end_time_1], 'company_studio': [group.company_studio_1], 
								'rank_1': [group.rank_1], 'rank_2': [group.rank_2],  'rank_3': [group.rank_3],  'rank_4': [group.rank_4], 'rank_5': [group.rank_5], 
								'num_reho': [group.num_reho], 'num_members': [group.company_size]})
		df_request = pd.concat([group_request, df_request], ignore_index=True, sort=False)

	df_results = pd.DataFrame(data=None, columns=['Name','Studio','Day','Start_Time','End_Time'])

	# fill in the unavailable times for each studio
	unavailable = {}

	dance_studios = ['wilcox','bloomberg', 'dillondance','dillonmar','dillonmpr','whitman','ns','nswarmup','nstheatre']
	days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
	groups = df_request['name']

	# given a list hours, return the dictionary that gives initial availability of each day
	def get_init_avail(hours):
		hours_dance_stud_num = []
		for item in dance_studios:
			hours_dance_stud_num.append(copy.deepcopy(hours))
		initial_availability = dict(zip(copy.deepcopy(dance_studios), copy.deepcopy(hours_dance_stud_num)))
		return initial_availability

	# create avail a dictionary that stores the times the dance studios are free
	# initial_availability = dict(zip(copy.deepcopy(dance_studios), copy.deepcopy(hours_dance_stud_num)))
	# avail is a dictionary containing a dictionary for each day of the week.
	# the day of the week dictionary has studios as its keys and then 0:24 hours that it is available

	avail = {}
	for day in copy.deepcopy(days_of_week):
		hours = [i for i in range(0,24)]
		if (day is 'Sunday') or (day is 'Saturday'): 
			for i in range(1, 9):
				hours.remove(i)
		else: 
			for i in range(1, 17):
				hours.remove(i)
		avail[day] = copy.deepcopy(get_init_avail(copy.deepcopy(hours)))

	reho_count = dict(zip(df_request['name'], df_request['num_reho']))
	for group in reho_count:
		reho_count[group] = int(reho_count[group])

	"""Schedule Company For Every Group"""

	# identify conflicts
	# conflict(studio, day, start_time, end_time)

	'''group_info=df_request[df_request.name=='BAC']
	studio = group_info.iloc[:, df_request.columns.get_loc('company_studio')].values[0]
	day = group_info.iloc[:, df_request.columns.get_loc('company_day')].values[0]
	start_time = group_info.iloc[:, df_request.columns.get_loc('company_start_time')].values[0]
	end_time = group_info.iloc[:, df_request.columns.get_loc('company_end_time')].values[0]
	'''

	'''df_results[df_results.Studio == "NS Main"]'''

	# randomize the rows of the dataframe
	df_request = df_request.sample(frac=1).reset_index(drop=True)

	# for each group, schedule the company rehearsal space
	for group in df_request['name']:
		group_info=df_request[df_request.name==group]
		studio = group_info.iloc[:, df_request.columns.get_loc('company_studio')].values[0]
		day = group_info.iloc[:, df_request.columns.get_loc('company_day')].values[0]
		start_time = group_info.iloc[:, df_request.columns.get_loc('company_start_time')].values[0]
		end_time = group_info.iloc[:, df_request.columns.get_loc('company_end_time')].values[0]
		# if conflict --> conflict can just be a try/except thing
		# cant do times from 23-1
		# remove times from list
		'''if ((int(start_time) not in avail[day][studio]) or 
		(int(start_time)+1 not in avail[day][studio]) or 
		(int(start_time)+1 not in avail[day][studio])):'''
			# get company 2nd choice TO DO FOR NICOLE!!

		(avail[day][studio]).remove(int(start_time))
		(avail[day][studio]).remove(int(start_time)+1)
		(avail[day][studio]).remove(int(start_time)+2)
		
		group_results = pd.DataFrame(data={'Name': [group], 
											'Studio': [studio], 
											'Day': [day], 
											'Start_Time': [start_time], 
											'End_Time': [end_time]})
									
		df_results = pd.concat([group_results, df_results], ignore_index=True, sort=False)

	"""Cycle through the list of requests until everyone's requests are filled"""



	# while there are still spaces to book
	while (int(max(reho_count.values()))>0): 
		# randomize the order of groups
		for group in groups.sample(frac=1):
			# print(group)
			# if the group still has spaces to book, book a space
			if reho_count[group] != 0: 
				
				group_info=df_request[df_request.name==group]
				rank_1 = group_info.iloc[:, df_request.columns.get_loc('rank_1')].values[0]
				rank_2 = group_info.iloc[:, df_request.columns.get_loc('rank_2')].values[0]
				rank_3 = group_info.iloc[:, df_request.columns.get_loc('rank_3')].values[0]
				rank_4 = group_info.iloc[:, df_request.columns.get_loc('rank_4')].values[0]
				rank_5 = group_info.iloc[:, df_request.columns.get_loc('rank_5')].values[0]
				# if conflict --> conflict can just be a try/except thing
				# cant do times from 23-1
				# remove times from list

				# pick a random day 
				random.shuffle(days_of_week)
				day = days_of_week[0]
				studio = rank_1
				times_to_pick_from = [i for i in avail[day][studio] if (i>0 and ((i+1) in avail[day][studio]))]
				if (sum(times_to_pick_from) == 0): 
					studio = rank_2
					times_to_pick_from = [i for i in avail[day][studio] if (i>0 and ((i+1) in avail[day][studio]))]
				elif (sum(times_to_pick_from) == 0): 
					studio = rank_3
					times_to_pick_from = [i for i in avail[day][studio] if (i>0 and ((i+1) in avail[day][studio]))]
				elif (sum(times_to_pick_from) == 0): 
					studio = rank_4
					times_to_pick_from = [i for i in avail[day][studio] if (i>0 and ((i+1) in avail[day][studio]))]
				elif (sum(times_to_pick_from) == 0): 
					studio = rank_5
					times_to_pick_from = [i for i in avail[day][studio] if (i>0 and ((i+1) in avail[day][studio]))]
				elif (sum(times_to_pick_from) == 0):
					for free_studio in avail[day]:
						if sum(avail[day][free_studio]) > 0:
							studio = free_studio
				start_time = times_to_pick_from[0]
				(avail[day][studio]).remove(int(start_time))
				(avail[day][studio]).remove(int(start_time)+1)
				
				group_results = pd.DataFrame(data={'Name': [group], 
													'Studio': [studio], 
													'Day': [day], 
													'Start_Time': [int(start_time)], 
													'End_Time': [int(start_time)+1]})
				df_results = pd.concat([group_results, df_results], ignore_index=True, sort=False)   
				reho_count[group]-= 1

	studioList = dict(zip(dance_studios, list(range(0,10))))
	daysList = dict(zip(days_of_week, range(0,7)))
	
	for i, space in df_results.iterrows():
		book = Booking(studio_id=studioList[space['Studio']],
				company_id=0, 
				company_name=space['Name'],
				start_time=space['Start_Time'], 
				end_time=space['End_Time'],
				week_day=daysList[space['Day']],
				booking_date=datetime.datetime.today())
		book.save()

	return redirect('/')

