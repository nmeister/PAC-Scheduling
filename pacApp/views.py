from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.template.defaulttags import register
from django.contrib import messages
import math
#from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from uniauth.decorators import login_required
from django.conf.urls.static import static
from . import models
from .models import ADRequest, Booking, CompanyRequest, RehearsalRequest, Group
import datetime
from datetime import date, timedelta
import pandas as pd
import numpy as np
import copy
import random
import calendar
import json
# from uniauth.models import Institution, InstitutionAccount, LinkedEmail


# Create your views here.
# our home page


def error_404(request, exception):
    data = {}
    return render(request, 'templates/pacApp/404.html', data)


def error_500(request):
    data = {}
    return render(request, 'templates/pacApp/404.html', data)


def carouselAvailable():
    startdate = date.today()
    currenttime = int(datetime.datetime.now().time().hour)
    # print(currenttime)
    notfree = Booking.objects.filter(start_time__exact=currenttime).filter(
        booking_date__exact=startdate)

    studioList = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    for i in notfree:
        studioList[i.studio_id_id] = 0

    # print(studioList)

    return studioList

# rendering the home page with today's date


def about(request):
    context = {}
    return render(request, "templates/pacApp/about.html", context)

def homepage(request):
    try:
        profile = request.user.uniauth_profile.get_display_id()
    except:
        profile = 'None'
    print(profile)
    starttoday = date.today()
    groups = 'None'
    context = createContext(starttoday, groups)
    context['available'] = carouselAvailable()
    context['user'] = profile
    return render(request, "templates/pacApp/home.html", context)

# displays the calendar schedule


def createContext(startdate, groups):
    week = {}
    # for one week
    startday = startdate.strftime('%w')
    if startday != '0': 
      print('today is not sunday')
      sunday = startdate - timedelta(days=int(startday))
      enddate = sunday + timedelta(days=6)
      print('sunday is ' + sunday.strftime('%Y-%m-%d'))
      for i in range(7):
        week[(sunday + timedelta(days=i)).strftime('%w')
             ] = (sunday + timedelta(days=i)).strftime('%Y-%m-%d')
      print(week)
    else: 
      print('today is sunday')
      sunday = startdate
      enddate = startdate + timedelta(days=6)
      for i in range(7):
        print('creating the days of the week')
        week[(startdate + timedelta(days=i)).strftime('%w')
             ] = (startdate + timedelta(days=i)).strftime('%Y-%m-%d')
      print(week)

    # studio list for matching studio and names, just for reference
    studioList = {'bloomberg': 0, 'dillondance': 1, 'dillonmar': 2, 'dillonmpr': 3,
                  'murphy': 4, 'ns': 5, 'nswarmup': 6, 'nstheatre': 7, 'whitman': 8, 'wilcox': 9}
    # filter by studio and week
    context = {'Bloomberg': Booking.objects.filter(studio_id_id=0).filter(booking_date__range=[sunday, enddate]),
               'DillonDance': Booking.objects.filter(studio_id=1).filter(booking_date__range=[sunday, enddate]),
               'DillonMAR': Booking.objects.filter(studio_id_id=2).filter(booking_date__range=[sunday, enddate]),
               'DillonMPR': Booking.objects.filter(studio_id_id=3).filter(booking_date__range=[sunday, enddate]),
               'Murphy': Booking.objects.filter(studio_id_id=4).filter(booking_date__range=[sunday, enddate]),
               'NewSouth': Booking.objects.filter(studio_id_id=5).filter(booking_date__range=[sunday, enddate]),
               'NSWarmup': Booking.objects.filter(studio_id_id=6).filter(booking_date__range=[sunday, enddate]),
               'NSTheatre': Booking.objects.filter(studio_id_id=7).filter(booking_date__range=[sunday, enddate]),
               'Whitman': Booking.objects.filter(studio_id_id=8).filter(booking_date__range=[sunday, enddate]),
               'Wilcox': Booking.objects.filter(studio_id_id=9).filter(booking_date__range=[sunday, enddate]),
               'sun': week['0'], 'mon': week['1'], 'tue': week['2'], 'wed': week['3'],
               'thu': week['4'], 'fri': week['5'], 'sat': week['6']}

    context['formatdate'] = startdate.strftime('%Y-%m-%d')
    context['enddate'] = enddate.strftime('%Y-%m-%d')
    # on default opened day is on the same as the date in the week start
    # this is the tab that will be opened whether itbe what the user was on before clicked something or today
    context['openday'] = startday


    if groups != 'None':
      print('in create context where groups is not None')
      print(groups)
      print(type(groups))
      if groups[0] == 0:
        print('there is a non group')
      
      bloombergNew = context['Bloomberg'].filter(group_id_id__in=groups)
      bloombergGray = context['Bloomberg'].exclude(group_id_id__in=groups)
      context['Bloomberg'] = bloombergNew
      context['BloombergGray'] = bloombergGray

      dillonDanceNew = context['DillonDance'].filter(group_id_id__in=groups)
      dillonDanceGray = context['DillonDance'].exclude(group_id_id__in=groups)
      context['DillonDance'] = dillonDanceNew
      context['DillonDanceGray'] = dillonDanceGray


      dillonMARNew = context['DillonMAR'].filter(group_id_id__in=groups)
      dillonMARGray = context['DillonMAR'].exclude(group_id_id__in=groups)
      context['DillonMAR'] = dillonMARNew
      context['DillonMARGray'] = dillonMARGray

      dillonMPRNew = context['DillonMPR'].filter(group_id_id__in=groups)
      dillonMPRGray = context['DillonMPR'].exclude(group_id_id__in=groups)
      context['DillonMPR'] = dillonMPRNew
      context['DillonMPRGray'] = dillonMPRGray
      
      murphyNew = context['Murphy'].filter(group_id_id__in=groups)
      murphyGray = context['Murphy'].exclude(group_id_id__in=groups)
      context['Murphy'] = murphyNew
      context['MurphyGray'] = murphyGray

      nsNew = context['NewSouth'].filter(group_id_id__in=groups)
      nsGray = context['NewSouth'].exclude(group_id_id__in=groups)
      context['NewSouth'] = nsNew
      context['NewSouthGray'] = nsGray

      nsWarmNew = context['NSWarmup'].filter(group_id_id__in=groups)
      nsWarmGray = context['NSWarmup'].exclude(group_id_id__in=groups)
      context['NSWarmup'] = nsWarmNew
      context['NSWarmupGray'] = nsWarmGray
       
      nsTNew = context['NSTheatre'].filter(group_id_id__in=groups)
      nsTGray = context['NSTheatre'].exclude(group_id_id__in=groups)
      context['NSTheatre'] = nsTNew
      context['NSTheatreGray'] = nsTGray
        
      whitNew = context['Whitman'].filter(group_id_id__in=groups)
      whitGray = context['Whitman'].exclude(group_id_id__in=groups)
      context['Whitman'] = whitNew
      context['WhitmanGray'] = whitGray

      wilNew = context['Wilcox'].filter(group_id_id__in=groups)
      wilGray = context['Wilcox'].exclude(group_id_id__in=groups)
      context['Wilcox'] = wilNew
      context['WilcoxGray'] = wilGray 

    return context



