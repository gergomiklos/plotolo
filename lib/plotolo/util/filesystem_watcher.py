from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os


class DirectoryWatcher(FileSystemEventHandler):
    """
    Watcher for top-level subdirectory creations and deletions changes within the given directory.
    """
    def __init__(self, path, on_created, on_deleted):
        super().__init__()
        self.path = path
        self.observer = Observer()
        self.observer.schedule(self, self.path, recursive=True)
        self.on_created_callback = on_created
        self.on_deleted_callback = on_deleted

    def on_deleted(self, event):
        if event.is_directory and os.path.dirname(event.src_path) == self.path:  # only top-level subdirectories
            self.on_deleted_callback(os.path.basename(event.src_path))

    def on_created(self, event):
        if event.is_directory and os.path.dirname(event.src_path) == self.path:  # only top-level subdirectories
            self.on_created_callback(os.path.basename(event.src_path))

    def start(self):
        self.observer.start()

    def stop(self):
        self.observer.stop()

    def join(self):
        self.observer.join()


