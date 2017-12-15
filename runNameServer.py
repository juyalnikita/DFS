# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 20:54:41 2017

@author: Nikita Juyal
"""

import web

import dfs.nameserver

urls = (
        '(/.*)', 'dfs.nameserver.NameServer',
       )

app = web.application(urls, globals())


if __name__ == '__main__':
    app.run()