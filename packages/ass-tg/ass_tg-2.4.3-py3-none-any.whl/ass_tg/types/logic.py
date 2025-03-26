import contextlib
from typing import Any, Optional

from babel.support import LazyProxy

from ass_tg.entities import ArgEntities
from ass_tg.exceptions import ArgTypeError, ArgSimpleTypeError, ArgIsRequiredError
from ass_tg.i18n import lazy_gettext as l_, gettext as _
from ass_tg.types.base_abc import ArgFabric, ParsedArgs
from ass_tg.types.wrapped import WrappedArgFabricABC


class OptionalArg(WrappedArgFabricABC):
    can_be_empty = True

    def needed_type(self) -> tuple[LazyProxy, LazyProxy]:
        needed_type = self.child_fabric.needed_type()

        return (
            l_("Optional {}").format(needed_type[0]),
            l_("Optionals {}").format(needed_type[0]),
        )

    def check(self, text: str, entities: ArgEntities) -> bool:
        return True

    async def parse(self, text: str, offset: int, entities: ArgEntities) -> tuple[int, Any]:
        with contextlib.suppress(ArgTypeError, ArgSimpleTypeError):
            if self.child_fabric.check(text, entities):
                arg = await self.child_fabric(text, offset, entities)
                return arg.length, arg.value
        return 0, None


class OrArg(ArgFabric):
    args_type: tuple[ArgFabric, ...]

    def __init__(self, *args_type: ArgFabric, description: Optional[LazyProxy | str] = None):
        super().__init__(args_type[0].description)
        self.args_type = args_type
        self.description = description

    def needed_type(self) -> tuple[LazyProxy, LazyProxy]:
        return (l_(" or ").join(f"'{arg.needed_type()[0]}'" for arg in self.args_type),
                l_(" or ").join(f"'{arg.needed_type()[1]}'" for arg in self.args_type))

    def check(self, text: str, entities: ArgEntities) -> bool:
        return bool(text)

    async def pre_parse(
            self,
            text: str,
            offset: int,
            entities: ArgEntities,
            **_kwargs
    ) -> tuple[int, Any]:
        for arg_fabric in self.args_type:
            try:
                if arg_fabric.know_the_end:
                    text = _kwargs.get("know_end_arg_text", text)
                else:
                    text = _kwargs.get("not_known_end_arg_text", text)

                try:
                    if not arg_fabric.check(text, entities):
                        continue
                except ArgSimpleTypeError:
                    continue

                self.know_the_end = arg_fabric.know_the_end
                arg = await arg_fabric(text, offset, entities)

                return arg.length, arg.value

            except ArgTypeError:
                continue

        raise ArgTypeError(
            needed_type=self.needed_type(),
            description=self.description,
            examples=self.examples,
            length=len(text),
            offset=offset
        )

    def __repr__(self):
        return f'<{self.__class__.__name__}>: {", ".join(str(x) for x in self.args_type)}'


class AndArg(ArgFabric):
    """
    Represents a basic and the first argument, which contains the child ones.
    Each argument contains its name and a fabric.
    Implements arguments validation.
    """

    fabrics: dict[str, ArgFabric]

    def __init__(self, *args, **kwargs: ArgFabric):
        super().__init__(*args)

        self.fabrics = kwargs

    def needed_type(self):
        return _(", and ").join(str(x.needed_type()[0]) for x in self.fabrics.values()), ""

    @property
    def examples(self) -> Optional[dict[str, Optional[LazyProxy]]]:

        example_str = ''

        for idx, fabric in enumerate(self.fabrics.values()):
            example_str += " " if idx > 0 else ""

            if not fabric.examples:
                return None

            example_str += str(tuple(fabric.examples.keys())[0])

        return {
            example_str: l_("Example syntax")
        }

    def check(self, text: str, entities: ArgEntities) -> bool:
        return True

    async def parse(
            self,
            text: str,
            offset: int,
            entities: ArgEntities
    ) -> tuple[int, ParsedArgs]:

        args_data = ParsedArgs()
        length = 0
        args_length = 0

        for arg_codename, arg_fabric in self.fabrics.items():
            # Strip text and count offset
            stripped_offset = (len(text) - len(text := text.lstrip()))
            offset += stripped_offset
            args_length += stripped_offset
            length += stripped_offset

            arg_entities = entities.cut_before(args_length)

            if not arg_fabric.can_be_empty and not text.strip():
                raise ArgIsRequiredError(
                    description=arg_fabric.description,
                    examples=arg_fabric.examples,
                    needed_type=arg_fabric.needed_type(),
                    offset=offset
                )

            arg = await arg_fabric(text, offset, arg_entities)
            args_data[arg_codename] = arg
            length += arg.length

            args_length += arg.length
            offset += arg.length
            text = text[arg.length:]

        return length, args_data
