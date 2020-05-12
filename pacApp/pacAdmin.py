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
from .models import ADRequest, Booking, CompanyRequest, RehearsalRequest, Group, Studio
import datetime
from datetime import date, timedelta
import pandas as pd
import numpy as np
import copy
import random
import calendar
import json
from .utils import studentInfo, handleDateStr, handleGroup, handledate, get_range, get_duration,  must_be_pac
from .create import createContext, create_booking, delete_booking
# from uniauth.models import Institution, InstitutionAccount, LinkedEmail

# Create your views here.
# our home page

# 
def drop_ad_request(request: HttpResponse):
    request_id = request.GET.get('id')
    print(request_id)
    delete_ad_request(request_id)
    # return render(request, "templates/pacApp/form/adminForm.html", context)
    return redirect('../../adminForm')

def delete_ad_request(request_id):

    print('in delete ad request, deleting', request_id)
    # grab the booking you want to delete
    '''
    reho_req_to_del = RehearsalRequest.objects.get(request_id=request_id)
    
    print(reho_req_to_del.request_id)
    co_req_1 = CompanyRequest.objects.get(request_id_id=request_id, company_choice_num=1)
    co_req_2 = CompanyRequest.objects.filter(request_id_id=request_id, company_choice_num=2)
    co_req_3 = CompanyRequest.objects.filter(request_id_id=request_id, company_choice_num=3)
    
    print(co_req_1.request_id_id)

    co_req_1.delete()
    co_req_2.delete()
    co_req_3.delete()
 
    reho_req_to_del.delete()'''
  
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

'''
def check_dup_group(request: HttpResponse):
    groups_in_db = list(RehearsalRequest.objects.values_list('group_id_id', flat=True).filter(scheduled=0))
    print(groups_in_db)
    if request.POST['company_name'] in groups_in_db:

'''

def renew_schedule(request: HttpResponse):

    CompanyRequest.objects.filter(company_choice_num=1, scheduled=0).update(scheduled=2)
    CompanyRequest.objects.filter(company_choice_num=2, scheduled=0).update(scheduled=2)
    CompanyRequest.objects.filter(company_choice_num=3, scheduled=0).update(scheduled=2)
    RehearsalRequest.objects.filter(scheduled=0).update(scheduled=2)

    return redirect('/adminForm')

def handle_1ams(time):
    if int(time)==1: return 25
    else: return time


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

    company_end_time_1=handle_1ams(company_end_time_1)
    company_end_time_2=handle_1ams(company_end_time_2)
    company_end_time_3=handle_1ams(company_end_time_3)

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




# @permission_required("pacApp.add_ad_request")
@login_required
@user_passes_test(must_be_pac, login_url='/notpac', redirect_field_name=None)
def adminForm(request):

    context = {}
    context['company_req_1'] = CompanyRequest.objects.filter(company_choice_num=1, scheduled=0)
    context['company_req_2'] = CompanyRequest.objects.filter(company_choice_num=2, scheduled=0)
    context['company_req_3'] = CompanyRequest.objects.filter(company_choice_num=3, scheduled=0)
    context['reho_req'] = RehearsalRequest.objects.filter(scheduled=0)
    context['all_requests'] = ADRequest.objects.all()
    context['groups'] = Group.objects.all()
    context['studios'] = Studio.objects.all()
    context['has_report'] = 'False'
    # gets the netid
    profile = request.user.uniauth_profile.get_display_id()
    # gets via tiger book the info about person given netid
    studentDets = studentInfo(profile)
    context['firstname'] = profile
    if studentDets != None:
      first_name = studentDets['first_name']
      context['firstname'] = first_name

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

