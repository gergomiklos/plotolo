import os
import shutil
import zipfile

import tornado.ioloop
import tornado.web

from plotolo.util.util import hash_string
from plotolo.config import ROOT_SCRIPT_DIR


class ScriptFileHandler(tornado.web.RequestHandler):
    """
    This handler is responsible for uploading, downloading, and deleting Jupyter Notebook files on the server.
    """

    async def post(self):
        """
        Upload a script file to the server as a .zip or .ipynb file
        """
        self.authenticate()

        fileinfo = self.request.files['file'][0]
        filename = fileinfo['filename']

        if not (filename.endswith('.ipynb') or filename.endswith('.zip')):
            raise tornado.web.HTTPError(400, reason="Invalid file type. Please upload .ipynb or .zip file.")

        # Calculate hte script's id and create its directory
        script_id = hash_string(filename)
        directory = os.path.join(ROOT_SCRIPT_DIR, script_id)
        os.makedirs(directory, exist_ok=True)

        # Save the file
        filepath = os.path.join(directory, filename)
        with open(filepath, 'wb') as f:
            f.write(fileinfo['body'])

        # Unzip if the file is a zip file
        if filename.endswith('.zip'):
            with zipfile.ZipFile(filepath, 'r') as z:
                z.extractall(directory)

        self.set_status(200)
        await self.finish()


    async def get(self, script_id):
        """
        Download the script as a .zip or .ipynb file based on availability
        """
        self.authenticate()

        path = os.path.join(ROOT_SCRIPT_DIR, script_id)
        if not os.path.exists(path):
            raise tornado.web.HTTPError(404)

        # Look for .zip file, else look for .ipynb files to serve based on availability

        filepath = None
        # Iterate over all files in the directory
        for file in os.listdir(path):
            # Check if current file is a .zip file
            if file.endswith(".zip"):
                filepath = os.path.join(path, file)
                break

        # If no .zip file found, search for a .ipynb file
        if filepath is None:
            for file in os.listdir(path):
                if file.endswith(".ipynb"):
                    filepath = os.path.join(path, file)
                    break

        if not filepath:
            raise tornado.web.HTTPError(404)

        filename = os.path.basename(filepath)
        # stream file in chunks for efficiency
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', f'attachment; filename={filename}')
        with open(filepath, 'rb') as f:
            while True:
                # read and send 10MB at a time
                data = f.read(1024 * 1024 * 10)
                if not data:
                    break
                self.write(data)
                await self.flush()
        await self.finish()


    async def delete(self, script_id):
        """
        Delete the script's directory or return 404 if it doesn't exist.
        """
        self.authenticate()

        directory = os.path.join(ROOT_SCRIPT_DIR, script_id)

        if not os.path.exists(directory):
            raise tornado.web.HTTPError(404)

        shutil.rmtree(directory, ignore_errors=True)

        self.set_status(200)
        await self.finish()


    def authenticate(self):
        pass  # todo


    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')


    @staticmethod
    def cleanup_files():
        shutil.rmtree(ROOT_SCRIPT_DIR, ignore_errors=True)
