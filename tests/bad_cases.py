from typing import Tuple

bad_case_type = Tuple[str, int, int]

case_print_two_tabs = (
"""print("kurwa"
		"dsfsf")"""
)

case_print_two_tabs: bad_case_type = (case_print_two_tabs, 2, 2) # type: ignore [no-redef] # noqa

case_if_with_diff_indents = (
"""if (aboba
				and string):
					pass"""
)

case_if_with_diff_indents: bad_case_type = (case_if_with_diff_indents, 2, 4) # type: ignore [no-redef] # noqa

case_def_with_diff_indents = (
"""def base(
	a1,
	a100,
			a2,
		a3
):
	pass"""
)

case_def_with_diff_indents: bad_case_type = (case_def_with_diff_indents, 4, 3) # type: ignore [no-redef] # noqa

case_def_with_two_tabs = (
"""def base(
		a1,
		a100,
		a2,
		a3
):
	pass"""
)

case_def_with_two_tabs: bad_case_type = (case_def_with_two_tabs, 2, 2) # type: ignore [no-redef] # noqa

case_class_def_with_diff_indents = (
"""class Test:
	def base(
		a1,
		a100,
			a2,
		a3
	):
		pass"""
)

case_class_def_with_diff_indents: bad_case_type = (case_class_def_with_diff_indents, 5, 3) # type: ignore [no-redef] # noqa

case_print_in_context = (
"""import github
import greenlogistic

print(
	greenlogistic.name,
		greenlogistic.date
	)"""
)

case_print_in_context: bad_case_type = (case_print_in_context, 6, 2) # type: ignore [no-redef] # noqa

def collect_all_cases() -> Tuple[bad_case_type]:
	return ( # type: ignore [return-value]
		# case_print_two_tabs,
		# case_if_with_diff_indents,
		case_def_with_diff_indents,
		case_def_with_two_tabs,
		case_class_def_with_diff_indents,
		# case_print_in_context
	)