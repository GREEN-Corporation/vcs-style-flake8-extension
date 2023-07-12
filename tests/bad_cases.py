from typing import Literal, Tuple

case_print_two_tabs = (
"""print("kurwa"
		"dsfsf")"""
)

case_print_two_tabs = (case_print_two_tabs, 2, 2)

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

case_def_with_two_tabs = (
"""def base(
		a1,
		a100,
		a2,
		a3
):
	pass"""
)

case_def_with_two_tabs = (case_def_with_two_tabs, 2, 2)

case_class_def_with_diff_intents = (
"""class Test:
	def base(
		a1,
		a100,
			a2,
		a3
	):
		pass"""
)

case_class_def_with_diff_intents = (case_class_def_with_diff_intents, 5, 4)

case_print_in_context = (
"""import github
import greenlogistic

print(
	greenlogistic.name,
		greenlogistic.date
	)"""
)

case_print_in_context = (case_print_in_context, 6, 2)

def collect_all_cases() -> Tuple[str]:
	return (
		case_print_two_tabs, # type: ignore
		case_if_with_diff_indents,
		case_def_with_diff_indents,
		case_def_with_two_tabs,
		case_class_def_with_diff_intents,
		case_print_in_context
	)