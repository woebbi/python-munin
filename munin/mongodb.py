#!/usr/bin/env python

import os
from munin import MuninPlugin
import pymongo


class MuninMongoPlugin(MuninPlugin):
    category = "Mongo"

    def __init__(self):
        super(MuninMongoPlugin, self).__init__()
        if 'MONGO_DB_URI' in os.environ:
            c = pymongo.MongoClient(os.environ['MONGO_DB_URI'])
        else:
            c = pymongo.MongoClient()
        self.server_status = c.admin.command('serverStatus', workingSet=True)

    def autoconf(self):
        return bool(self.server_status)
