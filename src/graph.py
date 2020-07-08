from dataclasses import dataclass
from typing import List


@dataclass
class Graph:
    number_of_verticies: int = None
    number_of_edges: int = None
    edges: List[List[int]] = None
