from typing import Optional

from aiogram.types import User
from babel.support import LazyProxy
from stfu_tg import UserLink

from ass_tg.entities import ArgEntities
from ass_tg.exceptions import ArgTypeError, ArgSimpleTypeError, ArgCustomError
from ass_tg.i18n import gettext as _
from ass_tg.i18n import lazy_gettext as l_
from ass_tg.types import OrArg
from ass_tg.types.base_abc import ArgFabric, OneWordArgFabricABC


class UserIDArg(OneWordArgFabricABC):
    def needed_type(self) -> tuple[LazyProxy, LazyProxy]:
        return l_("User ID (Numeric)"), l_("User IDs (Numeric)")

    async def value(self, text: str) -> int:
        return int(text.split()[0])

    async def check_type(self, text: str) -> bool:
        return bool(text) and text.split()[0].isdigit()

    @property
    def examples(self) -> Optional[dict[str, Optional[LazyProxy]]]:
        return {
            '1234567890': None,
            '33334856': None
        }


class UsernameArg(OneWordArgFabricABC):
    prefix = '@'

    def needed_type(self) -> tuple[LazyProxy, LazyProxy]:
        return l_("Username (starts with @)"), l_("Username (starts with @)")

    async def value(self, text: str) -> str:
        return text.split()[0].removeprefix(self.prefix)

    async def check_type(self, text: str) -> bool:
        if not text:
            return False

        if not text.startswith(self.prefix):
            raise ArgSimpleTypeError(_("Should start with a prefix"))
        if len(text) < 2:
            raise ArgSimpleTypeError(_("Username is too short"))
        if len(text) > 32:
            raise ArgSimpleTypeError(_("Username is too long"))

        return True

    @property
    def examples(self) -> Optional[dict[str, Optional[LazyProxy]]]:
        return {
            '@username': None,
            '@ofoxr_bot': None
        }


class UserMentionArg(ArgFabric):
    _allowed_entities = ('mention', 'text_mention')

    def needed_type(self) -> tuple[LazyProxy, LazyProxy]:
        return l_("User mention (a link to user)"), l_("User mentions (links to users)")

    @property
    def examples(self) -> Optional[dict[str, Optional[LazyProxy]]]:
        return {
            UserLink(
                user_id=1111224224,
                name="OrangeFox BOT",
            ): None
        }

    def check(self, text: str, entities: ArgEntities) -> bool:
        # It would be nice to check an offset here, but we don't pass it in check()
        return any(x.type in self._allowed_entities for x in entities)

    async def parse(
            self,
            text: str,
            offset: int,
            entities: ArgEntities
    ) -> tuple[int, User]:
        # Check
        mention_entities = [
            x for x in entities if x.type in self._allowed_entities and x.user and x.offset == offset
        ]

        if not mention_entities:
            raise ArgTypeError(
                needed_type=self.needed_type(),
                description=self.description,
                length=len(text),
                offset=offset,
                text=_("Should start with mention!"),
                examples=self.examples
            )

        mention = mention_entities[0]

        if not mention.user:
            raise ArgCustomError(
                _("Unexpected error while trying to get the user! Please report this in the support chat!"),
                _("Could not find the user mention")
            )

        return mention.length, mention.user


class UserArg(OrArg):
    def __init__(self, *args):
        super().__init__(UserMentionArg(), UserIDArg(), UsernameArg(), *args)

    def needed_type(self) -> tuple[LazyProxy, LazyProxy]:
        return l_(
            "User: 'User ID (numeric) / Username (starts with @) / Mention (links to users)'"
        ), l_(
            "Users: 'User IDs (numeric) / Usernames (starts with @) / Mentions (links to users)'"
        )

    @property
    def examples(self) -> Optional[dict[str, Optional[LazyProxy]]]:
        return {
            '1111224224': l_("User ID"),
            '@ofoxr_bot': l_("Username"),
            UserLink(
                user_id=1111224224,
                name="OrangeFox BOT"
            ): l_(
                "A link to user, usually creates by mentioning a user without username."
            )
        }
