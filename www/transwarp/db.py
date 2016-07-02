#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Database operation module.
"""

import time, uuid, functools, threading, logging

# Dict object:

class Dict(dict):
    """
    Simple dict but support access x.y style
    """
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(*kw)
        for k, v, in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" %(key))

    def __setattr__(self, key, value):
        self[key] = value
            

def next_id(t=None):
    """
    Return next id as 50-char string.

    Args:
        t: unix timestamp, default to None and using time.time().
    """
    if t is None:
        t = time.time()
    return '%015d%s000' % (int(t*1000), uuid.uuid4().hex)

def _profiling(start, sql=''):
    t = time.time() -start
    if t > 0.1:
        logging.warning('[PROFILING] [DB] %s : %s' % (t, sql))
    else:
        logging.info('[PROFILING] [DB] %s : %s' %(t, sql))

class DBError(Exception):
    pass

class MultiColumnsError(DBError):
    pass

class _LazyConnection(object):
    def __init__(self):
        self.connection = None

    def cursor(self):
        if self.connection is None:
            connection = engine.connect()
            logging.info('open connection <%s>...' % hex(id(connection)))
            self.connection = connection
        return self.connection.curor()
    
    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def cleanup(self):
       if self.connection:
           connection = self.connection
           self.connection = None
           logging.info('close connection <%s>...' % hex(id(connection)))
           connection.close()


