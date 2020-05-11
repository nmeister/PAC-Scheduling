from django.template.defaulttags import register
import hashlib
import random
from base64 import b64encode
import requests
import datetime
import math


def studentInfo(profile):
  url = 'https://tigerbook.herokuapp.com/api/v1/undergraduates/' + profile
  req = requests.get(url, headers=create_tigerbook_header(profile))
  if req.status_code == 200:
    return req.json()
  return None


def create_tigerbook_header(profile):
  created = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
  nonce = ''.join([random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/=') for i in range(32)])
  username = profile
  password = '93247de4c77fc8367434e9f0c06db417'
  hash_arg = (nonce + created + password).encode()
  generated_digest = b64encode(hashlib.sha256(hash_arg).digest()).decode()
  headers = {
        'Authorization': 'WSSE profile="UsernameToken"',
        'X-WSSE': 'UsernameToken Username="{}", PasswordDigest="{}", Nonce="{}", Created="{}"'
                  .format(username, generated_digest, b64encode(nonce.encode()).decode(), created)
                  }
  return headers 


# takes in string, returns type of object date
def handleDateStr(date):
    print(date)
    print(type(date))
    date = date.split('-')
    startdate = datetime.date(int(date[0]), int(date[1]), int(date[2]))
    return startdate

def handleGroup(groups):
  if groups == 'None':
    return 'None'
  else: 
    groups = groups.split('-')
    # the last one is a - which should be empty
    groups.pop(-1)
    return groups



# transform str "April 27, 2020" into list [yyyy, mm, dd]
def handledate(date):
    date = date.replace(',', '')
    date = date.split(' ')
    month = date[0]
    day = date[1]
    year = date[2]

    # chance month to a number
    abbr_to_num = {name: num for num,
                   name in enumerate(calendar.month_abbr) if num}
    month = abbr_to_num[month[0:3]]

    return year, month, day


@register.filter
# creates a function that can be called directly from the template
def get_range(start, end):
    return range(start, end)


@register.filter
def get_duration(start, end):
    return end-start+1

def must_be_pac(user):
    return user.groups.filter(name='Pac').count()
