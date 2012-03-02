import datetime

from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer

from weddingwebsite.models import DBSession
from weddingwebsite.models import MyModel, BlogEntry

def home_page(request):
  dbsession = DBSession()
  root = dbsession.query(MyModel).filter(MyModel.name==u'root').first()
  if "first_visit" not in request.cookies:
    url = request.route_url('landing')
    return HTTPFound(location=url)
  else:
    dbsession = DBSession()
    latest_entry = dbsession.query(BlogEntry).order_by(BlogEntry.id.desc()).first()
    right_sidebar = get_renderer('templates/right_sidebar.pt').implementation()
    blog_entry = get_renderer('templates/blog_entry.pt').implementation()

    return {'root':root,
            'project':'WeddingWebsite',
            'right_sidebar':right_sidebar,
            'blog_entry':blog_entry,
            'latest_entry':latest_entry.to_dict()}

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
  query = dbsession.query(BlogEntry)
  offset_date = None
  if 'offset' in request.params:
    offset = request.params['offset']
    if 'dir' in request.params and request.params['dir'] == 'newer':
      query = query.filter(BlogEntry.id > offset)
    else:
      query = query.filter(BlogEntry.id < offset)
  entries = query.order_by(BlogEntry.id.desc()).limit(3).all()

  prev_url = None
  next_url = None
  if entries:
    last = entries[-1].id
    first = entries[0].id
    count = dbsession.query(BlogEntry) \
        .filter(BlogEntry.id < last).count()
    if count:
      next_url="/blog?offset=%d&dir=older" % last
    count = dbsession.query(BlogEntry) \
        .filter(BlogEntry.id > first).count()
    if count:
      prev_url = "/blog?offset=%d&dir=newer" % first

  return {'main':main,
          'right_sidebar':right_sidebar,
          'blog_entry':blog_entry,
          'all_entries': [entry.to_dict() for entry in entries],
          'prev_url': prev_url,
          'next_url': next_url}

def events(request):
  main = get_renderer('templates/index.pt').implementation()
  return {'main': main}

def _set_cookie(request, response):
  response.set_cookie('first_visit', 'blah')
