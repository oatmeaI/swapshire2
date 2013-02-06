'''
dev.py

These are classes and methods to make Swapshire developers' lives easier.
They should be deactivated in main.py when the site is live.

Copyright 2012 Keenan Villani-Holland
'''

from basics import BasicHandler
from models import User

# This will login a test user without having to go through Persona.
# This way, we can test the site without an Internet connection.
class OfflineLogin(BasicHandler):
    templates = { 'get' : 'templates/main_get.html' }
    def get(self):
        email = "test@example.com"
        key = "test"
        stored_user = User.get_or_insert(key_name = key, email = email)
        self.session['email'] = email
        self.session['user_key'] = key
        if not stored_user.name:
            self.redirect('/user/u/'+key)
        else:
            self.session['name'] = stored_user.name