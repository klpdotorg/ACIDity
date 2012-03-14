# -*- coding: utf-8 -*-

import warnings
import traceback
import sqlalchemy

warnings.simplefilter('ignore', DeprecationWarning)
warnings.simplefilter('ignore', sqlalchemy.exceptions.SAWarning)

import os
import sys
from pprint import pformat

from pyramid.config import Configurator
from pyramid.security import authenticated_userid
import pyramid.httpexceptions

from pyramid_beaker import set_cache_regions_from_settings
from beaker import cache as bcache
from pyramid_whoauth.auth import WhoAuthenticationPolicy

import db.schema as schema
from common.log import logger

log = logger("rest")

default_config_file = os.path.join(epsilon_base, 'conf', 'epsilon.ini')
default_key_file = os.path.join(epsilon_base, 'conf', 'keyfile')
conf_dir_path = os.path.join(epsilon_base, 'conf')
epsilon_version = get_epsilon_version()


def load_epsilon_env(settings={}):
    """Load up and init the epsilon specific stuff"""
    epsilon_config_file = settings.get('epsilon_config', default_config_file)
    epsilon_key_file = settings.get('epsilon_key', default_key_file)
    print "epsilon:", epsilon_config_file

    if not os.path.exists(epsilon_config_file):
        print >> sys.stderr, "Could not find epsilon config file %s" % epsilon_config_file
        sys.exit(1)

    if not os.path.exists(epsilon_key_file):
        print >> sys.stderr, "Could not find epsilon key file %s" % epsilon_key_file
        sys.exit(1)

    epsilon_cfg = server_config(epsilon_config_file)

    dburi = epsilon_cfg.get('dburi', '')
    scramble.init(epsilon_key_file)
    meta, Session, engine = init_model_webapp(dburi=dburi)
    log.debug("engine:%s url:%s" % (engine, dburi))
    DBSession.configure(bind=engine)


def verify_user(identity, request):
    #log.debug("identity:\n%s" % (pformat(dict(identity.items())),))
    log.debug("verify_user: %s" % request.path_info)
    # caller = get_caller_name(3)
    # log.debug("caller: %s" % caller)
    if not identity.get('user', None):
        return False
    if not identity.get('group', None):
        return False
    return ((identity['user'], identity['group']),)


def get_user(request):
    token = authenticated_userid(request)
    if token and len(token)==2:
        return token[0]


def get_group(request):
    token = authenticated_userid(request)
    if token and len(token)==2:
        return token[1]


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    #setup auth first
    authentication_policy = WhoAuthenticationPolicy.from_settings(settings)
    authorization_policy = EpsilonKuberAuthorizationPolicy()

    set_cache_regions_from_settings(settings)
    init_caches()

    config = Configurator(settings=settings,
                          root_factory=RootFactory,
                          authentication_policy=authentication_policy,
                          authorization_policy=authorization_policy)

    config.set_request_property(get_user, 'user', reify=True)
    config.set_request_property(get_group, 'group', reify=True)

    config.add_view('pyramid.view.append_slash_notfound_view',
                    context='pyramid.httpexceptions.HTTPNotFound')

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')

    config.add_route('row', '/tables/{tableid:\d+}/rows/{rowid:\d+}/{action}')
    config.add_route('row_create', '/tables/{tableid:\d+}/rows/create')
    config.add_route('row_get', '/tables/{tableid:\d+}/rows/{rowid:\d+}/')
    config.add_route('row_index', '/tables/{tableid:\d+}/rows/')
    config.add_route('table', '/tables/{tableid:\d+}/{action}')
    config.add_route('table_index', '/tables/')
    config.add_route('table_create', '/tables/create')
    config.add_route('type', '/types/{typeid:\d+}/{action}')
    config.add_route('type_index', '/types/')
    config.add_route('type_create', '/types/create')

    config.scan()

    load_epsilon_env(settings)

    log.info("Kuber is hoarding data for Epsilon %s" % epsilon_version)

    return HttpMethodOverrideMiddleware(config.make_wsgi_app())

