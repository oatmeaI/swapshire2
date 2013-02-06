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

'''
main.py

The main script of Swapshire.com

Copyright 2012 Keenan Villani-Holland
'''
import webapp2
from crud import Crud
from models import User, Product
from auth import SessionCreator
from basics import BasicHandler, ErrorHandler
from dev import OfflineLogin
from categories import CategoryBrowser
import gaesessions


# The class that handles Create, Update, Read and Delete functions for Users.
# IMPORTANT: The create method is actually never called.
# The datastore entity is created in SessionCreator when get_or_insert() is called. 
class UserCrud(Crud):
    templates = {  'get_create' : 'templates/user_get_create.html',
                   'get_read' : 'templates/user_get_read.html',
                   'get_update' : 'templates/user_get_update.html',
                   'get_delete' : 'templates/user_get_delete.html' }
    properties = [  'name', 
                    'email',
                    'pronouns',
                    'school',
                    'picture_key',
                    'blurb' ]
    model = "User"

    # We have to set put the user's name into our session variable
    # so that we can access it easily.
    # This is done in the Update method because the 
    # Create method is never called (see above). 
    def post_update(self, obj_key):
        self.session['name'] = self.request.get('name')
        Crud.post_update(self, self.session['user_key'])

# Same as UserCrud, but for Products.
# The Create method is called here, so this class works
# just the way you'd expect (unlike UserCrud).
class ProductCrud(Crud):
    templates = {  'get_create' : 'templates/prod_get_create.html',
                   'get_read' : 'templates/prod_get_read.html',
                   'get_update' : 'templates/prod_get_update.html',
                   'get_delete' : 'templates/prod_get_delete.html' }
    properties = [  'name',
                    'blurb',
                    'picture_key',
                    'price',
                    'created',
                    'user',
                    'school',
                    'category']
    model = "Product"

    def post_delete(self, obj_key):
        obj = Product.get_by_key_name(obj_key)
        # For some reason, obj.user.key.name doesn't work here, so we just figure out what the user key is using the email address.
        # This is a hack which WILL NOT work if we change how user keys work. Need to figure out the right way to do this.
        obj_user_key = obj.user.email.split('@')[0]
        if obj_user_key == self.session['user_key']:
            Crud.post_delete(self, obj_key)
            self.redirect('/user/r/'+self.session['user_key'])
        else:
            self.redirect('/error/not_owner')

# Just renders the homepage
class MainHandler(BasicHandler):
    templates = { 'get' : 'templates/main_get.html' }
    def get(self):
        self.render_template('get', {})

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/user/(.*)/(.*)', UserCrud),
    ('/user/(.*)', UserCrud),
    ('/product/(.*)/(.*)', ProductCrud),
    ('/product/(.*)', ProductCrud),
    ('/login/(.*)', SessionCreator),
    ('/error/(.*)', ErrorHandler),
    ('/category', CategoryBrowser),
    ('/category/(.*)', CategoryBrowser),
    ('/dev/offlinelogin', OfflineLogin)
    ], debug=True)
