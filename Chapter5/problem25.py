import numpy as np
from enum import IntEnum
import sys
import math

sys.setrecursionlimit(3000)

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

res = np.zeros((len(first_line) + 1, 2))

class BackTrack(IntEnum):
    down = 1
    right = 2
    diag = 3
    start = 4

backtrack = np.zeros((len(first_line) + 1, 2), dtype=int)

def middle_edge(top, bottom, left, right, middle):
    res[top, 0] = 0
    for i in range(top + 1, bottom + 1):
        res[i, 0] = res[i-1, 0] + indel_penalty
    for j in range(left + 1, middle + 1):
        res[top, 1] = res[top, 0] + indel_penalty
        for i in range(top + 1, bottom + 1):
            res[i, 1] = max(res[i-1, 1] + indel_penalty,
                 res[i-1, 0] + substitution_costs[(first_line[i-1], second_line[j-1])],
                 res[i, 0] + indel_penalty)
        res[:, 0] = res[:, 1]
    from_source_res = res[:, 0].copy()

    res[bottom, 0] = 0
    for i in range(bottom - 1, top - 1, -1):
        res[i, 0] = res[i+1, 0] + indel_penalty
        backtrack[i, 0] = BackTrack.down
    for j in range(right - 1, middle - 1, -1):
        res[bottom, 1] = res[bottom, 0] + indel_penalty
        backtrack[bottom, 1] = BackTrack.right
        for i in range(bottom - 1, top - 1, -1):
            best_move = max(
                [(res[i+1, 1] + indel_penalty, BackTrack.down),
                 (res[i+1, 0] + substitution_costs[(first_line[i], second_line[j])], BackTrack.diag),
                 (res[i, 0] + indel_penalty, BackTrack.right)], 
                key=lambda x : x[0])
            res[i, 1] = best_move[0]
            backtrack[i, 1] = best_move[1]
        res[:, 0] = res[:, 1]
        backtrack[:, 0] = backtrack[:, 1]
    from_sink_res = res[:, 0]

    mid_column_res = from_source_res + from_sink_res
    mid_node = top + np.argmax(mid_column_res[top : bottom + 1])
    return (mid_node, backtrack[mid_node, 0], mid_column_res[mid_node])

def linear_space_alignment(top, bottom, left, right, alignment):
    if left == right:
        alignment[0] += first_line[top : bottom]
        alignment[1] += '-' * (bottom - top)
        return
    elif top == bottom:
        alignment[0] += '-' * (right - left)
        alignment[1] += second_line[left:right]
        return
    middle = math.floor((left + right) / 2)
    mid_node, mid_edge, max_score = middle_edge(top, bottom, left, right, middle)
    linear_space_alignment(top, mid_node, left, middle, alignment)
    if mid_edge == BackTrack.right:
        alignment[0] += '-'
        alignment[1] += second_line[middle]
    elif mid_edge == BackTrack.down:
        alignment[0] += first_line[mid_node]
        alignment[1] += '-'
    elif mid_edge == BackTrack.diag:
        alignment[0] += first_line[mid_node]
        alignment[1] += second_line[middle]
    if mid_edge == BackTrack.right or mid_edge == BackTrack.diag:
        middle += 1
    if mid_edge == BackTrack.down or mid_edge == BackTrack.diag:
        mid_node += 1
    linear_space_alignment(mid_node, bottom, middle, right, alignment)
    return max_score

alignment = ['', '']
max_score = linear_space_alignment(0, len(first_line), 0, len(second_line), alignment)

with open('output.txt', 'w', encoding='utf8') as f:
    print(int(max_score), file=f)
    print(alignment[0], file=f)
    print(alignment[1], file=f)