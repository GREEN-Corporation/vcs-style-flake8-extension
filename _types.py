import ast
from typing import Union, Dict

LinenoSupportObjects = Union[ast.arg, ast.Name, ast.BoolOp]
LinenoStorage = Dict[LinenoSupportObjects, int]