from webapp2_extras.routes import RedirectRoute, PathPrefixRoute, DomainRoute
from services import rpc
from web import admin, handlers

_routes = [
    # Sample for administering
    PathPrefixRoute('/admin',[
        RedirectRoute('/', admin.HomeHandler, name='admin-home', strict_slash=True),
    ]),

    PathPrefixRoute('/user',[
        RedirectRoute('/login', 'web.handlers.LoginHandler', name='user-login', strict_slash=True),
        # Lazy loading sample
        RedirectRoute('/logout', 'web.handlers.LogoutHandler', name='user-logout', strict_slash=True)
    ]),

    # Main Routes
    RedirectRoute('/', handlers.HomeHandler, name='home', strict_slash=True),
    RedirectRoute('/<folder:(img|css|js|html|fonts)>/<path:(.+)>', handlers.StaticHandler, name='static', strict_slash=True),
    RedirectRoute('/rpc', rpc.ApiHandler, name='rpc', strict_slash=True)
]


def get_routes():
    return _routes