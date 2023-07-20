import ast
from typing import Dict, Union

LinenoSupportObjects = Union[ast.arg, ast.Name, ast.BoolOp]
LinenoStorage = Dict[LinenoSupportObjects, int]