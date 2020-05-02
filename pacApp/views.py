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
from . import models, studio, hours
from .models import ADRequest, Booking
from .studio import Studio
import datetime
from datetime import date, timedelta
import pandas as pd
import numpy as np
import copy
import random
import calendar
# from uniauth.models import Institution, InstitutionAccount, LinkedEmail


# Create your views here.
# our home page


def error_404(request, exception):
    data = {}
    return render(request, 'templates/pacApp/404.html', data)


def error_500(request):
    data = {}
    return render(request, 'templates/pacApp/404.html', data)


def createContext(startdate, endweek, newdate, groups, getGroups):
    actualdate = date.today()
    currday = 'None'
    week = {}
    for i in range(7):
        # week.append((startdate + timedelta(days=i)).strftime('%Y-%m-%d-%w'))
        week[(startdate + timedelta(days=i)).strftime('%w')
             ] = (startdate + timedelta(days=i)).strftime('%Y-%m-%d')
        if (startdate + timedelta(days=i)).strftime('%Y-%m-%d') == actualdate.strftime('%Y-%m-%d'):
            currday = actualdate.strftime('%w')
    # print(week)

    studioList = {'bloomberg': 0, 'dillondance': 1, 'dillonmar': 2, 'dillonmpr': 3,
                  'murphy': 4, 'ns': 5, 'nswarmup': 6, 'nstheatre': 7, 'whitman': 8, 'wilcox': 9}
    # filter by date range, but not sure where the date should be coming from
    # creating context for each day of the week plus the data
    if isinstance(newdate, str):
        print('str')
        formatdate = newdate.split(
            '-')[0] + '-' + newdate.split('-')[1] + '-' + newdate.split('-')[2]
        #formatdate = datetime.strptime(newdate, "%Y-%m-%d") 
        #formatdate = formatdate.strftime('%Y-%m-%d')
        print(formatdate)
    else:
        print('date')

        # formatdate = str(newdate.year) + '-' + str(newdate.month) + '-' + str(newdate.day)
        formatdate = newdate.strftime('%Y-%m-%d')
        print(formatdate)
    # we would want these to be for those that are shaded 
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
               'currday': currday,
               'mon': week['1'], 'tue': week['2'], 'wed': week['3'],
               'thu': week['4'], 'fri': week['5'], 'sat': week['6']}
    # want to gather whatever is not shaded
    if getGroups == True:
        bloombergNew = context['Bloomberg'].filter(company_name__in=groups)
        bloombergGray = context['Bloomberg'].exclude(company_name__in=groups)
        context['Bloomberg'] = bloombergNew
        context['BloombergGray'] = bloombergGray

        dillonDanceNew = context['DillonDance'].filter(company_name__in=groups)
        dillonDanceGray = context['DillonDance'].exclude(company_name__in=groups)
        context['DillonDance'] = dillonDanceNew
        context['DillonDanceGray'] = dillonDanceGray


        dillonMARNew = context['DillonMAR'].filter(company_name__in=groups)
        dillonMARGray = context['DillonMAR'].exclude(company_name__in=groups)
        context['DillonMAR'] = dillonMARNew
        context['DillonMARGray'] = dillonMARGray

        dillonMPRNew = context['DillonMPR'].filter(company_name__in=groups)
        dillonMPRGray = context['DillonMPR'].exclude(company_name__in=groups)
        context['DillonMPR'] = dillonMPRNew
        context['DillonMPRGray'] = dillonMPRGray
        
      
        murphyNew = context['Murphy'].filter(company_name__in=groups)
        murphyGray = context['Murphy'].exclude(company_name__in=groups)
        context['Murphy'] = murphyNew
        context['MurphyGray'] = murphyGray

        nsNew = context['NewSouth'].filter(company_name__in=groups)
        nsGray = context['NewSouth'].exclude(company_name__in=groups)
        context['NewSouth'] = nsNew
        context['NewSouthGray'] = nsGray

        nsWarmNew = context['NSWarmup'].filter(company_name__in=groups)
        nsWarmGray = context['NSWarmup'].exclude(company_name__in=groups)
        context['NSWarmup'] = nsWarmNew
        context['NSWarmupGray'] = nsWarmGray
       
        nsTNew = context['NSTheatre'].filter(company_name__in=groups)
        nsTGray = context['NSTheatre'].exclude(company_name__in=groups)
        context['NSTheatre'] = nsTNew
        context['NSTheatreGray'] = nsTGray
        
        whitNew = context['Whitman'].filter(company_name__in=groups)
        whitGray = context['Whitman'].exclude(company_name__in=groups)
        context['Whitman'] = whitNew
        context['WhitmanGray'] = whitGray

        wilNew = context['Wilcox'].filter(company_name__in=groups)
        wilGray = context['Wilcox'].exclude(company_name__in=groups)
        context['Wilcox'] = wilNew
        context['WilcoxGray'] = wilGray

    return context


