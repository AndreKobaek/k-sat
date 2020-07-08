from os import getcwd, listdir, system

# from random import sample

# nodes = [1,2,5]


job_number = 1

generic_job = [
    "#!/bin/bash",
    "#SBATCH --job-name=job",
    "#SBATCH --partition=red",
    "#SBATCH --mem=1G",
    "#SBATCH --nodes=1",
    "#SBATCH --time=10:00:00",
    "#SBATCH --ntasks-per-node=1",
    "#SBATCH --cpus-per-task=1",
    "ml Python",
    "srun hostname",
    "echo " + str(job_number),
]

# "#SBATCH --nodelist=cn{}".format(sample(nodes,1)[0]),
def find_fast_instances():
    number_of_literals = 220
    clause_width = 3
    for number_of_clauses in [25 * 2 ** x for x in range(26)]:
        for i in range(10):
            input_command = "python execute_experiment.py {} {} {} {}".format(
                number_of_literals, number_of_clauses, clause_width, job_number
            )

            with open("commit.job", "w") as job_file:
                job_file.writelines(line + "\n" for line in generic_job)
                job_file.write(input_command)

            system("sbatch commit.job")

            job_number += 1


def find_working_s():
    localpath = getcwd + "/s-experiment/"
    filename = localpath + listdir(localpath)[7]
    for s in [2 ** x for x in range(12)]:
        input_command = "python run_apx_to_d.py {} {} {}".format(s, filename, job_number)

        with open("commit.job", "w") as job_file:
            job_file.writelines(line + "\n" for line in generic_job)
            job_file.write(input_command)

        system("sbatch commit-job")

        job_number += 1
