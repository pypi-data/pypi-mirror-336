from ..core_models import ChangeTemplate


class GruppenverwaltungAttributes(ChangeTemplate):
    awsRole: list[str] | None = None  # AWS role mapping
    cn: str | None = None  # GOESTERN-ID
    description: str | None = None  # Description
    displayName: str | None = None  # Displayname
    excludeMember: list[str] | None = None  # Excluded members
    goesternExpirationDate: str | None = None  # Expiration date
    goesternSamAccountName: str | None = None  # Account name in source system
    groupMemberFilter: str | None = None  # Group member filter
    groupMemberFilterAttribute: str | None = (
        None  # Attribute name for determining members
    )
    groupMemberFilterError: str | None = None  # Group calculation error
    groupMemberLimit: str | None = None  # group member limit
    groupMemberScope: str | None = None  # Group member scope
    hideFromAddressLists: str | None = None  # Hide from address lists
    includeMember: list[str] | None = None  # Additional members
    isProtected: str | None = None  # Only editable by "Managed by"
    mail: str | None = None  # Primary email address
    mailboxServer: str | None = None  # Mailbox server
    managedBy: list[str] | None = None  # Managed by
    member: list[str] | None = None  # Members
    nameSpace: str | None = None  # Namespace
    ou: str | None = None  # Institute
    proxyAddress: list[str] | None = None  # Email addresses
    scope: list[str] | None = None  # Visibility
    sendPermission: list[str] | None = None  # Send permissions
    sendPermissionLevel: str | None = None  # Send permission level


class GruppenverwaltungAttributes_MDMP(GruppenverwaltungAttributes):
    dn: str | None = None  # DN
