from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.session import SignedCookieSessionFactory
from pyramid.httpexceptions import HTTPFound


@view_config(route_name='start')
def start(request):
    return render_to_response('templates/text.jinja2', {'title': 'Start'}, request=request)


@view_config(route_name='/')
def MainPage(request):
    return HTTPFound(location='/start')  # redirection


if __name__ == '__main__':
    config = Configurator(
        settings={'debug_all': True, 'default_locale_name': 'ru', })
    my_session_factory = SignedCookieSessionFactory('TryToGuess')
    config.set_session_factory(my_session_factory)
    config.add_route('/', '/')
    config.add_route('start', '/start')
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static/')
    config.scan()
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()
