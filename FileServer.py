
import web
import os
import os.path
import utils
import time
import logging
from contextlib import closing
from httplib import HTTPConnection

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
        _raise_if_dir_or_not_servable(filepath)
        _raise_if_locked(filepath)

        p = _get_local_path(filepath)

        with open(p, 'w') as f:
            f.write(web.data())

        web.header('Last-Modified', time.ctime(os.path.getmtime(p)))

        return ''
        
    def DELETE(self, filepath): # This'll remove the filepath if unlocked or if it gets the correct lock_id
        web.header('Content-Type', 'text/plain; charset=UTF-8')

        _raise_if_dir_or_not_servable(filepath)
        _raise_if_not_exists(filepath)
        _raise_if_locked(filepath)

        os.unlink(_get_local_path(filepath))
        return 'OK'
    
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
        
def _init_file_server():
    """Just notify the nameserver about which directories we serve."""

    host, port = utils.get_host_port(_config['nameserver'])
    with closing(HTTPConnection(host, port)) as con:
        data = 'srv=%s&dirs=%s' % (_config['srv'],
                                '\n'.join(_config['directories']),)
        con.request('POST', '/', data)

        
_config = {
        
        'lockserver': None,
        'nameserver': None,
        'directories': [],
        'fsroot': 'fs/',
        'srv': None,
        }

logging.info('Loading config file fileserver.dfs.json.')
utils.load_config(_config, 'fileserver.dfs.json')

_init_file_server()
