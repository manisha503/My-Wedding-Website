import datetime
import string

from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer

from weddingwebsite.models import DBSession
from weddingwebsite.models import MyModel, BlogEntry, User

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
  right_sidebar = get_renderer('templates/right_sidebar.pt').implementation()
  return {'main': main,
          'right_sidebar': right_sidebar}

def bridal_party(request):
  main = get_renderer('templates/index.pt').implementation()
  return {'main': main}

def rsvp(request):
  main = get_renderer('templates/index.pt').implementation()
  right_sidebar = get_renderer('templates/right_sidebar.pt').implementation()
  request.add_response_callback(_set_cookie)
  return {'main': main,
          'right_sidebar': right_sidebar}

def retrieve_rsvp(request):
  dbsession = DBSession()
  query = dbsession.query(User)
  last_name = None
  zip = None

  if 'user_id' in request.params:
    query = query.filter(User.id == request.params['user_id'])
  else:
    if 'last_name' in request.params:
      last_name = string.lower(request.params['last_name'])
      query = query.filter(User.last_name == last_name)
    if 'zip' in request.params:
      zip = request.params['zip']
      query = query.filter(User.zip == zip)
    #adding the group by ensures we get one entry per family (the last one)
    query = query.group_by(User.family_id)
  entries = query.all()

  if not entries:
    return {"error_message": "Couldn't find a record with last name: %s and zip: %s" \
        % (request.params['last_name'], zip)}
  entry_list = [entry.to_dict() for entry in entries]
  response = dict(entries=entry_list)
  return response

def record_rsvp(request):
  dbsession = DBSession()
  query = dbsession.query(User)
  query = query.filter(User.family_id == request.params['family_id'])
  entries = query.all()

  if not entries:
    return {"error_message": "An error occurred recording your RSVP.  Please try again later."}

  family_name = ""
  num_garba = int(request.params["num_garba"])
  num_wedding = int(request.params["num_wedding"])
  num_reception = int(request.params["num_reception"])
  accepted = int(request.params["accepted"])
  for entry in entries:
    family_name = entry.family_name
    entry.declined = 1 if accepted == 0 else 0
    entry.accepted = 1 if accepted == 1 else 0
    if accepted:
      entry.num_rsvp_garba = num_garba
      entry.num_rsvp_wedding = num_wedding
      entry.num_rsvp_reception = num_reception
    else:
      entry.num_rsvp_garba = 0
      entry.num_rsvp_wedding = 0
      entry.num_rsvp_reception = 0

    dbsession.add(entry);
  response = dict(family_name=family_name,
                  accepted=accepted,
                  num_rsvp_garba=num_garba,
                  num_rsvp_wedding=num_wedding,
                  num_rsvp_reception=num_reception)
  return response

def _set_cookie(request, response):
  response.set_cookie('first_visit', 'blah')
