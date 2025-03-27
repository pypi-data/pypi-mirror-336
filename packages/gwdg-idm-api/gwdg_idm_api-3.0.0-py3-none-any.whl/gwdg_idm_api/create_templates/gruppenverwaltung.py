from ..core_models import CreateTemplate


class CreateGruppenverwaltung_MDMP(CreateTemplate):
    create_template_name: str = "MDMP"  # Name of the template
    description: str | None = None  # Description
    displayName: str  # Display name
    goesternExpirationDate: str | None = None  # Expiration date
    goesternSamAccountName: str  # actual group name
    hideFromAddressLists: str | None = None  # Hide from address list
    isProtected: str | None = None  # Make protected group
    mail: str | None = None  # Primary mail address
    managedBy: list[str] | None = None  # Managed by
    member: list[str] | None = None  # member by internal ID
    nameSpace: str = "MPG"  # Namespace
    proxyAddress: list[str] | None = None  # Email addresses
    sendPermission: list[str] | None = None  # Senders allowed to send emails
    sendPermissionLevel: str | None = None  # Send permission level
