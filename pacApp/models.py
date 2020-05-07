from django.db import models
from datetime import date

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
    bloomberg_rank = models.IntegerField(default=0)
    dillon_dance_rank = models.IntegerField(default=0)
    dillon_mar_rank = models.IntegerField(default=0)
    dillon_mpr_rank = models.IntegerField(default=0)
    murphy_rank = models.IntegerField(default=0)
    ns_rank = models.IntegerField(default=0)
    ns_warmup_rank = models.IntegerField(default=0)
    ns_theatre_rank = models.IntegerField(default=0)
    whitman_rank = models.IntegerField(default=0)
    wilcox_rank = models.IntegerField(default=0)
    # option to add default='___' option to prevent erroroneous entrys


# Table of all the dance studios and their characteristics
class Studio(models.Model):
    studio_name = models.CharField(max_length=50)
    # primary key 
    studio_id = models.IntegerField(unique=True)
    address = models.CharField(max_length=50)
    capacity = models.IntegerField(default=0)

# Table of all the PAC arts groups


class Group(models.Model):
    group_name = models.CharField(max_length=50)
    group_id = models.IntegerField(default=0,unique=True)
    showtime = models.DateField()
    contact = models.CharField(max_length=50)
    size = models.IntegerField(default=0)

# Bookings in the calendar


class Booking(models.Model):
    group_id = models.IntegerField()
    # foreign key 
    studio_id = models.ForeignKey(
        Studio, to_field='studio_id', default=1, on_delete=models.SET_DEFAULT)
    group_id = models.ForeignKey(
        Group, to_field = 'group_id', default=0, on_delete = models.SET_DEFAULT)
    group_name = models.CharField(max_length=50)
    from_alg = models.IntegerField(default=0)
    user_netid = models.CharField(max_length=50)
    start_time = models.IntegerField()
    end_time = models.IntegerField()
    week_day = models.IntegerField()
    booking_date = models.DateField(auto_now_add=False)  # 2018/12/19

# Choices for company per one group

# Choices of rehearsal per one group

class RehearsalRequest(models.Model):
    # request_id = models.ForeignKey(CompanyRequest, to_field='request_id', default=0, verbose_name="Rehearsals", on_delete=models.SET_DEFAULT)
	group_id = models.ForeignKey(Group, to_field='group_id', default=0, on_delete=models.SET_DEFAULT)
	scheduled = models.IntegerField(default=0)
	num_reho = models.IntegerField()
	member_size = models.IntegerField()
	submit_date = models.CharField(max_length=50, unique=True)
	rank_1 = models.IntegerField(default=0)
	rank_2 = models.IntegerField(default=0)
	rank_3 = models.IntegerField(default=0)
	rank_4 = models.IntegerField(default=0)
	rank_5 = models.IntegerField(default=0)
	rank_6 = models.IntegerField(default=0)
	rank_7 = models.IntegerField(default=0)
	rank_8 = models.IntegerField(default=0)
	rank_9 = models.IntegerField(default=0)
	rank_10 = models.IntegerField(default=0)
	request_id = models.CharField(max_length=50, unique=True)

class CompanyRequest(models.Model):
	# request_id = models.CharField(max_length=50, unique=True, default=0)
	request_id = models.ForeignKey(RehearsalRequest, to_field='request_id', default="", verbose_name="Rehearsals", on_delete=models.SET_DEFAULT)
	company_choice_num = models.IntegerField()
	scheduled = models.IntegerField()
	group_id = models.ForeignKey(
        Group, to_field='group_id', default=0, on_delete=models.SET_DEFAULT)
	company_day = models.CharField(max_length=50)
	company_start_time = models.IntegerField()
	company_end_time = models.IntegerField()
	company_studio = models.ForeignKey(Studio, to_field='studio_id', default=1, on_delete=models.SET_DEFAULT)
	submit_date = models.CharField(max_length=50)
	