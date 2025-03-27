from __future__ import annotations

from pydantic import Field

from ..attributes import LDAPVerteilerAttributes

try:
    from ..base_models import LDAPVerteilerBase
except ImportError:
    from ..core_models import IDMUserClass

    class LDAPVerteilerBase(IDMUserClass):
        pass


from ..core_models import ChangeTemplate


class LDAPVerteiler(LDAPVerteilerBase):
    api_suffix: str = Field(default="/LDAPVerteiler/objects")
    user_class: type[ChangeTemplate] = Field(default=LDAPVerteilerAttributes)
