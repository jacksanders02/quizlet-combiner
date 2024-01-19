"""duplicate_handler.py
Handles duplicate terms within a quizlet tsv file
"""

__author__ = "Jack Sanders"
__license__ = "GNU General Public License v3.0"
__version__ = "0.0.1"

import csv
import os.path

import colorama
from colorama import Fore, Style


def main():
    study_set = ""
    while not os.path.exists(f"study-sets/{study_set}.tsv"):
        study_set = input("Enter study set to find duplicates for: ")

    flashcards = {}
    n_loaded = 0
    with open(f"study-sets/{study_set}.tsv", "r") as f:
        reader = csv.reader(f, delimiter='\t')
        for fc in reader:
            term = fc[0].lower().strip()
            definition = fc[1].lower().strip()

            if flashcards.get(term) is None:
                flashcards[term] = []

            flashcards[term].append(definition)
            n_loaded += 1

    print(f"{Fore.GREEN}Loaded {n_loaded} flashcards!{Style.RESET_ALL}\n")
    print("Checking for duplicate terms...")

    n_changes = 0

    duplicate_defs = {}
    for term, defs in flashcards.items():
        if len(defs) > 1:
            n_changes += 1
            print(f"""\nDuplicate term "{term}": Possible definitions {defs}""")
            for definition in defs:
                action = input(f"""Enter new term for definition "{definition}", or type 'del' to delete $ """)
                if action.lower() != 'del':
                    if action.strip() == "":
                        action = term
                    if duplicate_defs.get(definition) is None:
                        duplicate_defs[definition] = [action]
                    else:
                        duplicate_defs[definition].append(action)
        else:
            if duplicate_defs.get(defs[0]) is None:
                duplicate_defs[defs[0]] = [term]
            else:
                duplicate_defs[defs[0]].append(term)

    print("\n\nChecking for duplicate definitions...")
    unique_flashcards = {}
    for definition, terms in duplicate_defs.items():
        if len(terms) > 1:
            n_changes += 1
            print(f"""\nDuplicate definition "{definition}": Possible terms {terms}""")
            for term in terms:
                action = input(f"""Enter new definition for term "{term}", or type 'del' to delete $ """)
                if action.lower() != 'del':
                    if action.strip() == "":
                        action = definition
                    unique_flashcards[term] = action
        else:
            unique_flashcards[terms[0]] = definition

    ufs = [[i[0], i[1]] for i in unique_flashcards.items()]

    if n_changes > 0:
        with open(f"study-sets/{study_set}-unique.tsv", "w") as f:
            csv.writer(f, delimiter='\t').writerows(ufs)
    else:
        print("No duplicates found!")


if __name__ == "__main__":
    colorama.init()
    main()
