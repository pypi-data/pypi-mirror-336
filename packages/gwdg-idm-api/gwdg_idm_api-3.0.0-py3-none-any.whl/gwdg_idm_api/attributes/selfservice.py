from ..core_models import ChangeTemplate


class SelfServiceAttributes(ChangeTemplate):
    cn: str | None = None  # GOESTERN-ID
    effectivePrivilege: list[str] | None = None  # Privileges
    givenName: str | None = None  # First name
    goesternProxyAddresses: list[str] | None = None  # Email addresses
    mail: str | None = None  # Primary email address
    ou: str | None = None  # Institute
    sn: str | None = None  # Last name
    uid: str | None = None  # Username
    umgArztnummer: str | None = None  # Doctor number
