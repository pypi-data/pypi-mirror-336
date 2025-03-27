from __future__ import annotations

from pydantic import Field

from ..attributes import GruppenverwaltungAttributes, GruppenverwaltungAttributes_MDMP

try:
    from ..base_models import GruppenverwaltungBase
except ImportError:
    from ..core_models import IDMUserClass

    class GruppenverwaltungBase(IDMUserClass):
        pass


from ..core_models import ChangeTemplate


class Gruppenverwaltung(GruppenverwaltungBase):
    api_suffix: str = Field(default="/Gruppenverwaltung/objects")
    user_class: type[ChangeTemplate] = Field(default=GruppenverwaltungAttributes)


class Gruppenverwaltung_MDMP(GruppenverwaltungBase):
    api_suffix: str = Field(default="/Gruppenverwaltung/objects")
    user_class: type[ChangeTemplate] = Field(default=GruppenverwaltungAttributes_MDMP)
