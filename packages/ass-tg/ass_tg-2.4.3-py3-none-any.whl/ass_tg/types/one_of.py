from typing import Iterable, Optional

from babel.support import LazyProxy

from ass_tg.i18n import gettext as _
from ass_tg.i18n import lazy_gettext as l_
from ass_tg.types.logic import OrArg
from ass_tg.types.text_eq import EqualsArg


class OneOf(OrArg):
    know_the_end = True

    def __init__(
            self,
            one_of: Iterable[str],
            description: Optional[LazyProxy | str] = None,
            *args):
        self.one_of = tuple(one_of)
        super().__init__(*[EqualsArg(v) for v in one_of], description=description, *args)

    def needed_type(self) -> tuple[LazyProxy, LazyProxy]:
        return (
            LazyProxy(lambda: _("One of: {}").format(
                l_(" or ").join(f"'{v}'" for v in self.one_of)
            )),
            LazyProxy(lambda: _("One of: {}").format(
                l_(" or ").join(f"'{v}'" for v in self.one_of)
            ))
        )

    @property
    def examples(self) -> Optional[dict[str, Optional[LazyProxy]]]:
        return {str(self.one_of[0]): None}
