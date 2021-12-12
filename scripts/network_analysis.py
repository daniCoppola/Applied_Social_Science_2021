from pprint import pprint

import networkx as nx
from pathlib import Path
import statistics
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
import json


def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))


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


def reverse(domain):
    url_list = domain.split('.')
    url_list.reverse()
    domain_reversed = '.'.join(url_list)
    return domain_reversed


def get_leaning(domain, leanings):
    # list of list [0] domain [1] leaning
    for l in leanings:
        if domain == l[0] or domain == reverse(l[0]):
            try:
                return float(l[1])
            except Exception as e:
                print(f"{l[1]} not float, {domain}")
    return -15


def filter_domains(G):
    domains_path = root / "input_files" / "domains"
    with open(domains_path) as f:
        domains = f.readlines()
    domains = [x.strip() for x in domains]
    for n in dict(G.nodes):
        if G.nodes[n]['domain'] not in domains and reverse(G.nodes[n]['domain']) not in domains:
            print(G.nodes[n]['domain'])
            G.remove_node(n)


def add_domains_label(G):
    path_to_leaning = root / "input_files" / "domains.tsv"
    with open(path_to_leaning) as f:
        leanings = f.readlines()
    leanings = leanings[1:]
    leanings = [x.split("\t")[:2] for x in leanings]

    path_to_nodes = root / "input_files" / "filtered_nodes"
    with open(path_to_nodes) as f:
        lines = f.readlines()
    lines = [x.split("\t")[:2] for x in lines]  # [id, domain]
    dic_attribute = {}
    for x in lines:
        dic_attribute[x[0]] = {"domain": x[1], "leaning": get_leaning(x[1], leanings)}
        if dic_attribute[x[0]] == -15 and x[0] in G.nodes:
            print(f"Removing\t{x[0]}\t{x[1]}")
            G.remove_node(x[0])

    # dic_attribute = {x[0]: {"domain": x[1]} for x in lines}
    nx.set_node_attributes(G, dic_attribute)


def load_gefx(path_to_graph):
    G = nx.read_gexf(path_to_graph)
    return G


def plot_degree_hist(G):
    sns.set_theme()
    x = list(dict(G.degree(G.nodes())).values())
    # x.sort()
    # x = x[:-200]
    n, bins, patches = plt.hist(x, 50)
    plt.xlabel('Degrees')
    plt.ylabel('Count')
    plt.title('Degrees of the domains')
    # plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
    # plt.xlim(40, 160)
    # plt.ylim(0, 0.03)
    plt.grid(True)
    plt.show()


def plot_leanings_not_in_score():
    path = root / "output_files" / "leanings_not_in_core.txt"
    with open(path) as f:
        lines = f.readlines()
    leanings = [float(x.split()[1].strip("\n")) for x in lines]
    norm = NormalizeData(np.array(leanings))
    ax = sns.distplot(norm, kde=True)
    ax.set_title("Leanings of domains NOT in the 200 core")
    ax.set_xlabel("Leanings")
    plt.show()
    input("Press any key to close")


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


def order_edges():
    path = root / "input_files" / "filtered_edges"
    o_path = root / "output_files" / "tmp_ordered_filtered_edges"
    with open(path, 'r') as f:
        lines = f.readlines()
    ordered = []
    for line in lines:
        line_list = [x.strip() for x in line.split("\t")]
        line_list.sort()
        ordered.append("\t".join(line_list) + '\n')
    with open(o_path, 'w') as f:
        f.writelines(ordered)


def extract_core(G, k, path):
    core = nx.k_core(G, k)
    analyze_graph(core)
    nx.write_gexf(core, path)


def in_core(d1, domains_in_core):
    for d2 in domains_in_core:
        if d1 == d2 or d1 == reverse(d2):
            return True
    return False


def distribution_leaning_non_200_k(domains_in_core):
    path_to_leaning = root / "input_files" / "domains.tsv"
    with open(path_to_leaning) as f:
        leanings = f.readlines()
    leanings = leanings[1:]
    leanings = [x.split("\t")[:2] for x in leanings]
    domains_not_in_core = {}
    for l in leanings:
        if not in_core(l[0], domains_in_core):
            domains_not_in_core[l[0]] = float(l[1])
    lines = [x + " " + str(domains_not_in_core[x]) + "\n" for x in domains_not_in_core.keys()]
    output = root / "output_files" / "leanings_not_in_core.txt"
    with open(output, "w") as f:
        f.writelines(lines)


def write_nodes_list(path_to_news_node, casted):
    with open(path_to_news_node, "w") as f:
        f.write("id,domain,leaning\n")
        for x in casted.nodes:
            f.write(str(x) + "," + casted.nodes[x]['domain'] + "," + str(-casted.nodes[x]['leaning'])+'\n')

def add_normalized_label():
    pass

def main():
    path_to_full_graph = root / "input_files" / "filtered_edges"
    path_to_main_core_graph = root / "output_files" / "main_core.edg"
    path_to_main_core_gexf = root / "input_files" / "main_core_with_attributes.gexf"
    path_to_reciprocated = root / "input_files" / "reciprocated_edges"
    path_to_reciprocated_core = root / "input_files" / "reciprocated_core.gexf"
    path_to_reciprocated_k_core = root / "output_files" / "200_core.graphml"
    path_to_k_core_labelled = root / "input_files" / "reciprocated_200_core_labelled.gexf"

    path_to_full = root / "output_files" / "full.csv"
    path_to_full_attributes = root / "output_files" / "full_attributes.json"
    path_to_full_ml = root / "output_files" / "full.graphml"
    path_to_news_edg = root / "output_files" / "news_edges.csv"
    path_to_news_node = root / "output_files" / "news_nodes.csv"
    path_to_news_graph_ml = root / "output_files" / "news.graphml"
    G = nx.read_graphml(path_to_news_graph_ml)
    analyze_graph(G)



if __name__ == "__main__":
    main()
    # plot_leanings_not_in_score()
    # order_edges()
