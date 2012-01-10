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
    return config.make_wsgi_app()

