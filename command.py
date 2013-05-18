# -*- coding: utf-8 -*-
import json
import hashlib

class Command(object):
    """ The base class for commands the clients can run.
        TBD (to be documented)
    """
    required = []

    def __init__(self, sock, data):
        self.sock = sock
        try:
            self.data = json.loads(data)
            if self.data['pwd']:
                self.data['pwd'] = hashlib.sha256(self.data['pwd']).hexdigest()
        except ValueError:
            self.error("Unable to decode request JSON")
            self._handle = False
            return
        except KeyError:
            pass
        missing = []
        for k in self.required:
            if k in self.data:
                continue
            missing.append(k)
        if missing:
            self.error("Missing keys: {0}".format(', '.join(missing)))
            self._handle = False
            return
        # This is so we don't call handle() unless we should
        self._handle = True

    def handle(self, *args, **kwargs):
        self.error("This command has not been implemented correctly")

    def success(self, payload, message=None, close=True):
        self.sock.send(json.dumps({
            "success": True,
            "message": message,
            "payload": payload
        }))
        if close:
            self.sock.close()

    def error(self, message, payload=None, close=True):
        self.sock.send(json.dumps({
            "success": False,
            "message": message,
            "payload": payload
        }))
        if close:
            self.sock.close()
