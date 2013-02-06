'''
categories.py

This is a RequestHandler that allows browsing products by categories. 
URLs are formed like this:

/category/[ category name ]?offset=[offset]&limit=[limit]
(offset and limit are optional)

Copyright 2012 Keenan Villani-Holland
'''

from basics import BasicHandler
from models import Product

class CategoryBrowser(BasicHandler):
    templates = { "get_read" : "templates/category_get_read.html" }

    def get(self, category=None):
        if self.request.get('offset'):
            offset = int(self.request.get('offset'))
        else:
            offset = 0

        if self.request.get('limit'):
            limit = int(self.request.get('limit'))
        else:
            limit = 15

        if category:
            products = Product.all().order('-created').filter('category =', category).fetch(limit, offset=offset)
        else:
            products = Product.all().order('-created').fetch(limit, offset=offset)
        
        self.render_template('get_read', { 'products' : products, 'offset' : offset, 'limit' : limit, 'category' : category })