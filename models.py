'''
models.py

The database models for Swapshire.com

Copyright 2012 Keenan Villani-Holland
'''

from google.appengine.ext import db,blobstore
from time import time
from random import randrange


# This is the user class. It stores information for users
# that have accounts on the site.
# Pretty much exactly the same as the Product class
class User(db.Model):
    name = db.StringProperty()
    email = db.EmailProperty()
    school = db.StringProperty()
    pronouns = db.StringProperty()
    picture_key = blobstore.BlobReferenceProperty()
    blurb = db.StringProperty()

    def assign_properties(self, properties):
        self.name = properties['name']
        # This is optional, so only try to assign it if we got it.
        if 'blurb' in properties:
            self.blurb = properties['blurb']

        if 'pronouns' in properties:
            self.blurb = properties['pronouns']

    # This just makes it so that we can do User.products and it will give
    # us an array of products that are associated with the user.
    @property
    def products(self):
        products = Product.all().filter('user =', self)
        return products.fetch(1000)

# This is the product / item class. It's what people sell on the site.
# Pretty straightforward: First, the list of properties that this class has.
# Second, the function that we use to give a new Product it's data
class Product(db.Model):
    name = db.StringProperty()
    blurb = db.TextProperty()
    picture_key = blobstore.BlobReferenceProperty()
    price = db.FloatProperty()
    created = db.DateTimeProperty(auto_now = True)
    user = db.ReferenceProperty(User)
    school = db.StringProperty()
    category = db.StringProperty()

    # This function gets called from the CRUDer
    # Give it a dictionary of values where the key for each value in the dictionary
    # corresponds to the name of the class's property.
    def assign_properties(self, properties):
        self.name = properties['name']
        self.blurb = properties['blurb']
        self.price = float(properties['price'])
        self.user = User.get_by_key_name(properties['user'])
        self.category = properties['category']
        
        # This looks a little complicated, but it's pretty simple
        # We're going to generate a key name for the new object
        # It builds it by taking the object's name, turing it from unicode object to string,
        # lowercasing that string, replacing any spaces with dashes, and then takes the first
        # ten characters.
        new_key_name = str.replace(str(properties['name'].lower()), " ", "-")[:10]
        
        # Make sure we don't get two products with the same key names.
        # As long as there is another product in the datastore with the same key name, 
        # we add another random number to the end of the our key name.
        while Product.get_by_key_name(new_key_name):
            new_key_name = new_key_name + str(randrange(0,9))
        self._key_name = new_key_name