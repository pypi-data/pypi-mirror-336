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

# 2. Returns a random string of given length from ascii_letters.
def randstring(length: int, chars: str = string.ascii_letters) -> str:
    """
    Generate a random string from given characters.

    :param length: Length of the string.
    :param chars: Characters to choose from.
    :return: Random string.
    """
    return ''.join(random.choice(chars) for _ in range(length))

# 3. Returns a list of random floats between Start and End.
def randfloatlist(NoOfElements: int, Start: float = 0.0, End: float = 1.0) -> List[float]:
    """
    Generate a list of random floats.

    :param NoOfElements: Number of floats.
    :param Start: Lower bound (inclusive).
    :param End: Upper bound (inclusive).
    :return: List of random floats.
    """
    return [random.uniform(Start, End) for _ in range(NoOfElements)]

# 4. Returns a matrix (list of lists) of random integers.
def randmatrix(rows: int, cols: int, Start: int = 0, End: int = 100) -> List[List[int]]:
    """
    Generate a matrix of random integers.

    :param rows: Number of rows.
    :param cols: Number of columns.
    :param Start: Lower bound for elements (inclusive).
    :param End: Upper bound for elements (inclusive).
    :return: Matrix (list of lists) of random integers.
    """
    return [[random.randint(Start, End) for _ in range(cols)] for _ in range(rows)]

# 5. Returns a random "word" of given length.
def randword(length: int) -> str:
    """
    Generate a random lowercase word.

    :param length: Length of the word.
    :return: Random word.
    """
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

# 6. Returns a random sentence composed of random words.
def randsentence(wordCount: int, minWordLength: int = 3, maxWordLength: int = 8) -> str:
    """
    Generate a random sentence composed of random words.

    :param wordCount: Number of words in the sentence.
    :param minWordLength: Minimum length of each word.
    :param maxWordLength: Maximum length of each word.
    :return: Random sentence.
    """
    words = [randword(random.randint(minWordLength, maxWordLength)) for _ in range(wordCount)]
    return ' '.join(words).capitalize() + '.'

# 7. Returns a random date string between two years.
def randdate(StartYear: int = 2000, EndYear: int = 2025) -> str:
    """
    Generate a random date string in the format YYYY-MM-DD.

    :param StartYear: Starting year.
    :param EndYear: Ending year.
    :return: Random date string.
    """
    year = random.randint(StartYear, EndYear)
    month = random.randint(1, 12)
    day = random.randint(1, 28)  # Simplified day selection.
    return f"{year:04d}-{month:02d}-{day:02d}"

# 8. Returns a list of random boolean values.
def randboollist(NoOfElements: int) -> List[bool]:
    """
    Generate a list of random boolean values.

    :param NoOfElements: Number of boolean values.
    :return: List of booleans.
    """
    return [random.choice([True, False]) for _ in range(NoOfElements)]

# 9. Returns a random hex color code.
def randcolor() -> str:
    """
    Generate a random hexadecimal color code.

    :return: Hex color string (e.g., '#1A2B3C').
    """
    return '#' + ''.join(random.choice('0123456789ABCDEF') for _ in range(6))

# 10. Returns a list of lists of random integers.
def randlistoflists(noOfSublists: int, sublistLength: int, Start: int = 0, End: int = 100) -> List[List[int]]:
    """
    Generate a list of lists of random integers.

    :param noOfSublists: Number of sublists.
    :param sublistLength: Number of integers in each sublist.
    :param Start: Lower bound for integers (inclusive).
    :param End: Upper bound for integers (inclusive).
    :return: List of lists of random integers.
    """
    return [randlist(sublistLength, Start, End) for _ in range(noOfSublists)]

# 11. Returns a random string made up of ascii letters, digits, and punctuation.
def randascii(length: int) -> str:
    """
    Generate a random string containing ascii letters, digits, and punctuation.

    :param length: Length of the string.
    :return: Random string with diverse characters.
    """
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

# 12. Returns a list of unique random integers.
def randunique(NoOfElements: int, Start: int = 0, End: int = 100) -> List[int]:
    """
    Generate a list of unique random integers.

    :param NoOfElements: Number of unique integers.
    :param Start: Lower bound (inclusive).
    :param End: Upper bound (inclusive).
    :return: List of unique random integers.
    """
    nums: Set[int] = set()
    while len(nums) < NoOfElements:
        nums.add(random.randint(Start, End))
    return list(nums)

# 13. Returns a list of random even integers.
def randeven(NoOfElements: int, Start: int = 0, End: int = 100) -> List[int]:
    """
    Generate a list of random even integers.

    :param NoOfElements: Number of even integers.
    :param Start: Lower bound (inclusive).
    :param End: Upper bound (inclusive).
    :return: List of even integers.
    """
    evens: List[int] = []
    while len(evens) < NoOfElements:
        num = random.randint(Start, End)
        if num % 2 == 0:
            evens.append(num)
    return evens

# 14. Returns a list of random odd integers.
def randodd(NoOfElements: int, Start: int = 0, End: int = 100) -> List[int]:
    """
    Generate a list of random odd integers.

    :param NoOfElements: Number of odd integers.
    :param Start: Lower bound (inclusive).
    :param End: Upper bound (inclusive).
    :return: List of odd integers.
    """
    odds: List[int] = []
    while len(odds) < NoOfElements:
        num = random.randint(Start, End)
        if num % 2 != 0:
            odds.append(num)
    return odds

