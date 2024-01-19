"""main.py
Acts as the entrypoint for the quizlet combiner program.
"""

__author__ = "Jack Sanders"
__license__ = "GNU General Public License v3.0"
__version__ = "0.0.1"

import csv

import colorama
from colorama import Fore, Style

ANOTHER_PROMPT = "Add another study set? [Y/N] $ "


def get_study_set() -> list[list[str]]:
    """
    Grabs unlimited lines of text from standard input
    :return: a list, with each line of input being an list of the form [term, definition]
    """
    print("Paste a quizlet study set below (export from quizlet with default settings), and hit enter twice to confirm.")

    study_set = []

    data_in = input()
    while len(data_in.strip()) != 0:
        study_set.append(data_in.split("\t"))
        data_in = input()

    return study_set


def main():
    next_study_set = get_study_set()
    all_lines = next_study_set

    print(f"Study set added! Total number of flashcards: {Fore.GREEN}{len(all_lines)}{Style.RESET_ALL}")
    add_another = input(ANOTHER_PROMPT)

    while add_another.lower().startswith("y"):
        next_study_set = get_study_set()
        all_lines += next_study_set

        print(f"Study set added! Total number of flashcards: {Fore.GREEN}{len(all_lines)}{Style.RESET_ALL}")
        add_another = input(ANOTHER_PROMPT)

    file_name = input("Enter name of combined study set: ")

    with open(f"study-sets/{file_name}.tsv", "w") as f:
        csv.writer(f, delimiter='\t').writerows(all_lines)

    print(f"Combined study set saved to study-sets/{file_name}.tsv!")


if __name__ == "__main__":
    colorama.init()
    main()
