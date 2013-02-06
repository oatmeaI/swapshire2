'''
auth.py

Deals with authentication with Persona and initializing sessions on Swapshire.com.

To Do:
    - Error handling for if verification fails
    - Check email against valid_emails array

Important Note: Right now, we use the beginning of users' email addresses (before the @) as their
database key names. At the moment, that's not a problem: no two Hampshire students can have the same
email address, so those should always be unique. However, in the future, when we launch to the 5 Colleges
and beyond, there is a possibility of having two users with the same beginning of their email address, 
which would break the system. Something to think about. We could probably fix this in the same
way we fixed the problem of possible duplicate Product key names (adding random numbers to the key name),
however, since we use get_or_insert here, it would have to be a bit more complicated.

Copyright 2012 Keenan Villani-Holland
'''

import webapp2
from google.appengine.ext.webapp import template
from basics import BasicHandler
import gaesessions
import urllib,urllib2
try:
    import json
except ImportError:
    from django.utils import simplejson as json

from models import User

# This is the list of different email servers we accept.
# Right now, it's only open to Hampshire students and faculty.
# Eventually, when we launch to the 5 Colleges, it will
# include all 5 College email addresses.
valid_emails = ['hampshire.edu']

# This gets called after we have an assertion from Persona.
# It verifies the assertion and if it's valid, it creates a session
# with gaesessions that will be used to track information about the
# logged in user.
class SessionCreator(BasicHandler):
    def get(self, assertion):
       
        # Here we validate the assertion with Persona's verification server.
        data = {
            "assertion" : assertion,
            "audience" : urllib2.Request(self.request.url).get_host()
        }
        req = urllib2.Request('https://verifier.login.persona.org/verify',urllib.urlencode(data))        
        json_result = urllib2.urlopen(req).read()

        # We assume the verification was successful (which is bad, we should fix that).
        # Anyway, we parse JSON and extract the email that the user signed in with here.
        result = json.loads(json_result)
        user_email = result.get('email')
        
        # Check to make sure the email is one we allow to access our site.
        # If it is, set up the user's session.
        if user_email.endswith('hampshire.edu'):
            # Build a key name for the user. (It's just the beginning of their
            # email address for now. See comment at top).
            user_key = user_email.split('@')[0]
            self.session['email'] = user_email
            self.session['user_key'] = user_key
            stored_user = User.get_or_insert(key_name = user_key, email = user_email)
            # The user doesn't already have a profile, take them to the
            # create profile page. If they do, send them to the homepage.
            if not stored_user.name:
                self.redirect('/user/u/'+user_key+"?first_time=true")
            else:
                self.session['name'] = stored_user.name
                self.redirect('/')
        else:
            self.redirect('/error/wrong_email')


