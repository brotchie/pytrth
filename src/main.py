#!/usr/bin/env python

import sys

import db
import api

import mx.DateTime

def expose(f):
    expose.exposed.add(f)
    return f
expose.exposed = set()

class Operations(object):
    def __init__(self):
        self._api = api.TRTHApi()
        self._api.setup()
        self._db = db.connect()

    @expose
    def getoptionexpirymonths(self):
        expiry_months = self._api.GetOptionExpiryMonths()
        c = self._db.cursor()
        c.execute('DROP TABLE IF EXISTS expiry_months')
        c.execute('CREATE TABLE expiry_months (label CHAR, month STRING, monthint INT)')
        for d in expiry_months.data:
            if d.field != 'OptionMonth':
                continue
            for label in d.value:
                c.execute('INSERT INTO expiry_months (label, month, monthint) VALUES (?,?,?)', (label, d.longName, mx.DateTime.Month[d.longName]))
        self._db.commit()

    def get_exposed(self):
        exposed = [f.__name__ for f in 
                    expose.exposed & set(self.__class__.__dict__.values())]
        exposed.sort()
        return exposed
            
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: %s command [arg1 arg2 ...]' % (sys.argv[0],)
        sys.exit(1)

    operations = Operations()
    getattr(operations, sys.argv[1])()
