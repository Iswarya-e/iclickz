from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    my_session_factory = SignedCookieSessionFactory('itsaseekreet')
    config.set_session_factory(my_session_factory)
    config.include('pyramid_excel')
    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')
    config.add_accept_view_order('text/css')
    config.scan()
    config.add_static_view(name='static', path='classroom:static')
    return config.make_wsgi_app()
