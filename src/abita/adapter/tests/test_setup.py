from Products.CMFCore.utils import getToolByName
from abita.adapter.tests.base import IntegrationTestCase


class TestCase(IntegrationTestCase):
    """TestCase for Plone setup."""

    def setUp(self):
        self.portal = self.layer['portal']

    def test_is_abita_adapter_installed(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(installer.isProductInstalled('abita.adapter'))

    def test_uninstall__package(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['abita.adapter'])
        self.assertFalse(installer.isProductInstalled('abita.adapter'))
