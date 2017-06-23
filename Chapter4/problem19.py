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
    if end_ind > len(string):
        return string[start_ind : ] + string[: end_ind % len(string)] if include_cycles else []
    return string[start_ind : end_ind]

def build_cyclospectrums(peptide, include_cycles):
    peptide = peptide[1:]
    peptide_spectrum = set()
    for step in range(len(peptide) + 1):
        for i in range(0, len(peptide)):
            peptide_spectrum.add(mass(get_cyclic_string(peptide, i, i + step, include_cycles)))
    return peptide_spectrum

def calc_score(peptide, spectrum, include_cycles=False):
    peptide_spectrum = build_cyclospectrums(peptide, include_cycles)
    return len(peptide_spectrum.intersection(spectrum))

def cut_leaderboard(leaderboard, N):
    leaderboard = sorted(leaderboard, key=lambda x : x[1], reverse=True)
    return leaderboard[:N]

def cyclopeptide_sequencing(spectrum, N):
    leader_peptide = (0, )
    leader_peptide_score = 1
    leaderboard = set([leader_peptide])
    parent_mass = spectrum[-1]
    spectrum = set(spectrum)
    while leaderboard:
        leaderboard = expand(leaderboard)
        new_leaderboard = []
        for peptide in leaderboard:
            peptide_score = calc_score(peptide, spectrum, True)
            if mass(peptide) == parent_mass:
                if peptide_score > leader_peptide_score:
                    leader_peptide = peptide
                    leader_peptide_score = peptide_score
            elif mass(peptide) > parent_mass:
                continue
            new_leaderboard.append((peptide, peptide_score))
        new_leaderboard = cut_leaderboard(new_leaderboard, N)
        leaderboard = set(pair[0] for pair in new_leaderboard)
    return leader_peptide

with open('input.txt', encoding='utf8') as f:
    N = int(f.readline().strip())
    spectrum = [int(x) for x in f.readline().strip().split(' ')]
with open('output.txt', 'w', encoding='utf8') as f:
    peptide = cyclopeptide_sequencing(spectrum, N)
    for peptide_mass in peptide[:-1]:
        if peptide_mass != 0:
            print(peptide_mass, end='-', file=f)
    print(peptide[-1], end=' ', file=f)