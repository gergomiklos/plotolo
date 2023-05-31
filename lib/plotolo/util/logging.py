import logging
from plotolo.config import Config

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.DEBUG if Config.DEBUG else logging.INFO
)
logger = logging.getLogger()


def to_msg(args):
    return ' '.join(str(arg) for arg in args)


class SessionLogger(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return f'{self.extra["session_id"]} - {msg}', kwargs

    @classmethod
    def getLogger(cls, session_id: str):
        return cls(logger, {'session_id': session_id[:8]})

    def debug(self, *args):
        super().debug(to_msg(args))

    def info(self, *args):
        super().debug(to_msg(args))

    def warning(self, *args):
        super().debug(to_msg(args))

    def error(self, *args):
        super().debug(to_msg(args))
