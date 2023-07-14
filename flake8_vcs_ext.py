import ast
from typing import Any, Final, Generator, List, Tuple, Type, Union

MSG_VCS001: Final = "VCS001 no one tab for line continuation"

def _containsSameIntegers(target: List[int]) -> bool:
	if len(set(target)) == 1:
		return True
	return False

class MultilineDeterminator:

	def __init__(self, tree: ast.Module) -> None:
		self.tree = tree
		self.correct_indent = 0

	def getMultilinesIndents(self) -> Union[List[ast.arg], None]:
		for node in self.tree.body:
			if (isinstance(node, ast.FunctionDef) or
				isinstance(node, ast.AsyncFunctionDef)):
				return self._findMultilinesInFunctionDef(node)
			elif isinstance(node, ast.ClassDef):
				return self._findMultilinesInClassDef(node)
		return None

	def getCorrectIndent(self) -> int:
		return self.correct_indent

	def _findMultilinesInFunctionDef(self,
		node: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> List[ast.arg]:
		self.correct_indent = node.col_offset + 1
		args = node.args.args
		args_lineno = list(map(lambda x: x.lineno, args))
		if _containsSameIntegers(args_lineno):
			return []
		return args

	def _findMultilinesInClassDef(self, node: ast.ClassDef)\
		-> Union[List[ast.arg], None]:
		for functionDef in node.body:
			return self._findMultilinesInFunctionDef(functionDef) # type: ignore
		return None
		
class IndentChecker:
	
	def __init__(self, correct_indent: int, args: List[ast.arg]) -> None:
		self.correct_indent = correct_indent
		self.args = args
		self.problems: List[Tuple[int, int]] = []

	def updateProblems(self) -> None:
		self._checkMultilinesIndents()

	def _checkMultilinesIndents(self) -> None:
		args_indents = list(map(lambda x: x.col_offset, self.args))
		if not self._allCorrect(args_indents):
			arg_with_indent_not_one = self._getArgWithIndentNotOne(self.args)
			if not arg_with_indent_not_one:
				raise Exception("A VCS001 mismatch was found, but the offending"
					" argument could not be determined.")
			self.problems.append((arg_with_indent_not_one.lineno,
				arg_with_indent_not_one.col_offset))
			return
		# if not _containsSameIntegers(args_indents):
		# 	arg_with_differ_indent = self._getArgWithDifferindent(self.args)
		# 	if not arg_with_differ_indent:
		# 		raise Exception("A VCS001 mismatch was found, but the offending"
		# 			" argument could not be determined.")
		# 	self.problems.append((arg_with_differ_indent.lineno,
		# 		arg_with_differ_indent.col_offset))
			
	def _allCorrect(self, target: List[int]) -> bool:
		for number in target:
			if number != self.correct_indent:
				return False
		return True
	
	def _getArgWithIndentNotOne(self, args_indents: List[ast.arg])\
		-> Union[None, ast.arg]:
		for arg in args_indents:
			if arg.col_offset != self.correct_indent:
				return arg
		return None

	def _getArgWithDifferindent(self, args_indents: List[ast.arg])\
		-> Union[None, ast.arg]:
		last_indent = args_indents[0].col_offset
		for arg in args_indents[1:]:
			if arg.col_offset != last_indent:
				return arg
			last_indent = arg.col_offset
		return None

class Plugin:

	def __init__(self, tree: ast.Module) -> None:
		self.tree = tree

	def __iter__(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
		# иначе TypeError: 'Plugin' object is not iterable. Вместо __iter__
		# должен быть run
		determinator = MultilineDeterminator(self.tree)
		indents = determinator.getMultilinesIndents()
		correct_indent = determinator.getCorrectIndent()
		if indents:
			checker = IndentChecker(correct_indent, indents)	
			checker.updateProblems()
			for (lineno, col) in checker.problems:
				yield lineno, col, MSG_VCS001, type(self)