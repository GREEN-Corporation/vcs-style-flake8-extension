import ast
from typing import Any, Final, Generator, List, Tuple, Type, Union

from _types import LinenoSupportObject

MSG_VCS001: Final = "VCS001 no one tab for line continuation"

def isinstanceInIterable(target: Iterable[Any], classinfo: Any) -> bool:
	for obj in target:
		if not isinstance(obj, classinfo):
			return False

class MultilineDeterminator:

	def __init__(self, tree: ast.Module) -> None:
		self.tree = tree
		self.correct_indent = 0

	def getMultilinesIndents(self) -> Union[List[ast.arg], List[ast.Name], None]:
		for node in self.tree.body:
			if (isinstance(node, ast.FunctionDef) or
				isinstance(node, ast.AsyncFunctionDef)):
				return self._findMultilinesInFunctionDef(node)
			elif isinstance(node, ast.ClassDef):
				return self._findMultilinesInClassDef(node)
			elif isinstance(node, ast.If):
				return self._findMultilinesInIf(node)
		return None

	def getCorrectIndent(self) -> int:
		return self.correct_indent

	def _findMultilinesInFunctionDef(self,
		node: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> List[ast.arg]:
		def_statement_indent = node.col_offset
		indent_differ_inter_def_statement_and_body = 1
		self.correct_indent = (def_statement_indent +
			indent_differ_inter_def_statement_and_body)
		args = node.args.args
		args_lineno = list(map(lambda x: x.lineno, args))
		if _containsSameIntegers(args_lineno):
			return []
		args = self._removeObjectsOnSameLine(args)
		return args

	def _findMultilinesInClassDef(self, node: ast.ClassDef)\
		-> Union[List[ast.arg], None]:
		for functionDef in node.body:
			return self._findMultilinesInFunctionDef(functionDef) # type: ignore
		return None
		
	def _findMultilinesInIf(self, node: ast.If)\
		-> Union[List[ast.Name], None]:
		if_statement_indent = node.col_offset
		indent_differ_inter_if_statement_and_signature = 4
		self.correct_indent = (if_statement_indent +
			indent_differ_inter_if_statement_and_signature)
		operators = node.test
		operands = operators.values
		operands_lineno = list(map(lambda x: x.lineno, operands))
		if _containsSameIntegers(operands_lineno):
			return []
		multilines_operands = self._removeObjectsOnSameLine(operands)
		multilines_operators = self._removeObjectsOnSameLine(operators)
		return operands

	def _removeObjectsOnSameLine(
		self,
		signature_objects: List[LinenoSupportObject]
	) -> List[Union[ast.Name, ast.arg]]:
		result: List[Union[ast.Name, ast.arg]] = []
		last_added_obj_lineno: int = 0
		for obj in signature_objects:
			if obj.lineno != 0 and obj.lineno > last_added_obj_lineno:
				last_added_obj_lineno = obj.lineno
				result.append(obj)
		return result

	def _mixOperandsAndOperators(self, operands, operators):
		result = []
		

class IndentChecker:
	
	def __init__(self, correct_indent: int, args: List[Union[ast.arg, ast.Name]])\
		-> None:
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
			
	def _allCorrect(self, target: List[int]) -> bool:
		for number in target:
			if number != self.correct_indent:
				return False
		return True
	
	def _getArgWithIndentNotOne(self, args_indents: List[Union[ast.arg, ast.Name]])\
		-> Union[None, ast.arg]:
		for arg in args_indents:
			if arg.col_offset != self.correct_indent:
				return arg
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