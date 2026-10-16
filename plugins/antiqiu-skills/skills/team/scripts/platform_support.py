"""Native Windows support without changing worker permissions or model choices."""

import os
import queue
import subprocess
import sys
import threading


WINDOWS_ENV = {'SYSTEMROOT', 'WINDIR', 'COMSPEC', 'PATHEXT', 'USERPROFILE',
               'HOMEDRIVE', 'HOMEPATH', 'APPDATA', 'LOCALAPPDATA', 'TEMP', 'TMP'}


def deny_hook_command(config_root):
    if os.name == 'nt':
        return subprocess.list2cmdline([sys.executable, '-B', str(config_root / 'deny-tool.py')])
    import shlex
    return '/bin/sh ' + shlex.quote(str(config_root / 'deny-tool.sh'))


class PipeEvents:
    """Read both anonymous pipes; Windows select() supports sockets only."""

    def __init__(self, process):
        self.events = queue.Queue()
        self.active = {'stdout', 'stderr'}
        self.readers = []
        for name in self.active:
            reader = threading.Thread(target=self._read, args=(name, getattr(process, name)), daemon=True)
            reader.start()
            self.readers.append(reader)

    def _read(self, name, pipe):
        try:
            while chunk := os.read(pipe.fileno(), 65536):
                self.events.put((name, chunk))
        finally:
            self.events.put((name, b''))

    def read(self, timeout):
        try:
            name, chunk = self.events.get(timeout=timeout)
        except queue.Empty:
            return []
        if not chunk:
            self.active.discard(name)
        return [(name, chunk)]

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        # The caller stops its process before closing the pipes. Reader threads
        # are daemons so an abnormal CLI shutdown cannot keep the launcher alive.
        for reader in self.readers:
            reader.join(timeout=.05)
