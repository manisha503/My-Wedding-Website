from pyramid.httpexceptions import HTTPFound

from weddingwebsite.models import DBSession
from weddingwebsite.models import MyModel

def home_page(request):
  dbsession = DBSession()
  root = dbsession.query(MyModel).filter(MyModel.name==u'root').first()
  if "first_visit" not in request.cookies:
    url = request.route_url('landing')
    return HTTPFound(location=url)
  else:
    return {'root':root, 'project':'WeddingWebsite'}

def landing(request):
  if "first_visit" in request.cookies:
    url = request.route_url('home')
    return HTTPFound(location=url)

  request.add_response_callback(_set_cookie)
  home_page_url = request.route_url('home')
  return {'redirect_url': home_page_url}

def _set_cookie(request, response):
  response.set_cookie('first_visit', 'blah')
