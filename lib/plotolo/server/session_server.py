import tornado.ioloop
import tornado.web
import tornado.websocket

from plotolo.server.session_fileserver import FileHandler
from plotolo.script.script_info import ScriptInfo
from plotolo.script.script_storage import ScriptStorage
from plotolo.session.session_handler import SessionHandler
from plotolo.session.data_storage import DataStorage
from plotolo.util.util import generate_id
from plotolo.util.logging import logger
from plotolo.util.constant import SESSION_COOKIE_NAME
from plotolo.config import Config


class AuthHandler(tornado.web.RequestHandler):
    """
    This handler is used to authenticate the user's session,
    as it is not possible to set cookies from the WebSocketHandler.
    """
    async def get(self, script_id=None):
        if not script_id:
            raise tornado.web.HTTPError(400)

        if not ScriptStorage.get_current().get(script_id):
            raise tornado.web.HTTPError(404)

        # using permanent session part for every user
        session_id = self.get_cookie(SESSION_COOKIE_NAME, None)
        if not session_id:
            # make session id unique for each script
            self.set_cookie(SESSION_COOKIE_NAME, f'{generate_id()}_{script_id}')
        else:
            if session_id.split('_')[1] != script_id:  # changing just the script_id
                self.set_cookie(SESSION_COOKIE_NAME, f'{session_id.split("_", 1)[0]}_{script_id}')

        await self.finish()
        return


    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET')


class WebSocketHandler(tornado.websocket.WebSocketHandler):

    async def on_message(self, message):
        """
        Set by the SessionHandler
        """
        pass


    async def open(self, script_id):
        await SessionServer.get_current().open_connection(self, script_id)


    def check_origin(self, origin):
        return True


class SessionServer:
    """
    Manages new websocket connections, session creations, and disconnections.
    """
    _singleton: 'SessionServer' = None


    @classmethod
    def get_current(cls) -> 'SessionServer':
        if SessionServer._singleton is None:
            SessionServer._singleton = SessionServer()
        return SessionServer._singleton


    def __init__(self):
        if SessionServer._singleton is not None:
            raise RuntimeError("Singleton already initialized. Call 'get_current' instead")
        SessionServer._singleton = self

        self.ioloop: tornado.ioloop.IOLoop | None = None

        self.scripts: dict[str, ScriptInfo] = {}  # script_id/path: info
        self.sessions: dict[str, SessionHandler] = {}  # session_id: handler
        self.data_storage: DataStorage = DataStorage.get_current()
        self.script_storage: ScriptStorage = ScriptStorage.get_current()


    def listen(self, ioloop: tornado.ioloop.IOLoop):
        self.ioloop = ioloop
        self.script_storage.listen()


    async def open_connection(self, websocket: tornado.websocket.WebSocketHandler, script_id: str):
        """
        Called by the WebSocketHandler when a new connection is opened.
        Creates a new session if it doesn't exist, or reconnects to an existing one.
        """
        if not self.script_storage.get(script_id):
            logger.error('Error: requested script is not found!')
            websocket.close(404)
            return

        session_id = websocket.get_cookie(SESSION_COOKIE_NAME, None)
        if not session_id or script_id != session_id.split('_', 1)[1]:  # {random_id}_{script_id}
            logger.error('Error: session cookie is not found!')
            websocket.close(401)
            return

        logger.info("Client (re)connected with session id: %s", session_id)

        if self.sessions.get(session_id):
            self.sessions[session_id].reconnect(websocket)
        else:
            session_handler = SessionHandler(session_id, script_id, self.ioloop)
            self.sessions[session_id] = session_handler
            session_handler.connect(websocket)

        websocket.on_close = lambda: self.close_connection(session_id)


    def close_connection(self, session_id):
        """
        Deletes the connection if the websocket is not reconnected within the timeout.
        """
        def _close_connection():
            session = self.sessions.get(session_id)
            if session and not session.websocket:
                self.sessions[session_id].close()
                del self.sessions[session_id]
                self.data_storage.cleanup()
                FileHandler.cleanup_session_files(session_id)


        self.sessions[session_id].websocket = None
        self.ioloop.call_later(Config.SESSION_INACTIVITY_TIMEOUT, _close_connection)


    def stop(self):
        self.script_storage.stop()