def delete_schedule_alg(request: HttpResponse):
    print('in delete schedule alg')
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']

    all_requests = RehearsalRequest.objects.filter(scheduled=1)
    company1 = CompanyRequest.objects.filter(company_choice_num=1, scheduled=1)
    company2 = CompanyRequest.objects.filter(company_choice_num=2, scheduled=1)
    company3 = CompanyRequest.objects.filter(company_choice_num=3, scheduled=1)

    context = {}

    start_date_new = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date_new = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    print(start_date_new, end_date_new)
    diff = end_date_new-start_date_new
    weeks = abs(math.ceil(diff.days/7))

    delta = end_date_new - start_date_new       # as timedelta


    try:
        total_to_del = 0
        for i in range(delta.days + 1):
            day = start_date_new + timedelta(days=i)
            print(day)
            slots_to_del = Booking.objects.filter(from_alg=1, booking_date = day)
            total_to_del += slots_to_del.count()
            print(slots_to_del)
            slots_to_del.delete()
        if total_to_del==0:
            report = ['The scheduling algorithm has not scheduled slots on the calendar yet for the dates you specified. Please edit the date range or click "Schedule All Groups". ']
            context['success'] = 'False'
        else:

            report = ['Deleted all groups from ' + str(start_date) + ' to ' + str(end_date) + '. The requests will show up again in Step 2.' ]
            
            for group in all_requests:
                (RehearsalRequest.objects.filter(request_id=group.request_id)).update(scheduled=0)

            for group in company1:
                CompanyRequest.objects.filter(company_choice_num=1, request_id_id=group.request_id_id).update(scheduled=0)

            for group in company2:
                CompanyRequest.objects.filter(company_choice_num=2, request_id_id=group.request_id_id).update(scheduled=0)

            for group in company3:
                CompanyRequest.objects.filter(company_choice_num=3, request_id_id=group.request_id_id).update(scheduled=0) 
            context['success'] = 'True'
        
    except:
        print('not able to drop scheduling alg')
        report = ['Not able to drop the spaces in the dates specified. Please edit the date range to include weeks that have spaces scheduled.']
        context['success']='False'

    context['start_date'] = start_date
    context['has_report'] = 'True'
    context['company_req_1'] = CompanyRequest.objects.filter(company_choice_num=1, scheduled=0)
    context['company_req_2'] = CompanyRequest.objects.filter(company_choice_num=2, scheduled=0)
    context['company_req_3'] = CompanyRequest.objects.filter(company_choice_num=3, scheduled=0)
    context['reho_req'] = RehearsalRequest.objects.filter(scheduled=0)
    context['all_requests'] = ADRequest.objects.all()
    context['groups'] = Group.objects.all()
    context['studios'] = Studio.objects.all()
    context['report'] = report
    context['newdate'] = start_date
    print(context['report'])
    return render(request, "templates/pacApp/form/adminForm.html", context)


def total_spaces(all_requests):
    AVAILABLE_SPACES = 660 # (16 hours on weekend +(10*5) on weekdays) * 10 (studios)
    total = AVAILABLE_SPACES
    for group in all_requests:
        total -= 3 # for company
        total -= 2 * (int(group.num_reho))
    if (total>0): 
        return True # enough space
    else:
         return False


