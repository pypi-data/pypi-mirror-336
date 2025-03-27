from __future__ import annotations

from pydantic import Field

from ..attributes import SelfServiceAttributes

try:
    from ..base_models import SelfServiceBase
except ImportError:
    from ..core_models import IDMUserClass

    class SelfServiceBase(IDMUserClass):
        pass


from ..core_models import ChangeTemplate


class SelfService(SelfServiceBase):
    api_suffix: str = Field(default="/SelfService/objects")
    user_class: type[ChangeTemplate] = Field(default=SelfServiceAttributes)