@login_required
def schedule(request):
    # render with today's date
    profile = request.user.uniauth_profile.get_display_id()
    print(profile)
    starttoday = date.today()
    print(starttoday)
    groups = 'None'

    context = createContext(starttoday, groups)
    context['user'] = profile
    
    return render(request, "templates/pacApp/schedule.html", context)


# takes in string, returns type of object date
def handleDateStr(date):
    print(date)
    print(type(date))
    date = date.split('-')
    startdate = datetime.date(int(date[0]), int(date[1]), int(date[2]))
    return startdate

def handleGroup(groups):
  if groups == 'None':
    return 'None'
  else: 
    groups = groups.split('-')
    # the last one is a - which should be empty
    groups.pop(-1)
    return groups

def updateWeek(request):
    # we get something of type string in the form of yyyy-mm-dd
    # transform date string into DATE object
    newdate = request.GET.get('newdate')
    startdate = handleDateStr(newdate)
    

    # getting groups, it is type string, if no groups selected will be 'None' (str)
    groups = handleGroup(request.GET.get('groups'))
    print(groups)

    # creating for week, we know that the date inputted in must be the same as open date
    context = createContext(startdate, groups)

    return render(request, "templates/pacApp/tableElements/calendar.html", context)


def updateGroupOnly(request):
    # the opened day user is on 
    openday = handleDateStr(request.GET.get('openday'))
    # this is the current week user is on 
    startdate = handleDateStr(request.GET.get('currweek'))
    # getting groups, it is type string, if no groups selected will be 'None' (str)

    groups = handleGroup(request.GET.get('groups'))
    context = createContext(startdate, groups)
    # overwrites this because we want week to stay consistent and the tab opened consistent
    context['openday'] = openday.strftime('%w')
    print(context['openday'])

    return render(request, "templates/pacApp/tableElements/calendar.html", context)

