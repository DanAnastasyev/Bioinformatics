import numpy as np

with open('input.txt', encoding='utf8') as f:
    n, m = [int(x) for x in f.readline().strip().split()]
    down = [[int(x) for x in f.readline().strip().split()] for _ in range(n)]
    f.readline()
    right = [[int(x) for x in f.readline().strip().split()] for _ in range(n+1)]

res = np.zeros((n + 1, m + 1), dtype=int)
for i in range(1, n + 1):
    res[i, 0] = res[i-1, 0] + down[i-1][0]

for j in range(1, m + 1):
    res[0, j] = res[0, j-1] + right[0][j-1]

for i in range(1, n + 1):
    for j in range(1, m + 1):
        res[i, j] = max(res[i-1, j] + down[i-1][j], res[i, j-1] + right[i][j-1])

print(res[n, m])