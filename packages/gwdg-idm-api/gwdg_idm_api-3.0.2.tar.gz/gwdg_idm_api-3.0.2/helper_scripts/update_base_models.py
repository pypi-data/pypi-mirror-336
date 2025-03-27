import argparse
import inspect
import os
import pathlib
import re
from dataclasses import dataclass

from gwdg_idm_api import Workspaces


@dataclass
class Config:
    output_folder: pathlib.Path
    username: str
    password: str
    api_url: str

    _attribute_folder: pathlib.Path | None = None
    _model_folder: pathlib.Path | None = None
    _create_templates_folder: pathlib.Path | None = None

    @property
    def attribute_folder(self):
        if self._attribute_folder is None:
            folder = self.output_folder / "attributes"
            folder.mkdir(exist_ok=True, parents=True)
            self._attribute_folder = folder
        return self._attribute_folder

    @property
    def models_folder(self):
        if self._model_folder is None:
            folder = self.output_folder / "models"
            folder.mkdir(exist_ok=True, parents=True)
            self._model_folder = folder
        return self._model_folder

    @property
    def create_templates_folder(self):
        if self._create_templates_folder is None:
            folder = self.output_folder / "create_templates"
            folder.mkdir(exist_ok=True, parents=True)
            self._create_templates_folder = folder
        return self._create_templates_folder


def args_to_config(args) -> Config:
    return Config(
        pathlib.Path(args.output_folder),
        os.environ["IDM_USERNAME"],
        os.environ["IDM_PASSWORD"],
        os.environ["IDM_API_URL"],
    )


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("output_folder")
    return parser.parse_args()


def get_workspaces(config: Config):
    check = Workspaces(
        username=config.username, password=config.password, api_url=config.api_url
    )
    return check.get_workspace_attributes()


def create_attributes(workspaces: dict, config: Config):
    add_attributes = {
        "benutzerverwaltung": {
            "MDMP": [
                {"name": "dn", "multiValue": False, "displayName": "DN"},
                {"name": "workGroup", "multiValue": False, "displayName": "WorkGroup"},
                {
                    "name": "throttlingpolicy",
                    "multiValue": False,
                    "displayName": "Throttling Policy",
                },
                {
                    "name": "externalTaskCommand",
                    "multiValue": False,
                    "displayName": "External Task command",
                },
            ]
        },
        "gruppenverwaltung": {
            "MDMP": [{"name": "dn", "multiValue": False, "displayName": "DN"}]
        },
    }

    ### Helper functions to be inserted as validators!
    def to_upper(cls, value):
        if value is None:
            return value
        return value.upper()

    ### Helper functions end

    validators = {
        "benutzerverwaltung": {
            "isScheduledForDeletion": to_upper,
        }
    }

    init_string = []
    created_classes = {}
    for key, attributes in workspaces.items():
        class_names = {}
        base_class = f"{key}Attributes"
        class_names[""] = base_class

        out_string = []
        out_string.append("from ..core_models import ChangeTemplate")
        out_string.append("")
        out_string.append("")

        cur_validator = validators.get(key.lower(), {})
        class_string = create_attribute_class(
            base_class, "ChangeTemplate", attributes, cur_validator
        )
        out_string.extend(class_string)

        for new_key, new_attrs in add_attributes.get(key.lower(), {}).items():
            new_base_class = f"{base_class}_{new_key}"
            class_names[new_key] = new_base_class
            class_string = create_attribute_class(
                new_base_class, base_class, new_attrs, cur_validator
            )
            out_string.append("")
            out_string.append("")
            out_string.extend(class_string)

        out_string.append("")
        out_text = "\n".join(out_string)

        if "pydantic." in out_text:
            out_text = "import pydantic\n" + out_text

        (config.attribute_folder / f"{key.lower()}.py").write_text(out_text)

        init_string.append(
            f"from .{key.lower()} import {', '.join(sorted(class_names.values()))}  # noqa"
        )

        created_classes[key] = class_names

    (config.attribute_folder / "__init__.py").write_text("\n".join(sorted(init_string)))

    return created_classes


