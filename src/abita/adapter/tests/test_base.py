from Products.CMFCore.utils import getToolByName
from abita.adapter.tests.base import IntegrationTestCase
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

import mock


class TestCase(IntegrationTestCase):
    """TestCase for Plone setup."""

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])


    def test__get_brains__empty(self):
        from abita.adapter.interfaces import IBaseAdapter
        base = IBaseAdapter(self.portal)

        query = {}

        self.assertEqual(len(base.get_brains(**query)), 0)
        self.assertEqual(len(base.get_content_listing(**query)), 0)
        self.assertIsNone(base.get_brain(**query))

    def test__one_folder(self):
        """Add folder under portal."""
        from abita.adapter.interfaces import IBaseAdapter
        base = IBaseAdapter(self.portal)

        folder1 = self.portal[self.portal.invokeFactory('Folder', 'folder1')]
        folder1.reindexObject()

        query = {}

        self.assertEqual(len(base.get_brains(**query)), 1)
        self.assertEqual(len(base.get_content_listing(**query)), 1)
        self.assertEqual(base.get_brain(**query).id, 'folder1')

        query = {'path': '/'.join(folder1.getPhysicalPath())}

        self.assertEqual(len(base.get_brains(**query)), 1)
        self.assertEqual(len(base.get_content_listing(**query)), 1)
        self.assertEqual(base.get_brain(**query).id, 'folder1')

        query['depth'] = 0
        self.assertEqual(len(base.get_brains(**query)), 1)
        self.assertEqual(len(base.get_content_listing(**query)), 1)
        self.assertEqual(base.get_brain(**query).id, 'folder1')

        query['depth'] = 1
        self.assertEqual(len(base.get_brains(**query)), 0)
        self.assertEqual(len(base.get_content_listing(**query)), 0)
        self.assertIsNone(base.get_brain(**query))

    def test__two_folders(self):
        from abita.adapter.interfaces import IBaseAdapter
        base = IBaseAdapter(self.portal)

        folder1 = self.portal[self.portal.invokeFactory('Folder', 'folder1')]
        folder1.reindexObject()
        folder2 = folder1[folder1.invokeFactory('Folder', 'folder2')]
        folder2.reindexObject()

        query = {}

        self.assertEqual(len(base.get_brains(**query)), 2)
        self.assertEqual(len(base.get_content_listing(**query)), 2)

        query['sort_limit'] = 1
        self.assertEqual(len(base.get_brains(**query)), 1)
        self.assertEqual(len(base.get_content_listing(**query)), 1)

    @mock.patch('abita.adapter.base.getToolByName')
    def test__localized_time(self, getToolByName):
        from abita.adapter.interfaces import IBaseAdapter
        base = IBaseAdapter(self.portal)

        folder1 = self.portal[self.portal.invokeFactory('Folder', 'folder1')]
        folder1.reindexObject()

        getToolByName().ulocalized_time.return_value = u'Dec 05, 2012'

        self.assertEqual(base.localized_time(base.get_brain()), u'Dec 05, 2012')
