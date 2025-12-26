from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..container import Container

class Provider:
    def __init__(self, application) -> None:
        self.application = application

    def register(self) -> None:
        pass

    def boot(self) -> None:
        pass