def create_attribute_class(class_name, inherit_name, attributes, validators):
    out_string = []
    out_string.append(f"class {class_name}({inherit_name}):")
    inner_strings = []
    old_attrs = set()
    for attr in attributes:
        assert attr["name"] not in old_attrs, (class_name, attr["name"], old_attrs)
        old_attrs.add(attr["name"])
        inner_string = []
        inner_string.append(f"    {attr['name']}:")
        if attr["multiValue"]:
            inner_string.append("list[str]")
        else:
            inner_string.append("str")
        if "mandatory" not in attr or not attr["mandatory"]:
            inner_string.append("|")
            inner_string.append("None")
            inner_string.append("=")
            inner_string.append(
                f'"{attr["default"]}"'
                if "default" in attr and attr["default"] is not None
                else "None" if not attr["multiValue"] else "[]"
            )
        if "mandatory" in attr and attr["mandatory"] and "default" in attr:
            inner_string.append("=")
            inner_string.append(f'"{attr["default"]}"')
        inner_string.append(" #")
        inner_string.append(attr["displayName"])
        inner_strings.append(" ".join(inner_string))
    out_string.extend(sorted(inner_strings))
    for vali_key, vali_value in validators.items():
        if vali_key in old_attrs:
            out_string.append("")
            out_string.append(f'    @pydantic.field_validator("{vali_key}")')
            out_string.append("    @classmethod")
            function_source = "".join(inspect.getsource(vali_value))
            function_source = re.sub(
                "def [^(]+", f"def {vali_key}_validator", function_source
            )
            out_string.append(function_source)
    return out_string


def create_models(created_classes, config):

    init_string = []
    for base_name, class_dict in created_classes.items():
        out_string = []
        out_string.append("from __future__ import annotations")
        out_string.append("")
        out_string.append("from pydantic import Field")
        out_string.append("")
        out_string.append(
            f"from ..attributes import {', '.join(sorted(class_dict.values()))}"
        )
        out_string.append("")
        out_string.append(
            f"""
try:
    from ..base_models import {base_name}Base
except ImportError:
    from ..core_models import IDMUserClass

    class {base_name}Base(IDMUserClass):
        pass
            """.strip()
        )
        out_string.append("")
        out_string.append("from ..core_models import ChangeTemplate")
        class_names = []
        for prefix, class_name in class_dict.items():
            if prefix:
                suffix = f"_{prefix}"
            else:
                suffix = ""
            new_class_name = f"{base_name}{suffix}"
            class_names.append(new_class_name)
            out_string.append("")
            out_string.append("")
            out_string.append(
                f"""
class {new_class_name}({base_name}Base):
    api_suffix: str = Field(default="/{base_name}/objects")
    user_class: type[ChangeTemplate] = Field(default={class_name})
            """.strip()
            )

        out_string.append("")
        (config.models_folder / f"{base_name.lower()}.py").write_text(
            "\n".join(out_string)
        )

        init_string.append(
            f"from .{base_name.lower()} import {', '.join(sorted(class_names))}  # noqa"
        )

    (config.models_folder / "__init__.py").write_text("\n".join(sorted(init_string)))


