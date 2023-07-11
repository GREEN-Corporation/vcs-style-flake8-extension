import os
import ast
import sys
import pytest
from typing import Set, List

from flake8_vcs_ext import Plugin

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(THIS_DIR)

import tests.good_cases as good_cases
import tests.bad_cases as bad_cases

def _results(src_code: str) -> Set[str]:
	tree = ast.parse(src_code)
	plugin = Plugin(tree)
	return {
		f'{line}:{col} {msg}' for line, col, msg, _ in plugin.__iter__()
	}

@pytest.mark.parametrize('src_code', good_cases.collect_all_cases())
def test_ok_cases(src_code: str) -> None:
   assert _results(src_code) == set()

@pytest.mark.parametrize('src_code, lines', bad_cases.collect_all_cases())
def test_no_ok_cases(src_code: str, lines: List[int]) -> None:
	expected_violation_messages = {
		f'{line}:0 VCS001 no tab for line continuation'
		for line in lines
	}
	assert _results(src_code) == expected_violation_messages