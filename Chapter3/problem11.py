with open('input.txt', encoding='utf8') as f:
    k = int(f.readline().strip())
    graph = {}
    from_nodes = set()
    to_nodes = set()
    for kmer in f:
        kmer = kmer.strip()
        node_from, node_to = kmer[:-1], kmer[1:]
        from_nodes.add(node_from)
        to_nodes.add(node_to)
        if node_from not in graph:
            graph[node_from] = []
        graph[node_from].append(node_to)

start_node = next(iter(from_nodes - to_nodes))

reconstructed_string = start_node
cur_node = start_node
while cur_node in graph:
    cur_node = graph[cur_node].pop()
    reconstructed_string += cur_node[-1]

with open('output.txt', 'w', encoding='utf8') as f:
    print(reconstructed_string, file=f)