from google.appengine.ext import db

from datetime import datetime
from math import ceil
import logging, traceback

class Day(db.Model):
  label = db.StringProperty()
  date = db.DateTimeProperty()
  width = db.IntegerProperty()
  height = db.IntegerProperty()
  
  def get_images(self, t1=None, t2=None):
    iq = Image.all().filter('day =', self)
    #where = 'WHERE day=:day'
    #kwargs = { 'day':self }
    #logging.error('day:'+self.label)
    
    if not t1 is None and not t2 is None:
      #where += ' AND date >= :t1 AND date <= :t2'
      #kwargs.update({ 't1': t1, 't2':t2 })
      iq = iq.filter('date >=', t1).filter('date <=', t2)
      
    #logging.error('where:'+where)
    #logging.error('kwargs:'+str(kwargs))
    
    #images = Image.gql(where, **kwargs)
    return iq
    
  def to_json(self, width, t1, t2):
    json = { 
      'label':self.label, 
      'date':self.date.strftime("%c"),
      'width':self.width,
      'height':self.height,
      'images': []
    }
    iq = self.get_images(t1=t1, t2=t2)
    image_count = iq.count()
    totalw = self.width * image_count
    logging.error('totalw:%s' % totalw)
    skip = int(ceil(float(totalw) / width))
    pos = 0
    totalw = 0
    logging.error('image_count:%s' % image_count)
    logging.error('skip:%s' % skip)
    for imageN in range(0,image_count):
      pos += 1
      if pos == image_count or (pos % skip == 1):
        totalw += self.width
        logging.error('fetching image %d' % imageN)
        image = iq.fetch(1, offset=imageN)[0]
        json['images'].append(image.to_json())
    return json
    
class Image(db.Model):
  day = db.ReferenceProperty(Day)
  stamp = db.StringProperty()
  date = db.DateTimeProperty()

  def to_json(self):
    return {
      'stamp': self.stamp,
      'date': self.date.strftime("%c")
    }