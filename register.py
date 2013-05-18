# -*- coding: utf-8 -*-
import json
import random
import mongo
import command
from hashlib import sha1


class Register(command.Command):
    """Allows clients to register an account. The
server generates a random address and password,
registers it, and sends it back to the client.

fingerprint: {"cmd": "register"}
"""
    required = []

    def handle(self, *args, **kwargs):

        # Send error message to old clients, that used to chose the address themselves.
        try:
            self.data['addr'], self.data['pwd']
            self.error("Registration failed. Update your client.")
        except KeyError:
            pass
        
        addr = sha1(str(random.randint(0, 100000000000000))).hexdigest()
        pwd = sha1(str(random.randint(0, 100000000000000))).hexdigest()

        # Making sure the address doesn't exist already.
        while mongo.db.addresses.find_one({"addr": addr}):
            addr = sha1(str(random.randint(0, 100000000000000))).hexdigest()

        mongo.db.addresses.insert({"addr": addr, "pwd": pwd})
        self.success({"addr": addr, "pwd": pwd})
