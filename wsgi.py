import logging
from gevent.pywsgi import WSGIServer
import webapp2
import gevent
import config
import routes
import models
from services import ws
from web import errors
from lib import basehandler, utils
from ws4py.websocket import EchoWebSocket
from ws4py.server.geventserver import WSGIServer
from ws4py.server.wsgiutils import WebSocketWSGIApplication
import gevent.monkey
gevent.monkey.patch_all()


models.create_tables()

app = webapp2.WSGIApplication(debug=basehandler.IS_DEV, config=config.webapp2_config, routes=routes.get_routes())


# defined custom error handlers
class Webapp2HandlerAdapter(webapp2.BaseHandlerAdapter):

    def __call__(self, request, response, exception):
        request.route_args = {
            'exception': exception
        }
        logging.exception(exception)
        handler = self.handler(request, response)

        return handler.get()

app.error_handlers[403] = Webapp2HandlerAdapter(errors.Error403Handler)
app.error_handlers[404] = Webapp2HandlerAdapter(errors.Error404Handler)
app.error_handlers[503] = Webapp2HandlerAdapter(errors.Error503Handler)
app.error_handlers[500] = Webapp2HandlerAdapter(errors.Error500Handler)


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    http_server = WSGIServer(('', 8080), app)
    ws_server = WSGIServer(('', 9000), WebSocketWSGIApplication(handler_cls=ws.Commands))

    greenlets = [
        gevent.spawn(http_server.serve_forever),
        gevent.spawn(models.Sensor.background_send_values),
        gevent.spawn(ws_server.serve_forever)
    ]

    try:
        gevent.joinall(greenlets)
    except KeyboardInterrupt:
        http_server.stop()
        print 'Stopping'
