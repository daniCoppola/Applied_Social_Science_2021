To test the set up:
gzip nodes.txt
gzip edges.txt
gunzip -c <nodes.txt.gz> | python3 filter.py nodes| gzip > filtered_nodes.gz
gunzip -c <edges.txt.gz> | python3 filter.py edges| gzip > filtered_edges.gz

Running the filter on the real data:
- make sure to name the leaning file as leaning.tzv or change the path in filter.py
gunzip -c cc-main-2018-19-nov-dec-jan-domain-vertices.txt.gz | python3 filter.py nodes| gzip > full_filtered_nodes.gz
gunzip -c cc-main-2018-19-nov-dec-jan-domain-edges.txt.gz | python3 filter.py edges| gzip > full_filtered_edges.gz