def scheduling_alg(request: HttpResponse):

    start_date = request.POST['start_date']
    end_date = request.POST['end_date']
    print(start_date, end_date)

    report = []
    # based on the dates specified
    new_date = start_date

    start_date_new = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date_new = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    print(start_date_new, end_date_new)
    diff = end_date_new-start_date_new
    weeks = abs(math.ceil(diff.days/7))

    delta = end_date_new - start_date_new       # as timedelta

    for i in range(delta.days + 1):
        day = start_date_new + timedelta(days=i)
        print(day)
        # find out if prev bookings on that day in db are from alg 
        temp = Booking.objects.filter(booking_date=day, from_alg=1).count()
        if temp > 0:
            report = ['Spaces have already been scheduled for ' + str(day) + '. Please select a new date range.']
            context = {}
            context['start_date'] = start_date
            context['company_req_1'] = CompanyRequest.objects.filter(company_choice_num=1, scheduled=0)
            context['company_req_2'] = CompanyRequest.objects.filter(company_choice_num=2, scheduled=0)
            context['company_req_3'] = CompanyRequest.objects.filter(company_choice_num=3, scheduled=0)
            context['reho_req'] = RehearsalRequest.objects.all(scheduled=0)
            context['all_requests'] = ADRequest.objects.all()
            context['groups'] = Group.objects.all()
            context['studios'] = Studio.objects.all()
            context['has_report'] = 'True'
            context['success'] = 'False'
            context['report'] = report
            print(context['report'])
            return render(request, "templates/pacApp/form/adminForm.html", context)



    report.append("Booking from " + str(start_date) + " to "  + str(end_date) + " (" + str(weeks) + " weeks).")
    
    # get everything in db
    all_requests = RehearsalRequest.objects.filter(scheduled=0)
    company1 = CompanyRequest.objects.filter(company_choice_num=1, scheduled=0)
    company2 = CompanyRequest.objects.filter(company_choice_num=2, scheduled=0)
    company3 = CompanyRequest.objects.filter(company_choice_num=3, scheduled=0)

    # no groups to schedule
    if (RehearsalRequest.objects.filter(scheduled=0).count() == 0):
        report = ['No groups to schedule. Please ensure that data is populated into Step 2.']
        context = {}
        context['start_date'] = start_date
        context['company_req_1'] = CompanyRequest.objects.filter(company_choice_num=1, scheduled=0)
        context['company_req_2'] = CompanyRequest.objects.filter(company_choice_num=2, scheduled=0)
        context['company_req_3'] = CompanyRequest.objects.filter(company_choice_num=3, scheduled=0)
        context['reho_req'] = RehearsalRequest.objects.filter(scheduled=0)
        context['all_requests'] = ADRequest.objects.all()
        context['groups'] = Group.objects.all()
        context['studios'] = Studio.objects.all()
        context['has_report'] = 'True'
        context['report'] = report
        context['success'] = 'False'
        print(context['report'])
        return render(request, "templates/pacApp/form/adminForm.html", context)


    # check if there are enough spaces to allocate
    enough_space = total_spaces(all_requests)
    if not enough_space:
        report = ['Not enough space to allocate, please request less space']
        context = {}
        context['start_date'] = start_date
        context['company_req_1'] = CompanyRequest.objects.filter(company_choice_num=1, scheduled=0)
        context['company_req_2'] = CompanyRequest.objects.filter(company_choice_num=2, scheduled=0)
        context['company_req_3'] = CompanyRequest.objects.filter(company_choice_num=3, scheduled=0)
        context['reho_req'] = RehearsalRequest.objects.filter(scheduled=0)
        context['all_requests'] = ADRequest.objects.all()
        context['groups'] = Group.objects.all()
        context['studios'] = Studio.objects.all()
        context['has_report'] = 'True'
        context['success'] = 'False'
        context['report'] = report
        print(context['report'])
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

        report.append('Scheduled spaces for ' + groups_list[group.group_id_id-1] + '.')
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

    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
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
        hours = [i for i in range(0, 25)]
        if (day is 'Sunday') or (day is 'Saturday'):
            for i in range(1, 9):
                hours.remove(i)
        else:
            for i in range(1, 16):
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
        preference = 1
        studio = group_info.iloc[:, df_request.columns.get_loc(
            'company_studio_1')].values[0]
        day = group_info.iloc[:, df_request.columns.get_loc(
            'company_day_1')].values[0]
        start_time = group_info.iloc[:, df_request.columns.get_loc(
            'company_start_time_1')].values[0]
        end_time = int(group_info.iloc[:, df_request.columns.get_loc(
            'company_end_time_1')].values[0])
        

        # if the company time is already booked

        next_pref = 0
        for time in range(start_time, end_time):
            if (int(time) not in avail[day][studio]): next_pref = 1
            print('going to pref 2')

        if (next_pref):
            studio = group_info.iloc[:, df_request.columns.get_loc(
                'company_studio_2')].values[0]
            day = group_info.iloc[:, df_request.columns.get_loc(
                'company_day_2')].values[0]
            start_time = group_info.iloc[:, df_request.columns.get_loc(
                'company_start_time_2')].values[0]
            end_time = group_info.iloc[:, df_request.columns.get_loc(
                'company_end_time_2')].values[0]
            preference = 2
            
        next_pref = 0
        for time in range(start_time, end_time):
            if (int(time) not in avail[day][studio]): next_pref = 1
        
        if (next_pref):
            studio = group_info.iloc[:, df_request.columns.get_loc(
                'company_studio_3')].values[0]
            day = group_info.iloc[:, df_request.columns.get_loc(
                'company_day_3')].values[0]
            start_time = group_info.iloc[:, df_request.columns.get_loc(
                'company_start_time_3')].values[0]
            end_time = group_info.iloc[:, df_request.columns.get_loc(
                'company_end_time_3')].values[0]
            preference = 3
        
        next_pref = 0
        for time in range(start_time, end_time):
            if (int(time) not in avail[day][studio]): next_pref = 1
        
        if (next_pref):
            report.append(groups_list[group-1] + " did not get any Company Preference. Please return back to Step 2 and ensure that " + groups_list[group-1] + "'s company preference does not conflict with anyone else. ")
            bookable=False
            reho_count = {'0': 0}

        else:
            # add the company time to df and remove from available times
            for time in range(start_time, end_time):
                (avail[day][studio]).remove(int(time))
            
            group_results = pd.DataFrame(data={'Name': [group],
                                            'Studio': [studioList[studio]],
                                            'Day': [day],
                                            'Start_Time': [start_time],
                                            'End_Time': [int(end_time)],
                                            'Booking_Date': [None]})
            report.append(groups_list[group-1] + " got Preference " + str(preference) + " for company.")

            df_results = pd.concat([group_results, df_results],
                                ignore_index=True, sort=False)

    """Cycle through the list of requests until everyone's requests are filled"""
    bookable = True
    
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
                                                        report.append("No more spaces left.")
                                                        print('NO MORE SPACES LEFT. THROW ERROR')
                                                        bookable = False
                                                        break


                if bookable:
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

    user_netid = request.user.uniauth_profile.get_display_id()
    for week in range(weeks+1):
        for i, space in df_results.iterrows():
            book = Booking(studio_id_id=space['Studio'],
                        group_id_id=int(space['Name']),
                        from_alg = 1,
                        group_name=groups_list[int(space['Name'])-1],
                        start_time=space['Start_Time'],
                        end_time=space['End_Time'],
                        week_day=daysList[space['Day']],
                        user_netid=str(user_netid),
                        booking_date=(start_date_new + timedelta(days=(week*6))))
            book.save()

