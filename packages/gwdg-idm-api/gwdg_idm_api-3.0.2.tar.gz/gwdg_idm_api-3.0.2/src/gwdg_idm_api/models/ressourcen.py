from __future__ import annotations

from pydantic import Field

from ..attributes import RessourcenAttributes

try:
    from ..base_models import RessourcenBase
except ImportError:
    from ..core_models import IDMUserClass

    class RessourcenBase(IDMUserClass):
        pass


from ..core_models import ChangeTemplate


class Ressourcen(RessourcenBase):
    api_suffix: str = Field(default="/Ressourcen/objects")
    user_class: type[ChangeTemplate] = Field(default=RessourcenAttributes)
