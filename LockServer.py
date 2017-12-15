# -*- coding: utf-8 -*-
"""
Created on Thu Dec 11 22:33:44 2017

@author: Nikita Juyal
"""

import atexit
import datetime
import logging
import web
import utils
import collections
import shelve
import random

Lock = collections.namedtuple('Lock', 'lock_id granted last_used')

class LockServer: # lock server will handle locking of files


    def GET(self, filepath):
        
          #Return server with directory in which filepath is located.
          
           #filepath is the actual file path
        web.header('Content-Type', 'text/plain; charset=UTF-8')
        filepath = str(filepath)
        i = web.input()

        if filepath == '/': # To print dirs/lock
            
            return '\n'.join('%s=(%s, %s)' % (filepath,
                   str(_locks[filepath].granted), # list of files granted
                   str(_locks[filepath].last_used),) # list of last used file
                   for filepath in sorted(_locks))

        elif filepath not in _locks and 'lock_id' not in i:
            return 'OK' # Since no locks, just return OK

        elif 'lock_id' in i:
            lock = _locks.get(filepath, -1) # If lock_id is requested and filepath is locked
            try:
                if int(i['lock_id']) == lock.lock_id:
                    
                    _update_lock(filepath) #update last used file
                    return 'OK'
                else:
                    raise Exception("Bad lock_id") #Error

            except (Exception, ValueError) as e:
                # logging exception(e)
                _revoke_lock(filepath)
                raise web.conflict()

        elif _lock_expired(filepath):
            
            _revoke_lock(filepath)
            return 'OK'

        # IF its already locked, or wrong lock_id- error
        raise web.conflict()


    def POST(self, filepath):
        web.header('Content-Type', 'text/plain; charset=UTF-8')
        filepath = str(filepath)

        if filepath == '/':
            granted_locks = {}

            for filepath in web.data().split('\n'):
                if not filepath:
                       continue

                try:
                    granted_locks[filepath] = _grant_new_lock(filepath)
                except Exception as e:
                    logging.exception(e)

                    for filepath in granted_locks: #revoke all reviously allocated locks
                        _revoke_lock(filepath)

                    raise web.unauthorized()

            return '\n'.join('%s=%d' % (filepath, lock_id,) #list file name, lock id
                    for filepath, lock_id in granted_locks.items())

        try:
            return _grant_new_lock(filepath)
        except Exception as e:
            logging.exception(e)
            raise web.unauthorized()
            

    def DELETE(self, filepath):
        
        web.header('Content-Type', 'text/plain; charset=UTF-8')

        filepath = str(filepath)
        i = web.input()

        # allow deletion of multiple locks
        
        if filepath == '/':
            if 'filepaths' not in i or 'lock_ids' not in i:
                raise web.badrequest()

            #revoke locks if filepath =/
            for filepath, lock_id in zip(i['filepaths'].split('\n'), i['lock_ids'].split('\n')):
                if _locks[filepath].lock_id == int(lock_id):
                    _revoke_lock(filepath)

        return 'OK'
        
        elif filepath in _locks:
            if 'lock_id' in i:
                lock_id = i['lock_id']  

                if _locks[filepath].lock_id == int(lock_id):
                    _revoke_lock(filepath)   

                
                return 'OK'

            raise web.badrequest()

        else:
            return 'OK'
        
def _lock_expired(filepath): # If lock has expired
    
    last_used = _locks[filepath].last_used
    return (datetime.datetime.now() - last_used).seconds> _config['lock_lifetime']


def _grant_new_lock(filepath): # If new lock can be created. Also revokes the older lock and creates a new one in place
   
    if filepath in _locks:
        if not _lock_expired(filepath):
            #Lock has not expired
            raise Exception('Unable to grant a new lock (%s).' % filepath)

        _revoke_lock(filepath)

    return _new_lock(filepath)


def _new_lock(filepath): # creates new lock and returns lock id
   
    lock_id = random.randrange(0, 32068)
    logging.info('Granting lock (%d) on %s.', lock_id, filepath)
    t = datetime.datetime.now() # putting timestamp
    _locks[filepath] = Lock(lock_id, t, t)

    return lock_id


def _update_lock(filepath): #put new timestamp on last_used field
    t = datetime.datetime.now()

    logging.info('Update lock on %s from %s to %s.',
                 filepath, _locks[filepath].last_used, t)

    l = _locks[filepath]
    l = Lock(l.lock_id, l.granted, t)
    _locks[filepath] = l


def _revoke_lock(filepath): # Revoke lock
   
    if filepath in _locks:
        logging.info('Revoking lock on %s.', filepath)
        del _locks[filepath]

_config = {
            'dbfile': 'locks.db',
            'lock_lifetime': 60,
         }

logging.info('Loading config file lockserver.dfs.json.')
utils.load_config(_config, 'lockserver.dfs.json')
_locks = shelve.open(_config['dbfile'])

atexit.register(lambda: _locks.close())