# RehearsalRequest.objects.filter(scheduled=0)
    for group in all_requests:
        (RehearsalRequest.objects.filter(request_id=group.request_id)).update(scheduled=1)

    for group in company1:
        CompanyRequest.objects.filter(company_choice_num=1, request_id_id=group.request_id_id).update(scheduled=1)

    for group in company2:
        CompanyRequest.objects.filter(company_choice_num=2, request_id_id=group.request_id_id).update(scheduled=1)

    for group in company3:
        CompanyRequest.objects.filter(company_choice_num=3, request_id_id=group.request_id_id).update(scheduled=1) 
    
    context = {}
    context['start_date'] = start_date
    context['company_req_1'] = CompanyRequest.objects.filter(company_choice_num=1, scheduled=0)
    context['company_req_2'] = CompanyRequest.objects.filter(company_choice_num=2, scheduled=0)
    context['company_req_3'] = CompanyRequest.objects.filter(company_choice_num=3, scheduled=0)
    context['reho_req'] = RehearsalRequest.objects.filter(scheduled=0)
    context['all_requests'] = ADRequest.objects.all()
    context['groups'] = Group.objects.all()
    context['studios'] = Studio.objects.all()
    context['has_report'] = 'True'
    context['report'] = report
    context['newdate'] = new_date
    print(context['report'])

    # for item in context['all_requests']:
    #	print(item.name)
    return render(request, "templates/pacApp/form/adminForm.html", context)
    # return render(request, "templates/pacApp/tableElements/calendar.html", context)
    # return redirect('../../schedule')
    # return redirect('../../adminForm')

def showResults(request):
    # render with today's date
    profile = request.user.uniauth_profile.get_display_id()
    print(profile)
    studentDets = studentInfo(profile)
    startdate = handleDateStr(request.GET.get('newdate'))
    groups = 'None'
    context = createContext(startdate, groups)
    context['user'] = profile
    context['firstname'] = profile
    if studentDets != None:
      first_name = studentDets['first_name']
      context['firstname'] = first_name
    
    return render(request, "templates/pacApp/schedule.html", context)
