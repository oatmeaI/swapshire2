'''
crud.py

This is a class that handles generic Create, Read, Update and Delete functions for
any given database model on Swapshire.com. This class is only for inheriting from.

Copyright 2012 Keenan Villani-Holland
'''

import webapp2
from google.appengine.ext.webapp import template
from models import *
from basics import BasicHandler

class Crud(BasicHandler):

    # These are placeholders that should be set in classes that inherit from Crud.
    properties = [  ] # This is a list of properties that the given model has.
    model = "" # This is the name of the model as a string.

    # When a CRUDer is called, it is called with a mode argument (C, R, U, or D).
    # Here, in the basic GET handler, we check which mode is being called,
    # and then call the appropriate method.
    # If it's any mode other than Create, we should've gotten a key name
    # that refers to the object we're Reading, Updating or Deleting, so we pass
    # that key name to the function as well.
    def get(self, mode, obj_key=None):
        if mode == 'c':
            self.get_create()
        elif mode == 'r':
            self.get_read(obj_key)
        elif mode == 'u':
            self.get_update(obj_key)
        elif mode == 'd':
            self.get_delete(obj_key)

    def get_create(self, obj_key=None):
        if obj_key is not None:
            self.render_template('get_create', { 'obj_key' : obj_key })
        else:
            self.render_template('get_create', {})

    def get_read(self, obj_key):
        obj = eval(self.model).get_by_key_name(obj_key)
        logged_in = self.session.is_active()
        self.render_template('get_read', { "obj" : obj, 'session' : self.session, 'logged_in' : logged_in })

    def get_update(self, obj_key):
        obj = eval(self.model).get_by_key_name(obj_key)
        if self.request.get("first_time"):
            first_time = True
        else:
            first_time = False
        self.render_template('get_update', { "obj" : obj, "first_time" : first_time })

    def get_delete(self, obj_key):
        obj = eval(self.model).get_by_key_name(obj_key)
        self.render_template('get_delete', { "obj" : obj })

    # Now on to the POST handlers. Works the same way as above
    def post(self, mode, obj_key=None):
        if mode == 'c':
            self.post_create()
        elif mode == 'r':
            self.get_read(obj_key) # This shouldn't ever happen, but if it does, just display it as if it had been post rather than get
        elif mode == 'u':
            self.post_update(obj_key)
        elif mode == 'd':
            self.post_delete(obj_key)

    def post_create(self):
        # Loop through our list of properties, if a variable with that name is in the post variables, add it to the dictionary of values which the new object will be created with
        property_dict = {}
        for prop in self.properties:
            if self.request.get(prop):
                property_dict[prop] = self.request.get(prop)
        
        # Now that we have all the properties defined, create the new object
        new_object = eval(self.model)()
        new_object.assign_properties(property_dict)
        new_object.put()
        self.get_read(new_object.key().name())
    
    def post_update(self, obj_key):
        obj = eval(self.model).get_by_key_name(obj_key)
        property_dict = {}
        for prop in self.properties:
            if self.request.get(prop):
                property_dict[prop] = self.request.get(prop)

        obj.assign_properties(property_dict)
        obj.put()
        self.get_read(obj_key)

    def post_delete(self, obj_key):
        obj = eval(self.model).get_by_key_name(obj_key)
        obj.delete()
