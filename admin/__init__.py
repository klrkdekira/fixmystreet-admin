from pyramid.config import Configurator

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from pyramid_beaker import session_factory_from_settings

import sqlsoup
from admin.models import (DBConnect,
                          groupfinder,
                          RequestWithUserAttribute)

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    db = DBConnect(**settings)
    db.connect()
    # db.create()

    authn_policy = AuthTktAuthenticationPolicy('randomstuffs123',
                                               hashalg='sha512',
                                               callback=groupfinder)

    authz_policy = ACLAuthorizationPolicy()
   
    config = Configurator(settings=settings,
                          root_factory='admin.models.RootFactory',
                          authentication_policy=authn_policy,
                          authorization_policy=authz_policy)

    config.include('pyramid_chameleon')
    
    session_factory = session_factory_from_settings(settings)
    config.set_session_factory(session_factory)

    config.set_request_factory(RequestWithUserAttribute)

    db = sqlsoup.SQLSoup(settings['sqlsoup.url'])
    def add_db(request):
        return db

    config.add_request_method(add_db, 'db', reify=True)
    
    config.add_static_view('static', 'admin:static', cache_max_age=3600)

    config.include('admin.views.views_include')
    
    return config.make_wsgi_app()
