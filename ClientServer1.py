# -*- coding: utf-8 -*-

import utils
from tempfile import SpooledTemporaryFile
from httplib import HTTPConnection
from contextlib import closing


class DFSIOError(IOError): # Error when file is locked
    
    pass


class File(SpooledTemporaryFile):

    def __init__(self, filepath, mode='rtc'):
        

        self.mode = mode
        self.filepath = filepath
        host, port = utils.get_host_port(_config['nameserver'])
        self.srv = utils.get_server(filepath, host, port)
        
        
        self.last_modified = None
        
        SpooledTemporaryFile.__init__(self, _config['max_size'], mode.replace('c',''))

        host, port = utils.get_host_port(_config['lockserver'])
        if utils.is_locked(filepath, host, port):
            raise DFSIOError('The file %s is locked.' % filepath)

        if 'w' not in mode:
            host, port = utils.get_host_port(self.srv)
            with closing(HTTPConnection(host, port)) as con:
                con.request('GET', filepath)
                response = con.getresponse()
                self.last_modified = response.getheader('Last-Modified')
                status = response.status

                if status not in (200, 204):
                    raise DFSIOError('Error (%d)while opening file.' % status)

                if status != 204:
                    self.write(response.read())

                if 'r' in mode:
                    self.seek(0)

                self.lock_id = None

        if 'a' in mode or 'w' in mode: # automatically lock file if appending or writing in file
            host, port = utils.get_host_port(_config['lockserver'])
            self.lock_id = int(utils.get_lock(filepath, host, port))

        if 'c' in mode:
            File._cache[filepath] = self        
         #
         
         
    def __exit__(self):#Wil call close function
        
        pass
    
    def close(self):
        
        self.flush()
        if 'c' not in self.mode:
            SpooledTemporaryFile.close(self)
        
        
    def flush(self): # flush data to server
    
        SpooledTemporaryFile.flush(self)
        self.commit()
        
        
    def commit(self): # send local file to fileserver
        pass
        
        
_config = {
        'nameserver': None,
        'lockserver': None,
        'max_size': 1024 ** 2,
         } 

utils.load_config(_config, 'client.dfs.json')
