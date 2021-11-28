import networkx as nx
from pathlib import Path
import statistics

root = Path(__file__).parent.parent


def analyze_graph(path_to_graph):
    G = nx.read_edgelist(path_to_graph)
    print(nx.info(G))
    degree_dict = dict(G.degree(G.nodes()))
    max_deg = max(degree_dict.values())
    min_deg = min(degree_dict.values())

    print(f"Max degree: {max_deg}")
    print(f"Min degree: {min_deg}")
    print(f"Avg degree: {statistics.mean(degree_dict.values())}")


def get_main_K_core(G):
    return nx.k_core(G)


def main():
    path_to_full_graph = root / "input_files" / "filtered_edges"
    path_to_main_core_graph = root / "output_files" / "main_core.edg"
    analyze_graph(path_to_main_core_graph)

if __name__ == "__main__":
    main()
