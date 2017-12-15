import random

import dfs.client

if __name__ == '__main__':
    
    with dfs.client.open('/wtf/42', 'a') as filec:
        
        filec.write('%6d' % random.randint(0, 10 ** 6))

        try:
            open('/wtf/42')
            
        except:
            return 'OK'