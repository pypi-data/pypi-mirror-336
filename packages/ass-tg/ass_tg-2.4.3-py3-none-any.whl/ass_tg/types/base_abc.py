from abc import ABC
from typing import Any, Generic, Optional, TypeVar, List, Awaitable

from babel.support import LazyProxy

from ass_tg.entities import ArgEntities
from ass_tg.exceptions import ArgTypeError, ArgSimpleTypeError, ArgStrictError, ArgCustomError

ArgValueType = TypeVar('ArgValueType')


class ArgFabric(Generic[ArgValueType]):
    """Provides an interface to create an argument fabric."""
    description: Optional[LazyProxy | str] = None

    # Whatever argument can find its own end or would occupy all the provided text
    know_the_end: bool = False

    # Whatever argument can find its start position, used by the ReverseArg, must implement get_start()
    # Otherwise it will start from the 0th index as default
    know_the_start: bool = False

    # Whatever argument can parse from the empty string?
    # Disables empty argument string checks.
    # For example, OptionalArg can always be empty
    can_be_empty: bool = False

    # Default value if no value is provided, used by the KeyValue arg, if only key is provided
    default_no_value_value: Optional[Any] = None

    def __init__(self, description: Optional[LazyProxy | str] = None):
        self.description = description

    def needed_type(self) -> tuple[LazyProxy, LazyProxy]:
        """
        Returns a needed type text.
        """
        raise NotImplementedError

    @property
    def examples(self) -> Optional[dict[str, Optional[LazyProxy]]]:
        """
        Returns a dictionary of examples using this argument, and its description.
        description is optional as well as the dictionary itself.
        """
        return None

    def check(
            self,
            text: str,
            entities: ArgEntities
    ) -> bool:
        """
        Checks if the given text is valid for this type.
        It should check by the start of the text, as it could contain other arguments separated.
        Return boolean or raises TypeCheckCustomError.

        Be aware that text CAN BE longer and more entities CAN BE SUPPLIED than argument should take.
        You CAN NOT check the Argument type by the end of the text!
        """
        return True

    async def parse(
            self,
            text: str,
            offset: int,
            entities: ArgEntities
    ) -> tuple[int, ArgValueType]:
        """
        Parses the arguments texts and returns the length of argument and value.
        Returns None if there's no more arguments.

        Be aware that text CAN BE longer and more entities CAN BE SUPPLIED than argument should take.
        You should use only what you need and return an occupied amount of symbols.
        """

        raise NotImplementedError

    async def pre_parse(
            self,
            text: str,
            offset: int,
            entities: ArgEntities,
            **_kwargs
    ) -> tuple[int, ArgValueType]:
        """
        Very special function, usually you DON'T use it. Unless you need to access _kwargs
        """
        return await self.parse(text, offset, entities)

    def unparse(
            self,
            data: ArgValueType,
            **kwargs
    ) -> str:
        """Unparses the argument data back into text"""

        raise NotImplementedError

    def get_start(self, raw_text: str, entities: ArgEntities) -> int:
        """Returns a preliminary start offset of the argument, usually always 0. See ReverseArg for details."""
        return 0

    def get_end(self, raw_text: str, entities: ArgEntities) -> int:
        return len(raw_text)

    async def _call(
            self,
            text: str,
            offset: int,
            entities: ArgEntities,
            **kwargs) -> "ParsedArg[ArgValueType]":

        arg_type_error_text = None
        try:
            if self.check(text, entities):
                length, value = await self.pre_parse(text, offset, entities, **kwargs)
                return ParsedArg(self, value, offset, length)

        except ArgStrictError as e:
            raise ArgCustomError(
                e.text,
                offset=offset,
                length=self.get_end(text, entities),
            )

        except ArgSimpleTypeError as e:
            arg_type_error_text = e.text

        raise ArgTypeError(
            needed_type=self.needed_type(),
            description=self.description,
            offset=offset,
            length=self.get_end(text, entities),
            text=arg_type_error_text or None,
            examples=self.examples or {},
        )

    def __call__(self, *args, **kwargs) -> Awaitable:
        return self._call(*args, **kwargs)

    # def __await__(self, *args, **kwargs):
    #    return self._call(*args, **kwargs).__await__()

    def __repr__(self):
        return f"<{self.__class__.__name__}>"


ParsedArgType = TypeVar('ParsedArgType')


class ParsedArg(ABC, Generic[ParsedArgType]):
    """Argument object."""

    fabric: ArgFabric
    value: ParsedArgType

    offset: int
    length: int

    def __init__(self, fabric: ArgFabric, value: ParsedArgType, offset: int, length: int):
        self.fabric = fabric
        self.value = value
        self.offset = offset
        self.length = length

    def get_value(self) -> Any:
        if isinstance(self.value, ParsedArg):
            return self.value.get_value()

        elif isinstance(self.value, List):
            return [x.get_value() if isinstance(x, ParsedArg) else x for x in self.value]

        return self.value

    @property
    def values(self) -> tuple[ParsedArgType]:
        if not isinstance(self.value, list):
            raise TypeError("Value must be a ArgFabric")

        return tuple(x.value for x in self.value)

    def __repr__(self):
        return f"<{self.fabric}: {self.value=} {self.length=}>"


class ParsedArgs(dict[str, ParsedArg]):
    pass


class OneWordArgFabricABC(ArgFabric, ABC):
    def needed_type(self) -> tuple[LazyProxy, LazyProxy]:
        raise NotImplementedError

    async def check_type(self, text: str) -> bool:
        raise NotImplementedError

    async def value(self, text: str) -> Any:
        raise NotImplementedError

    async def parse(self, raw_text: str, offset: int, entities: ArgEntities) -> tuple[int, Any]:
        first_word, *_rest = raw_text.split(maxsplit=1) or ('',)

        if not await self.check_type(first_word):
            raise ArgTypeError(
                # text=first_word,
                needed_type=self.needed_type(),
                description=self.description,
                length=len(first_word),
                offset=offset,
                examples=self.examples or {}
            )

        return len(first_word), await self.value(first_word)
