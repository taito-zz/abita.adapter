from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from abita.adapter.interfaces import IBaseAdapter
from five import grok
from plone.app.contentlisting.interfaces import IContentListing
from plone.memoize.instance import memoize
from zope.interface import Interface


class BaseAdapter(grok.Adapter):
    """Base class for adapters"""

    grok.context(Interface)
    grok.provides(IBaseAdapter)

    @memoize
    def _catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    def get_brains(self, **query):
        # Set default path
        path = query.get('path')
        if path is None:
            path = '/'.join(aq_inner(self.context).getPhysicalPath())
        depth = query.get('depth')
        if depth:
            path = {'query': path, 'depth': depth}
        query['path'] = path
        sort_limit = query.get('sort_limit')
        if sort_limit:
            return self._catalog()(query)[:sort_limit]
        return self._catalog()(query)

    def get_brain(self, **query):
        brains = self.get_brains(**query)
        if brains:
            return brains[0]

    def get_object(self, **query):
        brain = self.get_brain(**query)
        if brain:
            return brain.getObject()

    def get_content_listing(self, **query):
        return IContentListing(self.get_brains(**query))

    @memoize
    def ulocalized_time(self):
        """Return ulocalized_time method.

        :rtype: method
        """
        translation_service = getToolByName(self.context, 'translation_service')
        return translation_service.ulocalized_time
