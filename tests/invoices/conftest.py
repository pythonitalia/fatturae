import os

import pytest

from lxml import etree


@pytest.fixture
def sample_invoice_xml():
    here = os.path.dirname(__file__)

    parser = etree.XMLParser(remove_blank_text=True)

    root = etree.parse(
        os.path.join(here, "../data/IT01234567890_FPA01.xml"), parser=parser
    )

    for elem in root.iter("*"):
        if elem.text is not None:
            elem.text = elem.text.strip()

    return root