# 15. Returns a list of random prime numbers (simple check; not optimized for large ranges).
def is_prime(n: int) -> bool:
    """
    Check if a number is prime.

    :param n: Number to check.
    :return: True if prime, False otherwise.
    """
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def randprime(NoOfElements: int, Start: int = 2, End: int = 100) -> List[int]:
    """
    Generate a list of random prime numbers.

    :param NoOfElements: Number of prime numbers.
    :param Start: Lower bound for prime candidates (inclusive).
    :param End: Upper bound for prime candidates (inclusive).
    :return: List of prime numbers.
    """
    primes: List[int] = []
    attempts = 0
    while len(primes) < NoOfElements and attempts < NoOfElements * 100:
        num = random.randint(Start, End)
        if is_prime(num):
            primes.append(num)
        attempts += 1
    return primes

# 16. Returns a random index from a given sequence.
def randindex(data: Sequence[Any]) -> Any:
    """
    Get a random valid index from a sequence.

    :param data: The sequence from which to pick an index.
    :return: Random index, or None if the sequence is empty.
    """
    if not data:
        return None
    return random.randint(0, len(data) - 1)

# 17. Returns a shuffled copy of a list.
def randshuffle(lst: List[Any]) -> List[Any]:
    """
    Return a shuffled copy of the provided list.

    :param lst: List to shuffle.
    :return: New list with shuffled elements.
    """
    new_list = lst[:]
    random.shuffle(new_list)
    return new_list

# 18. Returns a list of k unique random elements from a list.
def randsample(lst: List[Any], k: int) -> List[Any]:
    """
    Return k unique random elements from the list.

    :param lst: List to sample from.
    :param k: Number of unique elements to return.
    :return: List of sampled elements.
    :raises ValueError: If k is larger than the length of lst.
    """
    if k > len(lst):
        raise ValueError("Sample larger than list")
    return random.sample(lst, k)

# 19. Returns a list of random words of fixed length.
def randwordlist(NoOfElements: int, wordLength: int = 5) -> List[str]:
    """
    Generate a list of random words.

    :param NoOfElements: Number of words.
    :param wordLength: Length of each word.
    :return: List of random words.
    """
    return [randword(wordLength) for _ in range(NoOfElements)]

# 20. Returns a dictionary with random integer keys and random string values.
def randdictkeys(NoOfElements: int, Start: int = 0, End: int = 100, strLength: int = 5) -> Dict[int, str]:
    """
    Generate a dictionary with random integer keys and random string values.

    :param NoOfElements: Number of key-value pairs.
    :param Start: Lower bound for integer keys (inclusive).
    :param End: Upper bound for integer keys (inclusive).
    :param strLength: Length of the random string values.
    :return: Dictionary with random keys and values.
    """
    return {random.randint(Start, End): randstring(strLength) for _ in range(NoOfElements)}

# 21. Returns a tuple of sets, each with random integers.
def randtupleofsets(NoOfElements: int, setSize: int, Start: int = 0, End: int = 100) -> Tuple[Set[int], ...]:
    """
    Generate a tuple containing sets of random integers.

    :param NoOfElements: Number of sets.
    :param setSize: Number of integers in each set.
    :param Start: Lower bound for integers (inclusive).
    :param End: Upper bound for integers (inclusive).
    :return: Tuple of sets with random integers.
    """
    return tuple(randset(setSize, Start, End) for _ in range(NoOfElements))

# 22. Returns a 2D list (list of lists) of random integers.
def rand2dlist(NoOfElements: int, innerLength: int, Start: int = 0, End: int = 100) -> List[List[int]]:
    """
    Generate a 2D list of random integers.

    :param NoOfElements: Number of sublists.
    :param innerLength: Number of integers in each sublist.
    :param Start: Lower bound for integers (inclusive).
    :param End: Upper bound for integers (inclusive).
    :return: 2D list of random integers.
    """
    return [randlist(innerLength, Start, End) for _ in range(NoOfElements)]

# 23. Returns a nested dictionary with specified depth and breadth.
def randnesteddict(depth: int, breadth: int, Start: int = 0, End: int = 100) -> Dict[str, Any]:
    """
    Generate a nested dictionary with specified depth and breadth.

    :param depth: Depth of nesting.
    :param breadth: Number of key-value pairs at each level.
    :param Start: Lower bound for integer values (inclusive).
    :param End: Upper bound for integer values (inclusive).
    :return: Nested dictionary.
    """
    if depth == 0:
        return random.randint(Start, End)
    return {randstring(3): randnesteddict(depth - 1, breadth, Start, End) for _ in range(breadth)}

# 24. Returns a random datetime between two years.
def randdatetime(StartYear: int = 2000, EndYear: int = 2025) -> datetime.datetime:
    """
    Generate a random datetime object.

    :param StartYear: Starting year.
    :param EndYear: Ending year.
    :return: Random datetime.
    """
    year = random.randint(StartYear, EndYear)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return datetime.datetime(year, month, day, hour, minute, second)

# 25. Returns a list using a custom function to generate each element.
def randcustomlist(NoOfElements: int, customFunc: Callable[[], Any]) -> List[Any]:
    """
    Generate a list where each element is produced by a custom function.

    :param NoOfElements: Number of elements.
    :param customFunc: Function to generate each element.
    :return: List of elements generated by customFunc.
    """
    return [customFunc() for _ in range(NoOfElements)]

# 26. Returns a random choice from a sequence.
def randchoice(seq: Sequence[Any]) -> Any:
    """
    Return a random element from the given sequence.

    :param seq: Non-empty sequence of elements.
    :return: Randomly selected element, or None if sequence is empty.
    """
    if not seq:
        return None
    return seq[random.randint(0, len(seq) - 1)]
