from pprint import pprint

import networkx as nx
from pathlib import Path
import statistics
import matplotlib.pyplot as plt

root = Path(__file__).parent.parent


def analyze_graph(G):
    print(nx.info(G))
    degree_dict = dict(G.degree(G.nodes()))
    max_deg = max(degree_dict.values())
    min_deg = min(degree_dict.values())
    plot_degree_hist(G)
    print(f"Max degree: {max_deg}")
    print(f"Min degree: {min_deg}")
    print(f"Avg degree: {statistics.mean(degree_dict.values())}")


def get_main_K_core(G):
    return nx.k_core(G)


def add_domains_label(G):
    path_to_nodes = root / "input_files" / "filtered_nodes"
    with open(path_to_nodes) as f:
        lines = f.readlines()
    lines = [x.split("\t")[:2] for x in lines]  # [id, domain]
    dic_attribute = {x[0]: {"domain": x[1]} for x in lines}
    nx.set_node_attributes(G, dic_attribute)


def load_gefx(path_to_graph):
    G = nx.read_gexf(path_to_graph)
    return G


def plot_degree_hist(G):
    x = dict(G.degree(G.nodes()))
    n, bins, patches = plt.hist(x.values(), 50)
    plt.xlabel('Node degree')
    plt.ylabel('Count')
    plt.title('Histogram of nodes degree')
    # plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
    # plt.xlim(40, 160)
    # plt.ylim(0, 0.03)
    plt.grid(True)
    plt.show()


def analyze_degree(G):
    plot_degree_hist(G)
    degree_dict = dict(G.degree(G.nodes()))
    max_deg = max(degree_dict.values())
    domains_with_max_deg = [G.nodes[n[0]]['domain'] + "\n" for n in degree_dict.items() if n[1] == max_deg]
    path_to_full_graph = root / "output_files" / "nodes_with_max_deg.txt"
    with open(path_to_full_graph, "w") as f:
        f.writelines(domains_with_max_deg)


def is_core_connected_after_removal(G):
    degree_dict = dict(G.degree(G.nodes()))
    max_deg = max(degree_dict.values())
    domains_with_max_deg = [n[0] for n in degree_dict.items() if n[1] > 1820]
    complement = [label for label in list(G.nodes) if label not in domains_with_max_deg]
    H = G.subgraph(complement)
    print(f"Subgraph connected: {nx.is_connected(H)}")


def main():
    path_to_full_graph = root / "input_files" / "filtered_edges"
    path_to_main_core_graph = root / "output_files" / "main_core.edg"
    path_to_main_core_gexf = root / "input_files" / "main_core_with_attributes.gexf"
    G = load_gefx(path_to_main_core_gexf)
    analyze_degree(G)
    #is_core_connected_after_removal(G)


if __name__ == "__main__":
    main()
