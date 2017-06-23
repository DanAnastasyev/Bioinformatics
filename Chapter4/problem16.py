codon_table = {
    'TTT':'F', 'CTT':'L', 'ATT':'I', 'GTT':'V', 'TTC':'F', 'CTC':'L', 'ATC':'I', 'GTC':'V', 'TTA':'L', 
    'CTA':'L', 'ATA':'I', 'GTA':'V', 'TTG':'L', 'CTG':'L', 'ATG':'M', 'GTG':'V', 'TCT':'S', 'CCT':'P', 
    'ACT':'T', 'GCT':'A', 'TCC':'S', 'CCC':'P', 'ACC':'T', 'GCC':'A', 'TCA':'S', 'CCA':'P', 'ACA':'T', 
    'GCA':'A', 'TCG':'S', 'CCG':'P', 'ACG':'T', 'GCG':'A', 'TAT':'Y', 'CAT':'H', 'AAT':'N', 'GAT':'D', 
    'TAC':'Y', 'CAC':'H', 'AAC':'N', 'GAC':'D', 'TAA':'X', 'CAA':'Q', 'AAA':'K', 'GAA':'E', 'TAG':'X', 
    'CAG':'Q', 'AAG':'K', 'GAG':'E', 'TGT':'C', 'CGT':'R', 'AGT':'S', 'GGT':'G', 'TGC':'C', 'CGC':'R', 
    'AGC':'S', 'GGC':'G', 'TGA':'X', 'CGA':'R', 'AGA':'R', 'GGA':'G', 'TGG':'W', 'CGG':'R', 'AGG':'R', 'GGG':'G'
}

reverse_complement_mapping = {'A' : 'T', 'T' : 'A', 'G' : 'C', 'C' : 'G'}

def translate(dna):
    peptide = []
    for i in range(0, len(dna), 3):
        peptide.append(codon_table[dna[i : i + 3]])
    return ''.join(peptide)

def collect_substrings(dna, peptide):
    substrings_coords = []
    for i in range(0, len(dna) - step + 1, 3):
        if translate(dna[i : i + step]) == peptide:
            substrings_coords.append(i)
    return substrings_coords

with open('input.txt', encoding='utf8') as f, open('output.txt', 'w', encoding='utf8') as f1:
    dna = f.readline().strip()
    peptide = f.readline().strip()
    step = len(peptide) * 3
    substrings_coords = set()
    for i in range(3):
        substrings_coords |= set(x + i for x in collect_substrings(dna[i:], peptide))
    reverse_complement_dna = ''.join([reverse_complement_mapping[char] for char in dna[::-1]])
    for i in range(3):
        substrings_coords |= set(len(dna) - (step + x + i) 
            for x in collect_substrings(reverse_complement_dna[i:], peptide))
    for coord in substrings_coords:
        print(dna[coord : coord + step], file=f1)
