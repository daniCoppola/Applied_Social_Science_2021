#! /usr/python3
import sys

domain_leaning_path = "../input_files/domains.tsv"
nodes_filtered_path = "../input_files/filtered_nodes.txt"


def read_tzv():
    with open(domain_leaning_path, 'r') as f:
        domains = [line.split()[0] for line in f.readlines()][1:]
        reverse_domains = []
        for domain in domains:
            url_list = domain.split('.')
            url_list.reverse()
            domain_reversed = '.'.join(url_list)
            reverse_domains.append(domain_reversed)
        # print(domains)
    return sorted(domains + reverse_domains)


def read_nodes():
    with open(nodes_filtered_path, 'r') as f:
        nodes = [int(line.strip()) for line in f.readlines()]
        # print(domains)
    return sorted(nodes)


def bin_search(arr, low, high, x):
    if high >= low:
        mid = (high + low) // 2
        if arr[mid] == x:
            return mid
        elif arr[mid] > x:
            return bin_search(arr, low, mid - 1, x)
        else:
            return bin_search(arr, mid + 1, high, x)
    else:
        return -1


def read_common_crawls():
    common_crawl_domains = []
    for line in sys.stdin:
        id = line.split("\t")[0]
        domain = line.split("\t")[1]
        common_crawl_domains.append(domain)
    return common_crawl_domains


def main():
    domains = read_tzv()
    common_crawl_domains = read_common_crawls()
    print(f"N of domains in ccrawl:{len(common_crawl_domains)}")
    print(f"N of domains in domains:{len(domains)}")
    leaning_not_in_crawl = [x + "\n" for x in domains if x not in common_crawl_domains]
    with open("../output_files/crawl_not_in_leaning.txt", "w") as f:
        f.writelines(leaning_not_in_crawl)


# gunzip -c edges.txt.gz | python3 filter.py edges| gzip > filtered_edges.gz

if __name__ == "__main__":
    main()
