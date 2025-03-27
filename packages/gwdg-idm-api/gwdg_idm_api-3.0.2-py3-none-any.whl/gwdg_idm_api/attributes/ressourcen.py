from ..core_models import ChangeTemplate


class RessourcenAttributes(ChangeTemplate):
    capacity: str | None = None  # Capacity
    city: str | None = None  # City
    createTimestamp: str | None = None  # Creation date
    delegate: list[str] | None = []  # Delegate
    department: str | None = None  # Department
    description: str | None = None  # Description
    displayName: str | None = None  # Displayname
    fullAccessAllowed: list[str] | None = []  # Full access
    hideFromAddressLists: str | None = None  # Hide from address lists
    mail: str | None = None  # Primary email address
    mailboxServer: str | None = None  # Mailbox server
    managedBy: list[str] | None = []  # Managed by
    memberOfStaticExchangeDistGrp: list[str] | None = (
        []
    )  # Member of static distribution group
    modifyTimeStamp: str | None = None  # Modified on
    ou: str | None = None  # Institute
    postalCode: str | None = None  # Postal code
    proxyAddress: list[str] | None = []  # Email addresses
    resourceType: str | None = None  # Resource type
    roomNumber: str | None = None  # Room number
    st: str | None = None  # State
    street: str | None = None  # Street
    telephoneNumber: str | None = None  # Telefonnumber
