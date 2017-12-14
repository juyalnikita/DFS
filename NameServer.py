import os
import atextit
import shelve
import logging

class NameServer:#Map directory name and file server
      
     def GET(self, filepath):
           #Return server with directory in which filepath is located.
          
           #filepath is the actual file path
 
        web.header('Content-Type', 'text/plain; charset=UTF-8')
        filepath = str(filepath)

        if filepath == '/': 
            return '\n'.join('%s=%s' % (directorypath, _names[directorypath]) # return list of directory 
                    
        for directorypath in sorted(_names))

        directorypath = str(os.path.directoryname(filepath))
        
        if directorypath in _names:
            return _names[directorypath]

        raise web.notfound('No file server serve this file.')


     def POST(self, directorypath):
        
        return _update(str(directorypath)) # posts the path of directory

    def DELETE(self, directorypath):
        
        return _update(str(directorypath), False)
      

      
def _update(directorypath, add=True): #Adding directory/server to the name server.
          

    web.header('Content-Type', 'text/plain; charset=UTF-8')
    i = web.input()

    if 'srv' not in i:
        raise web.badrequest()

    srv = i['srv'] #srv is the server to associate with dirpath

    if directorypath == '/': 
        if 'dirs' not in i: 
            raise web.badrequest()

        for directorypath in i['dirs'].split('\n'): # if directorypath='/', add list of directories from dir
            if not directorypath:
                continue

            try:
                _update_names(directorypath, srv, add)
            except ValueError as e:
                logging.exception(e)

    else:
        try:
            _update_names(directorypath, srv, add) 
        except ValueError as e:
            logging.exception(e)

    return 'OK'


def _update_names(directorypath, srv, add=True):
   
    if directorypath[-1] == '/':
        directorypath = os.path.dirname(directorypath)

    if add:
        logging.info('Update directory %s on %s.', directorypath, srv)  #adding both directory service and srv
        _names[directorypath] = srv

    elif directorypath in _names:
        logging.info('Remove directory %s on %s.', directorypath, srv)
        del _names[directorypath]   # if not True, delete the directory path

    else:
        raise ValueError('%s was not deleted, because it wass not in the dictionary database.' % directorypath)

_config = {
            'dbfile': 'names.db',
         }


logging.info('Loading config file nameserver.dfs.json.')
utils.load_config(_config, 'nameserver.dfs.json')
_names = shelve.open(_config['dbfile'])
atexit.register(lambda: _names.close())
