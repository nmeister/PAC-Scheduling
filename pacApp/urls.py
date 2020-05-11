from django.urls import path
from django.conf.urls import handler404, handler500

from . import views
from . import dancers
from . import errors

urlpatterns = [
    # when referencing home page it eneds to be given url of '/'
    path('', dancers.homepage, name='homepage'),
    path('homepage', dancers.homepage, name='homepage'),
    path('schedule', dancers.schedule, name='schedule'),
    path('insert_space/', views.insert_space_item, name='insert_space_item'),
    path('insert_ad_request/', views.insert_ad_request, name='insert_ad_request'),
    path('scheduling_alg', views.scheduling_alg, name='scheduling_alg'),
    path('adminForm', views.adminForm, name='adminForm'),
   # path('create_booking', views.create_booking, name='create_booking'),
   # path('delete_booking', views.delete_booking, name='delete_booking'),
    path('drop_ad_request', views.drop_ad_request, name='drop_ad_request'),
    path('delete_ad_request', views.delete_ad_request, name='delete_ad_request'),
    path('delete_schedule_alg', views.delete_schedule_alg, name='delete_schedule_alg'),
    path('showResults', views.showResults, name="showResults"),
    # for updating by weeks
    path('updateWeek', dancers.updateWeek, name='updateWeek'),
    path('updateGroupOnly', dancers.updateGroupOnly, name='updateGroupOnly'),
    path('updateBooking', dancers.updateBooking, name='updateBooking'),
    path('updateDropping', dancers.updateDropping, name='updateDropping'),
    path('updateMulti', dancers.updateMulti, name='updateMulti'),
    path('about', dancers.about, name='about'),
    path('notpac', dancers.notpac, name='notpac'), 
]

handler404 = errors.error_404
handler500 = errors.error_500
