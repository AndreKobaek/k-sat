import signal
from contextlib import contextmanager
from multiprocessing import Process
from os import getcwd
from time import sleep

from cnf_generator import generate_cnf
from cnf_io import write_cnf_file
from count_exact import count_exact
from count_few import query_solver

number_of_literals = 220
clause_width = 3


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


def bin_search_best_value_of_m(n):
    for m in [2 ** x for x in range(11)]:
        for i in range(100):
            F = generate_cnf(n, clause_width, m)

            if query_solver(F):
                break
            # else:
            #     # write file to disk
            #     filename = "cnf-gen-L{}-W{}-C{}-I{}.cnf".format(
            #         F.number_of_literals, clause_width, F.number_of_clauses, i
            #     )
            #     write_filename = "{}/generated-input-bin_search/{}".format(getcwd(), filename)
            #     write_cnf_file(F, write_filename)
        if i == 99:
            return print("m_upper = {}".format(m))


# m_upper = 1024 3/4 2**10
# bin_search_best_value_of_m(number_of_literals)


def bin_search(n: int, m_upper: int, timeout_limit: int, target_num_solutions: int) -> int:
    m_lower = 768

    while True:
        print("m_upper: {}, m_lower {}".format(m_upper, m_lower))
        if abs(m_lower - m_upper) < 2:
            return -1
        m = m_lower + ((m_upper - m_lower) // 2)
        num_sol_list = list()
        num_sol_list.append(0)
        for i in range(100):
            print(
                "m_upper: {}, m_lower {}, m: {}, i: {}, last_sol: {}".format(m_upper, m_lower, m, i, num_sol_list[-1])
            )
            F = generate_cnf(n, clause_width, m)
            timed_out = True
            with timeout(timeout_limit):
                num_sol_list.append(count_exact(F))
                timed_out = False
            if timed_out:
                break
        if timed_out:
            m_lower = m
        elif instances_in_range(num_sol_list, target_num_solutions) > 60:
            return m
        elif sum(num_sol_list) / (len(num_sol_list)) > target_num_solutions:
            m_lower = m
        else:
            m_upper = m


def linear_search(n: int, m_lower: int, m_upper: int, maximum_num_sols: int, iterations: int):
    for m in range(m_lower, m_upper):
        num_sol_list = [0]
        for i in range(iterations):
            F = generate_cnf(n, clause_width, m)
            num_sol = count_exact(F)
            num_sol_list.append(num_sol)
            if 0 < num_sol <= maximum_num_sols:
                # write file to disk
                filename = "cnf-gen-L{}-W{}-C{}-I{}-S{}.cnf".format(
                    F.number_of_literals, clause_width, F.number_of_clauses, i, num_sol
                )
                write_filename = "{}/generated-input-bin_search/{}".format(getcwd(), filename)
                write_cnf_file(F, write_filename)
                return num_sol
        print(
            "n: {}, m: {}, sols_in_range: {}".format(
                n, m, len([1 for x in num_sol_list if 0 < x <= maximum_num_sols])
            )
        )


def instances_in_range(num_sol_list: list(), target_num_solutions: int):
    lower_bound = target_num_solutions // 2
    upper_bound = target_num_solutions * 2
    a = len([1 for x in num_sol_list if lower_bound <= x <= upper_bound * 2])
    print("lb: {}, ub: {}, sols: {}".format(lower_bound, upper_bound, a))
    return a


def generate_instances(target_num_solutions: int, number_of_literals: int, clause_width: int, number_of_clauses: int):
    generated_cnfs = 0
    while generated_cnfs < 200:
        F = generate_cnf(number_of_literals, clause_width, number_of_clauses)
        num_sol = count_exact(F)
        if 0 < num_sol <= target_num_solutions:
            # write file to disk
            filename = "cnf-gen-L{}-W{}-C{}-S{}.cnf".format(
                F.number_of_literals, clause_width, F.number_of_clauses, num_sol
            )
            write_filename = "{}/generated-input-bin_search/{}".format(getcwd(), filename)
            write_cnf_file(F, write_filename)
            generated_cnfs += 1


# print(bin_search(number_of_literals, 1024, 60, 1000))
# linear_search(number_of_literals, 965, 990, 20000, 50)
generate_instances(400, number_of_literals, clause_width, 969)
