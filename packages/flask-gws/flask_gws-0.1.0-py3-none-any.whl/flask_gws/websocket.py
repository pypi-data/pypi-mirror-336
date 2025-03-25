import os
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Callable, Union, TypeVar

from gevent import spawn, wait
from gevent.event import Event
from gevent.monkey import patch_all
from gevent.queue import Queue, Empty
from gevent.select import select

from werkzeug.exceptions import HTTPException
from werkzeug.routing import Map, Rule, MapAdapter

from ._uwsgi import uwsgi


# Type alias for message data
WSMessage = Union[str, bytes, None]
T = TypeVar('T')


@dataclass
class GeventWebSocketClient:
    """WebSocket client implementation using gevent for asynchronous I/O."""
    environ: Dict[str, Any]
    fd: int
    send_event: Event
    send_queue: Queue
    recv_event: Event
    recv_queue: Queue
    timeout: int = 5
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    connected: bool = True

    def send(self, msg: WSMessage, binary: bool = False) -> None:
        """Send a message to the client."""
        if binary:
            return self.send_binary(msg)
        self.send_queue.put(msg)
        self.send_event.set()

    def send_binary(self, msg: WSMessage) -> None:
        """Send a binary message to the client."""
        self.send_queue.put(msg)
        self.send_event.set()

    def receive(self) -> WSMessage:
        """Receive a message from the client (alias for recv)."""
        return self.recv()

    def recv(self) -> WSMessage:
        """Receive a message from the client."""
        return self.recv_queue.get()

    def recv_nb(self) -> WSMessage:
        """Non-blocking receive."""
        try:
            return self.recv_queue.get_nowait()
        except Empty:
            return None

    def close(self) -> None:
        """Close the connection."""
        self.connected = False


class GeventWebSocketMiddleware:
    """WebSocket middleware implementation using gevent."""
    client = GeventWebSocketClient

    def __init__(self, wsgi_app, websocket):
        self.wsgi_app = wsgi_app
        self.websocket = websocket

    def __call__(self, environ: Dict[str, Any], start_response: Callable) -> List[bytes]:
        """Handle the WSGI request."""
        urls: MapAdapter = self.websocket.url_map.bind_to_environ(environ)
        try:
            endpoint, args = urls.match()
            handler = self.websocket.view_functions[endpoint]
        except HTTPException:
            handler = None

        # If not a WebSocket request or no handler, pass to WSGI app
        if not handler or 'HTTP_SEC_WEBSOCKET_KEY' not in environ:
            return self.wsgi_app(environ, start_response)

        # Perform WebSocket handshake
        uwsgi.websocket_handshake(
            environ['HTTP_SEC_WEBSOCKET_KEY'],
            environ.get('HTTP_ORIGIN', '')
        )

        # Setup communication channels
        send_event, send_queue = Event(), Queue()
        recv_event, recv_queue = Event(), Queue()

        # Create WebSocket client instance
        client = self.client(
            environ=environ, 
            fd=uwsgi.connection_fd(), 
            send_event=send_event,
            send_queue=send_queue, 
            recv_event=recv_event, 
            recv_queue=recv_queue,
            timeout=self.websocket.timeout
        )

        # Spawn handler to process client events
        handler = spawn(handler, client, **args)

        # Define listener function that waits for socket events
        def listener(client: GeventWebSocketClient) -> None:
            select([client.fd], [], [], client.timeout)
            recv_event.set()
            
        # Spawn initial listener
        listening = spawn(listener, client)

        # Main event loop
        while True:
            # Check if client disconnected
            if not client.connected:
                recv_queue.put(None)
                listening.kill()
                handler.join(client.timeout)
                return []

            # Wait for any events (handler, send, receive)
            wait([handler, send_event, recv_event], None, 1)

            # Process send events
            if send_event.is_set():
                try:
                    while True:
                        uwsgi.websocket_send(send_queue.get_nowait())
                except Empty:
                    send_event.clear()
                except IOError:
                    client.connected = False

            # Process receive events
            elif recv_event.is_set():
                recv_event.clear()
                try:
                    # Read all available messages until an empty message
                    message: WSMessage = True
                    while message:
                        message = uwsgi.websocket_recv_nb()
                        if message:
                            recv_queue.put(message)
                    listening = spawn(listener, client)
                except IOError:
                    client.connected = False

            # Handle completion of handler
            elif handler.ready():
                listening.kill()
                return []


class WebSocket:
    """WebSocket implementation using gevent."""
    middleware = GeventWebSocketMiddleware

    def __init__(self, app=None, timeout=5):
        if app:
            self.init_app(app)
        self.timeout = timeout
        self.url_map = Map()
        self.view_functions = {}
        self.blueprints = {}
        if app is not None:
            self.debug = app.debug
            self._got_first_request = app._got_first_request
        else:
            self.debug = False
            self._got_first_request = False

    def init_app(self, app):
        """Initialize the Flask application with gevent patches."""
        self.app = app
        
        # Apply gevent monkey patching
        aggressive = app.config.get('GWS_AGGRESSIVE_PATCH', True)
        patch_all(aggressive=aggressive)
        
        # Add debugging middleware if needed
        if os.environ.get('FLASK_GWS_DEBUG'):
            from werkzeug.debug import DebuggedApplication
            app.wsgi_app = DebuggedApplication(app.wsgi_app, True)
            app.debug = True

        app.wsgi_app = self.middleware(app.wsgi_app, self)
        app.run = lambda **kwargs: self.run(**kwargs)

    def run(self, app=None, debug=False, host='localhost', port=5000, uwsgi_binary=None, **kwargs):
        if not app:
            app = self.app.name + ':app'

        if self.app.debug:
            debug = True

        run_uwsgi(app, debug, host, port, uwsgi_binary, **kwargs)

    def route(self, rule, **options):
        def decorator(f):
            endpoint = options.pop('endpoint', None)
            self.add_url_rule(rule, endpoint, f, **options)
            return f
        return decorator

    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        assert view_func is not None, 'view_func is mandatory'
        if endpoint is None:
            endpoint = view_func.__name__
        options['endpoint'] = endpoint
        # WebSockets only support GET
        methods = set(('GET', ))
        if 'methods' in options:
            methods = methods.union(options['methods'])
            options.pop('methods')
        provide_automatic_options = False
        try:
            rule = Rule(rule, methods=methods, websocket=True, **options)
        except TypeError:
            rule = Rule(rule, methods=methods, **options)
        rule.provide_automatic_options = provide_automatic_options
        self.url_map.add(rule)
        if view_func is not None:
            old_func = self.view_functions.get(endpoint)
            if old_func is not None and old_func != view_func:
                raise AssertionError('View function mapping is overwriting an '
                                    'existing endpoint function: %s' % endpoint)
            self.view_functions[endpoint] = view_func

    def register_blueprint(self, blueprint, **options):
        '''
        Registers a blueprint on the WebSockets.
        '''
        first_registration = False
        if blueprint.name in self.blueprints:
            assert self.blueprints[blueprint.name] is blueprint, \
                'A blueprint\'s name collision occurred between %r and ' \
                '%r.  Both share the same name "%s".  Blueprints that ' \
                'are created on the fly need unique names.' % \
                (blueprint, self.blueprints[blueprint.name], blueprint.name)
        else:
            self.blueprints[blueprint.name] = blueprint
            first_registration = True
        blueprint.register(self, options, first_registration) 