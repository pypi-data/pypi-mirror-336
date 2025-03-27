from ..core_models import ChangeTemplate


class LDAPVerteilerAttributes(ChangeTemplate):
    createTimestamp: str | None = None  # Creation date
    description: str | None = None  # Description
    filterAttribute1: list[str] | None = None  # Filter attribute 1
    filterAttribute2: list[str] | None = None  # Filter attribute 2
    filterAttribute3: list[str] | None = None  # Filter attribute 3
    goesternExchHideFromAddressLists: str | None = None  # Hide from address lists
    goesternExpirationDate: str | None = None  # Expiration date
    goesternGWDGadDisplayName: str | None = None  # Displayname
    goesternMailroutingAddresses: list[str] | None = None  # Routing addresses
    goesternProxyAddresses: list[str] | None = None  # Email addresses
    goesternUserType: str | None = None  # User type
    mail: str | None = None  # Primary email address
    managedBy: list[str] | None = None  # Managed by
    modifyTimeStamp: str | None = None  # Modified on
    uid: str | None = None  # Username
