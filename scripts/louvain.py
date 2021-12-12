import statistics
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from pathlib import Path


root = Path(__file__).parent.parent
def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))


def plot_leanings_not_in_score():
    sns.set_theme()
    path = root /"output_files"/"louvain_nodes_normalized"
    with open(path) as f:
        lines = f.readlines()
    louvain_dic = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[]}
    lines = lines[1:]
    for x in lines:
        x = [y.strip().strip('\"') for y in x.split(",")]
        louvain_dic[int(x[1])].append(-float(x[0])+1)

    fig1, ax1 = plt.subplots()
    ax1.set_title("Leanings in different communities")
    ax1.set_xlabel("Community")
    ax1.set_ylabel("Leaning")

    medianprops = dict( linewidth=1.5, color='firebrick')
    bplot = ax1.boxplot([louvain_dic[1], louvain_dic[0], louvain_dic[3], louvain_dic[4],
                         louvain_dic[2]], showfliers=False,patch_artist=True,
                        medianprops=medianprops
                        )
    colors = ["#BEBADA","#80B1D3","#FB8072","#8DD3C7","#FFFFB3"]
    colors.reverse()
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)

    plt.grid(visible=True)

    plt.show()

def plot_leaning_distribution():
    sns.set_theme()
    path = root / "output_files" / "louvain_nodes_normalized"
    with open(path) as f:
        lines = f.readlines()
    leanings = []
    lines = lines[1:]
    for x in lines:
        x = [y.strip().strip('\"') for y in x.split(",")]
        leanings.append(float(x[0]))
    x = leanings
    n, bins, patches = plt.hist(NormalizeData(np.array(x)), 50)
    plt.xlabel('Leaning')
    plt.ylabel('Count')
    plt.title('Leanings of domains')
    # plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
    # plt.xlim(40, 160)
    # plt.ylim(0, 0.03)
    plt.grid(True)
    plt.show()

def normalize():
    path = root / "output_files" / "louvain_nodes"
    out = root / "output_files" / "louvain_nodes_normalized"
    with open(path) as f:
        lines = f.readlines()
    leanings = []
    lines = lines[1:]
    columns = [[],[]]
    for x in lines:
        x = [y.strip().strip('\"') for y in x.split(",")]
        columns[0].append(float(x[0]))
        columns[1].append(x[1])
    normalized = NormalizeData(np.array(columns[0]))
    with open(out, "w") as f:
        for n, r in zip(normalized, columns[1]):
            f.write(f'"{n}","{r}"\n')


plot_leanings_not_in_score()
plot_leaning_distribution()