from __future__ import annotations

from pydantic import Field

from ..attributes import BenutzerverwaltungAttributes, BenutzerverwaltungAttributes_MDMP

try:
    from ..base_models import BenutzerverwaltungBase
except ImportError:
    from ..core_models import IDMUserClass

    class BenutzerverwaltungBase(IDMUserClass):
        pass


from ..core_models import ChangeTemplate


class Benutzerverwaltung(BenutzerverwaltungBase):
    api_suffix: str = Field(default="/Benutzerverwaltung/objects")
    user_class: type[ChangeTemplate] = Field(default=BenutzerverwaltungAttributes)


class Benutzerverwaltung_MDMP(BenutzerverwaltungBase):
    api_suffix: str = Field(default="/Benutzerverwaltung/objects")
    user_class: type[ChangeTemplate] = Field(default=BenutzerverwaltungAttributes_MDMP)
