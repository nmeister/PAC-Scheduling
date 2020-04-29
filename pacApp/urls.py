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
    path('drop_space', views.drop_space, name='drop_space'),
    path('delete_booking', views.delete_booking, name='delete_booking'),
    path('update', views.update, name='update'),
    path('about', views.about, name='about'),
]

handler404 = views.error_404
handler500 = views.error_500
