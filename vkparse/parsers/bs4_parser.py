import re
from collections.abc import Generator
from datetime import datetime, timezone
from typing import final

import bs4
from bs4.element import Tag

from vkparse.models import author
from vkparse.models.author import Author
from vkparse.models.message import Message
from vkparse.parsers.abstract_parser import AbstractParser

# FIXME: нyжнo paзличaть id пa6ликa и чeлoвeкa
_LINK_REGEX = re.compile(r"https?://vk\.com/(:?id|club|public)(\d+)")


def get_id_from_link(link: str) -> int:
    id_ = _LINK_REGEX.findall(link)
    if not id_:
        # TODO: custom error
        message = f"Cannot parse link: '{link}'"
        raise ValueError(message)
    return int(id_[0][1])


@final
class BS4Parser(AbstractParser):
    def parse(self, content: str) -> Generator[Message, None, None]:
        soup = bs4.BeautifulSoup(content, "html.parser")

        messages = soup.find_all("div", class_="item__main")
        yield from map(self._parse_message, messages)

    @staticmethod
    def _parse_message(html: Tag) -> Message:
        header = html.find("div", class_="message__header")
        author_tag = header.find("a")  # type: ignore[optionalMemberAccess]
        from_ = author.YOU
        if author_tag:
            id_ = get_id_from_link(author_tag.get("href"))  # type: ignore[optMember]
            from_ = Author(id_, author_tag.text)  # type: ignore[optionalMemberAccess]

        # FIXME: text matching
        kludges = html.find("div", class_="kludges")
        text = kludges.previous_element.text  # type: ignore[optionalMemberAccess]
        if not isinstance(text, str):
            text = None
        # TODO: attachments
        # TODO: time
        return Message(
            author=from_,
            date=datetime.now(tz=timezone.utc),
            text=text,
            attachments=None,
        )
