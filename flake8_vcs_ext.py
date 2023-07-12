import ast
from typing import Any, Final, Generator, Iterable, List, Tuple, Type, Union

MSG_VCS001: Final = "VCS001 no one tab for line continuation"

def _containsSameIntegers(target: Iterable[int]) -> bool:
	if len(set(target)) == 1:
		return True
	return False

class MultilineDeterminator:

	def __init__(self, tree: ast.Module) -> None:
		self.tree = tree

	def getMultilinesIntents(self) -> Union[List[ast.arg], None]:
		for node in self.tree.body:
			if (isinstance(node, ast.FunctionDef) or
				isinstance(node, ast.AsyncFunctionDef)):
				return self._findMultilinesInFunctionDef(node)
			elif isinstance(node, ast.ClassDef):
				return self._findMultilinesInClassDef(node)

	def _findMultilinesInFunctionDef(self,
		node: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> List[ast.arg]:
		args = node.args.args
		args_lineno = map(lambda x: x.lineno, args)
		if _containsSameIntegers(args_lineno):
			return []
		return args

	def _findMultilinesInClassDef(self, node: ast.ClassDef)\
		-> Union[List[ast.arg], None]:
		for functionDef in node.body:
			return self._findMultilinesInFunctionDef(functionDef) # type: ignore
		
class IntentChecker:
	
	def __init__(self, args: List[ast.arg]) -> None:
		self.args = args
		self.problems: List[Tuple[int, int]] = []

	def updateProblems(self) -> None:
		self._checkMultilinesIntents()

	def _checkMultilinesIntents(self) -> None:
		args_intents = map(lambda x: x.col_offset, self.args)
		if not _containsSameIntegers(args_intents):
			arg_with_differ_intent = self._getArgWithDifferIntent(self.args)
			if arg_with_differ_intent:
				self.problems.append((arg_with_differ_intent.lineno,
					arg_with_differ_intent.col_offset))
			
	def _getArgWithDifferIntent(self, args_intents: List[ast.arg])\
		-> Union[None, ast.arg]:
		last_intent = args_intents[0].col_offset
		for arg in args_intents[1:]:
			if arg.col_offset != last_intent:
				return arg
			last_intent = arg.col_offset

class Plugin:

	def __init__(self, tree: ast.Module) -> None:
		self.tree = tree

	def __iter__(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
		# иначе TypeError: 'Plugin' object is not iterable. Вместо __iter__
		# должен быть run
		determinator = MultilineDeterminator(self.tree)
		intents = determinator.getMultilinesIntents()
		if intents:
			checker = IntentChecker(intents)
			checker.updateProblems()
			for (lineno, col) in checker.problems:
				yield lineno, col, MSG_VCS001, type(self)