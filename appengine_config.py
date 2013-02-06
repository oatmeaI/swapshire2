from gaesessions import SessionMiddleware
def webapp_add_wsgi_middleware(app):
    # Generate your own cookie_key!
    # You can do so by running this (in the terminal, not in your code here):
    #   from uuid import uuid4
    #   print str(uuid4().hex+uuid4().hex)
    app = SessionMiddleware(app, cookie_key="jfgrtyurcfyufg7645t3vcsed6erd6v756ufyugvi56drcfgc", cookie_only_threshold = 0)
    return app