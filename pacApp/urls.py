from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('schedule', views.schedule, name ='schedule'),
    path('insert_space/', views.insert_space_item, name='insert_space_item'),
    path('insert_ad_request/', views.insert_ad_request, name='insert_ad_request'),
    path('div/', views.div, name='div'),
    path('fors', views.fors, name='fors'),
]