import sys
import time

from problem.Problem import Problem
from problem.ProblemParser import ProblemParser
from problem.SolutionWriter import SolutionWriter


def get_output_file_name(minutes, problem_file):
    return "res-{0}-{1}.txt".format(
        str(minutes) + "m" if minutes == 1 or minutes == 5 else "n",
        problem_file.split(".")[0]
    )


def main():
    problem_file = sys.argv[1]
    minutes = int(sys.argv[2])

    problem = Problem(problem_file)

    parser = ProblemParser(problem)
    parser.parse()

    solutions_count = 0
    time_end = time.time() + 60 * minutes
    while time.time() < time_end:
        problem.make_objects()
        if problem.solve():
            solutions_count += 1

    print("Solutions count", solutions_count)
    print("Best: ", problem.best_gg1, problem.best_gg2)
    output_file_name = get_output_file_name(minutes, problem_file)
    writer = SolutionWriter(problem)
    writer.write(output_file_name)


if __name__ == "__main__":
    main()
