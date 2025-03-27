from ..core_models import ChangeTemplate


class MailinglistenAttributes(ChangeTemplate):
    createTimestamp: str | None = None  # Creation date
    goesternMailRoutingAddresses: list[str] | None = None  # Routing addresses
    goesternProxyAddresses: list[str] | None = None  # Email addresses
    listName: str | None = None  # Listname
    modifyTimeStamp: str | None = None  # Modified on
    ou: str | None = None  # Institute
