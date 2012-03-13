#!/usr/bin/env python

import os, sys
import argparse

import db.schema as schema
import common.config as config

# FIXME: Setup paths properly
sys.path.append('/home/alok/src/proto/')
default_config_file = os.path.join('.', 'conf', 'klp.ini')

def handle_init(args):
    """Initialise tables"""
    log.debug("Creating tables in %s" % engine.url.database)
    meta.create_all(engine, False)
    
def handle_reset(args):
    """Initialise tables"""
    cfg = config.core_config(args.config)

    meta, sess, engine = schema.init_model(cfg['dburi'])
    log.debug("Dropping tables in %s" % engine.url.database)
    meta.drop_all(engine)
    log.debug("Creating tables in %s" % engine.url.database)
    meta.create_all(engine, False)

def initdb(meta, engine, sess, admin_pw):
    url=engine.url
    log.info("Creating tables on %s@%s/%s" % (url.username, url.host, url.database))
    meta.create_all(engine, False)
    #create admin
    (admin, wheel, staff) = bootstrap(admin_pw, sess)
    #log.debug('created (admin, wheel, staff) : (%s,%s,%s)' % (admin, wheel, staff))

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="KLP Core DB tool")

    parser.add_argument('-c', '--config', default=default_config_file, metavar='configfile',
                        help="KLP core config file (default %(default)s)")
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="Be verbose, generate more log output")

    subparsers = parser.add_subparsers(title='subcommands', help='sub-command to run')

    #init command
    parser_init = subparsers.add_parser('init',
                                        help='Initialize KLP Core DB to fresh values')
    parser_init.set_defaults(func=handle_init)

    #reset command
    parser_reset = subparsers.add_parser('reset',
                                          help='Drop the KLP Core DB')
    parser_reset.set_defaults(func=handle_reset)

    args = parser.parse_args()
    cfg = config.core_config(args.config)

    meta, sess, engine = schema.init_model(cfg['dburi'])
    #FIXME: WTF is happening here ??
    #FIXME: Why doesn't set_defaults() fire ?
    meta.drop_all(engine)
    meta.create_all(engine, False)
