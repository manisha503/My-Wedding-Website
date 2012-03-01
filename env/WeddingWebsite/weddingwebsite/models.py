import csv
import datetime
import os
import transaction

from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import Unicode

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True)
    value = Column(Integer)

    def __init__(self, name, value):
        self.name = name
        self.value = value

class Page(Base):
    __tablename__ = 'pages'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    data = Column(Text)

    def __init__(self, name, value):
        self.name = name
        self.data = data

class BlogEntry(Base):
    __tablename__ = 'blog_entries'
    id = Column(Integer, primary_key=True)
    image_url = Column(Text)
    title = Column(Text)
    body = Column(Text)
    entry_date = Column(Date)

    def __init__(self, id, image_url, title, body, entry_date):
        self.id = id
        self.image_url = image_url
        self.title = title
        self.body = body
        self.entry_date = entry_date

    def to_dict(self):
      return {'id': self.id,
              'image_url': "static/style/images/blog/%s" % self.image_url,
              'title': self.title,
              'body': self.body,
              'entry_date': self.entry_date }

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    family_id = Column(Integer, nullable=False)
    last_name = Column(Text(50))
    first_name = Column(Text(50))
    address = Column(Text(100))
    city = Column(Text(100))
    state = Column(Text(50))
    zip = Column(Text(20))
    family_name = Column(Text(255))
    display_name = Column(Text(100))
    num_invited_garba = Column(Integer, default=0)
    num_invited_wedding = Column(Integer, default=0)
    num_invited_reception = Column(Integer, default=0)
    num_rsvp_garba = Column(Integer, default=0)
    num_rsvp_wedding = Column(Integer, default=0)
    num_rsvp_reception = Column(Integer, default=0)
    email = Column(Text(100))

    def __init__(self, id, family_id):
        self.id = id
        self.family_id = family_id

def populate():
    session = DBSession()
    populate_default(session)
    populate_users(session)
    populate_blog_entries(session)
    session.flush()
    transaction.commit()

def populate_default(session):
    records = session.query(MyModel).all()
    if not records:
      model = MyModel(name=u'root', value=55)
      session.add(model)

def populate_users(session):
    record = session.query(User).first()
    if not record:
      print "NO USERS FOUND; importing from db"
      here = os.path.dirname(__file__)
      user_file = csv.DictReader(open(os.path.join(here, 'data', 'AllWebsiteUsers.csv')))
      for row in user_file:
        # if we don't have a familyName assigned to them yet, skip for now
        if not row["[familyName]"]:
          continue
        id = row["[id]"]
        family_id = row["[familyId]"]
        user = User(id, family_id)
        user.last_name = row["[lastName]"]
        user.first_name = row["[firstName]"]
        user.address = row["[address1]"]
        user.city = row["[city]"]
        user.state = row["[state]"]
        user.zip = row["[zip]"]
        user.family_name = row["[familyName]"]
        user.num_invited_garba = row["[numGarba]"]
        user.num_invited_wedding = row["[numWedding]"]
        user.num_invited_reception = row["[numReception]"]
        user.email = row["[email]"]
        session.add(user)

def populate_blog_entries(session):
    record = session.query(BlogEntry).order_by(BlogEntry.id.desc()).first()
    latest_idx = 0
    if record:
      latest_idx = record.id

    here = os.path.dirname(__file__)
    blog_file = csv.DictReader(open(os.path.join(here, 'data', 'AllBlogEntries.csv')))
    for row in blog_file:
      id = row["[id]"]
      image_url = row["[image_url]"]
      title = row["[title]"]
      body = row["[body]"]
      date = datetime.datetime.strptime(row["[date]"], "%Y-%m-%d").date()
      blog_entry = BlogEntry(id, image_url, title, body, date)
      session.add(blog_entry)

def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    try:
        populate()
    except IntegrityError:
        transaction.abort()
