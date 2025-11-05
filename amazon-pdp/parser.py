from bs4 import BeautifulSoup
from typing import Union
import bs4


class _ParsedObject:
    def __init__(self, results: Union[bs4.element.Tag, bs4.element.ResultSet]) -> None:
        self.obj = results

    def text(self):
        """Get the text for the selector"""
        return "".join(x.get_text().strip() for x in self.obj if x is not None)

    def attr(self, attr_type: str):
        try:
            return self.obj.attrs[attr_type]
        except KeyError:
            return None

    def __len__(self):
        return len(self.obj)

    def __iter__(self):
        for each in self.obj:
            yield _ParsedObject(each)

    def __getitem__(self, key: str):
        return _ParsedObject(self.obj.select(key))


class DomParser:
    """Class to provide abstraction for the bs4 parser.

    The class provides a cleaner method to handle html parsing, normally,
    methods like `select` require us to check if it's none or not every step
    which can be abstracted. The `DomParser` class returns a _ParsedObject, this
    object handles additional operations much like php's `pq` method.
    """

    def __init__(self, html: str) -> None:
        """Intialize the parser class.

        Params:
            - html (str): The html content to parse

        Returns:
            - None
        """
        self.parsed_html = BeautifulSoup(html, "html.parser")

    def __call__(self, selector: str) -> _ParsedObject:
        """Provides a cleaner way to invoke the parser

        Params:
            - selector (str): The selector to search for.

        Returns:
            - ParsedObject
        """
        return _ParsedObject(self.parsed_html.select(selector))
