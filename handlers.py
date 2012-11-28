from google.appengine.ext.webapp import RequestHandler, template
from google.appengine.ext import db

import logging, traceback
import os
from datetime import datetime, timedelta

try:
  import simplejson as json
except:
  import json

from models import *

HEIGHT = 120
WIDTH = 160

class MainHandler(RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
    self.response.out.write(template.render(path, {}))
    
class DayHandler(RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'application/json'
    
    width = 800
    if self.request.get('width'):
      width = int(self.request.get('width'))
    height = 600
    if self.request.get('height'):
      height = int(self.request.get('height'))
    
    if self.request.get('d1') and self.request.get('d2'):
      d1 = datetime.strptime(self.request.get('d1'), '%Y%m%d')
      d2 = datetime.strptime(self.request.get('d2'), '%Y%m%d')
      days = list(Day.all().filter('date >=', d1).filter('date <=', d2))
      #logging.error('filtering >= %s and <= %s' % (d1,d2,))
    else:
      days = list(Day.all())

    t1 = None
    t2 = None
    if self.request.get('t1') and self.request.get('t2'):
      t1 = datetime.strptime(self.request.get('t1'), '%Y%m%d%H%M')
      t2 = datetime.strptime(self.request.get('t2'), '%Y%m%d%H%M')
      delta1 = t1 - t1.replace(hour=0,minute=0)
      delta2 = t2 - t2.replace(hour=0,minute=0)
      t1 = d1 + delta1
      t2 = d1 + delta2
      
    stat = {'status':True,'days':[]}
    day_count = len(days)
    totalh = HEIGHT * day_count
    #logging.error('totalh:%s' % totalh)
    stride = int(ceil(float(totalh) / height))
    pos = 0
    totalh = 0
    #logging.error('stride:%s' % stride)
    for day in days:
      pos += 1
      if pos == day_count or (pos % stride == 1 and totalh + day.height < height):
        totalh += day.height
        dt1 = None
        dt2 = None
        if t1 and t2:
          dt1 = t1 + timedelta(days=pos-1)
          dt2 = t2 + timedelta(days=pos-1)
          logging.error('dt1: %s' % dt1)
          logging.error('dt2: %s' % dt2)
        
        stat['days'].append(day.to_json(width, dt1, dt2))
      
    self.response.out.write(json.dumps(stat))
    
  def post(self):
    self.response.headers['Content-Type'] = 'application/json'
    
    if self.request.get('_method') == 'DELETE':
      total = 0
      imgs = Image.all()
      total += imgs.count()
      map(lambda img:img.delete(), imgs)
      
      days = Day.all()
      total += days.count()
      map(lambda day:day.delete(), days)
      
      stat = { 'status':True, 'count':total }
    else:
      if not self.request.get('count'):
        count = 60*24
      else:
        count = int(self.request.get('count'))
      
      next = Day.all().count() + 1
      label = '201109%02d' % next
      date = datetime.strptime(label, '%Y%m%d')
      day = Day(label=label,date=date, width=160, height=120)
      day.put()
      
      for i in range(0,count):
        date2 = date + timedelta(minutes=i)
        image = Image(day=day, stamp=date2.strftime('%Y%m%d%H%M'), date=date2)
        image.put()
      
      stat = { 'status': True }
      
    self.response.out.write(json.dumps(stat))