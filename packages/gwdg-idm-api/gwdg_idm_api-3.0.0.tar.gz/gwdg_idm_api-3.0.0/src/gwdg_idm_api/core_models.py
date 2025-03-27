from __future__ import annotations

import json
import logging
import os
import typing
import urllib.parse

import pydantic
import requests

from .util import (
    BadJsonError,
    IDMNotReachableError,
    IDMRequestError,
    UnexpectedJsonError,
)

if typing.TYPE_CHECKING:
    from requests import Response


__all__ = ["ChangeTemplate", "PasswordTemplate"]


DATA_TYPE = str | list | dict | None


class IDMRequest(pydantic.BaseModel):
    username: str
    password: str
    api_url: str = os.environ.get("IDM_API_URL", "")
    api_suffix: str = ""

    def run_request(
        self, func: typing.Callable[..., Response], url: str, data: DATA_TYPE = None
    ) -> Response:
        try:
            return func(
                url,
                auth=(self.username, self.password),
                timeout=240,  # Needs to be this high to allow for an all-objects query
                headers={
                    "Accept": "application/json",
                    "Accept-Language": "en",
                    "Content-Type": "application/json",
                },
                data=data,
            )
        except Exception as e:
            raise IDMNotReachableError(
                f"Could not connect to IDM: IDM not reachable!\n{e}"
            )

    def get_request(self, url: str) -> Response:
        return self.run_request(requests.get, url)

    def put_request(self, url: str, data: DATA_TYPE) -> Response:
        return self.run_request(requests.put, url, data)

    def post_request(self, url: str, data: DATA_TYPE) -> Response:
        return self.run_request(requests.post, url, data)

    def get_suffix(self, filter_string: str | None = None) -> list[object] | dict:
        request_url = f"{self.api_url}{self.api_suffix}"
        if filter_string is not None:
            request_url = f"{request_url}?filter={urllib.parse.quote(filter_string)}"
        resp = self.get_request(request_url)
        try:
            return json.loads(resp.text)
        except json.decoder.JSONDecodeError:
            raise BadJsonError(resp.text)


class PasswordTemplate(pydantic.BaseModel):
    template_name: str = "changepassword"
    id: str  # GWDG idm ID
    password: str
    isinitial: bool = True
    create_pdf: bool = False

    @property
    def pdf_suffix(self) -> str:
        if self.create_pdf:
            return "/pdf"
        else:
            return ""

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def to_dict(self) -> dict:
        data = [
            {
                "name": "password",
                "value": [self.password],
            }
        ]
        if self.isinitial:
            data.append(
                {
                    "name": "isinitial",
                    "value": ["true"],
                }
            )
        return {"attributes": data}


class ChangeTemplate(pydantic.BaseModel):
    id: str

    @staticmethod
    def update_dict(name: str, value: str | list[str] | None) -> dict:
        if value is not None:
            value = [value] if not isinstance(value, list) else value
        else:
            value = []
        data = {
            "name": name,
            "value": value,
        }
        return {"attributes": [data]}

    @staticmethod
    def update_json(name: str, value: str | list[str] | None) -> str:
        return json.dumps(ChangeTemplate.update_dict(name, value))

    @classmethod
    def from_json(cls, json: dict) -> ChangeTemplate:
        response_dict: dict[str, list[str] | str]

        response_dict = {
            "id": [json["id"]],
            "dn": [json["dn"]],
        }
        response_dict.update(
            {entry["name"]: entry["value"] for entry in json["attributes"]}
        )

        remove_keys = []
        for key, value in sorted(response_dict.items()):
            try:
                ann: type
                try:
                    ann = cls.model_fields[key].annotation.__args__[0]
                except AttributeError:
                    ann = cls.model_fields[key].annotation

                try:
                    outer_type = ann.__origin__
                except Exception:
                    outer_type = ann

                expected_type = type(outer_type())
            except KeyError:
                remove_keys.append(key)
                logging.warning(
                    "\n"
                    "  key unknown to model\n"
                    f"  User: {response_dict['id']}\n"
                    f"  Key: {key}"
                    f"  Value: {value}"
                )
                continue
            if isinstance(value, expected_type):
                continue

            if isinstance(value, expected_type):
                continue
            elif expected_type is str and isinstance(value, list):
                if len(value) > 1:
                    logging.warning(
                        "\n"
                        "  str expected, but found list: Using first element\n"
                        "  Please check your class specifications.\n"
                        f"  User: {response_dict['id']}\n"
                        f"  Key: {key}"
                        f"  Value: {value}"
                    )
                try:
                    new_val: str = value[0]
                except IndexError:
                    logging.warning(
                        "  str expected, but empty list found: Set to empty string\n"
                        "  Please check your class specifications.\n"
                        f"  User: {response_dict['id']}\n"
                        f"  Key: {key}"
                        f"  Value: {value}"
                    )
                    new_val: str = ""
                response_dict[key] = new_val
            else:
                assert False, (
                    "  Only str and list types are supported so far!"
                    "  Please check your class specifications.\n"
                    f"  User: {response_dict['id']}\n"
                    f"  Key: {key}"
                    f"  Value: {value}"
                )

        return cls(**{key: value for key, value in response_dict.items() if key not in set(remove_keys)})  # type: ignore