# for booking slot
# creates a booking in table, updates with same current week and opened tab 
def updateBooking(request):
    print('in updating booking')
    # the booker for authentication
    profile = request.user.uniauth_profile.get_display_id()
    # these are all related to booking 
    bookingdate = handleDateStr(request.GET.get('date'))
    studio = request.GET.get('studio')
    username = request.GET.get('name')
    userid = request.GET.get('nameid')
    starttime = request.GET.get('starttime')
    endtime = request.GET.get('endtime')
    weekdaybooked = request.GET.get('day')
    # try to make a booking in the table 
    # returns 0 upon FAIL and 1 upon SUCCESS
    success = create_booking(bookingdate, studio, username, userid, starttime, endtime, weekdaybooked, profile)
    print(success)
    # this is the current week start on 
    startdate = handleDateStr(request.GET.get('currweek'))
    groups = handleGroup(request.GET.get('groups'))
    openday = handleDateStr(request.GET.get('openday'))

    context = createContext(startdate, groups)
    context['openday'] = openday.strftime('%w')
    context['booksuccess'] = success
    return render(request, "templates/pacApp/tableElements/calendar.html", context)

def create_booking(date, studio, name, nameid, starttime, endtime, day, profile):
    studioList = {'bloomberg': 0, 'dillondance': 1, 'dillonmar': 2, 'dillonmpr': 3,
                  'murphy': 4, 'ns': 5, 'nswarmup': 6, 'nstheatre': 7, 'whitman': 8, 'wilcox': 9}
    count = 0 
    for i in range(int(starttime),int(endtime)):
      bookExist = Booking.objects.filter(studio_id_id=studioList[studio]).filter(booking_date=date)
      bookExist = bookExist.filter(start_time=int(i)).filter(end_time=i+1).filter(week_day=day)
      if bookExist.exists():
        print('bad already exists, cannot be booked')
        return 0
      else:
        print(name)
      # doesn't exist therefore make a new booking
        book = Booking(studio_id_id=studioList[studio],
                   group_id_id=nameid,
                   group_name=name,
                   from_alg=0,
                   user_netid=profile,
                   start_time=i,
                   end_time=i+1,
                   week_day=day,
                   booking_date=date)
      book.save()
      count += 1
    print(count)
    return 1

def updateMulti(request: HttpResponse):
    profile = request.user.uniauth_profile.get_display_id()
    slots = request.POST['slots[]']
    data = json.loads(slots)
    for i in data:
      create_booking(handleDateStr(i['booking_date']), i['studio'], 
        i['company_name'], i['company_id'], i['start_time'], 
        i['end_time'], i['week_day'], i['user_netid'])
    startdate = handleDateStr(request.POST['currweek'])
    openday = handleDateStr(request.POST['openday'])
    groups = handleGroup(request.POST['groups'])
    context = createContext(startdate, groups)
    context['openday'] = openday.strftime('%w')
    context['user'] = profile
    return render(request, "templates/pacApp/tableElements/calendar.html", context)

def updateDropping(request: HttpResponse):

    print('in drop space')
    profile = request.user.uniauth_profile.get_display_id()

    # get variables from post resuts
    # this is for dropping the space 
    studio = request.POST['studio']
    bookingdate = handleDateStr(request.POST['date'])  # booking date
    starttime = request.POST['starttime']
    endtime = request.POST['endtime']
    day = request.POST['day']  # weekday
    name = request.POST['name']
    nameid = request.POST['nameid']
    # delete the booking from the db
    success = delete_booking(bookingdate, studio, name, nameid, starttime, endtime, day, profile)
    print(success)
    groups = handleGroup(request.POST['groups'])
    startdate = handleDateStr(request.POST['currweek'])
    openday = handleDateStr(request.POST['openday'])

    context = createContext(startdate, groups)

    context['user'] = profile
    context['openday'] = openday.strftime('%w')
    context['dropsuccess'] = success
    return render(request, "templates/pacApp/tableElements/calendar.html", context)
   

# delete the booking
def delete_booking(date, studio, name, nameid, starttime, endtime, day, profile):
    print('in delete booking')
    studioList = {'bloomberg': 0, 'dillondance': 1, 'dillonmar': 2, 'dillonmpr': 3,
                  'murphy': 4, 'ns': 5, 'nswarmup': 6, 'nstheatre': 7, 'whitman': 8, 'wilcox': 9}
    print(name)
    # grab the booking you want to delete
    try:
        book_to_del = Booking.objects.get(studio_id_id=studioList[studio],
                                          group_id_id=nameid,
                                          group_name = name,
                                          user_netid=profile,
                                          start_time=starttime,
                                          end_time=endtime,
                                          week_day=day,
                                          from_alg=0,
                                          booking_date=date)
        book_to_del.delete()
    except:
        print('not able to drop')
        return 0 
    return 1


# transform str "April 27, 2020" into list [yyyy, mm, dd]
def handledate(date):
    date = date.replace(',', '')
    date = date.split(' ')
    month = date[0]
    day = date[1]
    year = date[2]

    # chance month to a number
    abbr_to_num = {name: num for num,
                   name in enumerate(calendar.month_abbr) if num}
    month = abbr_to_num[month[0:3]]

    return year, month, day


