from collections import UserList
from json import dumps, loads
from typing import Any, Dict, List, Self, TextIO, Tuple

import jmespath
from jsonpath_ng.ext import parse


class Node:
    """Node represents a JSON node"""

    @classmethod
    def from_filename(cls, filename: str, encoding: str = "utf-8") -> Self:
        with open(filename, "r", encoding=encoding) as f:
            return cls.from_file(f)

    @classmethod
    def from_file(cls, file: TextIO) -> Self:
        txt: str = file.read()
        return cls.from_string(txt)

    @classmethod
    def from_string(cls, txt: str, **kws: Tuple[str, ...]) -> Self:
        parsed = loads(txt)
        return cls(parsed, **kws)

    @property
    def node(self) -> Any:
        return self._

    def __init__(self, json_data: Any, **kws: Tuple[str, ...]) -> None:
        self._ = json_data

    def jsonpath(self, expr: str, **kws: Tuple[str, ...]) -> "Nodes":
        nodes = Nodes()
        parsed = parse(expr).find(self._)
        if parsed:
            nodes.extends(parsed[0].value)
        return nodes

    def jmespath(self, query: str, **kws: Tuple[str, ...]) -> "Nodes":
        nodes = Nodes()
        parsed = jmespath.search(query, self._)
        if parsed:
            nodes.extends(parsed)
        return nodes

    def get(self) -> Any:
        return self._

    def to_string(self) -> Any:
        return dumps(self._)


class Nodes(UserList[Node | int | float | bool | str | None]):
    def extends(self, *nodes: Any) -> None:
        for node in nodes:
            if node is None or isinstance(
                node,
                (
                    int,
                    float,
                    bool,
                    str,
                ),
            ):
                self.append(node)
            elif isinstance(
                node,
                (
                    tuple,
                    list,
                    dict,
                ),
            ):
                self.append(Node(node))
            elif isinstance(node, Node):
                self.append(node)
            else:
                msg = f"else instance={nodes}\ntype={type(nodes)}"
                raise ValueError(msg)

    def jsonpath(self, query: str, **kws: Tuple[str, ...]) -> "Nodes":
        results = self.__class__()
        for node in self:
            if isinstance(node, Node):
                for result in node.jsonpath(query):
                    results.extends(result)
            elif isinstance(
                node,
                (
                    int,
                    float,
                    bool,
                    str,
                ),
            ):
                pass
            else:
                raise ValueError()
        return results

    def jmespath(self, query: str, **kws: Tuple[str, ...]) -> "Nodes":
        results = self.__class__()
        for node in self:
            if isinstance(node, Node):
                for result in node.jmespath(query):
                    results.extends(result)
            elif isinstance(
                node,
                (
                    int,
                    float,
                    bool,
                    str,
                ),
            ):
                pass
            else:
                raise ValueError()
        return results

    def get(self) -> int | float | bool | str | Tuple[Any] | List[Any] | Dict[str, Any] | None:
        if self:
            return self[0].get() if isinstance(self[0], Node) else self[0]
        return None

    def get_all(self) -> int | float | bool | str | Tuple[Any] | List[Any] | Dict[str, Any]:
        return [e.get() if isinstance(e, Node) else e for e in self]
