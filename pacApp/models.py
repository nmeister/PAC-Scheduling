from django.db import models

# Create your models here.


class TimeSlot(models.Model):	
	company_name =  models.CharField(max_length=50)
	time_start = models.IntegerField()
	time_end = models.IntegerField()
	studio = models.CharField(max_length=50)



class Hours(models.Model):
	start = models.IntegerField()
	end = models.IntegerField()
	duration = models.IntegerField()


