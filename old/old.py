
def the_algorithm(filename: str, epsilon: float, delta: float, s: int):
    copyInputFile(filename, tempFileName)
    F = read_cnf_file(tempFileName)
    n = F.number_of_literals
    if n / math.log(n, 2) <= 8 / delta:
        return count_few_branching(F)
    t = math.ceil(delta * n / 2.0 + 2.0 * math.log(1 / epsilon, 2))
    a = math.ceil(2 ** (t + (delta * n) / 2))
    try:
        return count_few_branching(F, a)
    except OutOfRunsException:
        z_m = 0
        for m in range(n-t):
            z_m = inner_m_loop(F, m, t, a, n, s)
            if z_m != None:
                return z_m
        return None