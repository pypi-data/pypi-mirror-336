'''
Flask-GWS
---------
High-performance WebSockets for your Flask apps powered by uWSGI and gevent.
'''

__docformat__ = 'restructuredtext'
from .__version__ import __version__
__license__ = 'MIT'
__author__  = 'Nidal Alhariri <level09@gmail.com>'

from ._uwsgi import uwsgi, run_uwsgi
from .websocket import WebSocket, GeventWebSocketClient, GeventWebSocketMiddleware 