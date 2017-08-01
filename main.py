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
import random
import webapp2
import jinja2
import os
from google.appengine.ext import ndb
from google.appengine.api import users

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Person(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    profile_image = ndb.BlobProperty()
    restaurants = ndb.StringProperty(repeated = True)
    entertainments = ndb.StringProperty(repeated = True)

class Restaurant(ndb.Model):
    name = ndb.StringProperty()

class Entertainment(ndb.Model):
    name = ndb.StringProperty()


class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        people = Person.query().fetch()
        in_people = False
        check = True
        if user:
            for person in people:
                if user.nickname() == person.email:
                    in_people = True
            if in_people == False:
                current_user = Person(name=user.nickname(), email=user.nickname(), profile_image="<img src='https://static.tplugin.com/tplugin/img/unknown-user.png'/>",
                    restaurants=[], entertainments=[])
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
            check = False
        template = jinja_environment.get_template('templates/onthefence.html')
        vars_dict = {'response': greeting, 'check': check}
        self.response.out.write(template.render(vars_dict))

class ProfilePage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        people = Person.query().fetch()
        for person in people:
            if user.nickname() == person.email:
                current_person = person
        vars_dict = {'name': current_person.name, 'restaurant_list': current_person.restaurants}
        template = jinja_environment.get_template("templates/profile-page.html")
        self.response.write(template.render(vars_dict))

    def post(self):
        user = users.get_current_user()
        person = Person.query(Person.name == user.nickname()).fetch()[0]
        new_restaurant = Restaurant(name = self.request.get('food'))
        if new_restaurant.name != "":
            new_restaurant.put()
        restaurants = Restaurant.query().fetch()
        restaurant_list = []
        for place in restaurants:
            restaurant_list.append(place.name)
        if new_restaurant.name not in restaurant_list and new_restaurant.name != "":
            restaurant_list.append(new_restaurant.name)
        person.restaurants = restaurant_list
        person.put()
        new_entertainment = Entertainment(name = self.request.get('entertainment'))
        if new_entertainment.name != "":
            new_entertainment.put()
        entertainments = Entertainment.query().fetch()
        entertainment_list = []
        for place in entertainments:
            entertainment_list.append(place.name)
        if new_entertainment.name not in entertainment_list and new_entertainment.name != "":
            entertainment_list.append(new_entertainment.name)
        person.entertainments = entertainment_list
        person.put()
        vars_dict = {'name': person.name, 'restaurant_list': restaurant_list, 'entertainment_list': entertainment_list}
        template = jinja_environment.get_template("templates/profile-page.html")
        self.response.write(template.render(vars_dict))


class Randomizer(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("templates/randomizer.html")
        self.response.write(template.render())
    def post(self):
        user = users.get_current_user()
        person = Person.query(Person.name == user.nickname()).fetch()[0]
        random_place = ''
        template = jinja_environment.get_template("templates/randomizer.html")
        # restaurants = Restaurant.query().fetch()
        # restaurant_list = []
        # for place in restaurants:
        #     restaurant_list.append(place.name)
        if self.request.get('category_answer') == 'Food':
            random_place = (random.choice(person.restaurants))
        vars_dict = {'random':random_place}
        self.response.write(template.render(vars_dict))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/profile', ProfilePage),
    ('/random', Randomizer)
], debug=True)
