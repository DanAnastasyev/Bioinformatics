from contextlib import redirect_stdout

with open('input.txt', encoding='utf8') as f:
    p = [int(x) for x in f.readline().strip()[1:-1].split()]

p = [0] + p + [len(p) + 1]

print(sum(1 for i in range(len(p) - 1) if p[i] + 1 != p[i+1]))