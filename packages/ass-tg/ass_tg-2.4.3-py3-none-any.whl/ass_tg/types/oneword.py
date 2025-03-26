from abc import ABC
from typing import Optional

from babel.support import LazyProxy

from ass_tg.i18n import lazy_gettext as l_
from ass_tg.types.base_abc import OneWordArgFabricABC


class WordArg(OneWordArgFabricABC, ABC):

    def needed_type(self) -> tuple[LazyProxy, LazyProxy]:
        return l_("Word (string with no spaces)"), l_("Words (strings with no spaces)")

    async def value(self, text: str) -> str:
        return text

    async def check_type(self, text: str) -> bool:
        return bool(text.strip())  # Is not empty

    @property
    def examples(self) -> Optional[dict[str, Optional[LazyProxy]]]:
        return {
            'Hello': None,
            'Foo': None,
            'bar': None
        }


class IntArg(OneWordArgFabricABC):

    def needed_type(self) -> tuple[LazyProxy, LazyProxy]:
        return l_("Integer (number)"), l_("Integers (numbers)")

    async def value(self, text: str) -> int:
        return int(text)

    async def check_type(self, text: str) -> bool:
        return text.removeprefix('-').isdigit()


class BooleanArg(OneWordArgFabricABC):
    default_no_value_value = True

    true_words = ("true", "t", "1", "yes", "y", "+", "on", "enable", "enabled", ":)")
    false_words = ("false", "f", "0", "no", "n", "-", "off", "disable", "disabled", ":(")

    def needed_type(self) -> tuple[LazyProxy, LazyProxy]:
        return l_("Boolean (Yes / No value)"), l_("Booleans (Yes / No values)")

    @property
    def examples(self) -> Optional[dict[str, Optional[LazyProxy]]]:
        return {
            'true': l_("True (can means Enabled or Yes)"),
            'false': l_("False (can means Disabled or No)"),
        }

    async def value(self, text: str) -> bool:
        return text.lower() in self.true_words

    async def check_type(self, text: str) -> bool:
        return text.lower() in {*self.true_words, *self.false_words}
