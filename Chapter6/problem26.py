from contextlib import redirect_stdout

with open('input.txt', encoding='utf8') as f:
    p = [int(x) for x in f.readline().strip()[1:-1].split()]

def print_perm(p):
    print('(', end='')
    for pos, i in enumerate(p):
        if i > 0:
            print('+', end='')
        print(i, end=(' ' if pos != len(p) - 1 else ''))
    print(')')

with open('output.txt', 'w', encoding='utf8') as f:
    with redirect_stdout(f):
        for i in range(1, len(p) + 1):
            if p[i-1] != i:
                ind = p.index(i) if i in p else p.index(-i)
                p[i-1 : ind+1] = reversed([-x for x in p[i-1 : ind+1]])
                print_perm(p)
                if p[i-1] == -i:
                    p[i-1] = i
                    print_perm(p)