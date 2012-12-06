from zope.interface import Interface


class IBaseAdapter(Interface):
    """Base interface for adapters"""

    def get_brains(**query):
        """Get brains."""

    def get_brain(**query):
        """Get brain which is surposed to be only one."""

    def get_content_listing(**query):
        """Get ContentListing from brains gotten from get_brains method."""

    def localized_time(item, date_type, long_format=False):
        """Returns localized time."""
