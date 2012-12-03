from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer

import unittest


class AbitaAdapterLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        # Load ZCML
        import abita.adapter
        self.loadZCML(package=abita.adapter)

    def setUpPloneSite(self, portal):
        """Set up Plone."""
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'abita.adapter:default')

    def tearDownZope(self, app):
        """Tear down Zope."""


FIXTURE = AbitaAdapterLayer()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name="AbitaAdapterLayer:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name="AbitaAdapterLayer:Functional")


class IntegrationTestCase(unittest.TestCase):
    """Base class for integration tests."""

    layer = INTEGRATION_TESTING


class FunctionalTestCase(unittest.TestCase):
    """Base class for functional tests."""

    layer = FUNCTIONAL_TESTING
