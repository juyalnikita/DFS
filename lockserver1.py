# -*- coding: utf-8 -*-
"""
Created on Thu Dec 11 22:33:44 2017

@author: Nikita Juyal
"""


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