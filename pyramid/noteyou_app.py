from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.session import SignedCookieSessionFactory
from pyramid.httpexceptions import HTTPFound
from DB_with import LogDataBase
from models.models import User, Session, Base, engine
from sqlalchemy import select

DBSession = Session(bind=engine)


def check_logged_in(request) -> bool:
    try:
        if(request.session['logged_in']):
            #print("from check_logged_in ",True)
            return True
        else:
            return False
    except Exception as err:
        print("Something went wrong in the check_logged_in function:", str(err))
        return False


@view_config(route_name='start')
def start(request):
    return render_to_response('templates/index.jinja2', {'title': 'Start'}, request=request)


@view_config(route_name='notes')
def notes(request):
    return render_to_response('templates/notes.jinja2', {'title': 'Notes', 'counter_notes': '5'}, request=request)


@view_config(route_name='/')
def MainPage(request):
    return HTTPFound(location='/start')  # redirection


@view_config(route_name='sign_in')
def SignIn(request):

    try:
        user = User(
            login=request.params['login'],
            password=request.params['pass']
        )
        DBSession.add(user)
        DBSession.commit()
        request.session['logged_in'] = True
        return HTTPFound(location='/notes')
    except Exception as err:
        print("Something went wrong while trying to create an account:", str(err))
        return Response("Something went wrong while trying to create an account...")


@view_config(route_name='login')
def login(request):
    try:
        query = DBSession.query(User).filter((
            User.login == request.params['login'], User.password == request.params['pass']))
        DBSession.commit()
        print(res)
        return Response("res = %s" % res)
        # else:
        #     # request.session['logged_in'] = True
        #     # request.session['user_id'] = res[0][0]
        #     return HTTPFound(location='/notes')

    except Exception as err:
        print("Something went wrong while trying to log in:", str(err))
        return Response("Something went wrong while trying to log in:...")


if __name__ == '__main__':
    config = Configurator(
        settings={'debug_all': True, 'default_locale_name': 'ru', })
    my_session_factory = SignedCookieSessionFactory('TryToGuess')
    config.set_session_factory(my_session_factory)
    config.add_route('/', '/')
    config.add_route('start', '/start')
    config.add_route('sign_in', '/sign_in')
    config.add_route('login', '/login')
    config.add_route('notes', '/notes')
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static/')
    config.scan()
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()

file.close()
