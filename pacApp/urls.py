from django.urls import path
from django.conf.urls import handler404, handler500

from . import pacAdmin
from . import dancers
from . import errors
from . import views

urlpatterns = [
    # when referencing home page it eneds to be given url of '/'
    path('', views.homepage, name='homepage'),
    path('homepage', views.homepage, name='homepage'),
    path('schedule', dancers.schedule, name='schedule'),
    path('insert_space/', pacAdmin.insert_space_item, name='insert_space_item'),
    path('insert_ad_request/', pacAdmin.insert_ad_request, name='insert_ad_request'),
    path('scheduling_alg', pacAdmin.scheduling_alg, name='scheduling_alg'),
    path('adminForm', pacAdmin.adminForm, name='adminForm'),
   # path('create_booking', pacAdmin.create_booking, name='create_booking'),
   # path('delete_booking', pacAdmin.delete_booking, name='delete_booking'),
    path('drop_ad_request', pacAdmin.drop_ad_request, name='drop_ad_request'),
    path('delete_ad_request', pacAdmin.delete_ad_request, name='delete_ad_request'),
    path('delete_schedule_alg', pacAdmin.delete_schedule_alg, name='delete_schedule_alg'),
    path('showResults', pacAdmin.showResults, name="showResults"),
    # for updating by weeks
    path('updateWeek', dancers.updateWeek, name='updateWeek'),
    path('updateGroupOnly', dancers.updateGroupOnly, name='updateGroupOnly'),
    path('updateBooking', dancers.updateBooking, name='updateBooking'),
    path('updateDropping', dancers.updateDropping, name='updateDropping'),
    path('updateMulti', dancers.updateMulti, name='updateMulti'),
    path('about', views.about, name='about'),
    path('notpac', views.notpac, name='notpac'), 
    path('logout', views.logout, name='logout'), 
]

handler404 = errors.error_404
handler500 = errors.error_500
