from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from abita.adapter.interfaces import IBaseAdapter
from five import grok
from plone.app.contentlisting.interfaces import IContentListing
from plone.memoize.forever import memoize
from zope.interface import Interface


class BaseAdapter(grok.Adapter):
    """Base class for adapters"""

    grok.context(Interface)
    grok.provides(IBaseAdapter)

    @property
    @memoize
    def _catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    def get_brains(self, interfaces=None, **query):
        if interfaces is not None:
            if not isinstance(interfaces, list):
                interfaces = [interfaces]
                query['object_provides'] = [interface.__identifier__ for interface in interfaces]
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
            return self._catalog(query)[:sort_limit]
        return self._catalog(query)

    def get_brain(self, interfaces=None, **query):
        brains = self.get_brains(interfaces=interfaces, **query)
        if brains:
            return brains[0]

    def get_object(self, interfaces=None, **query):
        brain = self.get_brain(interfaces=interfaces, **query)
        if brain:
            return brain.getObject()

    def get_content_listing(self, interfaces=None, **query):
        return IContentListing(self.get_brains(interfaces=interfaces, **query))

    @property
    @memoize
    def ulocalized_time(self):
        """Return ulocalized_time method.

        :rtype: method
        """
        return getToolByName(self.context, 'translation_service').ulocalized_time

    @property
    @memoize
    def getSessionData(self):
        """Returns getSessionData method.

        :rtype: method
        """
        return getToolByName(self.context, 'session_data_manager').getSessionData

    def event_datetime(self, item):
        start = item.start
        end = item.end
        start_dt = self.ulocalized_time(start, long_format=True, context=self.context)
        if start.Date() == end.Date():
            if start == end:
                dt = start_dt
            else:
                end_time = self.ulocalized_time(end, time_only=True)
                dt = u'{} - {}'.format(start_dt, end_time)
        else:
            end_dt = self.ulocalized_time(end, long_format=True, context=self.context)
            dt = u'{} - {}'.format(start_dt, end_dt)

        return dt
