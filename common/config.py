# -*- coding: utf-8 -*-

import os
from ConfigParser import SafeConfigParser, NoOptionError

def core_config(cfile):
    """Read the config file for the core DB"""

    default_config_file = os.path.join(os.getcwd(), 'conf', 'klp.ini')
    cfile = cfile if cfile else default_config_file
    
    defaults = { 'user': 'klp',
                 'password': '',
                 'dialect': 'postgresql',
                 'spath': '/var/run/postgresql' # Path to UDS
                 }

    config = SafeConfigParser(defaults)
    config.read(cfile)
    db = dict(config.items('db'))

    cfg = {}
    cfg['dburi'] = "{dialect}://{user}:{password}@{host}/{name}".format(**db)

    return cfg
