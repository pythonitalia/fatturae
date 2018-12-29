from typing import List, Dict

from lxml import etree

from .types import XMLDict


def _split_tags(tag_name: str, text: str) -> List[etree._Element]:
    tags: List[etree._Element] = []

    size = 200

    chunks = [text[y - size : y] for y in range(size, len(text) + size, size)]

    for value in chunks:
        tag = etree.Element(tag_name)
        tag.text = value
        tags.append(tag)

    return tags


def dict_to_xml(dict: XMLDict):
    tags: List[etree._Element] = []

    for key, value in dict.items():
        if isinstance(value, Dict):
            tag = etree.Element(key)

            for subtag in dict_to_xml(value):
                tag.append(subtag)

            tags.append(tag)
        else:
            if isinstance(value, int):
                value = str(value)

            for tag in _split_tags(key, value):
                tags.append(tag)

    return tags
