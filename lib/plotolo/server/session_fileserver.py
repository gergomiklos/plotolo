import os
import shutil

import tornado.ioloop
import tornado.web

from plotolo.util.constant import SESSION_COOKIE_NAME
from plotolo.config import ROOT_SESSION_DIR


class FileHandler(tornado.web.StaticFileHandler):
    """
    This handler is used to serve files inside the user's session,
    used by the download and upload widgets.
    """


    def parse_url_path(self, path):
        """
        This method is called by the tornado framework to parse the url path into a filesystem path.
        """
        session_id = self.authenticate_session()

        root_directory = os.path.join(ROOT_SESSION_DIR, session_id)
        os.makedirs(root_directory, exist_ok=True)

        if path:
            path = os.path.join(root_directory, path)
        else:
            path = root_directory

        return path


    async def post(self, url_path=None):
        # it is not allowed to upload files to the script's directory from a user session
        session_id = self.authenticate_session()

        fileinfo = self.request.files['file'][0]
        path = self.parse_url_path(url_path)
        directory = os.path.join(ROOT_SESSION_DIR, session_id, path)
        # Create the directory if it doesn't exist
        os.makedirs(directory, exist_ok=True)

        filepath = os.path.join(directory, fileinfo['filename'])
        with open(filepath, 'wb') as f:
            f.write(fileinfo['body'])

        self.set_status(200)
        await self.finish()


    def authenticate_session(self):
        session_id = self.get_cookie(SESSION_COOKIE_NAME, None)
        if not session_id:
            raise tornado.web.HTTPError(401)
        return session_id


    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')


    @staticmethod
    def cleanup_session_files(session_id):
        directory = os.path.join(ROOT_SESSION_DIR, session_id)
        shutil.rmtree(directory, ignore_errors=True)
