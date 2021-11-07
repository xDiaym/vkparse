from datetime import datetime
from typing import final

import bs4
from bs4 import Tag

from models import author
from models.author import Author
from models.message import Message
from parsers.abstract_parser import AbstractParser
from parsers.utils import get_id_from_link


@final
class BS4Parser(AbstractParser):
    def parse(self, content: str) -> list[Message]:
        soup = bs4.BeautifulSoup(content, "html.parser")

        messages = soup.find_all("div", class_="item__main")
        return list(map(self._parse_message, messages))

    @staticmethod
    def _parse_message(html: Tag) -> Message:
        header = html.find("div", class_="message__header")
        author_tag = header.find("a")
        from_ = author.YOU
        if author_tag:
            id_ = get_id_from_link(author_tag.get("href"))
            from_ = Author(id_, author_tag.text)

        # FIXME: text matching
        kludges = html.find("div", class_="kludges")
        text = kludges.previous_element.text
        if not isinstance(text, str):
            text = None
        # TODO: attachments
        # TODO: time
        return Message(
            author=from_, date=datetime.now(), text=text, attachments=None
        )
