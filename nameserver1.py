import os

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