def carouselAvailable():
    startdate = date.today()
    currenttime = int(datetime.datetime.now().time().hour)
    # print(currenttime)
    notfree = Booking.objects.filter(start_time__exact=currenttime).filter(
        booking_date__exact=startdate)

    studioList = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    for i in notfree:
        studioList[i.studio_id] = 0

    # print(studioList)

    return studioList

# rendering the home page with today's date


def homepage(request):
    try:
        profile = request.user.uniauth_profile.get_display_id()
    except:
        profile = 'None'
    print(profile)
    startdate = date.today()
    print(startdate)
    endweek = startdate + timedelta(days=6)
    groups = None
    getGroups = False
    context = createContext(startdate, endweek, startdate.strftime(
        '%Y-%m-%d'), groups, getGroups)
    context['currentdate'] = startdate.strftime('%Y-%m-%d')
    context['editable'] = False
    context['cursor'] = 'not'
    context['available'] = carouselAvailable()
    context['user'] = profile
    return render(request, "templates/pacApp/home.html", context)

# displays the calendar schedule


def about(request):
    context = {}
    return render(request, "templates/pacApp/about.html", context)


@login_required
def schedule(request):
    # render with today's date
    profile = request.user.uniauth_profile.get_display_id()
    print(profile)
    startdate = date.today()
    endweek = startdate + timedelta(days=6)
    groups = None
    getGroups = False
    context = createContext(startdate, endweek, startdate, groups, getGroups)
    context['currentdate'] = startdate.strftime('%Y-%m-%d')
    context['editable'] = True
    context['cursor'] = "pointer"
    context['user'] = profile
    return render(request, "templates/pacApp/schedule.html", context)


def create_booking(date, studio, name, starttime, endtime, day, profile):
    studioList = {'bloomberg': 0, 'dillondance': 1, 'dillonmar': 2, 'dillonmpr': 3,
                  'murphy': 4, 'ns': 5, 'nswarmup': 6, 'nstheatre': 7, 'whitman': 8, 'wilcox': 9}
    date = date.split('-')
    bookExist = Booking.objects.filter(studio_id=studioList[studio]).filter(booking_date=(datetime.date(int(date[0]), int(date[1]), int(date[2]))))
    bookExist = bookExist.filter(start_time=starttime).filter(end_time=endtime).filter(week_day=day)
    if bookExist.exists():
      print('bad already here')
      return -200
    else:
      book = Booking(studio_id=studioList[studio],
                   company_id=0,
                   user_netid=profile,
                   company_name=name,
                   start_time=starttime,
                   end_time=endtime,
                   week_day=day,
                   booking_date=(datetime.date(int(date[0]), int(date[1]), int(date[2]))))
      book.save()
      return book.week_day


def update(request: HttpResponse):
    # if there is a booking involved

    weekday = None
    # tries to see if user is logged in, which they must be in order to update
    try:
      profile = request.user.uniauth_profile.get_display_id()
    except:
      profile='None'
    # if this is not None, means we must be making a booking update 
    # create a booking 
    if (request.GET.get('studio') != None):
        weekday = create_booking(request.GET.get('date'), request.GET.get('studio'),
                                 request.GET.get('name'), request.GET.get(
                                     'starttime'),
                                 request.GET.get('endtime'), request.GET.get('day'), profile)

    retdate = request.GET.get('newdate').split('-')
    startdate = datetime.date(int(retdate[0]), int(retdate[1]), int(retdate[2]))
    endweek = startdate + timedelta(days=6)
    newdate = request.GET.get('newdate')
    # if there are groups 
    groups = request.GET.get('selectgroups')
    if (groups == 'None' or groups == None):
        groups = None
        getGroups = False
    else:
        groups = groups.split('-')
        # the first one is a -
        groups.pop(-1)
        getGroups = True
    # creating context with given startdate, endweek, newdate 
    context = createContext(startdate, endweek, newdate, groups, getGroups)
    # if booking did not fail and weekday is not none 
    if weekday != None and weekday != -200:
        context['success'] = 'True'
        # context['weekday'] = weekday
    groupday = request.GET.get('groupday')

    if weekday == None and groupday != None:
      context['weekday'] = groupday
      context['success'] = 'group'
    # if endweek < date.today():
    context['editable'] = request.GET.get('editable')
    context['user'] = profile
    # this is the currently active 
    
    if weekday == -200:
          weekday = request.GET.get('day')
          context['weekday'] = groupday
          context['success'] = 'False'
   
    return render(request, "templates/pacApp/tableElements/table.html", context)


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

