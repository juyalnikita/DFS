
import web
import os
import utils
import time

class FileServer: # This class will be responsible for storing and sharing files
    

    def GET(self, filepath): # fucntion will GET the correct file 
        
        web.header('Content-Type', 'text/plain; charset=UTF-8')
         _raise_if_dir_or_not_servable(filepath)
        _raise_if_not_exists(filepath)
        _raise_if_locked(filepath)
        
        p = _get_local_path(filepath)
        web.header('Last-Modified', time.ctime(os.path.getmtime(p)))
        with open(p) as f:
            return f.read()

    def PUT(self, filepath): # replace file by data
            pass
        
    def DELETE(self, filepath): # This'll remove the filepath if unlocked or if it gets the correct lock_id
        pass
    
    def HEAD(self, filepath):# To return the header/last time the file was modified
            
        pass

    
 
 def _get_local_path(filepath):  # convert filepath URL to local path in fileserver.
   
    return os.path.join(os.getcwd(), _config['fsroot'], filepath[1:])


def _raise_if_dir_or_not_servable(filepath): # raise exception 406 if file path should not be served

    p = _get_local_path(filepath)

    if (os.path.dirname(filepath) not in _config['directories'] or
            os.path.isdir(p)):
        # request a file which this server isn't supposed to serve!
        raise web.notacceptable()
        

def _raise_if_not_exists(filepath): # If filedoesn#t exist,raise exception 204
   
    p = _get_local_path(filepath)

    if not os.path.exists(p):
        raise web.webapi.HTTPError('204 No Content',
                                   {'Content-Type': 'plain/text'})

def _raise_if_locked(filepath): #Exception 401 if file is locked and lockid doesn't match as per the request

    i = web.input()

    host, port = utils.get_host_port(_config['lockserver'])
    if utils.is_locked(filepath, host, port, i.get('lock_id', None)):
        raise web.unauthorized()

_config = {
        
        'lockserver': None,
        'nameserver': None,
        'directories': [],
        'fsroot': 'fs/',
        'srv': None,
        }

