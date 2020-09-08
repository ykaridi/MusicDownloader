from collections import defaultdict
from typing import TypeVar, Iterable, Dict, Callable, List

T_co = TypeVar('T_co', covariant=True)
R_co = TypeVar('R_co', covariant=True)


def grouped(iterable: Iterable[T_co], key: Callable[[T_co], R_co]) -> Dict[R_co, List[T_co]]:
    """Groups iterable by provided key into a dictionary"""
    result: Dict[R_co, T_co] = defaultdict(default_factory=lambda: [])
    for item in iterable:
        result[key(item)].append(item)

    return dict(result)
