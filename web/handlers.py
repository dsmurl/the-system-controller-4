import logging
import mimetypes
import os
from lib.basehandler import BaseHandler


class HomeHandler(BaseHandler):

    def get(self):
        params = {}
        return self.render_template('main/index.html', **params)


class StaticHandler(BaseHandler):

    def get(self, folder, path):
        full_path = os.path.join(os.path.dirname(__file__), '..', 'static', folder, path)
        if os.path.exists(full_path):
            self.response.headers['Content-Type'] = mimetypes.guess_type(path)[0]
            with open(full_path, 'r') as f:
                return self.response.write(f.read())
        self.abort(404)