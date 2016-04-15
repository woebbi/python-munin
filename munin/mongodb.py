#!/usr/bin/env python

import os
from munin import MuninPlugin
import pymongo


class MuninMongoPlugin(MuninPlugin):

    category = "Mongo"
    dbname = None

    def __init__(self, config='serverStatus'):
        super(MuninMongoPlugin, self).__init__()
        if not self.dbname:
            self.dbname = os.environ.get('MONGODB_DATABASE')

        if 'MONGO_DB_URI' in os.environ:
            self.connection = pymongo.MongoClient(os.environ['MONGO_DB_URI'])
        else:
            self.connection = pymongo.MongoClient()
        self.server_status = self.connection.admin.command(config, workingSet=True)

    @property
    def db(self):
        if self.dbname is None:
            return None
        if not hasattr(self, '_db'):
            self._db = getattr(self.connection, self.dbname)
        return self._db

    def autoconf(self):
        return bool(self.connection)
