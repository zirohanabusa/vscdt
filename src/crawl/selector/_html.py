from collections import UserList
from typing import Any, List, Self, TextIO, Tuple

import cssselect
import lxml.html


class Node:
    """Node represents a HTML tree node"""

    @classmethod
    def from_filename(cls, filename: str, encoding: str = "utf-8") -> "Node":
        """Generate the HTML tree node from a HTML file name

        Args:
            filename (str): HTML file name
            encoding (str, optional): file encoding. Defaults to "utf-8".

        Returns:
            Self: HTML tree node
        """
        with open(filename, "r", encoding=encoding) as file:
            return cls.from_file(file)

    @classmethod
    def from_file(cls, file: TextIO) -> "Node":
        """Generate the HTML tree node from TextIO stream

        Args:
            file (TextIO): TextIO stream

        Returns:
            Self: HTML tree node
        """
        html: str = file.read()
        return cls.from_string(html)

    @classmethod
    def from_string(cls, html: str, **kws: Any) -> "Node":
        """Generate the HTML tree node from HTML string

        Args:
            html (str): HTML string

        Returns:
            Self: HTML tree node
        """
        dom = lxml.html.fromstring(html, **kws)
        return cls(dom)

    @property
    def node(self) -> Any:
        return self._

    def __init__(self, node: Any) -> None:
        self._ = node

    def xpath(self, query: str, **kws: Tuple[str, ...]) -> "Nodes":
        """Get the nodes corresponding to a XPath from the node

        Args:
            query (str): XPath string

        Returns:
            Any: HTML tree nodes
        """
        nodes: Nodes = Nodes()
        tmp = self._.xpath(query)
        if tmp:
            nodes.extends(*tmp)
        return nodes

    def css(self, query: str) -> "Nodes":
        """Get the nodes corresponding to a CSS selector from the node

        Args:
            query (str): CSS selecter string

        Returns:
            Any: HTML tree nodes
        """
        nodes: Nodes = Nodes()
        tmp = self._.cssselect(query)
        if tmp:
            nodes.extends(*tmp)
        return nodes

    def get(self, encoding: str = "utf-8") -> str | Any:
        """Get node string

        Args:
            encoding (str, optional): string encoding. Defaults to "utf-8".

        Returns:
            str | Any: Node string
        """
        return lxml.html.tostring(self._, encoding=encoding).decode().strip()

    def get_text(self, recursive: bool = False) -> str | list[str]:
        return [x for x in self._.itertext()] if recursive is True else self._.text


class Nodes(UserList[Node | Any]):
    def extends(self, *nodes: Any) -> None:
        for node in nodes:
            if isinstance(node, Node):
                self.append(node)
            elif isinstance(node, str):
                self.append(node)
            elif isinstance(node, (lxml.html.HtmlElement,)):
                self.append(Node(node))
            else:
                msg = f"else instance={node}\ntype={type(node)}"
                raise ValueError(msg)

    def xpath(self, query: str) -> "Nodes":
        nodes: Nodes = self.__class__()
        for node in self:
            if isinstance(node, Node):
                tmp = node.xpath(query)
                if tmp:
                    nodes.extends(*tmp)
            elif isinstance(node, str):
                pass
            else:
                raise ValueError()
        return nodes

    def css(self, query: str) -> "Nodes":
        nodes: "Nodes" = self.__class__()
        for node in self:
            if isinstance(node, Node):
                tmp = node.css(query)
                if tmp:
                    nodes.extends(*tmp)
            elif isinstance(node, str):
                pass
            else:
                raise ValueError()
        return nodes

    def get(self, encoding: str = "utf-8") -> Any:
        if self:
            return self[0] if isinstance(self[0], (str,)) else self[0].get(encoding=encoding)

    def get_text(self, recursive: bool = False) -> Any:
        if self:
            return self[0].get_text(recursive=recursive) if isinstance(self[0], Node) else self[0]

    def get_all(self, encoding: str = "utf-8") -> Any:
        return [e if isinstance(e, (str,)) else e.get(encoding=encoding) for e in self]

    def get_text_all(self, recursive: bool = False) -> Any:
        return [e.get_text(recursive=recursive) if isinstance(e, Node) else e for e in self]
