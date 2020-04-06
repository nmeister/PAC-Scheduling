from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('schedule', views.schedule, name ='schedule'),
    path('insert_space/', views.insert_space_item, name='insert_space_item'),
    path('div/', views.div, name='div')
]