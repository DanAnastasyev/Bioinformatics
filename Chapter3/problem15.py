with open('input.txt', encoding='utf8') as f:
    k, d = [int(x) for x in f.readline().strip().split()]
    graph = {}
    from_nodes = set()
    to_nodes = set()
    for kmer_pair in f:
        kmer1, kmer2 = kmer_pair.strip().split('|')
        node_from, node_to = kmer1[:-1] + kmer2[:-1], kmer1[1:] + kmer2[1:]
        from_nodes.add(node_from)
        to_nodes.add(node_to)
        if node_from not in graph:
            graph[node_from] = []
        graph[node_from].append(node_to)

start_node = next(iter(from_nodes - to_nodes))

reconstructed_string_head = start_node[:k - 1]
reconstructed_string_tail = start_node[k - 1:]
cur_node = start_node
while cur_node in graph:
    cur_node = graph[cur_node].pop()
    reconstructed_string_head += cur_node[k - 2]
    reconstructed_string_tail += cur_node[-1]

with open('output.txt', 'w', encoding='utf8') as f:
    print(reconstructed_string_head + reconstructed_string_tail[-(d + k):], file=f)