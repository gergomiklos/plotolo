import asyncio

import tornado.ioloop
import tornado.web
import tornado.websocket

from plotolo.config import Config
from plotolo.util.logging import logger
from plotolo.server.session_fileserver import FileHandler
from plotolo.server.session_server import SessionServer, AuthHandler, WebSocketHandler
from plotolo.server.app_server import AppHandler
from plotolo.server.script_fileserver import ScriptFileHandler
from plotolo.util.constant import WELCOME_MESSAGE


def start_plotolo(port: int = 8088):
    """
    Starts the tornado web application inclu
    """


    async def _start():
        ioloop = tornado.ioloop.IOLoop.current()
        SessionServer.get_current().listen(ioloop)

        tornado_web_application = tornado.web.Application([
            (r"/apps/ws/(.*)", WebSocketHandler),
            (r"/auth/(.*)", AuthHandler),
            (r"/apps/(.*)", AppHandler),
            (r"/apps", AppHandler),
            (r"/scripts/(.*)", ScriptFileHandler),
            (r"/scripts", ScriptFileHandler),
            (r"/file/(.*)", FileHandler, {"path": "/"}),
            (r"/file", FileHandler, {"path": "/"}),
        ],
            settings={
                'compress_response': Config.COMPRESS_RESPONSE,  # enable gzip compression
                'websocket_ping_interval': 30,  # ping every 30 seconds
                'websocket_ping_timeout': 60,  # wait 60 seconds for pong response
                'cookie_secret': Config.COOKIE_SECRET,
                'xsrf_cookies': Config.ENABLE_XSRF,
                'static_hash_cache': False,  # disable path resolution cache for static files
            }
        )

        tornado_web_application.listen(port)
        logger.info(WELCOME_MESSAGE)
        logger.info('Plotolo started listening on port: %d', port)
        await asyncio.Event().wait()

        SessionServer.get_current().stop()


    asyncio.run(_start())


if __name__ == '__main__':
    start_plotolo()
