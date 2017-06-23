def read_genome(line):
    genome_cycles = line.split(')')
    return [[int(x) for x in cur_cycle[1:].split(' ')] for cur_cycle in genome_cycles if len(cur_cycle) > 0]

with open('input.txt', encoding='utf8') as f:
    gen = read_genome(f.readline().strip())
    i1, i2, j1, j2 = [int(x) for x in f.readline().strip().split(', ')]

graph = {}
def chromosome_to_cycle(chromosome):
    nodes = []
    for j in range(len(chromosome)):
        i = chromosome[j]
        if i > 0:
            nodes.append(2 * i - 1)
            nodes.append(2 * i)
        else:
            nodes.append(-2 * i)
            nodes.append(-2 * i - 1)
    return nodes

def add_colored_edges(gen):
    for chromosome in gen:
        nodes = chromosome_to_cycle(chromosome)
        for i in range(len(chromosome)):
            if nodes[2 * i - 1] not in graph:
                graph[nodes[2 * i - 1]] = []
            if nodes[2 * i] not in graph:
                graph[nodes[2 * i]] = []
            graph[nodes[2 * i - 1]].append(nodes[2 * i])
            graph[nodes[2 * i]].append(nodes[2 * i - 1])

def add_black_edges(gen):
    number_of_nodes = max(graph) // 2
    for i in range(1, number_of_nodes + 1):
        graph[2 * i - 1].append(2 * i)
        graph[2 * i].append(2 * i - 1)

def remove_edge(i, j):
    graph[i].remove(j)
    graph[j].remove(i)

def add_edge(i, j):
    graph[i].append(j)
    graph[j].append(i)

add_colored_edges(gen)
add_black_edges(gen)

remove_edge(i1, i2)
remove_edge(j1, j2)
add_edge(i1, j1)
add_edge(i2, j2)

def find_cycle(graph, start):
    stack = [(start, [start])]
    while stack:
        vertex, path = stack.pop()
        for next_vertex in graph[vertex]:
            if next_vertex == start and (path[-2] != next_vertex or graph[vertex].count(next_vertex) > 1):
                return path
            if next_vertex in path:
                continue
            stack.append((next_vertex, path + [next_vertex]))

visited = set()
cycles = []
for start in graph:
    if start not in visited:
        cycle = find_cycle(graph, start)
        if cycle:
            cycles.append(cycle)
            visited |= set(cycles[-1])

def cycle_to_chromosome(cycle):
    res = '('
    for i in range(len(cycle) // 2):
        if cycle[i * 2] < cycle[i * 2 + 1]:
            res += '+' + str(cycle[i * 2 + 1] // 2)
        else:
            res += str(-cycle[i * 2] // 2)
        res += ' ' if i < len(cycle) // 2 - 1 else ''
    return res + ')'

def graph_to_genome(cycles):
    gen_cycles = set()
    for cycle in cycles:
        gen_cycles.add(cycle_to_chromosome(cycle))
    with open('output.txt', 'w', encoding='utf8') as f:
        for gen in gen_cycles:
            print(gen, end = ' ', file=f)

graph_to_genome(cycles)