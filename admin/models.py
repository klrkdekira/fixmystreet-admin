import os
import hashlib
import logging

from sqlalchemy import Column, Integer, Unicode

from sqlalchemy import engine_from_config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm import synonym

from zope.sqlalchemy import ZopeTransactionExtension

from pyramid.decorator import reify
from pyramid.request import Request
from pyramid.security import Allow, authenticated_userid

maker = sessionmaker(extension=ZopeTransactionExtension())
DBSession = scoped_session(maker)

Base = declarative_base()

log = logging.getLogger(__name__)

class DBConnect(object):
    def __init__(self, **settings):
        self.engine = engine_from_config(settings, 'sqlalchemy.')

    def connect(self):
        Base.metadata.bind = self.engine

    def create(self):
        Base.metadata.create_all(self.engine)

        import transaction
        
        session = DBSession()
        ppj = Login()
        ppj.username = u'ppjmanager'
        ppj.password = u'secret'
        ppj.body_id = 2
        session.add(ppj)
        session.flush()

        dbkl = Login()
        dbkl.username = u'dbklmanager'
        dbkl.password = u'secret'
        dbkl.body_id = 1
        session.add(dbkl)
        session.flush()

        transaction.commit()

class Login(Base):
    __tablename__ = 'login'

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(Unicode, unique=True, nullable=False)
    _password = Column('password', Unicode, nullable=False)
    body_id = Column(Integer, nullable=False)

    def _set_password(self, password):
        if isinstance(password, unicode):
            password = password.encode('utf-8')
        salt = hashlib.sha1(os.urandom(1024)).hexdigest()
        digest = hashlib.sha1(salt + password).hexdigest()
        hpassword = digest + salt
            
        if not isinstance(hpassword, unicode):
            hpassword = hpassword.decode('utf-8')
        self._password = hpassword

    def _get_password(self):
        return self._password
        
    def check_password(self, password):
        if isinstance(password, unicode):
            password = password.encode('utf-8')
        digest = self._password[:40]
        salt = self._password[40:]
        hdigest = hashlib.sha1(salt + password).hexdigest()
        return digest == hdigest

    password = synonym('password', descriptor=property(_get_password,
                                                       _set_password))

class RootFactory(object):
    """ACL for customer and merchant dashboard
    """
    __acl__ = [(Allow, 'body', 'body')]

    def __init__(self, request):
        pass

def groupfinder(userid, request):
    session = DBSession()

    user = (session.query(Login)
            .filter(Login.username==unicode(userid))
            .first())
    if user:
        return ['body']

class RequestWithUserAttribute(Request):
    """Add `user` attribute to `request` object
    `User` object can be accessed in view via `request.user`
    """
    @reify
    def user(self):
        username = authenticated_userid(self)
        if username:
            session = DBSession()
            return (session.query(Login)
                    .filter(Login.username==unicode(username))
                    .first())
