from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer

from weddingwebsite.models import DBSession
from weddingwebsite.models import MyModel, BlogEntry

def home_page(request):
  dbsession = DBSession()
  root = dbsession.query(MyModel).filter(MyModel.name==u'root').first()
  right_sidebar = get_renderer('templates/right_sidebar.pt').implementation()
  blog_entry = get_renderer('templates/blog_entry.pt').implementation()
  if "first_visit" not in request.cookies:
    url = request.route_url('landing')
    return HTTPFound(location=url)
  else:
    return {'root':root,
            'project':'WeddingWebsite',
            'right_sidebar':right_sidebar,
            'blog_entry':blog_entry}

def landing(request):
  if "first_visit" in request.cookies:
    url = request.route_url('home')
    return HTTPFound(location=url)

  request.add_response_callback(_set_cookie)
  home_page_url = request.route_url('home')
  return {'redirect_url': home_page_url}

def our_story(request):
  main = get_renderer('templates/index.pt').implementation()
  return {'main': main}

def blog(request):
  main = get_renderer('templates/index.pt').implementation()
  right_sidebar = get_renderer('templates/right_sidebar.pt').implementation()
  blog_entry = get_renderer('templates/blog_entry.pt').implementation()
  dbsession = DBSession()
  entries = dbsession.query(BlogEntry).order_by(BlogEntry.entry_date.desc()).all()
  return {'main':main,
          'right_sidebar':right_sidebar,
          'blog_entry':blog_entry,
          'all_entries': [entry.to_dict() for entry in entries]}

def events(request):
  main = get_renderer('templates/index.pt').implementation()
  return {'main': main}

def _set_cookie(request, response):
  response.set_cookie('first_visit', 'blah')
