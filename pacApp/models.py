from django.db import models

# Create your models here.


class TimeSlot(models.Model):	
	company_name =  models.CharField(max_length=50)
	time_start = models.IntegerField()
	time_end = models.IntegerField()
	studio = models.CharField(max_length=50)


class ADRequest(models.Model):	
	name =  models.CharField(max_length=50)
	company_day = models.CharField(max_length=50)
	company_start_time = models.IntegerField()
	company_end_time = models.IntegerField()
	company_studio = models.CharField(max_length=50)
	rank_1 = models.CharField(max_length=50)
	rank_2 = models.CharField(max_length=50)
	rank_3 = models.CharField(max_length=50)
	rank_4 = models.CharField(max_length=50)
	rank_5 = models.CharField(max_length=50)
	num_reho = models.IntegerField()
	num_members = models.IntegerField()


class Hours(models.Model):
	start = models.IntegerField()
	end = models.IntegerField()
	duration = models.IntegerField()


