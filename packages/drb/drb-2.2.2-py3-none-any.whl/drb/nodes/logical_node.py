from typing import Optional, Any, Union, List, Dict, Tuple, Callable

from drb.core.path import Path, parse_path, ParsedPath
from drb.core import DrbNode
from drb.nodes.mutable_node import MutableNode
from drb.exceptions.core import DrbException
from pathlib import PurePath


class DrbLogicalNode(MutableNode):
    """Logical Node for Drb
    This node implements an in-memory logical node, It can be used as default
    node for virtual nodes hierarchy. It can also be used as a wrapper of
    the source node, in this case, the source node is clone.

    Parameters:
        source (DrbNode | str | Path | PurePath):
    Keyword Arguments:
        namespace_uri (str): namespace URI of node - Used only if source is not
                             a DrbNode
        parent (DrbNode): parent of node - Used only if source is not a DrbNode
        value (Any): value of node - Used only if source is not a DrbNode
    """
    def __init__(self, source: Union[str, Path, PurePath], **kwargs):
        super().__init__()
        self._path_source = parse_path(source)
        self.name = self._path_source.filename
        self.namespace_uri = kwargs.get('namespace_uri', None)
        self.value = kwargs.get('value', None)
        self.parent = kwargs.get('parent', None)
        self._children = []

    @property
    def path(self) -> ParsedPath:
        if self._path_source.absolute or self.parent is None:
            path = self._path_source
        else:
            path = self.parent.path / self._path_source
        return path

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        return self._attrs

    @attributes.setter
    def attributes(self, attributes: Dict[Tuple[str, str], Any]) -> None:
        keys = set(self.attributes.keys())
        for n, ns in keys:
            self.remove_attribute(n, ns)
        for n, ns in attributes:
            self.add_attribute(n, attributes[n, ns], ns)

    @property
    def children(self) -> List[DrbNode]:
        return self._children

    @children.setter
    def children(self, children: List[MutableNode]) -> None:
        for idx in range(len(self)):
            self.remove_child(idx)
        for child in children:
            self.append_child(child)

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        try:
            return self._attrs[(name, namespace_uri)]
        except (IndexError, TypeError, KeyError) as error:
            raise DrbException(f'No attribute {name} found') from error

    def __str__(self):
        string = '<'
        if self.namespace_uri:
            string = string + f"{self.namespace_uri}:"
        string = string + f"{self.name}"
        if self.attributes:
            for name, namespace in self.attributes.keys():
                string = string + ' "'
                if namespace:
                    string = string + f'{namespace}:'
                string = string + f'{name}"="'
                string = \
                    string + f'{str(self.attributes.get((name, namespace)))}"'
        if self.value:
            string = string + f'>{str(self.value)}</{self.name}>'
        else:
            string = string + '/>'
        return string

    def __repr__(self):
        return self.__str__()

    def _insert_child(self, index: int, node: MutableNode) -> None:
        self._children.insert(index, node)

    def _append_child(self, node: MutableNode) -> None:
        self._children.append(node)

    def _replace_child(self, index: int, new_node: MutableNode) -> None:
        self._children[index] = new_node

    def _remove_child(self, index: int) -> None:
        del self._children[index]

    def _add_attribute(self, name: str, value: Optional[Any] = None,
                       namespace_uri: Optional[str] = None) -> None:
        if (name, namespace_uri) in self._attrs:
            raise DrbException(f'Attribute ({name}, {namespace_uri})'
                               f'already exist')
        self._attrs[name, namespace_uri] = value

    def _update_attribute_value(self, name: str, value: Any,
                                namespace_uri: str = None) -> None:
        if (name, namespace_uri) not in self._attrs:
            raise DrbException('Attribute not found: ('
                               f'{name}, {namespace_uri})')
        self._attrs[name, namespace_uri] = value

    def _remove_attribute(self, name: str, namespace_uri: str = None) -> None:
        if (name, namespace_uri) in self._attrs:
            del self._attrs[name, namespace_uri]


class WrappedNode(MutableNode):
    def __init__(self, node: DrbNode):
        super().__init__()
        self._wrapped = node

    @property
    def name(self) -> str:
        return self._wrapped.name

    @name.setter
    def name(self, new_name):
        self._wrapped.name = new_name

    @property
    def namespace_uri(self) -> str:
        return self._wrapped.namespace_uri

    def __imatmul__(self, other):
        self._wrapped.__imatmul__(other)

    def __matmul__(self, other):
        return self._wrapped.__matmul__(other)

    @namespace_uri.setter
    def namespace_uri(self, new_namespace):
        self._wrapped.namespace_uri = new_namespace

    @property
    def value(self) -> Optional[Any]:
        return self._wrapped.value

    @value.setter
    def value(self, new_value):
        self._wrapped.value = new_value

    @property
    def parent(self) -> str:
        return self._wrapped.parent

    @parent.setter
    def parent(self, new_parent):
        self._wrapped.parent = new_parent

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        return self._wrapped.attributes

    @attributes.setter
    def attributes(self, new_attributes: Dict[Tuple[str, str], Any]) -> None:
        self._wrapped.attributes = new_attributes

    @property
    def children(self) -> List[DrbNode]:
        return self._wrapped.children

    @children.setter
    def children(self, new_children: List[DrbNode]):
        self._wrapped.children = new_children

    def _insert_child(self, index: int, node: DrbNode) -> None:
        self._wrapped.insert_child(index, node)

    def _append_child(self, node: DrbNode) -> None:
        self._wrapped.append_child(node)

    def _replace_child(self, index: int, new_node: DrbNode) -> None:
        self._wrapped.replace_child(index, new_node)

    def _remove_child(self, index: int) -> None:
        self._wrapped.remove_child(index)

    def _add_attribute(self, name: str, value: Optional[Any] = None,
                       namespace_uri: Optional[str] = None) -> None:
        self._wrapped.add_attribute(name, value, namespace_uri)

    def _update_attribute_value(self, name: str, value: Any,
                                namespace_uri: str = None) -> None:
        self._wrapped.update_attribute_value(name, value, namespace_uri)

    def _remove_attribute(self, name: str, namespace_uri: str = None) -> None:
        self._wrapped.remove_attribute(name, namespace_uri)

    def has_impl(self, impl: type, identifier: str = None) -> bool:
        return self._wrapped.has_impl(impl, identifier)

    def get_impl(self, impl: type, identifier: str = None, **kwargs) -> Any:
        return self._wrapped.get_impl(impl, identifier, **kwargs)

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        return self._wrapped.get_attribute(name, namespace_uri)

    def close(self) -> None:
        self._wrapped.close()

    def register(self, event_type: str, callback: Callable):
        self._wrapped.register(event_type, callback)

    def unregister(self, event_type: str, callback: Callable):
        self._wrapped.unregister(event_type, callback)
