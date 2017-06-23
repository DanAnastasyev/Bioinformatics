from itertools import combinations

MASSES = [57, 71, 87, 97, 99, 101, 103, 113, 114, 115, 
          128, 129, 131, 137, 147, 156, 163, 186]

def expand(peptides):
    new_peptides = set()
    for peptide in peptides:
        for mass in MASSES:
            new_peptides.add(peptide + (mass, ))
    return new_peptides

def mass(peptide):
    return sum(peptide)

def get_cyclic_string(string, start_ind, end_ind, include_cycles):
    if end_ind >= len(string):
        return string[start_ind : ] + string[: end_ind % len(string)] if include_cycles else []
    return string[start_ind : end_ind]

def build_cyclospectrums(peptide, include_cycles=False):
    peptide = peptide[1:]
    peptide_spectrum = set()
    for step in range(len(peptide) + 1):
        for i in range(0, len(peptide)):
            peptide_spectrum.add(mass(get_cyclic_string(peptide, i, i + step, include_cycles)))
    return peptide_spectrum

def is_consistent_cyclospectrums(peptide, spectrum):
    peptide_spectrum = build_cyclospectrums(peptide)
    return peptide_spectrum.issubset(spectrum)

def cyclopeptide_sequencing(spectrum):
    peptides = set([tuple([0])])
    parent_mass = spectrum[-1]
    spectrum = set(spectrum)
    while peptides:
        peptides = expand(peptides)
        new_peptides = set()
        for peptide in peptides:
            if mass(peptide) == parent_mass:
                peptide_spectrum = build_cyclospectrums(peptide, True)
                if peptide_spectrum == spectrum:
                    yield peptide
            elif is_consistent_cyclospectrums(peptide, spectrum):
                new_peptides.add(peptide)
        peptides = new_peptides

spectrum = [int(x) for x in open('input.txt', encoding='utf8').read().strip().split(' ')]
with open('output.txt', 'w', encoding='utf8') as f:
    for peptide in cyclopeptide_sequencing(spectrum):
        for peptide_mass in peptide[:-1]:
            if peptide_mass != 0:
                print(peptide_mass, end='-', file=f)
        print(peptide[-1], end=' ', file=f)