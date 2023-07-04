import tokenize
import ast
import pycodestyle

from typing import Final, Generator, Tuple, Type, Any, List, Iterable

MSG_VCS001: Final = "VCS001 no tab for line continuation"

class TabValidator():

	def __init__(self, tokens: List[tokenize.TokenInfo]) -> None:
		self.tokens = tokens
		self.problems: List[Tuple[int, int]] = []

	def run(self) -> None:
		self.findContinuatuion()

	def findContinuatuion(self):
		for token in self.tokens:
			print(token)

class Plugin:

	def __init__(self, physical_line, )\
		-> None:
		pass
		# self.tree = tree
		# self.file_tokens = file_tokens
		# self.problems_strings: List[Tuple[int, int]] = []

	def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
		raise Exception
		# validator = TabValidator(self.file_tokens)
		# validator.run()
		# for (number, col) in validator.problems:
		# 	yield number, col, MSG_VCS001, type(self)