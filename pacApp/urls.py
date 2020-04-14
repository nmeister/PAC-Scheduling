from django.urls import path

from . import views

urlpatterns = [
	# when referencing home page it eneds to be given url of '/'
    path('', views.homepage, name='homepage'),
    path('schedule', views.schedule, name ='schedule'),
    path('insert_space/', views.insert_space_item, name='insert_space_item'),
    path('insert_ad_request/', views.insert_ad_request, name='insert_ad_request'),
    path('adminForm', views.adminForm, name='adminForm'),
    path('create_booking', views.create_booking, name='create_booking'),
]