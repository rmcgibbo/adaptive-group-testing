import math
from typing import Any, Callable, List, Tuple


def generalized_binary_splitting(
    pred: Callable[[List[Any],], bool],
    items: List[Any],
    d: int
) -> List[Any]:
    """Hwang's adaptive generalized binary splitting algorithm for group testing
    
    The generalised binary-splitting algorithm is an essentially-optimal
    adaptive group-testing algorithm that finds d or fewer defectives among
    n items.
    
    This implemenation follows the description of the algorithm here:
    https://en.wikipedia.org/wiki/Group_testing#Generalised_binary-splitting_algorithm

    Arguments
    ---------
    pred : callable
        Test function. Takes a list of items, and returns True if
        _any_ of the items are defective, and False otherwise.
    candidates : list
        Candidate pool. Note, the items must be hashable.
    d : int
        Upper bound on the number of defective items in the pool.
       
    Citations
    ---------
    Hwang, Frank K. "A method for detecting all defective members in a population
    by group testing." Journal of the American Statistical Association
    67.339 (1972): 605-608.

    Returns
    -------
    defective : List
        list of defective items
    """
    defects = []
    unsure = list(items)

    while len(unsure) > 0:
        n = len(unsure)

        if n == 1 or n <= 2*d - 2:
            # test items individually
            for c in unsure:
                if pred([c]):
                    defects.append(c)
            return defects

        else:
            l = n - d + 1
            alpha = math.floor(math.log2(l / 2))
            test_set = unsure[:2**alpha]
            remaining_set = unsure[2**alpha:]
            if pred(test_set):
                single_defect, confirmed_okay = _binary_search(pred, test_set)
                
                defects.append(single_defect)
                unsure = list(set(unsure) - {single_defect} - set(confirmed_okay))
            else:
                unsure = remaining_set                

    raise RuntimeError()

    
def _binary_search(
    pred: Callable[[List[Any],], bool],
    candidates: List[Any]
) -> Tuple[Any, List[Any]]:

    mid = 0
    start = 0
    end = len(candidates)
    nondefective = []

    while (start < end - 1):
        mid = (start + end) // 2

        test_set = candidates[start:mid]
        if pred(test_set):
            end = mid
        else:
            nondefective.extend(test_set)
            start = mid

    return candidates[start], nondefective


def test_binary_search():
    candidates = list(range(100))
    for c in candidates:
        res, non_defective = _binary_search((lambda x: c in x), candidates)
        assert res == c


def test_generalized_binary_splitting():
    d = 5
    N = 100000
    n_calls = 0

    def pred(xs):
        nonlocal n_calls
        n_calls += 1
        return any(x < d for x in xs)

    candidates = list(range(N))
    import random
    random.shuffle(candidates)
    
    assert sorted(generalized_binary_splitting(pred, candidates, d=2)) == list(range(d))
    print(n_calls)
