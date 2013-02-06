'''
basics.py

These are some basic classes that are used throughout the code for Swapshire.com.

Copyright 2012 Keenan Villani-Holland
'''

import webapp2
import gaesessions
from google.appengine.ext.webapp import template

# This is the list of categories that items can be in on the site.
categories = ['Electronics', 'Clothes', 'Dorm', 'Books', 'Other']

# This is class that most, if not all request handlers should inherit from.
# It adds some helpful functionality, such as a render template method, among others.
class BasicHandler(webapp2.RequestHandler):
    # This is a placeholder that should set in classes that inherit from BasicHandler.
    # It is a list of all the template files the class uses, e.g:
    # templates = { 'get_create' : 'products/get_create.html' } etc.
    templates = {}
    # This grabs the list of product categories there are from categories.py
    product_categories = categories

    # This property makes it so we can just use self.session to access the current session.
    # Not necessary, but it makes the code more elegant and easy to write.
    @property
    def session(self):
        return gaesessions.get_current_session()

    # This method makes it easier to render templates.
    # which_template is a string which refers to the self.templates dictionary.
    # data is a dictionary of things we want to access in the template.
    def render_template(self, which_template, data):
        # Automatically add the session object to the data
        data['session'] = self.session
        
        # All this does is set the data['logged_in'] according to whether or not
        # the session has an email set or not.
        # Originally, session['loggen_in'] was set according to self.session.is_active(),
        # but apparently that was unreliable, as it was possible to not be logged in
        # but have the session be "active." I think this was an extreme edge case due to
        # how I was restarting the development server, but this fixes it in case it could
        # ever happen in deployment. Also, it makes it easier to test anyway.
        # The try is there because the script will throw an error if you try to test
        # self.session['email'] when it isn't set.
        try:
            if self.session['email']:
                data['logged_in'] = True
        except:
            data['logged_in'] = False
        
        # This just gives the template the list of categories we have on the site.
        # It's required to render the header.
        data['categories'] = self.product_categories
        self.response.out.write(template.render(self.templates[which_template],data))


# This class just renders a generic error page. When loading the page, pass it an error type
# it will render the error message
class ErrorHandler(BasicHandler):
    templates = { 'get' : 'templates/error_get.html' }

    # This is a dictionary of all the error types that tells us what the error message should say
    error_messages = {  '' : 'An error occurred! Well damn. We don\'t even know what went wrong.',
                        'wrong_email' : 'Please use a Hampshire College email address to sign in.' }

    def get(self, error_type):
        self.render_template('get', { 'message' : self.error_messages[error_type]})
