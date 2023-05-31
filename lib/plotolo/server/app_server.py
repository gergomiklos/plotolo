import os
import shutil
from enum import Enum
import zipfile

import tornado.ioloop
import tornado.web

from plotolo.script.script_storage import ScriptStorage


class AppHandler(tornado.web.RequestHandler):
    """
    Returns scripts as a list of all apps (or a single app)
    """

    async def get(self, appId=None):

        self.authenticate()

        if appId:
            script = ScriptStorage.get_current().get(appId)
            if not script:
                raise tornado.web.HTTPError(404)
            else:
                self.write({'name': script.name, 'id': script.id})
        else:
            apps = [{'name': script.name, 'id': script.id} for script in ScriptStorage.get_current().all()]
            self.write({'apps': apps})

        await self.finish()


    def authenticate(self):
        pass  # todo server-side authentication
