# Copyright (C) 2020 AndieNoir
#
# PrdTest is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PrdTest is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PrdTest.  If not, see <https://www.gnu.org/licenses/>.

from flask import Flask
from flask_breadcrumbs import Breadcrumbs, default_breadcrumb_root
from flask_sockets import Sockets
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

from prdtest.views import home, binary_pk


app = Flask(__name__)
sockets = Sockets(app)

Breadcrumbs(app)
default_breadcrumb_root(home.blueprint, '.')

app.register_blueprint(home.blueprint)

app.register_blueprint(binary_pk.blueprint, url_prefix='/binary_pk')
sockets.register_blueprint(binary_pk.ws_blueprint, url_prefix='/binary_pk')

server = pywsgi.WSGIServer(('0.0.0.0', 57011), application=app, handler_class=WebSocketHandler)
server.serve_forever()
