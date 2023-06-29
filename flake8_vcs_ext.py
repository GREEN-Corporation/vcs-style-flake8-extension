import tokenize
from typing import Generator, Tuple, Type, Any, List, Union, Final, Optional

import importlib.metadata as importlib_metadata

MSG_VCS001: Final = "VCS001 no tab for line continuation"

# class Visitor(ast.NodeVisitor):

# 	def __init__(self) -> None:
# 		self.problems: List[Tuple[int, int]] = []

# 	def generic_visit(self, node: ModuleLikeTypes) -> None:
# 		self._check_one_node(node)

# 	def _check_one_node(self, node: ModuleLikeTypes) -> None:
# 		if 'body' in node.__dict__:
# 			self._check_a_list_of_items(node.body)

# 	def _check_a_list_of_items(self, item_list: ModuleLikeTypes) -> None:
# 		pass

class Plugin:

	def __init__(self, blank_before, blank_lines, checker_state, indent_char, indent_level) -> None:
		print(blank_before, blank_lines, indent_char, indent_level)

	def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
		raise TestError
		yield 21, 43, MSG_VCS001, type(self)