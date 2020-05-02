from django.urls import path
from django.conf.urls import handler404, handler500

from . import views

urlpatterns = [
    # when referencing home page it eneds to be given url of '/'
    path('', views.homepage, name='homepage'),
    path('homepage', views.homepage, name='homepage'),
    path('schedule', views.schedule, name='schedule'),
    path('insert_space/', views.insert_space_item, name='insert_space_item'),
    path('insert_ad_request/', views.insert_ad_request, name='insert_ad_request'),
    path('scheduling_alg/', views.scheduling_alg, name='scheduling_alg'),
    path('adminForm', views.adminForm, name='adminForm'),
    path('create_booking', views.create_booking, name='create_booking'),
    path('delete_booking', views.delete_booking, name='delete_booking'),
    path('drop_ad_request', views.drop_ad_request, name='drop_ad_request'),
    path('delete_ad_request', views.delete_ad_request, name='delete_ad_request'),
    path('delete_schedule_alg', views.delete_schedule_alg, name='delete_schedule_alg'),
    # for updating by weeks
    path('updateWeek', views.updateWeek, name='updateWeek'),
    path('updateGroupOnly', views.updateGroupOnly, name='updateGroupOnly'),
    path('updateBooking', views.updateBooking, name='updateBooking'),
    path('updateDropping', views.updateDropping, name='updateDropping'),
    path('about', views.about, name='about'),
    path('notpac', views.notpac, name='notpac'),
]

handler404 = views.error_404
handler500 = views.error_500
