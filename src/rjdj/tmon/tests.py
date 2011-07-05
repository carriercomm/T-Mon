##############################################################################
#
# Copyright (c) 2011 Reality Jockey Ltd. and Contributors.
# All Rights Reserved.
#
##############################################################################

# -*- coding: utf-8 -*-

__docformat__ = "reStructuredText"

from django.conf import settings

import unittest, doctest

from django.db.backends.creation import BaseDatabaseCreation

from django.core import management
from django.core.cache import cache
from django.core.management import call_command
from django.core.management.commands.flush import Command as FlushCommand
from django.test import utils
from django.db import connection, transaction

from zope.testing.doctestunit import DocFileSuite

from rjdj.tmon.utils import db

KEEP_DATA = True

## https://bitbucket.org/andrewgodwin/south/changeset/21a635231327
class SkipFlushCommand(FlushCommand):
    def handle_noargs(self, **options):
        return

def patch(f):
    def wrapper(*args, **kwargs):
        # hold onto the original and replace flush command with a no-op
        from django.core.management import get_commands
        get_commands()
        original_flush_command = management._commands['flush']
        try:
            management._commands['flush'] = SkipFlushCommand()
            # run create_test_db
            f(*args, **kwargs)
        finally:
            # unpatch flush back to the original
            management._commands['flush'] = original_flush_command
    return wrapper

class DjangoLayer(object):
    
    saved_state = []

    @classmethod
    def setUp(self):
        utils.setup_test_environment()
        connection.creation.create_test_db = patch(connection.creation.create_test_db)
        connection.creation.create_test_db(verbosity = 0, autoclobber = True)
        
        db.connect(**settings.TRACKING_DATABASE)
        saved_state = [d for d in db.server]
        
    @classmethod
    def tearDown(self):
        call_command('flush', verbosity = 0, interactive = False)
        
        if not KEEP_DATA and db.database:
            for datab in db.server:
                if datab not in self.saved_state and not datab.startswith("_"):
                    del db.server[datab]

    @classmethod
    def testSetUp(self):
        pass

    @classmethod
    def testTearDown(self):
        call_command('flush', verbosity = 0, interactive = False)


def test_suite():
    collect = DocFileSuite('collect.txt',
        optionflags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,
        )
    analyze = DocFileSuite('analyze.txt',
        optionflags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,
        )

    suite = unittest.TestSuite((
                                collect,
                                analyze,
                                ))
    suite.layer = DjangoLayer
    return suite
