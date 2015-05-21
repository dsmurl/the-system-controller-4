import json
import time
import hashlib
import logging
import os
import webapp2
from ws4py.websocket import WebSocket
import config
from webapp2_extras import jinja2
from webapp2_extras import sessions
from lib import jsonrpc

# Initialize constants & stuff for static files

IS_DEV = os.environ.get('PYCHARM_HOSTED') == '1'

# Bot user agents
BOT_USER_AGENTS = [
    'Googlebot',
    'Yahoo! Slurp',
    'YahooSeeker',
    'bingbot',
    'iaskspider'
]

# End


def user_required(handler):
    """
         Decorator for checking if there's a user associated
         with the current session.
         Will also fail if there's no session present.
    """

    def check_login(self, *args, **kwargs):
        """
            If handler has no login_url specified invoke a 403 error
        """
        if not self.user_id:
            try:
                self.redirect(self.uri_for('user-login'), abort=True)
            except (AttributeError, KeyError), e:
                self.abort(403)
        else:
            return handler(self, *args, **kwargs)

    return check_login


def admin_user_required(handler):
    """
         Decorator for checking if there's a admin/domain user associated
         with the current session.
         Will also fail if there's no session present.
    """

    def check_login(self, *args, **kwargs):
        # todo implement your is administrator here
        if self.user_id:
            return handler(self, *args, **kwargs)
        else:
            try:
                self.redirect(self.uri_for('user-login'), abort=True)
            except (AttributeError, KeyError), e:
                self.abort(403)

    return check_login

class BaseHandler(webapp2.RequestHandler):
    """
        BaseHandler for all requests
    """

    def dispatch(self):
        # Here there are bunch of stuff happening

        # rate limiting check
        if config.rate_limit:
            self._rate_limiter()

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    def _rate_limiter(self):
        # Rate limiting for bots & save resources
        # The reason we use 503 is because webapp2 does not have 429 code
        # in it's supported codes because it's not official status code yet
        user_agent = self.request.headers.get('User-Agent', 'Googlebot')
        robot = filter(lambda bot: user_agent.find(bot) != -1, BOT_USER_AGENTS)
        if robot:
            # use current minute cache
            cache_id = 'rate_limiter_%s' % hashlib.md5(robot.pop()).hexdigest()
            request_count = config.memcache.incr(cache_id)
            if not request_count and config.memcache.set(cache_id, '1', config.rate_limit[1]):
                request_count = 1

            if request_count >= config.rate_limit[0]:
                self.abort(503)
        else:
            # rate limiters for non bots non logged users
            request_count, time_started = self.session.get('rate_limiter_request', (0, time.time()))
            request_count += 1
            seconds = time.time() - time_started if time.time() > time_started else 0
            if seconds > config.rate_limit[1]:
                request_count, time_started = (0, time.time())
            elif request_count >= config.rate_limit[0] and seconds < config.rate_limit[1]:
                self.abort(503)
            self.session['rate_limiter_request'] = (request_count, time_started)

    @webapp2.cached_property
    def session_store(self):
        return sessions.get_store(request=self.request)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session(name=config.session_backend)

    @webapp2.cached_property
    def messages(self):
        return self.session.get_flashes(key='_messages')

    def add_message(self, message, level=None):
        self.session.add_flash(message, level, key='_messages')

    @webapp2.cached_property
    def user(self):
        if self.user_id:
            # todo implement this your way on how you want to access your user
            return
        return None

    @webapp2.cached_property
    def user_id(self):

        return self.session.get('user_id', 0)

    @webapp2.cached_property
    def is_ajax(self):
        return self.request.headers.get('X-Requested-With', None) == 'XMLHttpRequest'

    def static_url(self, num):

        return ''

    def jinja2_factory(self, app):
        j = jinja2.Jinja2(app)
        j.environment.filters.update({
            # Set filters.
        })
        j.environment.globals.update({
            # Set global variables.
            'uri_for': self.uri_for,
            'static_url': self.static_url
        })
        j.environment.tests.update({
            # Set tests.
            # ...
        })
        return j

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(factory=self.jinja2_factory, app=self.app)

    def render_template(self, filename, base_template="base.html", **kwargs):
        kwargs.update({
            'user_id': self.user_id,
            'url': self.request.url,
            'path': self.request.path,
            'query_string': self.request.query_string,
            'is_dev': IS_DEV,
            'base_template': base_template
        })

        if self.messages:
            kwargs['messages'] = self.messages

        self.response.headers.add_header('X-UA-Compatible', 'IE=Edge,chrome=1')
        self.response.write(self.jinja2.render_template(filename, **kwargs))


class RpcHandler(BaseHandler):

    def post(self):
        server = jsonrpc.Server(self)
        server.handle(self.request, self.response)


class BaseWebSocket(WebSocket):

    def received_message(self, message):
        data = json.loads(message.data)
        result = getattr(self, data['event'])(**data['data'])

        # if result:
        #     self.send(result, message.is_binary)
