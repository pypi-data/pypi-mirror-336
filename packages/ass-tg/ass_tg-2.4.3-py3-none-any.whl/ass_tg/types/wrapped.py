from abc import ABC
from typing import Generic, TypeVar

from babel.support import LazyProxy

from ass_tg.entities import ArgEntities
from ass_tg.types.base_abc import ArgFabric

WrappedArgType = TypeVar('WrappedArgType')


class WrappedArgFabricABC(ArgFabric, ABC, Generic[WrappedArgType]):
    child_fabric: ArgFabric

    def __init__(self, child_fabric: ArgFabric[WrappedArgType], *args):
        super().__init__(description=child_fabric.description)

        self.child_fabric = child_fabric
        self.know_the_end = child_fabric.know_the_end
        self.know_the_start = child_fabric.know_the_start

    def needed_type(self) -> tuple[LazyProxy, LazyProxy]:
        return self.child_fabric.needed_type()

    def check(self, text: str, entities: ArgEntities) -> bool:
        return self.child_fabric.check(text, entities)

    async def parse(self, text: str, offset: int, entities: ArgEntities) -> tuple[int, WrappedArgType]:
        return await self.child_fabric.parse(text, offset, entities)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>: {self.child_fabric}"


class WrappedNeededTypeArg(WrappedArgFabricABC):
    needed_type_var: LazyProxy

    def __init__(self, needed_type: LazyProxy, *args):
        super().__init__(*args)
        self.needed_type_var = needed_type

    def needed_type(self) -> tuple[LazyProxy, LazyProxy]:
        return self.needed_type_var, self.needed_type_var


class WrappedDescriptionArg(WrappedArgFabricABC):
    description: LazyProxy

    def __init__(self, description: LazyProxy, *args):
        super().__init__(*args)
        self.description = description
