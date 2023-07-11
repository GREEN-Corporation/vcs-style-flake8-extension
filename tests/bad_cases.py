from typing import Literal, Tuple

bad_case = Tuple[Literal[''], int, int]

case_two_tabs = (
"""print("kurwa"
		"dsfsf")"""
)

case_two_tabs = (case_two_tabs, 2, 2)

case_if_with_diff_indents = (
"""if (aboba
				and string):
					pass"""
)

case_if_with_diff_indents = (case_if_with_diff_indents, 2, 4)

case_def_with_diff_indents = (
"""def base(
	a1,
	a100,
			a2,
		a3
):
	pass"""
)

case_def_with_diff_indents = (case_def_with_diff_indents, 4, 3)

case_in_context = (
"""import github
import greenlogistic

print(
	greenlogistic.name,
		greenlogistic.date
	)"""
)

case_in_context = (case_in_context, 6, 2)

def collect_all_cases() -> Tuple[bad_case]:
	return (
		case_two_tabs, # type: ignore
		case_if_with_diff_indents,
		case_def_with_diff_indents,
		case_in_context
	)