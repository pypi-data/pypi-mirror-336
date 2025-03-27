from __future__ import annotations

from pydantic import Field

from ..attributes import DynamischeExchangeVerteilerAttributes

try:
    from ..base_models import DynamischeExchangeVerteilerBase
except ImportError:
    from ..core_models import IDMUserClass

    class DynamischeExchangeVerteilerBase(IDMUserClass):
        pass


from ..core_models import ChangeTemplate


class DynamischeExchangeVerteiler(DynamischeExchangeVerteilerBase):
    api_suffix: str = Field(default="/DynamischeExchangeVerteiler/objects")
    user_class: type[ChangeTemplate] = Field(
        default=DynamischeExchangeVerteilerAttributes
    )
