from ..core_models import ChangeTemplate


class DynamischeExchangeVerteilerAttributes(ChangeTemplate):
    createTimestamp: str | None = None  # Creation date
    displayName: str | None = None  # Displayname
    hideFromAddressLists: str | None = None  # Hide from address lists
    includeInstituteUsersOnly: str | None = None  # Add institute users only
    mail: str | None = None  # Primary email address
    mailboxServer: str | None = None  # Mailbox server
    managedBy: list[str] | None = []  # Managed by
    memberOfStaticExchangeDistGrp: list[str] | None = (
        []
    )  # Member of static distribution group
    modifyTimeStamp: str | None = None  # Modified on
    proxyAddress: list[str] | None = []  # Email addresses
    recipientFilter: str | None = None  # Recipient filter
    sendPermission: list[str] | None = []  # Send permissions
    sendPermissionLevel: str | None = None  # Send permission level