# preparation to drop the space


def drop_space(request: HttpResponse):

    print('in drop space')

    # get variables from post resuts
    studio = request.POST['studio']
    date = request.POST['date']  # booking date
    starttime = request.POST['starttime']
    endtime = request.POST['endtime']
    day = request.POST['day']  # weekday
    name = request.POST['name']
    groups = request.POST['selectgroups']
    profile = request.user.uniauth_profile.get_display_id()
    currday = request.POST['currday']

    if (groups == 'None' or groups == None):
        groups = None
        getGroups = False
    else:
        groups = groups.split('-')
        groups.pop(-1)
        getGroups = True

    y, m, d = handledate(date)  # format the date

    # delete the booking from the db
    delete_booking(y, m, d, studio, name, starttime, endtime, day, profile)
    print('day: ' + day)
    # create context
    startdate = datetime.date(int(y), int(m), (int(d)))

    endweek = startdate + timedelta(days=(6 - int(day)))
    startdate = startdate + timedelta(days=(-int(day)))
    # groups = None
    # getGroups = False

    context = createContext(startdate, endweek, startdate, groups, getGroups)

    context['weekday'] = day
    context['editable'] = True
    context['user'] = profile
    context['formatdate'] = currday

    return render(request, "templates/pacApp/tableElements/table.html", context)
    # return JsonResponse({"error": ""}, status=400)

# delete the booking


def delete_booking(y, m, d, studio, name, starttime, endtime, day, profile):
    print('in delete booking')
    studioList = {'bloomberg': 0, 'dillondance': 1, 'dillonmar': 2, 'dillonmpr': 3,
                  'murphy': 4, 'ns': 5, 'nswarmup': 6, 'nstheatre': 7, 'whitman': 8, 'wilcox': 9}

    print(y, m, d)

    # grab the booking you want to delete
    try:
        book_to_del = Booking.objects.get(studio_id=studioList[studio],
                                          company_id=0,
                                          user_netid=profile,
                                          company_name=name,
                                          start_time=starttime,
                                          end_time=endtime,
                                          week_day=day,
                                          booking_date=(datetime.date(int(y), int(m), int(d))))
        book_to_del.delete()
    except:
        print('not able to drop')
    return day

def drop_ad_request(request: HttpResponse):
    name = request.GET.get('company_name')
    delete_ad_request(name)
    return redirect('../../adminForm')

def delete_ad_request(name):
    print('in delete ad request')
    # grab the booking you want to delete
    try:
        req_to_del = ADRequest.objects.filter(company_name=name)
        req_to_del.delete()
    except:
        print('not able to drop')
    return

def insert_space_item(request: HttpResponse):
    return redirect('/schedule')


def grab_time(time_val):
    return int(time_val[0:2])


