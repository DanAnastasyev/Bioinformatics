def read_genome(line):
    cycles = line.split(')')
    return [[int(x) for x in cycle[1:].split(' ')] for cycle in cycles if len(cycle) > 0]

with open('input.txt', encoding='utf8') as f:
    gen1 = read_genome(f.readline().strip())
    gen2 = read_genome(f.readline().strip())

graph = {}
def add_edges(gen):
    for cycle in gen:
        for i in range(len(cycle)):
            v_from, v_to = cycle[i-1], -cycle[i]
            if v_from not in graph:
                graph[v_from] = []
            if v_to not in graph:
                graph[v_to] = []
            graph[v_from].append(v_to)
            graph[v_to].append(v_from)

add_edges(gen1)
add_edges(gen2)

def check_cycle(graph, visited, start):
    stack = [(start, None)]
    while stack:
        vertex, prev_vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            if start in graph[vertex] and (prev_vertex != start or graph[vertex].count(start) > 1):
                return True
            stack.extend([(next_vertex, vertex) for next_vertex in graph[vertex] if next_vertex not in visited])
    return False

visited = set()
number_of_cycles = 0
for start in graph:
    if start not in visited:
        number_of_cycles += 1 if check_cycle(graph, visited, start) else 0

print(max(graph) - number_of_cycles)
