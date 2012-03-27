from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from weddingwebsite.models import initialize_sql

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)
    config = Configurator(settings=settings)
    config.add_static_view('static', 'weddingwebsite:static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_view('weddingwebsite.views.home_page',
                    route_name='home',
                    renderer='templates/index.pt')
    config.add_route('landing', '/landing_page')
    config.add_view('weddingwebsite.views.landing',
                    route_name='landing',
                    renderer='templates/landing.pt')
    config.add_route('our_story', '/our_story')
    config.add_view('weddingwebsite.views.our_story',
                    route_name='our_story',
                    renderer='templates/our_story.pt')
    config.add_route('blog', '/blog')
    config.add_view('weddingwebsite.views.blog',
                    route_name='blog',
                    renderer='templates/blog.pt')
    config.add_route('events', '/events')
    config.add_view('weddingwebsite.views.events',
                    route_name='events',
                    renderer='templates/events.pt')
    config.add_route('bridal_party', '/bridal_party')
    config.add_view('weddingwebsite.views.bridal_party',
                    route_name='bridal_party',
                    renderer='templates/bridal_party.pt')
    config.add_route('rsvp', '/rsvp')
    config.add_view('weddingwebsite.views.rsvp',
                    route_name='rsvp',
                    renderer='templates/rsvp.pt')
    config.add_route('retrieve_rsvp', '/retrieve_rsvp')
    config.add_view('weddingwebsite.views.retrieve_rsvp',
                    route_name='retrieve_rsvp',
                    renderer='json')
    config.add_route('record_rsvp', '/record_rsvp')
    config.add_view('weddingwebsite.views.record_rsvp',
                    route_name='record_rsvp',
                    renderer='json')
    return config.make_wsgi_app()

