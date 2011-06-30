##############################################################################
#
# Copyright (c) 2011 Reality Jockey Ltd. and Contributors.
# All Rights Reserved.
#
##############################################################################

# -*- coding: utf-8 -*-

__docformat__ = "reStructuredText"

import settings

import unittest, doctest

from django.db.backends.creation import BaseDatabaseCreation

from django.core import management
from django.core.cache import cache
from django.core.management import call_command
from django.core.management.commands.flush import Command as FlushCommand
from django.test import utils
from django.db import connection, transaction

from zope.testing.doctestunit import DocFileSuite

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

    @classmethod
    def setUp(self):
        utils.setup_test_environment()
        connection.creation.create_test_db = patch(connection.creation.create_test_db)
        connection.creation.create_test_db(verbosity = 0, autoclobber = True)
        

    @classmethod
    def tearDown(self):
        call_command('flush', verbosity=0, interactive=False)

    @classmethod
    def testSetUp(self):
        pass

    @classmethod
    def testTearDown(self):
        call_command('flush',verbosity=0,interactive=False)


def test_suite():
    collect = DocFileSuite('collect.txt',
        optionflags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,
        )

    suite = unittest.TestSuite((
                                collect,
                                ))
    suite.layer = DjangoLayer
    return suite
