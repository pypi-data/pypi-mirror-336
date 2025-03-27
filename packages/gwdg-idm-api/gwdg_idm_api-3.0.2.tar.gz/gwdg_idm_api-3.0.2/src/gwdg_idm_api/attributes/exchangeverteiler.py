from ..core_models import ChangeTemplate


class ExchangeVerteilerAttributes(ChangeTemplate):
    createTimestamp: str | None = None  # Creation date
    description: str | None = None  # Description
    displayName: str | None = None  # Displayname
    hideFromAddressLists: str | None = None  # Hide from address lists
    mail: str | None = None  # Primary email address
    mailboxServer: str | None = None  # Mailbox server
    member: list[str] | None = []  # Members
    memberOfStaticExchangeDistGrp: list[str] | None = (
        []
    )  # Member of static distribution group
    modifyTimeStamp: str | None = None  # Modified on
    proxyAddress: list[str] | None = []  # Email addresses
    sendPermission: list[str] | None = []  # Send permissions
    sendPermissionLevel: str | None = None  # Send permission level
