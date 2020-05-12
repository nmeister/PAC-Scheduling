
#from django.contrib.auth.decorators import login_required
from . import models
from .models import Booking, Group, Studio
import datetime
from datetime import date, timedelta

# showing which studios are currently available 
def carouselAvailable(starttoday, currenttime):
    notfree = Booking.objects.filter(start_time__exact=currenttime).filter(
        booking_date__exact=starttoday)
    studioList = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    for i in notfree:
        studioList[i.studio_id_id] = 0
    return studioList

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