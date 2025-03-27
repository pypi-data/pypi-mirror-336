from __future__ import annotations

import datetime
import logging
import typing

from .core_models import ChangeTemplate, IDMRequest, IDMUserClass
from .util import AlreadyDeletedError, IDMRequestError

if typing.TYPE_CHECKING:
    from requests import Response

    from .core_models import PasswordTemplate


class Workspaces(IDMRequest):
    api_suffix: str = "/workspaces"

    def get_workspaces_json(self):
        return self.get_suffix()

    def get_workspace_attributes(self):
        json_resp = self.get_workspaces_json()
        workspace_list = json_resp["workspaceList"]
        workspaces = {}
        for entry in workspace_list:
            workspaces[entry["name"]] = entry["attributes"]
        return workspaces


class BenutzerverwaltungBase(IDMUserClass):
    def delete_user(
        self, user: ChangeTemplate, expire_datetime: datetime.datetime | datetime.date
    ):
        today: datetime.date
        expire_date: datetime.date
        activate_now: bool
        change_data: dict[str, str]

        today = datetime.datetime.now().date()
        try:
            expire_date = expire_datetime.date()
        except AttributeError:
            expire_date = expire_datetime

        current_user_status = self.get_single(user.id)

        activate_now = (expire_date - today).total_seconds() <= 0
        status_deleted = current_user_status.goesternUserStatus in ("2", "255")

        change_data = {}
        change_data["isScheduledForDeletion"] = "FALSE"
        change_data["goesternExpirationDate"] = ""

        self.update_single(user, change_data, single_call=True)  # type: ignore

        if activate_now and not status_deleted:
            change_data = {
                "isScheduledForDeletion": "TRUE",
            }
        elif activate_now:
            change_data = {}
        else:
            # TODO: After fixing the 'year 2038' problem in the IDM, this if statement can be removed again.
            if expire_date.year > 2037:
                logging.warn(
                    "Expire date year is bigger than 2037. Reduce expire date to 2038."
                )
                expire_date = datetime.date(2038, 1, 1)
            change_data = {
                "goesternExpirationDate": expire_date.strftime("%d.%m.%Y"),
            }

        return self.update_single(user, change_data)  # type: ignore

    def reactivate_user(self, user: ChangeTemplate, create_mailbox: bool = True):
        current_user_status = self.get_single(user.id)

        if current_user_status.goesternUserStatus == "255":
            raise AlreadyDeletedError
        elif current_user_status.goesternUserStatus != "2":
            return user

        if current_user_status.goesternExpirationDate:
            change_data = {"goesternExpirationDate": ""}
            user = self.update_single(user, change_data)  # type: ignore

        change_data = {
            "goesternUserStatus": "0",
        }
        if create_mailbox:
            change_data["externalTaskCommand"] = "CreateMailbox"
        return self.update_single(user, change_data)  # type: ignore

    def change_password(self, user: PasswordTemplate | list[PasswordTemplate]) -> list:
        resp: Response
        data: str

        if not isinstance(user, list):
            user = [user]

        pdfs = []
        for cur_user in user:
            request_url: str = (
                f"{self.api_url}{self.api_suffix}/{cur_user.id}/{cur_user.template_name}{cur_user.pdf_suffix}"
            )
            data = cur_user.to_json()
            resp = self.post_request(request_url, data)
            if cur_user.pdf_suffix:
                pdfs.append(resp.content)

            else:
                if "success" not in resp.text:
                    raise IDMRequestError(
                        f"Could not connect to IDM: Invalid combination\n{resp.text=}"
                    )
        return pdfs


class GruppenverwaltungBase(IDMUserClass):
    def delete_user(self, user: ChangeTemplate, remark: str = ""):
        request_url: str = (
            f"{self.api_url}/Deletion/DeleteObject{self.api_suffix}/{user.id}"
        )
        request_url = f"{self.api_url}{self.api_suffix}/objects/{user.id}/delete"
        data = {"_remark": remark}
        print(request_url)
        resp = self.post_request(request_url, data)
        print(resp.text)
