import random
import string
import datetime
from typing import List, Tuple, Dict, Set, Any, Callable, Sequence

# -2. Returns a random list of integers.
def randlist(NoOfElements: int, Start: int = 0, End: int = 100) -> List[int]:
    """
    Generate a list of random integers.

    :param NoOfElements: Number of elements in the list.
    :param Start: Lower bound (inclusive).
    :param End: Upper bound (inclusive).
    :return: List of random integers.
    """
    return [random.randint(Start, End) for _ in range(NoOfElements)]

# -1. Returns a random tuple of integers.
def randtuple(NoOfElements: int, Start: int = 0, End: int = 100) -> Tuple[int, ...]:
    """
    Generate a tuple of random integers.

    :param NoOfElements: Number of elements in the tuple.
    :param Start: Lower bound (inclusive).
    :param End: Upper bound (inclusive).
    :return: Tuple of random integers.
    """
    return tuple(random.randint(Start, End) for _ in range(NoOfElements))

# 0. Returns a random dictionary of given length.
def randdic(NoOfElements: int, Start: int = 0, End: int = 100) -> Dict[int, int]:
    """
    Generate a dictionary with random integer keys and values.

    :param NoOfElements: Number of key-value pairs.
    :param Start: Lower bound for keys and values (inclusive).
    :param End: Upper bound for keys and values (inclusive).
    :return: Dictionary with random integers.
    """
    return {random.randint(Start, End): random.randint(Start, End) for _ in range(NoOfElements)}

# 1. Returns a set of random integers.
def randset(NoOfElements: int, Start: int = 0, End: int = 100) -> Set[int]:
    """
    Generate a set of random integers.

    :param NoOfElements: Number of unique integers.
    :param Start: Lower bound (inclusive).
    :param End: Upper bound (inclusive).
    :return: Set of random integers.
    """
    s: Set[int] = set()
    while len(s) < NoOfElements:
        s.add(random.randint(Start, End))
    return s
