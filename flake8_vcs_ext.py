import ast
from typing import (Any, Dict, Final, Generator, Iterable, List, Tuple, Type, # noqa
					Union) # noqa
# noqa
from _types import LinenoStorage, LinenoSupportObjects

MSG_VCS001: Final = "VCS001 no one tab for line continuation"

def isinstanceInIterable(target: Iterable[Any], classinfo: Any) -> bool:
	for obj in target:
		if not isinstance(obj, classinfo):
			return False
	return True

def dictsConcatenation(left_dict: Dict[Any, Any], right_dict: Dict[Any, Any])\
	-> Dict[Any, Any]:
	return dict(list(left_dict.items()) + list(right_dict.items()))

class MultilineDeterminator:

	def __init__(self, tree: ast.Module) -> None:
		self.tree = tree
		self.correct_indent = 0

	def getMultilinesIndents(self) -> Union[List[LinenoSupportObjects], None]:
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

	def _findMultilinesInFunctionDef(
		self,
		node: Union[ast.FunctionDef, ast.AsyncFunctionDef]
	) -> List[LinenoSupportObjects]:
		def_statement_indent = node.col_offset
		indent_differ_inter_def_statement_and_body = 1
		self.correct_indent = (def_statement_indent +
			indent_differ_inter_def_statement_and_body)
		args = node.args.args
		linenums_args: LinenoStorage = dict(zip(args,
			map(lambda x: x.lineno, args)))
		if self._containsSameLinenums(list(linenums_args.values())):
			return []
		multilines_args = self._removeObjectsOnSameLine(linenums_args)
		return multilines_args

	def _findMultilinesInClassDef(self, node: ast.ClassDef)\
		-> Union[List[LinenoSupportObjects], None]:
		for functionDef in node.body:
			if isinstance(functionDef, ast.FunctionDef):
				return self._findMultilinesInFunctionDef(functionDef)
		return None
		
	def _findMultilinesInIf(self, node: ast.If)\
		-> Union[List[LinenoSupportObjects], None]:
		if_statement_indent = node.col_offset
		indent_differ_inter_if_statement_and_signature = 4
		self.correct_indent = (if_statement_indent +
			indent_differ_inter_if_statement_and_signature)
		maybe_operators = node.test
		if isinstance(maybe_operators, ast.BoolOp):
			operators: ast.BoolOp = maybe_operators
		maybe_operands = operators.values
		if isinstanceInIterable(maybe_operands, ast.Name):
			operands: List[ast.Name] = maybe_operands # type: ignore
		linenums_operators: LinenoStorage = {operators:
			operators.lineno}
		linenums_operands: LinenoStorage = dict(zip(operands, map(lambda x:
			x.lineno, operands)))
		if self._containsSameLinenums(list(linenums_operands.values())):
			return []
		multilines_operators = self._removeObjectsOnSameLine(linenums_operators)
		multilines_operands = self._removeObjectsOnSameLine(linenums_operands)
		if node.end_lineno:
			multiline_objects_for_check = self._mixOperandsAndOperators(
				multilines_operators,
				multilines_operands,
				node.lineno,
				node.end_lineno
			)
		return multiline_objects_for_check

	def _containsSameLinenums(
		self,
		linenums: List[int]
	) -> bool:
		if len(set(linenums)) == 1:
			return True
		return False

	def _removeObjectsOnSameLine(
		self,
		linenums_objs: LinenoStorage
	) -> LinenoStorage:
		result: LinenoStorage = {}
		last_added_obj_lineno: int = 0
		for (obj, lineno) in linenums_objs.items():
			if lineno != 0 and lineno > last_added_obj_lineno:
				last_added_obj_lineno = lineno
				result.update({obj: lineno})
		return result

	def _mixOperandsAndOperators(
		self,
		operators: LinenoStorage,
		operands: LinenoStorage,
		start_lineno: int,
		end_lineno: int
	) -> List[LinenoSupportObjects]:
		operators = self._createOperatorObjForEachLine(operators)
		result: LinenoStorage = dictsConcatenation(operators, operands)
		result = dict(sorted(result.items(), key=lambda x: (x[1], x[0].col_offset)))
		result = self._removeObjectsOnSameLine(result)
		return result

	def _createOperatorObjForEachLine(self, operators: LinenoStorage)\
		-> LinenoStorage:
		result: LinenoStorage = {}
		for (operator, lineno) in operators.items():
			diff_between_num_start_and_end_lines =\
				operator.end_lineno - operator.lineno # type: ignore
			correction_with_start_and_end_range = 1
			for current_lineno in range(1, diff_between_num_start_and_end_lines +
				correction_with_start_and_end_range):
				operator = ast.BoolOp(
					lineno=current_lineno,
					end_lineno=current_lineno,
					col_offset=operator.col_offset
				)
				result.update({operator: current_lineno})
		return result

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
	
	def _getArgWithIndentNotOne(
		self,
		args_indents: List[Union[ast.arg, ast.Name]]
	) -> Union[None, ast.arg]:
		for arg in args_indents:
			if arg.col_offset != self.correct_indent:
				return arg
		return None

class Plugin:

	def __init__(self, tree: ast.Module) -> None:
		self.tree = tree

	def __iter__(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
		# иначе TypeError: 'Plugin' object is not iterable. Вместо __iter__
		# должен быть run согласно документации и примерам flake8
		determinator = MultilineDeterminator(self.tree)
		indents = determinator.getMultilinesIndents()
		correct_indent = determinator.getCorrectIndent()
		if indents:
			checker = IndentChecker(correct_indent, indents)
			checker.updateProblems()
			for (lineno, col) in checker.problems:
				yield lineno, col, MSG_VCS001, type(self)