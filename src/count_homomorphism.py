import signal
from os import killpg, system, setsid
from subprocess import PIPE, Popen, TimeoutExpired
from time import monotonic as timer
from typing import Tuple

output_file = "input/output_graph.txt"

def count_homSub_with_timeout(
    count_type: str, input_pattern: int, input_graph: int, timeout_limit: int, output_file=output_file
) -> Tuple[int, float]:
    query = "./../SubgraphThesis/experiments-build/experiments/experiments  -count-{} -h {} -g {} > {}".format(
        count_type, input_pattern, input_graph, output_file
    )
    start = timer()
    with Popen(query, shell=True, stdout=PIPE, preexec_fn=setsid) as process:
        try:
            output_text = process.communicate(timeout=timeout_limit)[0]
        except TimeoutExpired:
            killpg(process.pid, signal.SIGINT)  # send signal to the process group
            return (-1, 2*timeout_limit)
    time = timer() - start
    res = read_result()
    if res == -1:
        time = timeout_limit*2
    return (res, time)


def count_homSub(count_type: str, input_pattern: int, input_graph: int, output_file=output_file) -> int:
    query_str = "./../SubgraphThesis/experiments-build/experiments/experiments  -count-{} -h {} -g {} > {}".format(
        count_type, input_pattern, input_graph, output_file
    )
    system(query_str)
    return read_result()


def read_result(output_file=output_file) -> int:
    with open(output_file, "r") as exactCount:
        resultLines = exactCount.readlines()
    try:
        return int(resultLines[0])
    except:
        return -1
