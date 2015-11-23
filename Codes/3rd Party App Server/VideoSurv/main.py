#!/usr/bin/env python

#
# Copyright 2015 Satvik Dhandhania <satvik.dhandhania2011@vit.ac.in>
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import json
import webapp2

from google.appengine.ext import db
from google.appengine.api import urlfetch

API_KEY = 'AIzaSyD6ktqBEKOqAp4jvYV8r9eth6hhP0KaQE4'


class AndroidDevice(db.Model):
    reg_id = db.StringProperty(indexed=False, required=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Video Surveillance Application Hosted Here!')


class RegisterHandler(webapp2.RequestHandler):
    def post(self):
        reg_id = self.request.get('id')
        device = AndroidDevice(reg_id=reg_id)
        device.put()
        self.response.write('Registered Device: ' + reg_id)


class IdentifyHandler(webapp2.RequestHandler):
    def post(self):
        name = self.request.get('name')
        devices = AndroidDevice.all()
        ids = []
        for device in devices:
            ids.append(str(device.reg_id))
        url = 'https://android.googleapis.com/gcm/send'
        my_key = "key=" + API_KEY
        json_data = {
            "data": {
                "name": name
            },
            "registration_ids": ids
        }
        result = urlfetch.fetch(url=url,
            payload=str(json.dumps(json_data)),
            method=urlfetch.POST,
            headers={'Content-Type': 'application/json', 'Authorization': my_key})

        self.response.write(json.dumps(result.content))  # This is a bad idea. You get a JSON object only if you give GCM the right parameters. So it might fail here.


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/register', RegisterHandler),
    ('/identify', IdentifyHandler)
], debug=True)
