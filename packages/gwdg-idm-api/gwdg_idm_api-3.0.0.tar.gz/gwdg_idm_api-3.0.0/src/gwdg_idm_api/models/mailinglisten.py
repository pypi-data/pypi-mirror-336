from __future__ import annotations

from pydantic import Field

from ..attributes import MailinglistenAttributes

try:
    from ..base_models import MailinglistenBase
except ImportError:
    from ..core_models import IDMUserClass

    class MailinglistenBase(IDMUserClass):
        pass


from ..core_models import ChangeTemplate


class Mailinglisten(MailinglistenBase):
    api_suffix: str = Field(default="/Mailinglisten/objects")
    user_class: type[ChangeTemplate] = Field(default=MailinglistenAttributes)
