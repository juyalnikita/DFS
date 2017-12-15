# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 22:58:49 2017

@author: Nikita Juyal
"""

import web

import dfs.lockserver

urls = (
        '(/.*)', 'dfs.lockserver.LockServer',
       )

app = web.application(urls, globals())


if __name__ == '__main__':
    app.run()