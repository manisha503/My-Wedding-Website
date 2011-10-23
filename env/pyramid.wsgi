from pyramid.paster import get_app
application = get_app(
    '/home/app/modwsgi/env/WeddingWebsite/production.ini', 'main')
