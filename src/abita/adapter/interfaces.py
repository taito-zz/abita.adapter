from zope.interface import Interface


class IBaseAdapter(Interface):
    """Base interface for adapters"""

    def get_brains(interfaces=None, **query):  # pragma: no cover
        """Get brains."""

    def get_brain(interfaces=None, **query):  # pragma: no cover
        """Get brain which is surposed to be only one."""

    def get_object(interfaces=None, **query):  # pragma: no cover
        """Get object which is surposed to be only one."""

    def get_content_listing(interfaces=None, **query):  # pragma: no cover
        """Get ContentListing from brains gotten from get_brains method."""

    # def localized_time(item, date_type, long_format=False):  # pragma: no cover
    #     """Returns localized time."""
