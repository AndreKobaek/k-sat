from dataclasses import dataclass
from typing import List


@dataclass
class CNF:
    number_of_literals: int = None
    number_of_clauses: int = None
    clauses: List[List[int]] = None
    automorphism_group_size: int = None
