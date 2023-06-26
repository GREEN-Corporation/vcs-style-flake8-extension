import ast
from typing import Generator, Tuple, Type, Any, List, Union, Final

import importlib.metadata as importlib_metadata

MSG_VCS001: Final = "VCS001 no tab for line continuation"
MSG_VCS002: Final = "VCS002 no exactly 1 blank line after the last import at the beginning of the file"

BLOCKS_REQUIRING_INDENT = (
	ast.Import,
	ast.ImportFrom
)

ModuleLikeTypes = Union[
   ast.Import,
	ast.ImportFrom
]

class Visitor(ast.NodeVisitor):

	def __init__(self) -> None:
		self.problems: List[Tuple[int, int]] = []

	def generic_visit(self, node: ModuleLikeTypes) -> None:
		self._check_one_node(node)

	def _check_one_node(self, node: ModuleLikeTypes) -> None:
		if 'body' in node.__dict__:
			self._check_a_list_of_items(node.body)

		if 'orelse' in node.__dict__:
			self._check_a_list_of_items(node.orelse)

		if 'handlers' in node.__dict__:
			self._check_a_list_of_items(node.handlers)

		if 'finalbody' in node.__dict__:
			self._check_a_list_of_items(node.finalbody)

	def _check_a_list_of_items(self, item_list) -> None:
		for i, this_item in enumerate(item_list):
			next_item = item_list[i + 1]
			if (
				not isinstance(next_item, ast.ExceptHandler)
				and next_item.lineno - this_item.end_lineno <= 1
			):
				line = this_item.end_lineno
				col = 0
				self.problems.append((line, col))

class Plugin:
	name = __name__
	version = importlib_metadata.version("vcs-style-flake8-extension")

	def __init__(self, tree: ast.AST) -> None:
		self._tree = tree

	def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
		visitor = Visitor()
		visitor.visit(self._tree)
		for line, col in visitor.problems:
			yield line, col, MSG_VCS001, type(self)