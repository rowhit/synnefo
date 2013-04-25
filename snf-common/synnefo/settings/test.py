import os
os.environ['SYNNEFO_SETTINGS_DIR'] = '/etc/synnefo-test-settings'

from synnefo.settings import *

DEBUG = False
TEST = True

DATABASES = {
    'default': {
        'ENGINE': 'sqlite3',
        'NAME': '/tmp/synnefo_test_db.sqlite',
    }
}

LOGGING_SETUP['handlers']['console']['level'] = \
    os.environ.get('SYNNEFO_TESTS_LOGGING_LEVEL', 'WARNING')

LOGIN_URL = 'http://host:port/'


SOUTH_TESTS_MIGRATE = bool(int(os.environ.get('SOUTH_TESTS_MIGRATE', True)))

ASTAKOS_IM_MODULES = ['local', 'shibboleth']
