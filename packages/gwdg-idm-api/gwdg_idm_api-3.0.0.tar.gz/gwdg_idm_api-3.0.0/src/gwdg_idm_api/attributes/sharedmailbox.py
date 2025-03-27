from ..core_models import ChangeTemplate


class SharedMailboxAttributes(ChangeTemplate):
    autoMapping: str | None = None  # Auto mapping
    city: str | None = None  # City
    createTimestamp: str | None = None  # Creation date
    delegate: list[str] | None = None  # Delegate
    department: str | None = None  # Department
    description: str | None = None  # Description
    displayName: str | None = None  # Displayname
    fullAccessAllowed: list[str] | None = None  # Full access
    goesternExchangeQuota: str | None = None  # Exchange quota
    hideFromAddressLists: str | None = None  # Hide from address lists
    mail: str | None = None  # Primary email address
    mailboxServer: str | None = None  # Mailbox server
    managedBy: list[str] | None = None  # Managed by
    memberOfStaticExchangeDistGrp: list[str] | None = (
        None  # Member of static distribution group
    )
    modifyTimeStamp: str | None = None  # Modified on
    ou: str | None = None  # Institute
    postalCode: str | None = None  # Postal code
    proxyAddress: list[str] | None = None  # Email addresses
    roomNumber: str | None = None  # Room number
    st: str | None = None  # State
    street: str | None = None  # Street
    telephoneNumber: str | None = None  # Telefonnumber
