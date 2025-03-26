from abc import abstractmethod
from typing import Any

from spiderpy3.objects.handler import Handler
from spiderpy3.mixins.protocol import ProtocolMixin


class Login(Handler, ProtocolMixin):
    @abstractmethod
    def action(self, *args, **kwargs) -> Any:
        pass
