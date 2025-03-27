import pydantic

from ..core_models import ChangeTemplate


class BenutzerverwaltungAttributes(ChangeTemplate):
    accountType: str | None = None  # Account type
    additionalPasswordExpirationTime: str | None = (
        None  # Password expiration date (additional password)
    )
    additionalPasswordModifyTime: str | None = (
        None  # Last password change (additional password)
    )
    city: str | None = None  # City
    createTimestamp: str | None = None  # Creation date
    departmentNumber: str | None = None  # Department
    description: str | None = None  # Description
    eduPersonPrincipalName: str | None = None  # eduPersonPrincipalName
    eduPersonScopedAffiliation: list[str] | None = []  # eduPersonScopedAffiliation
    effectivePrivilege: list[str] | None = []  # Privileges
    employeeNumber: str | None = None  # Employee number
    employeeStatus: str | None = None  # Employee status
    employeeType: str | None = None  # Employee type
    exchangeTargetAddress: str | None = None  # Exchange redirect address
    externalEmailAddress: list[str] | None = []  # External email addresses
    facsimileTelephoneNumber: str | None = None  # Fax number
    filterAttribute1: list[str] | None = []  # Filter attribute 1
    filterAttribute2: list[str] | None = []  # Filter attribute 2
    filterAttribute3: list[str] | None = []  # Filter attribute 3
    givenName: str | None = None  # First name
    goesternDisableDate: str | None = None  # Disable/Enable date
    goesternDisableReason: str | None = None  # Disable reason
    goesternExchHideFromAddressLists: str | None = None  # Hide from address lists
    goesternExchangeQuota: str | None = None  # Exchange quota
    goesternExpirationDate: str | None = None  # Expiration date
    goesternGWDGadDisplayName: str | None = None  # AD-Displayname
    goesternLockoutTime: str | None = None  # Short time lockout (AD)
    goesternMailRoutingAddresses: list[str] | None = []  # Routing addresses
    goesternMailboxServer: str | None = None  # Mailbox server
    goesternMailboxZugehoerigkeit: str | None = None  # Mailbox type
    goesternProxyAddresses: list[str] | None = []  # Email addresses
    goesternRemoveDate: str | None = None  # Remove date
    goesternSAMAccountName: str | None = None  # Account name in source system
    goesternUserStatus: str | None = None  # User status
    goesternUserType: str | None = None  # User type
    isEnforceMFA: str | None = None  # Multi-factor authentication activated
    isEnforceSSOFederatedLogin: str | None = None  # Federated account
    isInitialAdditionalPassword: str | None = (
        None  # Additional password is initial password
    )
    isInitialPassword: str | None = None  # Initial password
    isScheduledForDeletion: str | None = None  # Deferred deletion
    l: str | None = None  # Country
    loginExpirationTime: str | None = None  # Login expiration date
    mail: str | None = None  # Primary email address
    memberOfStaticExchangeDistGrp: list[str] | None = []  # Group memberships
    mobile: str | None = None  # Mobile
    modifyTimeStamp: str | None = None  # Modified on
    mpgEmployeeNumber: str | None = None  # Employee number MPG
    mwsEmployeeNumber: str | None = None  # MWS employee number
    oldUid: list[str] | None = []  # Previous usernames
    ou: str | None = None  # Institute
    ownCloudQuota: str | None = None  # OwnCloud Quota
    passwordExpirationTime: str | None = None  # Password expiration date
    postalCode: str | None = None  # Postal code
    pwdChangedTime: str | None = None  # Last password change
    responsiblePerson: list[str] | None = []  # Responsible user
    roomNumber: str | None = None  # Room number
    sn: str | None = None  # Last name
    st: str | None = None  # State
    street: str | None = None  # Street
    telephoneNumber: str | None = None  # Telefonnumber
    title: str | None = None  # Job title
    uid: str | None = None  # Username
    voPersonExternalAffiliation: list[str] | None = (
        []
    )  # voPerson Scoped External Affiliation

    @pydantic.field_validator("isScheduledForDeletion")
    @classmethod
    def isScheduledForDeletion_validator(cls, value):
        if value is None:
            return value
        return value.upper()


class BenutzerverwaltungAttributes_MDMP(BenutzerverwaltungAttributes):
    dn: str | None = None  # DN
    externalTaskCommand: str | None = None  # External Task command
    throttlingpolicy: str | None = None  # Throttling Policy
    workGroup: str | None = None  # WorkGroup
