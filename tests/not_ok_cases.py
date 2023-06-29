from typing import List, Tuple

case_two_tabs = (
"""print("kurwa"
		"dsfsf")"""
)

case_two_tabs = (case_two_tabs, [2])

case_if_four_tabs_and_space = ( 
"""if (aboba
				 and string):
					pass"""
)

case_if_four_tabs_and_space = (case_if_four_tabs_and_space, [2])

case_def_with_diff_indents = (
"""
def base(
	a1,
	a100,
			a2,
		a3
):
	pass
"""
)

case_def_with_diff_indents = (case_def_with_diff_indents, [4])

case_in_context = (
"""import github
import greenlogistic

print(
	greenlogistic.name,
		greenlogistic.date
	)"""
)

case_in_context = (case_in_context, [6])

def collect_all_cases() -> Tuple[Tuple[str, List[int]]]:
	return (
		case_two_tabs,
		case_if_four_tabs_and_space,
		case_def_with_diff_indents,
		case_in_context
	)