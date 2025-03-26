from typing import Any

from ass_tg.entities import ArgEntities
from ass_tg.types.base_abc import ArgFabric, ParsedArgs
from ass_tg.types.logic import AndArg


class ReverseArg(AndArg):
    """
    An argument type that tries to parse the arguments from right to left instead.

    Useful when you want to parse an argument list that contains an argument that doesn't know its end in the middle,
    and you want to parse it as the last from the left-overs.

    Example usage:
    arg = ReverseArg(first=TextArg(), second=SurroundedArg(TextArg()))
    arg('Hello world!! "Foo bar"', ...

    Using with AndArg:
    Normally we know the start of the argument as we start from the first symbol in the text and cut the
    consumed offset by the argument and pass the rest to the next argument in a list.
    But we can't do the same here, as we need to find a start of the argument in the middle of the text,
    cut it and pass the rest of the argument.
    That's why we are using a special ArgFabric function get_start() to get the start offset of the argument.
    """

    def __init__(self, *args, **kwargs: ArgFabric):
        if any(not (arg.know_the_start or idx == 0) for idx, arg in enumerate(kwargs.values())):
            raise ValueError("All arguments must know the start (except the first)")

        super().__init__(*args, **kwargs)

    def check(
            self,
            text: str,
            entities: ArgEntities
    ) -> bool:
        # TODO
        return True

    async def parse(self, text: str, offset: int, entities: ArgEntities) -> tuple[int, Any]:
        args_data = ParsedArgs()

        length = 0

        for arg_codename, arg_fabric in reversed(list(self.fabrics.items())):
            start_offset = arg_fabric.get_start(text, entities)
            arg_entities = entities.cut_after(start_offset)
            arg_offset = offset + start_offset
            post_offset_text = text[start_offset:]

            arg = await arg_fabric(post_offset_text, arg_offset, arg_entities)
            args_data[arg_codename] = arg

            length += arg.length

            # Prepare variable for the next arguments
            text = text[:-arg.length]
            entities = entities.cut_after(arg_offset - 1)
            stripped_offset = (len(text) - len(text := text.rstrip()))  # Strip to right
            length += stripped_offset

        return length, args_data
