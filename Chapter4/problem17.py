from collections import Counter
import math

MASSES = [57, 71, 87, 97, 99, 101, 103, 113, 114, 115, 
          128, 129, 131, 137, 147, 156, 163, 186]

m = int(input().strip())

def count_peptide_permutations(peptide):
    counter = Counter(peptide)
    denominator = 1
    for el in counter:
        denominator *= math.factorial(counter[el])
    return int(math.factorial(len(peptide)) / denominator)

def count_peptides(mass, used_masses, peptide):
    if mass == 0:
        return count_peptide_permutations(peptide)
    if mass < 0 or used_masses < 0:
        return 0
    return count_peptides(mass, used_masses - 1, peptide) + \
            count_peptides(mass - MASSES[used_masses], used_masses, peptide + [used_masses])

print(count_peptides(m, len(MASSES) - 1, []))