import re

# FIXME: нужно различать id паблика и человека
_LINK_REGEX = re.compile(r"https?://vk\.com/(:?id|club|public)(\d+)")


def get_id_from_link(link: str) -> int:
    id_ = _LINK_REGEX.findall(link)
    if not id_:
        # TODO: custom error
        raise ValueError(f"Cannot parse link: '{link}'")
    return int(id_[0][1])
