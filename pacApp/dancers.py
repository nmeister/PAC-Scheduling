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
from .models import Booking, Group, Studio
import datetime
from datetime import date, timedelta
import calendar
import json
from .utils import studentInfo, handleDateStr, handleGroup, handledate, get_range, get_duration, must_be_pac
from .create import createContext, create_booking, delete_booking



# displays the calendar schedule
@login_required
def schedule(request):
    # render with today's date
    profile = request.user.uniauth_profile.get_display_id()
    print(profile)
    studentDets = studentInfo(profile)
    starttoday = date.today()
    print(starttoday)
    groups = 'None'
    context = createContext(starttoday, groups)
    context['user'] = profile
    context['firstname'] = profile
    if studentDets != None:
        first_name = studentDets['first_name']
        context['firstname'] = first_name

    return render(request, "templates/pacApp/schedule.html", context)


def logoutView(request):
    #return render(request, '/accounts/logout')
    return redirect('%s?next=%s' % ('/accounts/logout/', '/homepage'))
   

# updates week
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

# update when group checked


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
    # these are all related to booking
    bookingdate = handleDateStr(request.POST['date'])
    studio = request.POST['studio']
    username = request.POST['name']
    userid = request.POST['nameid']
    profile = request.user.uniauth_profile.get_display_id()
    print(userid == profile)
    starttime = request.POST['starttime']
    endtime = request.POST['endtime']
    weekdaybooked = request.POST['day']
    # try to make a booking in the table
    # returns 0 upon FAIL and 1 upon SUCCESS
    success = create_booking(bookingdate, studio, username,
                             userid, starttime, endtime, weekdaybooked, profile)
    print(success)
    # this is the current week start on
    startdate = handleDateStr(request.POST['currweek'])
    groups = handleGroup(request.POST['groups'])
    openday = handleDateStr(request.POST['openday'])

    context = createContext(startdate, groups)
    context['openday'] = openday.strftime('%w')
    context['booksuccess'] = success
    return render(request, "templates/pacApp/tableElements/calendar.html", context)

# for multiple booking at a time


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
    success = delete_booking(bookingdate, studio, name,
                             nameid, starttime, endtime, day, profile)
    print(success)
    groups = handleGroup(request.POST['groups'])
    startdate = handleDateStr(request.POST['currweek'])
    openday = handleDateStr(request.POST['openday'])
    context = createContext(startdate, groups)
    context['openday'] = openday.strftime('%w')
    context['dropsuccess'] = success
    return render(request, "templates/pacApp/tableElements/calendar.html", context)
