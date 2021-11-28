#! /usr/python3
import sys
domain_leaning_path = "../input_files/domains.tsv"
nodes_filtered_path = "../input_files/filtered_nodes.txt"

def read_tzv():
    with open(domain_leaning_path, 'r') as f:
        
        domains = [ line.split()[0] for line in f.readlines()][1:]
        reverse_domains = []
        for domain in domains:
            url_list = domain.split('.')
            url_list.reverse()
            domain_reversed = '.'.join(url_list)
            reverse_domains.append(domain_reversed)
        #print(domains)
    return sorted(domains+reverse_domains)

def read_nodes():
    with open(nodes_filtered_path, 'r') as f:
        
        nodes = [ int(line.strip()) for line in f.readlines()]
        #print(domains)
    return sorted(nodes)


def bin_search(arr, low,high, x):
    if high>=low:
        mid = (high+low)//2
        if arr[mid] == x:
            return mid
        elif arr[mid]>x:
            return bin_search(arr, low, mid-1,x)
        else:
            return bin_search(arr, mid+1, high,x)
    else:
        return -1

def filter_nodes(domains):
    with open(nodes_filtered_path, 'w') as f:
        for line in sys.stdin:
            id     = line.split("\t")[0]
            domain = line.split("\t")[1]
            #print(domain)
            if bin_search(domains, 0, len(domains)-1, domain) != -1:
                print(line.strip())
                f.write(id + '\n')

def filter_edges(nodes):
    for line in sys.stdin:
            id1 = int(line.split("\t")[0])
            id2 = int(line.split("\t")[1])
            if bin_search(nodes, 0, len(nodes)-1, id1) != -1 and \
               bin_search(nodes, 0, len(nodes)-1, id2) != -1:
                print(line.strip())


def main():
    if sys.argv[1] == "nodes":
        domains = read_tzv()
        filter_nodes(domains)
    elif sys.argv[1] == "edges":
        nodes = read_nodes()
        filter_edges(nodes)

#gunzip -c edges.txt.gz | python3 filter.py edges| gzip > filtered_edges.gz

if __name__ == "__main__":
    main()
