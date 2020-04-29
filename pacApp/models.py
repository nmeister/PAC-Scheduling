from django.db import models

# Create your models here.

# AD request form for rehearsals and company 
class ADRequest(models.Model):	
	company_name = models.CharField(max_length=50)
	company_day_1 = models.CharField(max_length=50)
	company_start_time_1 = models.IntegerField()
	company_end_time_1 = models.IntegerField()
	company_studio_1 = models.CharField(max_length=50)
	company_day_2 = models.CharField(max_length=50)
	company_start_time_2 = models.IntegerField()
	company_end_time_2 = models.IntegerField()
	company_studio_2 = models.CharField(max_length=50)
	company_day_3 = models.CharField(max_length=50)
	company_start_time_3 = models.IntegerField()
	company_end_time_3 = models.IntegerField()
	company_studio_3 = models.CharField(max_length=50)
	num_reho = models.IntegerField()
	company_size = models.IntegerField()
	rank_1 = models.CharField(max_length=50, default='wilcox', editable=True)
	rank_2 = models.CharField(max_length=50)
	rank_3 = models.CharField(max_length=50)
	rank_4 = models.CharField(max_length=50)
	rank_5 = models.CharField(max_length=50)

class Studio(models.Model):
	name = models.CharField(max_length=50)
	address = models.CharField(max_length=50)

class Group(models.Model):
	name = models.CharField(max_length=50)
	showtime = models.DateField()
	contact = models.CharField(max_length=50)
	size = models.IntegerField()

class Booking(models.Model):
	studio_id = models.IntegerField()
	company_id = models.IntegerField()
	user_netid = models.CharField(max_length=50)
	company_name = models.CharField(max_length=50)
	start_time = models.IntegerField()
	end_time = models.IntegerField()
	week_day = models.IntegerField()
	booking_date = models.DateField(auto_now_add=False) #2018/12/19



