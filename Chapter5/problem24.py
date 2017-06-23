import numpy as np
from enum import IntEnum
import sys

substitution_costs = {}
with open('substitution_matrix.txt', encoding='utf8') as f:
    letters = [x.strip() for x in f.readline().strip().split(' ') if len(x.strip()) != 0]
    for line in f:
        from_letter = line[0]
        line = line[1:].strip()
        costs = [int(x.strip()) for x in line.split(' ') if len(x.strip()) != 0]
        for to_letter, cost in zip(letters, costs):
            substitution_costs[(from_letter, to_letter)] = cost

indel_penalty = -5

with open('input.txt', encoding='utf8') as f:
    first_line = f.readline().strip()
    second_line = f.readline().strip()

n = len(first_line) + 1
m = len(second_line) + 1

res = np.zeros((n, m), dtype=int)

class BackTrack(IntEnum):
    down = 1
    left = 2
    diag = 3
    start = 4

backtrack = np.zeros((n, m), dtype=int)

for i in range(1, n):
    res[i, 0] = res[i-1, 0] + indel_penalty
    backtrack[i, 0] = BackTrack.down
for j in range(1, m):
    res[0, j] = res[0, j-1] + indel_penalty
    backtrack[0, j] = BackTrack.left

for i in range(1, n):
    for j in range(1, m):
        best_move = max([(0, BackTrack.start),
            (res[i-1, j] + indel_penalty, BackTrack.down),
            (res[i-1, j-1] + substitution_costs[(first_line[i-1], second_line[j-1])], BackTrack.diag),
            (res[i, j-1] + indel_penalty, BackTrack.left)], key=lambda x : x[0])
        res[i, j] = best_move[0]
        backtrack[i, j] = best_move[1]

def print_alignment(backtrack, i, j, alignment):
    while i >= 0 and j >= 0:
        if backtrack[i, j] == BackTrack.start:
            break
        elif backtrack[i, j] == BackTrack.diag:
            alignment[0] += first_line[i-1]
            alignment[1] += second_line[j-1]
            i -= 1
            j -= 1
        elif backtrack[i, j] == BackTrack.down:
            alignment[0] += first_line[i-1]
            alignment[1] += '-'
            i -= 1
        elif backtrack[i, j] == BackTrack.left:
            alignment[0] += '-'
            alignment[1] += second_line[j-1]
            j -= 1
        else:
            break
    alignment[0], alignment[1] = alignment[0][::-1], alignment[1][::-1]

best_i, best_j = np.unravel_index(np.argmax(res), res.shape)

alignment = ['', '']
print_alignment(backtrack, best_i, best_j, alignment)
with open('output.txt', 'w', encoding='utf8') as f:
    print(np.max(res), file=f)
    print(alignment[0], file=f)
    print(alignment[1], file=f)