from __future__ import annotations

from pydantic import Field

from ..attributes import ExchangeVerteilerAttributes

try:
    from ..base_models import ExchangeVerteilerBase
except ImportError:
    from ..core_models import IDMUserClass

    class ExchangeVerteilerBase(IDMUserClass):
        pass


from ..core_models import ChangeTemplate


class ExchangeVerteiler(ExchangeVerteilerBase):
    api_suffix: str = Field(default="/ExchangeVerteiler/objects")
    user_class: type[ChangeTemplate] = Field(default=ExchangeVerteilerAttributes)
