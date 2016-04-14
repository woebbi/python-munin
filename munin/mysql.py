#!/usr/bin/python3

import os, sys, re
from configparser import SafeConfigParser
from munin import MuninPlugin
import pymysql.cursors


class MuninMySQLPlugin(MuninPlugin):
    dbname_in_args = False
    category = "MySQL"

    def __init__(self):
        super(MuninMySQLPlugin, self).__init__()
        self.default_name = "mobigate"
        self.dbname = ((sys.argv[0].rsplit('_', 1)[-1] if self.dbname_in_args else None)
                       or os.environ.get('DATABASE') or self.default_name)

        self.conninfo = dict(
            user="root",
            host="localhost",
            password="sa",
            cursorclass=pymysql.cursors.DictCursor
        )

        cnfpath = ""

        m = re.findall(r"--defaults-file=([^\s]+)", os.environ.get("mysqlopts") or "")
        if m:
            cnfpath = m[0]

        if not cnfpath:
            m = re.findall(r"mysql_read_default_file=([^\s;:]+)", os.environ.get("mysqlconnection") or "")
            if m:
                cnfpath = m[0]

        if cnfpath:
            cnf = SafeConfigParser()
            cnf.read([cnfpath])
            for section in ["client", "munin"]:
                if not cnf.has_section(section):
                    continue
                for connkey, opt in [("user", "user"), ("passwd", "password"), ("host", "host"), ("port", "port")]:
                    if cnf.has_option(section, opt):
                        self.conninfo[connkey] = cnf.get(section, opt)

        for k in ('user', 'passwd', 'host', 'port'):
            # Use lowercase because that's what the existing mysql plugins do
            v = os.environ.get(k)
            if v:
                self.conninfo[k] = v

    def connection(self):
        if not hasattr(self, '_connection'):
            connection = pymysql.connect(**self.conninfo)
        return connection

    def cursor(self):
        return self.connection().cursor()

    def autoconf(self):
        return bool(self.connection())
