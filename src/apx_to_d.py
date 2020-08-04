import math
import signal
from contextlib import contextmanager

from cnf import CNF
from count_exact import count_exact, count_exact_with_timeout
from count_few import count_few
from hashing import append_clauses, generate_hashing


def apx_to_d(F: CNF, delta: float, epsilon: float, s: int, timeout_limit: int):
    n = F.number_of_literals
    # if n / math.log(n, 2) <= 8 / delta:
    #    return count_exact(F)
    t = math.ceil(delta * n / 2.0 + 2.0 * math.log(1 / epsilon, 2))
    a = math.ceil(2 ** (t + (delta * n) / 2))
    # temp_result = count_few(F, a)
    # if temp_result is not None:
    #     return temp_result
    # t = 2
    t = math.ceil(1 / 3 * n / 2.0 + 2.0 * math.log(1.0 / 0.9, 2))
    z_m = 0
    for m in range(1, n - t):
        # z_m = inner_m_loop(F, m, t, a, n, s)
        z_m = inner_m_loop_withtimeout(F, m, t, a, n, s, timeout_limit)
        if z_m is not None:
            return z_m
    return None


def inner_m_loop(F: CNF, m: int, t: int, a: int, n: int, s: int):
    z = 0
    for i in range(2 ** t):
        hashed_clauses = generate_hashing(F, s, m + t, n)
        # print(hashed_clauses)
        if hashed_clauses is not None:
            F_mi = append_clauses(F, hashed_clauses)
        else:
            return None
        z += count_few(F_mi, 4 * a)
        if z is None:
            return None
        if z >= 4 * a:
            return None
    return 2 ** (m * z)


@contextmanager
def timeout(time):
    # Register a function to raise a TimeoutError on the signal.
    signal.signal(signal.SIGALRM, raise_timeout)
    # Schedule the signal to be sent after ``time``.
    signal.alarm(time)

    try:
        yield
    except TimeoutError:
        pass
    finally:
        # Unregister the signal so it won't be triggered
        # if the timeout is not reached.
        signal.signal(signal.SIGALRM, signal.SIG_IGN)


def raise_timeout(signum, frame):
    raise TimeoutError


def inner_m_loop_withtimeout(F: CNF, m: int, t: int, a: int, n: int, s: int, timeout_limit: int):
    z = 0
    for i in range(2 ** t):
        hashed_clauses = None
        with timeout(timeout_limit):
            hashed_clauses = generate_hashing(F, s, m + t, n)

        # some limit to how long the attempt for hashing can be
        # print(hashed_clauses)
        if hashed_clauses is not None:
            F_mi = append_clauses(F, hashed_clauses)
        else:
            return None
        z_i = count_exact_with_timeout(F_mi, timeout_limit)
        if z_i is not None:
            z += z_i
        # print(
        #     "m:{},i:{},t:{},s:{},#C:{}#L:{},z:{}".format(
        #         m, i, t, s, F_mi.number_of_clauses, F_mi.number_of_literals, z
        #     )
        # )
        if z is None:
            return None
        if z >= 4 * a:
            return None
    return 2 ** m * z
