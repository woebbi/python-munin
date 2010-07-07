from __future__ import division

import os
import re
import socket
import time
from subprocess import Popen, PIPE

from munin import MuninPlugin

class MuninCassandraPlugin(MuninPlugin):
    category = "Cassandra"

    def __init__(self, *args, **kwargs):
        super(MuninCassandraPlugin, self).__init__(*args, **kwargs)
        self.nodetool_path = os.environ["NODETOOL_PATH"]
        self.host = socket.gethostname()

    def execute_nodetool(self, cmd):
        p = Popen([self.nodetool_path, "-host", self.host, cmd], stdout=PIPE)
        output = p.communicate()[0]
        return output

    def parse_cfstats(self, text):
        text = text.strip().split('\n')
        cfstats = {}
        cf = None
        for line in text:
            line = line.strip()
            if not line or line.startswith('-'):
                continue

            name, value = line.strip().split(': ', 1)
            if name == "Keyspace":
                ks = {'cf': {}}
                cf = None
                cfstats[value] = ks
            elif name == "Column Family":
                cf = {}
                ks['cf'][value] = cf
            elif cf is None:
                ks[name] = value
            else:
                cf[name] = value
        return cfstats

    def cfstats(self):
        return self.parse_cfstats(self.execute_nodetool("cfstats"))