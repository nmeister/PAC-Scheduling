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
# showing which studios are currently available 
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
    context['firstname'] = profile
    if profile != 'None':
      studentDets = studentInfo(profile)
      if studentDets != None:
        first_name = studentDets['first_name']
        context['firstname'] = first_name

    return render(request, "templates/pacApp/home.html", context)


#my_group = Group.objects.get(name='Pac')
# my_group.user_set.add('test@pac.com')

# if user not pac and tries to go to PAC booking page show this endpage
def notpac(request):
    context = {}
    try:
        profile = request.user.uniauth_profile.get_display_id()
    except:
        profile = 'None'
    context['firstname'] = profile
    if profile != 'None':
        studentDets = studentInfo(profile)
        if studentDets != None:
            first_name = studentDets['first_name']
            context['firstname'] = first_name
    return render(request, "templates/pacApp/notPac.html", context)


# about page 
def about(request):
    context = {}
    try:
        profile = request.user.uniauth_profile.get_display_id()
    except:
        profile = 'None'
    context['firstname'] = profile
    if profile != 'None':
        studentDets = studentInfo(profile)
        if studentDets != None:
            first_name = studentDets['first_name']
            context['firstname'] = first_name

    context['user'] = profile
    return render(request, "templates/pacApp/about.html", context)
