import sys

sys.setrecursionlimit(5000)

k = int(input().strip())

cur_node = '0' * (k - 1)
reconstructed_string = []
checked_edges = set()

def reconstruct_string(node, letter, checked_edges, reconstructed_string):
    node = node[1:] + letter
    def check(next_letter):
        if node + next_letter not in checked_edges:
            reconstructed_string.append(next_letter)
            checked_edges.add(node + next_letter)
            if reconstruct_string(node, next_letter, checked_edges, reconstructed_string):
                return True
            else:
                reconstructed_string.pop()
                checked_edges.remove(node + next_letter)
                return False

    if check('0'):
        return True
    if check('1'):
        return True
    return len(checked_edges) == 2 ** k

if reconstruct_string(cur_node, '0', checked_edges, reconstructed_string):
    with open('output.txt', 'w', encoding='utf8') as f:
        print(''.join(reconstructed_string), file=f)