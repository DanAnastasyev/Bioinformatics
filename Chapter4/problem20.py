from collections import Counter

def collect_top_elements(spectrum, M):
    differencies = Counter()
    for first_mass in spectrum:
        for second_mass in spectrum:
            difference = first_mass - second_mass
            if 57 <= difference <= 200:
                differencies[difference] += 1
    top_elements = list(differencies.most_common(M))
    last_element_count = top_elements[-1][1]
    top_elements = [pair[0] for pair in top_elements]
    for pair in differencies.most_common():
        if pair[1] == last_element_count:
            top_elements.append(pair[0])
        elif pair[1] < last_element_count:
            break
    return top_elements

def expand(peptides, top_masses):
    new_peptides = set()
    for peptide in peptides:
        for mass in top_masses:
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
    known_spectrum = spectrum[:]
    peptide_spectrum = build_cyclospectrums(peptide, include_cycles)
    score = 0
    for x in peptide_spectrum:
        if x in known_spectrum:
            score += 1
            known_spectrum.remove(x)
    return score

def cut_leaderboard(leaderboard, N):
    leaderboard = sorted(leaderboard, key=lambda x : x[1], reverse=True)
    return leaderboard[:N] + [x for x in leaderboard[N:] if x[1] == leaderboard[N][1]]

def cyclopeptide_sequencing(spectrum, top_masses, N):
    leader_peptide = (0, )
    leader_peptide_score = 1
    leaderboard = set([leader_peptide])
    parent_mass = max(spectrum)
    while leaderboard:
        leaderboard = expand(leaderboard, top_masses)
        new_leaderboard = []
        for peptide in leaderboard:
            peptide_score = calc_score(peptide, spectrum)
            if mass(peptide) == parent_mass:
                peptide_score_cyclic = calc_score(peptide, spectrum, True)
                if peptide_score_cyclic > leader_peptide_score:
                    leader_peptide = peptide
                    leader_peptide_score = peptide_score_cyclic
            elif mass(peptide) > parent_mass:
                continue
            new_leaderboard.append((peptide, peptide_score))
        new_leaderboard = cut_leaderboard(new_leaderboard, N)
        leaderboard = set(pair[0] for pair in new_leaderboard)
    return leader_peptide

with open('input.txt', encoding='utf8') as f:
    M = int(f.readline().strip())
    N = int(f.readline().strip())
    spectrum = [int(x) for x in f.readline().strip().split(' ')]

top_masses = collect_top_elements(spectrum, M)
peptide = cyclopeptide_sequencing(spectrum, top_masses, N)
with open('output.txt', 'w', encoding='utf8') as f:
    for peptide_mass in peptide[:-1]:
        if peptide_mass != 0:
            print(peptide_mass, end='-', file=f)
    print(peptide[-1], end=' ', file=f)