#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Person(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    profile_image = ndb.BlobProperty()

class Place(ndb.Model):
    place_name = ndb.StringProperty()
    place_type = ndb.StringProperty()

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        people = Person.query().fetch()
        in_people = False
        if user:
            for person in people:
                if user.nickname() == person.email:
                    in_people = True
            if in_people == False:
                current_user = Person(name=user.nickname(), email=user.nickname(), profile_image="<img src='https://static.tplugin.com/tplugin/img/unknown-user.png'/>")
                current_user.put()
            else:
                for person in people:
                    if person.email == user.nickname():
                        current_user = person
            greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                (current_user.name, users.create_logout_url('/')))
        else:
            greeting = ('<a href="%s">Sign in or register</a>.' %
                users.create_login_url('/'))
        self.response.write('<html><body>%s</body></html>' % greeting)

# class ProfilePage(webapp2.RequestHandler):
#     templat
#     self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
