import datetime
import os
import uuid

from gwdg_idm_api import Benutzerverwaltung_MDMP as Benutzerverwaltung
from gwdg_idm_api import CreateBenutzerverwaltung_MDMP as NewGWDGUser
from gwdg_idm_api.util import AlreadyDeletedError, pretty_print

# Load idm credentials
# Do not upload credentials in any way to github/gitlab etc.
idm_username = os.environ["IDM_USERNAME"]
idm_password = os.environ["IDM_PASSWORD"]


# For testing purposes, we are using the idm-stage endpoint.
# This one is a copy of the previous day and can be used
# for sandbox testing.
# Change to "https://idm.gwdg.de/api/v3" for production.
if "stage" not in os.environ["IDM_API_URL"]:
    print("There is no stage in IDM_API_URL! This is not supported!")
    exit(1)
benutzerverwaltung = Benutzerverwaltung(
    api_url=os.environ["IDM_API_URL"],
    username=idm_username,
    password=idm_password,
)

# Get all users having their surename starting with 'a'
sn_a_users = benutzerverwaltung.get_multiple("$sn -eq 'a*'")
print("# First two entries starting with 'a'")
print(pretty_print(sn_a_users[:2]))

# Take the first user and print a more detailed view
print("# Get detailed information")
single_user = benutzerverwaltung.get_single(sn_a_users[0].id)
print(pretty_print(single_user))

single_user = benutzerverwaltung.create_new(
    NewGWDGUser(
        givenName=str(uuid.uuid4())[:8],
        sn=str(uuid.uuid4())[:8],
        workGroup="best_group",
        departmentNumber="best_department",
    )
)
print("# Create new user")
print(pretty_print(single_user))

# Change the lastname of the user to 'Upps bad lastnäme' and workGroup to '-'
# and check if the update happened
print("# Update user")
updated_user = benutzerverwaltung.update_single(
    single_user, {"workGroup": "-", "sn": "Upps bad lastnäme"}
)
print(pretty_print(updated_user))

# Ah that did not work out well!
# Now lets remove the user in 10 days (set goesternExpirationDate)
# If
print("# Delete user in 10 days")
try:
    deleted_user = benutzerverwaltung.delete_user(
        single_user, datetime.datetime.now() + datetime.timedelta(days=10)
    )
except AlreadyDeletedError:
    # If the user is already deleted an AlreadyDeletedError is thrown
    print("Already deleted")
else:
    print(pretty_print(deleted_user))

# Actually, lets delete him yesterday
# The delete_user functions will automatically just check the
# isScheduledForDeletion flag if the expire_datetime is in the past
print("# Delete user now")
try:
    deleted_user = benutzerverwaltung.delete_user(
        updated_user, datetime.datetime.now() - datetime.timedelta(days=1)
    )
except AlreadyDeletedError:
    print("Already deleted")
else:
    print(pretty_print(deleted_user))

# Lets create a new user
print("# Create new user")
new_user_tmp = NewGWDGUser(
    givenName="john", sn="doe", workGroup="-", departmentNumber="ZE"
)
new_user = benutzerverwaltung.create_new(new_user_tmp)
print(pretty_print(new_user))

print("# All done :)")
