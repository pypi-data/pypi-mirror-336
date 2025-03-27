from ..core_models import CreateTemplate


class CreateBenutzerverwaltung_MDMP(CreateTemplate):
    create_template_name: str = "MDMP"  # Name of the template
    departmentNumber: str  # Department name
    externalTaskCommand: str | None = "CreateMailbox"  # Task to perform on submission
    givenName: str  # first Name
    goesternUserType: str | None = "0"  # Type of user! 0 normal, 1 function
    roomNumber: str | None = ""  # Office room number
    sn: str  # last Name
    telephoneNumber: str | None = ""  # telephoneNumber
    workGroup: str  # Workgroup
