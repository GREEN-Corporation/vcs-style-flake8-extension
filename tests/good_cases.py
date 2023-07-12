from typing import Literal, Tuple

case_print = (
"""print("kurwa"
	"dasdasd"
	"dsfsf")"""
)

case_if = (
"""if (aboba
	and bvs
	and string):
		pass"""
)

case_def = (
"""def base(
	a1,
	a100,
	a2,
	a3
):
	pass"""
)

case_in_context = (
"""import github
import greenlogistic

print(
	greenlogistic.name,
	greenlogistic.date
	)"""
)

def collect_all_cases() -> Tuple[str, ...]:
	return (
		case_print,
		case_if,
		case_def,
		case_in_context
	)