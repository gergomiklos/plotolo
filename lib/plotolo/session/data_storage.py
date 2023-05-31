import gc


class DataStorage:
    """
    Stores hash-data pairs globally for the whole application,
    to avoid storing the same data multiple times between widgets and _sessions.
    """
    _singleton: 'DataStorage' = None

    @classmethod
    def get_current(cls) -> 'DataStorage':
        if DataStorage._singleton is None:
            DataStorage._singleton = DataStorage()
        return DataStorage._singleton


    def __init__(self):
        if DataStorage._singleton is not None:
            raise RuntimeError("Singleton already initialized. Call 'get_current' instead")
        DataStorage._singleton = self

        self._data: dict[str, any] = {}


    def get(self, hash: str, default=None):
        return self._data.get(hash, default)


    def set(self, hash: str, value: any):
        self._data[hash] = value


    def delete(self, hash):
        from plotolo.server.session_server import SessionServer

        if not self._data.get(hash):
            return

        for session in SessionServer.get_current().sessions.values():
            if session.has_hash(hash):
                return

        del self._data[hash]
        gc.collect()


    def cleanup(self):
        for hash in list(self._data.keys()):
            self.delete(hash)
