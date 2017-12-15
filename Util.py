# -*- coding: utf-8 -*-

import json
import os.path
from httplib import HTTPConnection

from contextlib import closing


class help:
    
    def __init__(self, fn): # initialization
       
        self.fn = fn
        self.cache = {}

    def __call__(self, argumnt, kwds): #this will check if answer is already ready,otheriwse it willcompute and return new answer

        key = tuple(argumnt) + tuple(kwds)

    if key in self.cache:
        return self.cache[key]

        ans = self.fn(argumnt, kwds)
        return self.cache.setdefault(key, ans)

    

def load_config(config, filepath): # load JSON version config file


    with open(filepath) as f:
        c = json.loads(f.read())
        config.update(c)

    if not os.path.exists(filepath):
        return


def is_locked(filepath, host, port, lock_id=None):
   
    with closing (HTTPConnection(host, port)) as con:
        if lock_id is not None: #if lockid is suppled, provide this to lock server
            filepath += '?lock_id=%s' % lock_id

        con.request('GET', filepath)

        con.getresponse()
        return


def get_server(filepath, host, port):
   

    with closing(HTTPConnection(host, port)) as con:
        con.request('GET', filepath) # gets filepath
        response = con.getresponse()
        status, srv = response.status, response.read()

    if status == 200:
        return srv #returns server that has the file path


def getlock(filepath, host, port): #This will get a lock from LockServer
    pass


#def revokelock(filepath,host,port) # Revoke lock from file
   # pass