class CreateTemplate(pydantic.BaseModel):
    create_template_name: str

    def to_dict(self) -> dict:
        data = [
            {
                "name": key.removeprefix("_"),
                "value": [value] if not isinstance(value, list) else value,
            }
            for key, value in self.dict().items()
            if key != "create_template_name"
        ]
        return {"attributes": data}

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


class IDMUserClass(IDMRequest):
    user_class: type[ChangeTemplate]

    def set_user_class(self, user_class: type[ChangeTemplate]):
        self.user_class = user_class

    def get_single(self, object_id: str) -> ChangeTemplate:
        request_url = f"{self.api_url}{self.api_suffix}/{object_id}"
        resp = self.get_request(request_url)
        try:
            json_resp = json.loads(resp.text)
        except json.decoder.JSONDecodeError:
            raise BadJsonError(resp.text)

        return self.user_class.from_json(json_resp)

    def get_multiple(self, filter_string: str | None = None) -> list[ChangeTemplate]:
        objects = self.get_suffix()
        try:
            return [self.user_class.from_json(obj) for obj in objects["Objects"]]
        except Exception:
            raise UnexpectedJsonError(objects)

    def update_single(
        self,
        user: ChangeTemplate,
        update_dict: dict[str, str | list[str] | None],
        *,
        single_call: bool = False,
    ) -> ChangeTemplate:
        request_url: str = f"{self.api_url}{self.api_suffix}/{user.id}"

        if "mail" in update_dict:
            # Run mail at the very last to avoid missing proxyMail entries
            mail = update_dict.pop("mail")
            update_dict["mail"] = mail

        if not single_call:
            for key, value in update_dict.items():
                data = user.update_json(key, value)

                resp = self.put_request(request_url, data)
                if "success" not in resp.text:
                    raise IDMRequestError(
                        f"Could not connect to IDM: Invalid combination\n{key=}\n{value=}\n{resp.text=}"
                    )
        else:
            data_list = []
            for key, value in update_dict.items():
                data_list.append(user.update_dict(key, value))
            base_data = data_list[0]
            for data_entry in data_list[1:]:
                base_data["attributes"].extend(data_entry["attributes"])
            resp = self.put_request(request_url, json.dumps(base_data))
            if "success" not in resp.text:
                raise IDMRequestError(
                    f"Could not connect to IDM: Invalid combination\n{data_list=}\n{resp.text=}"
                )
        return self.get_single(user.id)

    def create_new(self, new_user: CreateTemplate) -> ChangeTemplate:
        request_url: str = (
            f"{self.api_url}{self.api_suffix}/{new_user.create_template_name}"
        )
        data = new_user.to_json()
        resp = self.post_request(request_url, data)
        if "success" not in resp.text:
            raise IDMRequestError(
                f"Could not connect to IDM: Invalid combination\n{resp.text=}"
            )
        user_id = resp.headers["location"]
        return self.get_single(user_id)