def create_templates(workspaces: dict, config: Config):
    attributes = {
        "benutzerverwaltung": {
            "MDMP": [
                {
                    "name": "create_template_name",
                    "multiValue": False,
                    "displayName": "Name of the template",
                    "default": "MDMP",
                    "mandatory": True,
                },
                {
                    "name": "givenName",
                    "multiValue": False,
                    "displayName": "first Name",
                    "mandatory": True,
                },
                {
                    "name": "sn",
                    "multiValue": False,
                    "displayName": "last Name",
                    "mandatory": True,
                },
                {
                    "name": "workGroup",
                    "multiValue": False,
                    "displayName": "Workgroup",
                    "mandatory": True,
                },
                {
                    "name": "departmentNumber",
                    "multiValue": False,
                    "displayName": "Department name",
                    "mandatory": True,
                },
                {
                    "name": "roomNumber",
                    "multiValue": False,
                    "displayName": "Office room number",
                    "default": "",
                },
                {
                    "name": "telephoneNumber",
                    "multiValue": False,
                    "displayName": "telephoneNumber",
                    "default": "",
                },
                {
                    "name": "goesternUserType",
                    "multiValue": False,
                    "displayName": "Type of user! 0 normal, 1 function",
                    "default": "0",
                },
                {
                    "name": "externalTaskCommand",
                    "multiValue": False,
                    "displayName": "Task to perform on submission",
                    "default": "CreateMailbox",
                },
            ]
        },
        "gruppenverwaltung": {
            "MDMP": [
                {
                    "name": "create_template_name",
                    "multiValue": False,
                    "displayName": "Name of the template",
                    "default": "MDMP",
                    "mandatory": True,
                },
                {
                    "name": "goesternSamAccountName",
                    "multiValue": False,
                    "displayName": "actual group name",
                    "mandatory": True,
                },
                {
                    "name": "displayName",
                    "multiValue": False,
                    "displayName": "Display name",
                    "mandatory": True,
                },
                {
                    "name": "nameSpace",
                    "multiValue": False,
                    "displayName": "Namespace",
                    "mandatory": True,
                    "default": "MPG",
                },
                {
                    "name": "description",
                    "multiValue": False,
                    "displayName": "Description",
                    "mandatory": False,
                },
                {
                    "name": "goesternExpirationDate",
                    "multiValue": False,
                    "displayName": "Expiration date",
                    "mandatory": False,
                },
                {
                    "name": "member",
                    "multiValue": True,
                    "displayName": "member by internal ID",
                    "mandatory": False,
                },
                {
                    "name": "managedBy",
                    "multiValue": True,
                    "displayName": "Managed by",
                    "mandatory": False,
                },
                {
                    "name": "isProtected",
                    "multiValue": False,
                    "displayName": "Make protected group",
                    "mandatory": False,
                },
                {
                    "name": "proxyAddress",
                    "multiValue": True,
                    "displayName": "Email addresses",
                    "mandatory": False,
                },
                {
                    "name": "mail",
                    "multiValue": False,
                    "displayName": "Primary mail address",
                    "mandatory": False,
                },
                {
                    "name": "hideFromAddressLists",
                    "multiValue": False,
                    "displayName": "Hide from address list",
                    "mandatory": False,
                },
                {
                    "name": "sendPermission",
                    "multiValue": True,
                    "displayName": "Senders allowed to send emails",
                    "mandatory": False,
                },
                {
                    "name": "sendPermissionLevel",
                    "multiValue": False,
                    "displayName": "Send permission level",
                    "mandatory": False,
                },
            ],
        },
    }

    validators = {}

    init_string = []
    for key in workspaces:
        out_string = []
        out_string.append("from ..core_models import CreateTemplate")

        cur_validator = validators.get(key.lower(), {})
        class_names = []
        try:
            cur_attributes = attributes[key.lower()]
        except KeyError:
            continue
        for new_key, new_attrs in cur_attributes.items():
            class_name = f"Create{key}_{new_key}"
            class_names.append(class_name)

            class_string = create_attribute_class(
                class_name, "CreateTemplate", new_attrs, cur_validator
            )
            out_string.append("")
            out_string.append("")
            out_string.extend(class_string)

        out_string.append("")
        out_text = "\n".join(out_string)

        if "pydantic." in out_text:
            out_text = "import pydantic\n" + out_text

        (config.create_templates_folder / f"{key.lower()}.py").write_text(out_text)

        init_string.append(
            f"from .{key.lower()} import {', '.join(sorted(class_names))}  # noqa"
        )

    (config.create_templates_folder / "__init__.py").write_text(
        "\n".join(sorted(init_string))
    )


def main(config: Config):
    workspaces = get_workspaces(config)

    # Attributes
    created_classes = create_attributes(workspaces, config)

    # Models
    create_models(created_classes, config)

    # Create templates
    create_templates(workspaces, config)


if __name__ == "__main__":
    args = parse_args()
    config = args_to_config(args)
    main(config)
