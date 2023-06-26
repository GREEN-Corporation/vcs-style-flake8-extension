from typing import List, Tuple

case_1a_src = """
import aboba


print("kurwa")
"""
case_1a = (case_1a_src, [3])  # "3" means the violation happens on Line 3

def collect_all_cases() -> Tuple[Tuple[str, List[int]]]:
	return (
		case_1a,
	)