def drop_ad_request(request: HttpResponse):
    request_id = request.GET.get('id')
    print(request_id)
    delete_ad_request(request_id)
    # return render(request, "templates/pacApp/form/adminForm.html", context)
    return redirect('../../adminForm')

def delete_ad_request(request_id):

    print('in delete ad request, deleting', request_id)
    # grab the booking you want to delete

    reho_req_to_del = RehearsalRequest.objects.get(request_id=request_id)
    
    print(reho_req_to_del.request_id)
    co_req_1 = CompanyRequest.objects.get(request_id_id=request_id, company_choice_num=1)
    co_req_2 = CompanyRequest.objects.filter(request_id_id=request_id, company_choice_num=2)
    co_req_3 = CompanyRequest.objects.filter(request_id_id=request_id, company_choice_num=3)
    
    print(co_req_1.request_id_id)

    co_req_1.delete()
    co_req_2.delete()
    co_req_3.delete()
 
    reho_req_to_del.delete()
  
    try:
        reho_req_to_del = RehearsalRequest.objects.get(request_id=request_id)
    
        print(reho_req_to_del.request_id)
        co_req_1 = CompanyRequest.objects.get(request_id_id=request_id, company_choice_num=1)
        co_req_2 = CompanyRequest.objects.filter(request_id_id=request_id, company_choice_num=2)
        co_req_3 = CompanyRequest.objects.filter(request_id_id=request_id, company_choice_num=3)
        
        print(co_req_1.request_id_id)

        co_req_1.delete()
        co_req_2.delete()
        co_req_3.delete()
    
        reho_req_to_del.delete()
        print('in drop')
    except:
        print('not able to drop')
    return

def insert_space_item(request: HttpResponse):
    return redirect('/schedule')


def grab_time(time_val):
    return int(time_val[0:2])


