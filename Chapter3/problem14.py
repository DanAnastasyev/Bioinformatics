with open('input.txt', encoding='utf8') as f:
    out_nodes = {}
    in_nodes = {}
    for kmer in f:
        kmer = kmer.strip()
        node_from, node_to = kmer[:-1], kmer[1:]
        if node_from not in out_nodes:
            out_nodes[node_from] = []
        if node_to not in in_nodes:
            in_nodes[node_to] = []
        out_nodes[node_from].append(node_to)
        in_nodes[node_to].append(node_from)

k = len(next(iter(out_nodes))) + 1

non_branching_nodes = set(node for node in set(out_nodes.keys()) & set(in_nodes.keys()) 
                          if len(out_nodes[node]) == 1 and len(in_nodes[node]) == 1)

def build_contig(from_node, to_node, out_file):
    contig = from_node + to_node[-1]
    while to_node in non_branching_nodes:
        to_node = out_nodes[to_node][0] if to_node in out_nodes else ''
        contig += to_node[-1]
    print(contig, file=out_file)

start_nodes = set(out_nodes.keys()) - non_branching_nodes

with open('output.txt', 'w', encoding='utf8') as f:
    for from_node in start_nodes:
        for to_node in out_nodes[from_node]:
            build_contig(from_node, to_node, f)