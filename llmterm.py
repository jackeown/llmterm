import argparse
from rich import print
from rich.prompt import Prompt
import subprocess

from llms import translateLlama


def translateCommand(description, previous=[]):
    return translateLlama(description)


def proposeCommand(command):
    print(f"Proposed command: '{command}'")
    answer = Prompt.ask("Do you want to run the above command?: ", choices=['y','n'])
    return answer.lower() == 'y'

def proposeRetry():
    answer = Prompt.ask("Do you want to try generating a different command?: ", choices=['y','n'])
    return answer.lower() == 'y'


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("description", help="English description of the command you'd like to run")
    parser.add_argument("-y", "--yes", help="Run the command without asking for confirmation (dangerous)", action="store_true")
    parser.add_argument("--verbose", help="Print the command before running it", action="store_true")

    args = parser.parse_args()

    previousCommands = []
    keepTrying = True
    while keepTrying:
        command = translateCommand(args.description, previousCommands)
        if proposeCommand(command):
            keepTrying = False
            if args.verbose:
                print(f"Running command: '{command}'")

            p = subprocess.run(command, shell=True)

            if args.verbose:
                print(f"Command finished with returncode {p.returncode}")
            
        else:
            previousCommands.append(command)
            keepTrying = proposeRetry()

