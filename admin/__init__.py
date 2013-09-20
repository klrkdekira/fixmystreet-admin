from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)

    config.include('pyramid_formalchemy')
    config.include('fa.jquery')

    config.formalchemy_admin('/admin', package='admin',
                             view='fa.jquery.pyramid.ModelView')

    return config.make_wsgi_app()