def insert_ad_request(request: HttpResponse):

    groups_list = ['BAC', 'Bhangra', 'BodyHype', 'Disiac', 'eXpressions', 'HighSteppers',
                        'Kokopops', 'Naacho', 'PUB', 'Six14', 'Sympoh', 'Triple8']

    studioList = {'bloomberg': 0, 'dillondance': 1, 'dillonmar': 2, 'dillonmpr': 3,
                  'murphy': 4, 'ns': 5, 'nswarmup': 6, 'nstheatre': 7, 'whitman': 8, 'wilcox': 9}

    company_start_time_1 = grab_time(request.POST['company_start_time_1'])
    company_end_time_1 = grab_time(request.POST['company_end_time_1'])
    company_start_time_2 = grab_time(request.POST['company_start_time_2'])
    company_end_time_2 = grab_time(request.POST['company_end_time_2'])
    company_start_time_3 = grab_time(request.POST['company_start_time_3'])
    company_end_time_3 = grab_time(request.POST['company_end_time_3'])

    current_datetime = str(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
    name = groups_list[int(request.POST['company_name'])-1]
    print(name)

    reho_req = RehearsalRequest(scheduled=0,
                                num_reho=int(request.POST['num_reho']),
                                member_size=int(request.POST['num_members']),
                                rank_1=int(request.POST['rank_1']),
                                rank_2=int(request.POST['rank_2']),
                                rank_3=int(request.POST['rank_3']),
                                rank_4=int(request.POST['rank_4']),
                                rank_5=int(request.POST['rank_5']),
                                rank_6=int(request.POST['rank_6']),
                                rank_7=int(request.POST['rank_7']),
                                rank_8=int(request.POST['rank_8']),
                                rank_9=int(request.POST['rank_9']),
                                rank_10=int(request.POST['rank_10']),
                                request_id=(str(name)+current_datetime),
                                group_id_id=request.POST['company_name'],
                                submit_date = current_datetime)

    company_req_1 = CompanyRequest(request_id_id=(str(name)+current_datetime), 
                                company_choice_num = 1,                                                    
                                scheduled = 0,
                                group_id_id = request.POST['company_name'],
                                company_day = request.POST.get('company_day_1'),
                                company_start_time = int(company_start_time_1),
                                company_end_time = int(company_end_time_1),
                                company_studio_id = studioList[str(request.POST.get('company_studio_1'))],
                                submit_date = current_datetime)

    company_req_2 = CompanyRequest(request_id_id=(str(name)+current_datetime), 
                                company_choice_num = 2,                                                    
                                scheduled = 0,
                                group_id_id = request.POST['company_name'],
                                company_day = request.POST.get('company_day_2'),
                                company_start_time = int(company_start_time_2),
                                company_end_time = int(company_end_time_2),
                                company_studio_id = studioList[str(request.POST.get('company_studio_2'))],
                                submit_date = current_datetime)

    company_req_3 = CompanyRequest(request_id_id=(str(name)+current_datetime), 
                                company_choice_num = 3,                                                    
                                scheduled = 0,
                                group_id_id = request.POST['company_name'],
                                company_day = request.POST.get('company_day_3'),
                                company_start_time = company_start_time_3,
                                company_end_time = company_end_time_3,
                                company_studio_id = studioList[str(request.POST.get('company_studio_3'))],
                                submit_date = current_datetime)

    reho_req.save()
    company_req_1.save()
    company_req_2.save()
    company_req_3.save()
    
    return redirect('/adminForm')


@register.filter
# creates a function that can be called directly from the template
def get_range(start, end):
    return range(start, end)


@register.filter
def get_duration(start, end):
    return end-start+1


def must_be_pac(user):
    return user.groups.filter(name='Pac').count()

#my_group = Group.objects.get(name='Pac')
# my_group.user_set.add('test@pac.com')

# if user not pac and tries to go to PAC booking page show this endpage


def notpac(request):
    context = {}
    return render(request, "templates/pacApp/notPac.html", context)

# @permission_required("pacApp.add_ad_request")
@login_required
@user_passes_test(must_be_pac, login_url='/notpac', redirect_field_name=None)
def adminForm(request):

    context = {}
    context['company_req_1'] = CompanyRequest.objects.filter(company_choice_num=1, scheduled=0)
    context['company_req_2'] = CompanyRequest.objects.filter(company_choice_num=2, scheduled=0)
    context['company_req_3'] = CompanyRequest.objects.filter(company_choice_num=3, scheduled=0)
    context['reho_req'] = RehearsalRequest.objects.all()
    context['all_requests'] = ADRequest.objects.all()
    context['groups'] = Group.objects.all()
    context['has_report'] = 'False'

    # for item in context['all_requests']:
    #	print(item.name)
    return render(request, "templates/pacApp/form/adminForm.html", context)


def get_ranks(bloomberg_rank, dillon_dance_rank, dillon_mar_rank, dillon_mpr_rank, murphy_rank, ns_rank, ns_warmup_rank, ns_theatre_rank, whitman_rank, wilcox_rank):
    studio_ranking = {'bloomberg': bloomberg_rank, 'dillondance': dillon_dance_rank, 'dillonmar': dillon_mar_rank, 
    'dillonmpr': dillon_mpr_rank, 'murphy': murphy_rank, 'ns': ns_rank, 'nswarmup': ns_warmup_rank, 
    'nstheatre': ns_theatre_rank, 'whitman': whitman_rank, 'wilcox': wilcox_rank}

    sorted_studio = sorted(studio_ranking.items(), key=lambda x: x[1])
    rank_1 = sorted_studio[0][0]
    rank_2 = sorted_studio[1][0]
    rank_3 = sorted_studio[2][0]
    rank_4 = sorted_studio[3][0]
    rank_5 = sorted_studio[4][0]
    rank_6 = sorted_studio[5][0]
    rank_7 = sorted_studio[6][0]
    rank_8 = sorted_studio[7][0]
    rank_9 = sorted_studio[8][0]
    rank_10 = sorted_studio[9][0]

    return rank_1, rank_2, rank_3, rank_4, rank_5, rank_6, rank_7, rank_8, rank_9, rank_10

def delete_schedule_alg(response):
    print('in delete schedule alg')
    try:
        slots_to_del = Booking.objects.filter(from_alg=1)
        print(slots_to_del)
        slots_to_del.delete()
    except:
        print('not able to drop scheduling alg')
    return redirect('../../adminForm')


def scheduling_alg(request: HttpResponse):

    start_date = request.POST['start_date']
    end_date = request.POST['end_date']
    print(start_date, end_date)
  
    # get everything in db
    all_requests = RehearsalRequest.objects.all()
    company1 = CompanyRequest.objects.filter(company_choice_num=1)
    company2 = CompanyRequest.objects.filter(company_choice_num=2)
    company3 = CompanyRequest.objects.filter(company_choice_num=3)

    if (RehearsalRequest.objects.count() == 0):
         results = 'None'
         context = {}
         context['results'] = results
         return render(request, "templates/pacApp/form/adminForm.html", context)
    

    studioList = {'bloomberg': 0, 'dillondance': 1, 'dillonmar': 2, 'dillonmpr': 3,
                  'murphy': 4, 'ns': 5, 'nswarmup': 6, 'nstheatre': 7, 'whitman': 8, 'wilcox': 9}
    studios = list(studioList.keys())

    groups_list = ['BAC', 'Bhangra', 'BodyHype', 'Disiac', 'eXpressions', 'HighSteppers',
                        'Kokopops', 'Naacho', 'PUB', 'Six14', 'Sympoh', 'Triple8']

    df_request = pd.DataFrame(data=None, columns=['name', 
    'company_day_1', 'company_start_time_1', 'company_end_time_1', 'company_studio_1',
    'company_day_2', 'company_start_time_2', 'company_end_time_2', 'company_studio_2',
    'company_day_3', 'company_start_time_3', 'company_end_time_3', 'company_studio_3',
    'rank_1', 'rank_2',  'rank_3',  'rank_4', 'rank_5',
    'rank_6', 'rank_7',  'rank_8',  'rank_9', 'rank_10',
    'num_reho', 'num_members'])

    for group in all_requests:
        rank_1 = studios[group.rank_1] 
        rank_2 = studios[group.rank_2] 
        rank_3 = studios[group.rank_3] 
        rank_4 = studios[group.rank_4]  
        rank_5 = studios[group.rank_5] 
        rank_6 = studios[group.rank_6]  
        rank_7 = studios[group.rank_7]  
        rank_8 = studios[group.rank_8] 
        rank_9 = studios[group.rank_9] 
        rank_10 = studios[group.rank_10]  

        for comp_1 in company1:
            if (comp_1.request_id_id == group.request_id):
                company_day_1 = comp_1.company_day
                company_start_time_1 = comp_1.company_start_time
                company_end_time_1 = comp_1.company_end_time
                company_studio_1 = studios[comp_1.company_studio_id]
                break
                
        for comp_2 in company2:
            if (comp_2.request_id_id == group.request_id):
                company_day_2 = comp_2.company_day
                company_start_time_2 = comp_2.company_start_time
                company_end_time_2 = comp_2.company_end_time
                company_studio_2 = studios[comp_2.company_studio_id]
                break
                
        for comp_3 in company3:
            if (comp_3.request_id_id == group.request_id):
                company_day_3 = comp_3.company_day
                company_start_time_3 = comp_3.company_start_time
                company_end_time_3 = comp_3.company_end_time
                company_studio_3 = studios[comp_3.company_studio_id]
                break
                
        group_request = pd.DataFrame(data={'name': [group.group_id_id], 
        'company_day_1': [company_day_1], 'company_start_time_1': [company_start_time_1], 'company_end_time_1': [company_end_time_1], 'company_studio_1': [company_studio_1],
        'company_day_2': [company_day_2], 'company_start_time_2': [company_start_time_2], 'company_end_time_2': [company_end_time_2], 'company_studio_2': [company_studio_2],
        'company_day_3': [company_day_3], 'company_start_time_3': [company_start_time_3], 'company_end_time_3': [company_end_time_3], 'company_studio_3': [company_studio_3],
        'rank_1': rank_1, 'rank_2': rank_2, 'rank_3': rank_3, 'rank_4': rank_4, 'rank_5': rank_5, 
        'rank_6': rank_6, 'rank_7': rank_7, 'rank_8': rank_8, 'rank_9': rank_9, 'rank_10': rank_10, 
        'num_reho': [group.num_reho], 'num_members': [group.member_size]})
        df_request = pd.concat([group_request, df_request],
                               ignore_index=True, sort=False)


    df_results = pd.DataFrame(
        data=None, columns=['Name', 'Studio', 'Day', 'Start_Time', 'End_Time', 'Booking_Date'])

    # fill in the unavailable times for each studio
    unavailable = {}

    days_of_week = ['Monday', 'Tuesday', 'Wednesday',
                    'Thursday', 'Friday', 'Saturday', 'Sunday']
    groups = df_request['name']

    # given a list hours, return the dictionary that gives initial availability of each day
    def get_init_avail(hours):
        hours_dance_stud_num = []
        for item in studios:
            hours_dance_stud_num.append(copy.deepcopy(hours))
        initial_availability = dict(
            zip(copy.deepcopy(studios), copy.deepcopy(hours_dance_stud_num)))
        return initial_availability

    # create avail a dictionary that stores the times the dance studios are free
    # initial_availability = dict(zip(copy.deepcopy(dance_studios), copy.deepcopy(hours_dance_stud_num)))
    # avail is a dictionary containing a dictionary for each day of the week.
    # the day of the week dictionary has studios as its keys and then 0:24 hours that it is available

    avail = {}
    for day in copy.deepcopy(days_of_week):
        hours = [i for i in range(0, 24)]
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

    #group_info=df_request[df_request.name=='BAC']
	#studio = group_info.iloc[:, df_request.columns.get_loc('company_studio')].values[0]
	#day = group_info.iloc[:, df_request.columns.get_loc('company_day')].values[0]
	#start_time = group_info.iloc[:, df_request.columns.get_loc('company_start_time')].values[0]
	#end_time = group_info.iloc[:, df_request.columns.get_loc('company_end_time')].values[0]
	

    #df_results[df_results.Studio == "NS Main"]

    # randomize the rows of the dataframe
    df_request = df_request.sample(frac=1).reset_index(drop=True)

    # for each group, schedule the company rehearsal space
    for group in df_request['name']:
        group_info = df_request[df_request.name == group]
        studio = group_info.iloc[:, df_request.columns.get_loc(
            'company_studio_1')].values[0]
        day = group_info.iloc[:, df_request.columns.get_loc(
            'company_day_1')].values[0]
        start_time = group_info.iloc[:, df_request.columns.get_loc(
            'company_start_time_1')].values[0]
        end_time = group_info.iloc[:, df_request.columns.get_loc(
            'company_end_time_1')].values[0]
        # if conflict --> conflict can just be a try/except thing
        # cant do times from 23-1
        # remove times from list

        # if the company time is already booked
        if ((int(start_time) not in avail[day][studio]) or 
		(int(start_time)+1 not in avail[day][studio]) or 
		(int(start_time)+1 not in avail[day][studio])):
            studio = group_info.iloc[:, df_request.columns.get_loc(
                'company_studio_2')].values[0]
            day = group_info.iloc[:, df_request.columns.get_loc(
                'company_day_2')].values[0]
            start_time = group_info.iloc[:, df_request.columns.get_loc(
                'company_start_time_2')].values[0]
            end_time = group_info.iloc[:, df_request.columns.get_loc(
                'company_end_time_2')].values[0]

        if ((int(start_time) not in avail[day][studio]) or 
		(int(start_time)+1 not in avail[day][studio]) or 
		(int(start_time)+1 not in avail[day][studio])):
            studio = group_info.iloc[:, df_request.columns.get_loc(
                'company_studio_3')].values[0]
            day = group_info.iloc[:, df_request.columns.get_loc(
                'company_day_3')].values[0]
            start_time = group_info.iloc[:, df_request.columns.get_loc(
                'company_start_time_3')].values[0]
            end_time = group_info.iloc[:, df_request.columns.get_loc(
                'company_end_time_3')].values[0]

        # add the company time to df and remove from available times
        (avail[day][studio]).remove(int(start_time))
        (avail[day][studio]).remove(int(start_time)+1)
        (avail[day][studio]).remove(int(start_time)+2)
        group_results = pd.DataFrame(data={'Name': [group],
                                           'Studio': [studioList[studio]],
                                           'Day': [day],
                                           'Start_Time': [start_time],
                                           'End_Time': [int(end_time)+1],
                                           'Booking_Date': [None]})

        df_results = pd.concat([group_results, df_results],
                               ignore_index=True, sort=False)

    """Cycle through the list of requests until everyone's requests are filled"""

    # while there are still spaces to book
    while (int(max(reho_count.values())) > 0):
        # randomize the order of groups
        for group in groups.sample(frac=1):
            # print(group)
            # if the group still has spaces to book, book a space
            if reho_count[group] != 0:
                group_info = df_request[df_request.name == group]
                rank_1 = group_info.iloc[:, df_request.columns.get_loc(
                    'rank_1')].values[0]
                rank_2 = group_info.iloc[:, df_request.columns.get_loc(
                    'rank_2')].values[0]
                rank_3 = group_info.iloc[:, df_request.columns.get_loc(
                    'rank_3')].values[0]
                rank_4 = group_info.iloc[:, df_request.columns.get_loc(
                    'rank_4')].values[0]
                rank_5 = group_info.iloc[:, df_request.columns.get_loc(
                    'rank_5')].values[0]
                rank_6 = group_info.iloc[:, df_request.columns.get_loc(
                    'rank_6')].values[0]
                rank_7 = group_info.iloc[:, df_request.columns.get_loc(
                    'rank_7')].values[0]
                rank_8 = group_info.iloc[:, df_request.columns.get_loc(
                    'rank_8')].values[0]
                rank_9 = group_info.iloc[:, df_request.columns.get_loc(
                    'rank_9')].values[0]
                rank_10 = group_info.iloc[:, df_request.columns.get_loc(
                    'rank_10')].values[0]
                # if conflict --> conflict can just be a try/except thing
                # cant do times from 23-1
                # remove times from list

                # pick a random day
                random.shuffle(days_of_week)
                day = days_of_week[0]
                studio = rank_1
                times_to_pick_from = [i for i in avail[day][studio] if (
                    i > 0 and ((i+1) in avail[day][studio]))]
                if (sum(times_to_pick_from) == 0):
                    print('in rank 2')
                    studio = rank_2
                    times_to_pick_from = [i for i in avail[day][studio] if (
                        i > 0 and ((i+1) in avail[day][studio]))]
                    if (sum(times_to_pick_from) == 0):
                        print('in rank 3')
                        studio = rank_3
                        times_to_pick_from = [i for i in avail[day][studio] if (
                            i > 0 and ((i+1) in avail[day][studio]))]
                        if (sum(times_to_pick_from) == 0):
                            print('in rank 4')
                            studio = rank_4
                            times_to_pick_from = [i for i in avail[day][studio] if (
                                i > 0 and ((i+1) in avail[day][studio]))]
                            if (sum(times_to_pick_from) == 0):
                                print('in rank 5')
                                studio = rank_5
                                times_to_pick_from = [i for i in avail[day][studio] if (
                                    i > 0 and ((i+1) in avail[day][studio]))]
                                if (sum(times_to_pick_from) == 0):
                                    print('in rank 6')
                                    studio = rank_6
                                    times_to_pick_from = [i for i in avail[day][studio] if (
                                        i > 0 and ((i+1) in avail[day][studio]))]
                                    if (sum(times_to_pick_from) == 0):
                                        print('in rank 7')
                                        studio = rank_7
                                        times_to_pick_from = [i for i in avail[day][studio] if (
                                            i > 0 and ((i+1) in avail[day][studio]))]
                                        if (sum(times_to_pick_from) == 0):
                                            print('in rank 8')
                                            studio = rank_8
                                            times_to_pick_from = [i for i in avail[day][studio] if (
                                                i > 0 and ((i+1) in avail[day][studio]))]
                                            if (sum(times_to_pick_from) == 0):
                                                print('in rank 9')
                                                studio = rank_9
                                                times_to_pick_from = [i for i in avail[day][studio] if (
                                                    i > 0 and ((i+1) in avail[day][studio]))]
                                                if (sum(times_to_pick_from) == 0):
                                                    print('in rank 10')
                                                    studio = rank_10
                                                    times_to_pick_from = [i for i in avail[day][studio] if (
                                                        i > 0 and ((i+1) in avail[day][studio]))]
                                                    if (sum(times_to_pick_from) == 0):
                                                        print('NO MORE SPACES LEFT. THROW ERROR')
                                                        break


                #### COME BACK HERE NICOLE. What to do if there's absolutely no studio left?!?!
                
                print('times to pick from: ', times_to_pick_from)
                print('studio: ', studio)
                start_time = times_to_pick_from[0]
                
                (avail[day][studio]).remove(int(start_time))
                (avail[day][studio]).remove(int(start_time)+1)

                group_results = pd.DataFrame(data={'Name': [group],
                                                   'Studio': [studioList[studio]],
                                                   'Day': [day],
                                                   'Start_Time': [int(start_time)],
                                                   'End_Time': [int(start_time)+2],
                                                   'Booking_Date': [None]})
                                                   
                df_results = pd.concat(
                    [group_results, df_results], ignore_index=True, sort=False)
                reho_count[group] -= 1

    # studioList = dict(zip(dance_studios, list(range(0, 10))))
    daysList = dict(zip(days_of_week, range(0, 7)))

    # based on the dates specified
    
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    print(start_date, end_date)
    diff = end_date-start_date
    weeks = abs(math.ceil(diff.days/7))
    
    print(weeks)

    

    user_netid = request.user.uniauth_profile.get_display_id()
    for week in range(weeks):
        for i, space in df_results.iterrows():
            book = Booking(studio_id_id=space['Studio'],
                        group_id_id=int(space['Name']),
                        from_alg = 1,
                        group_name=groups_list[int(space['Name'])-1],
                        start_time=space['Start_Time'],
                        end_time=space['End_Time'],
                        week_day=daysList[space['Day']],
                        user_netid=str(user_netid),
                        booking_date=(start_date + timedelta(days=(week*6))))
            book.save()

    context = {}
    context['start_date'] = start_date
    context['company_req_1'] = CompanyRequest.objects.filter(company_choice_num=1, scheduled=0)
    context['company_req_2'] = CompanyRequest.objects.filter(company_choice_num=2, scheduled=0)
    context['company_req_3'] = CompanyRequest.objects.filter(company_choice_num=3, scheduled=0)
    context['reho_req'] = RehearsalRequest.objects.all()
    context['all_requests'] = ADRequest.objects.all()
    context['groups'] = Group.objects.all()
    context['has_report'] = 'True'
    context['report'] = 'report words!'
    print(context['report'])

    # for item in context['all_requests']:
    #	print(item.name)
    return render(request, "templates/pacApp/form/adminForm.html", context)
    # return render(request, "templates/pacApp/tableElements/calendar.html", context)
    # return redirect('../../schedule')
    # return redirect('../../adminForm')