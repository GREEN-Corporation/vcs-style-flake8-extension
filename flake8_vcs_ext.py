import ast
import pycodestyle

from typing import Final, Generator, Tuple, Type, Any, List, Iterable, Optional

MSG_VCS001: Final = "VCS001 no one tab for line continuation"

class MultilineDeterminator:

	def __init__(self, tree) -> None:
		self.tree = tree
		self.problems = []

	def checkAllMultilines(self):
		self.findAllMultilines()

	def findAllMultilines(self):
		for node in self.tree.body:
			if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
				self.findInFunctionDef(node)
			if isinstance(node, ast.ClassDef):
				self.findInClassDef(node)

	def findInFunctionDef(self, node) -> None:
		args = node.args.args
		args_intents = map(lambda x: x.col_offset, args)
		if not self.containsSameIntents(args_intents):
			arg_with_differ_intent = self.getArgWithDifferIntent(args_intents)
			self.problems.append(arg_with_differ_intent.lineno,
				arg_with_differ_intent.col_offset)

	def findInClassDef(self, node):
		for functionDef in node.body:
			self.findInFunctionDef(functionDef)
	
	def containsSameIntents(self, args) -> bool:
		if set(args) == 1:
			return False
		return True

	def getArgWithDifferIntent(self, args):
		last_intent: int = 0
		for arg in args:
			if arg.col_offset != last_intent:
				return arg
			last_intent = arg.col_offset

	def checkMultiline(self):
		pass

class Plugin:

	def __init__(
			self,
			tree,
		)\
		-> None:
		self.tree = tree

	def __iter__(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]: # иначе
		# TypeError: 'Plugin' object is not iterable
		determinator = MultilineDeterminator(self.tree)
		determinator.checkAllMultilines()
		for (lineno, col) in determinator.problems:
			yield lineno, col, MSG_VCS001, type(self)