def insert_ad_request(request: HttpResponse):

    company_start_time_1 = grab_time(request.POST['company_start_time_1'])
    company_end_time_1 = grab_time(request.POST['company_end_time_1'])
    company_start_time_2 = grab_time(request.POST['company_start_time_2'])
    company_end_time_2 = grab_time(request.POST['company_end_time_2'])
    company_start_time_3 = grab_time(request.POST['company_start_time_3'])
    company_end_time_3 = grab_time(request.POST['company_end_time_3'])

    ad_req = ADRequest(company_name=request.POST['company_name'],
                       company_day_1=request.POST.get('company_day_1'),
                       company_start_time_1=company_start_time_1,
                       company_end_time_1=company_end_time_1,
                       company_studio_1=request.POST.get('company_studio_1'),
                       company_day_2=request.POST.get('company_day_2'),
                       company_start_time_2=company_start_time_2,
                       company_end_time_2=company_end_time_2,
                       company_studio_2=request.POST.get('company_studio_2'),
                       company_day_3=request.POST.get('company_day_3'),
                       company_start_time_3=company_start_time_3,
                       company_end_time_3=company_end_time_3,
                       company_studio_3=request.POST.get('company_studio_3'),
                       num_reho=request.POST['num_reho'],
                       company_size=request.POST['num_members'],
                       bloomberg_rank=request.POST['bloomberg_rank'],
                       dillon_dance_rank=request.POST['dillon_dance_rank'],
                       dillon_mar_rank=request.POST['dillon_mar_rank'],
                       dillon_mpr_rank=request.POST['dillon_mpr_rank'],
                       murphy_rank=request.POST['murphy_rank'],
                       ns_rank=request.POST['ns_rank'],
                       ns_warmup_rank=request.POST['ns_warmup_rank'],
                       ns_theatre_rank=request.POST['ns_theatre_rank'],
                       whitman_rank=request.POST['whitman_rank'],
                       wilcox_rank=request.POST['wilcox_rank'])

    ad_req.save()
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
    context = {'all_requests': ADRequest.objects.all()}
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
        slots_to_del = Booking.objects.filter(company_id=1)
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
    all_requests = ADRequest.objects.all()

    studioList = {'bloomberg': 0, 'dillondance': 1, 'dillonmar': 2, 'dillonmpr': 3,
                  'murphy': 4, 'ns': 5, 'nswarmup': 6, 'nstheatre': 7, 'whitman': 8, 'wilcox': 9}
    studios = list(studioList.keys())

    df_request = pd.DataFrame(data=None, columns=['name', 
    'company_day_1', 'company_start_time_1', 'company_end_time_1', 'company_studio_1',
    'company_day_2', 'company_start_time_2', 'company_end_time_2', 'company_studio_2',
    'company_day_3', 'company_start_time_3', 'company_end_time_3', 'company_studio_3',
    'rank_1', 'rank_2',  'rank_3',  'rank_4', 'rank_5',
    'rank_6', 'rank_7',  'rank_8',  'rank_9', 'rank_10',
    'num_reho', 'num_members'])

    for group in all_requests:
        rank_1, rank_2, rank_3, rank_4, rank_5, rank_6, rank_7, rank_8, rank_9, rank_10 = get_ranks(group.bloomberg_rank, 
                group.dillon_dance_rank, group.dillon_mar_rank, group.dillon_mpr_rank, 
                group.murphy_rank, group.ns_rank, group.ns_warmup_rank, group.ns_theatre_rank, 
                group.whitman_rank, group.wilcox_rank)
        group_request = pd.DataFrame(data={'name': [group.company_name], 
        'company_day_1': [group.company_day_1], 'company_start_time_1': [group.company_start_time_1], 'company_end_time_1': [group.company_end_time_1], 'company_studio_1': [group.company_studio_1],
        'company_day_2': [group.company_day_2], 'company_start_time_2': [group.company_start_time_2], 'company_end_time_2': [group.company_end_time_2], 'company_studio_2': [group.company_studio_2],
        'company_day_3': [group.company_day_3], 'company_start_time_3': [group.company_start_time_3], 'company_end_time_3': [group.company_end_time_3], 'company_studio_3': [group.company_studio_3],
        'rank_1': rank_1, 'rank_2': rank_2, 'rank_3': rank_3, 'rank_4': rank_4, 'rank_5': rank_5, 
        'rank_6': rank_6, 'rank_7': rank_7, 'rank_8': rank_8, 'rank_9': rank_9, 'rank_10': rank_10, 
        'num_reho': [group.num_reho], 'num_members': [group.company_size]})
        df_request = pd.concat([group_request, df_request],
                               ignore_index=True, sort=False)

    df_results = pd.DataFrame(
        data=None, columns=['Name', 'Studio', 'Day', 'Start_Time', 'End_Time', 'Booking_Date'])

    # fill in the unavailable times for each studio
    unavailable = {}

    # dance_studios = ['wilcox', 'bloomberg', 'dillondance', 'dillonmar',
                     # 'dillonmpr', 'whitman', 'murphy', 'ns', 'nswarmup', 'nstheatre']
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
    for week in range(weeks):
        for i, space in df_results.iterrows():
            book = Booking(studio_id=space['Studio'],
                        company_id=1,
                        company_name=space['Name'],
                        start_time=space['Start_Time'],
                        end_time=space['End_Time'],
                        week_day=daysList[space['Day']],
                        booking_date=(start_date + timedelta(days=(week*6))))
            book.save()

    return redirect('../../adminForm')