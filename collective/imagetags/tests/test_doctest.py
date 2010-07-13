import unittest

from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite

from collective.imagetags.tests import base

ztc.installProduct('collective.imagetags')
ptc.setupPloneSite(products=['collective.imagetags'])

import collective.imagetags

class TestCase(ptc.PloneTestCase):
    class layer(PloneSite):
        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml',
                             collective.imagetags)
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass


def test_suite():
    return unittest.TestSuite([

        # Unit tests
        #doctestunit.DocFileSuite(
        #    'README.txt', package='collective.imagetags',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        #doctestunit.DocTestSuite(
        #    module='collective.imagetags.browser.helper',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        # Integration tests that use PloneTestCase
        ztc.ZopeDocFileSuite(
            'docs/vocabulary.txt', package='collective.imagetags',
            test_class=base.FunctionalTestCase),
            
        # Integration tests that use PloneTestCase
        ztc.ZopeDocFileSuite(
            'docs/browser.txt', package='collective.imagetags',
            test_class=base.FunctionalTestCaseWithContent),


        # Integration tests that use PloneTestCase
        #ztc.ZopeDocFileSuite(
        #    'README.txt', package='collective.imagetags',
        #    test_class=base.FunctionalTestCase),


        #ztc.FunctionalDocFileSuite(
        #    'browser.txt', package='collective.imagetags',
        #    test_class=TestCase),

        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
