#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from handlers import *

application = webapp.WSGIApplication([
    ('/', MainHandler),
    ('/days', DayHandler)
  ], debug=True)


def main():
  run_wsgi_app(application)


if __name__ == '__main__':
  main()
