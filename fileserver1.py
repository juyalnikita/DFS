
import web


class FileServer: # This class will be responsible for storing and sharing files
    

    def GET(self, filepath): # fucntion will GET the correct file 
        
        web.header('Content-Type', 'text/plain; charset=UTF-8')
        

    def PUT(self, filepath): # replace file by data
            pass
        
    def DELETE(self, filepath): # This'll remove the filepath if unlocked or if it gets the correct lock_id
        pass
    
    def HEAD(self, filepath):# To return the header/last time the file was modified
            
        pass
    

_config = {
        
        'lockserver': None,
        'nameserver': None,
        'directories': [],
        'fsroot': 'fs/',
        'srv': None,
        }

