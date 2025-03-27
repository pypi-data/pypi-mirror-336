from __future__ import annotations

from pydantic import Field

from ..attributes import SharedMailboxAttributes

try:
    from ..base_models import SharedMailboxBase
except ImportError:
    from ..core_models import IDMUserClass

    class SharedMailboxBase(IDMUserClass):
        pass


from ..core_models import ChangeTemplate


class SharedMailbox(SharedMailboxBase):
    api_suffix: str = Field(default="/SharedMailbox/objects")
    user_class: type[ChangeTemplate] = Field(default=SharedMailboxAttributes)
