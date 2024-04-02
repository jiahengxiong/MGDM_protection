from tools.Network import National_network
import numpy as np
import networkx as nx
from tools.uilts import gen_request
from tools.MGDM import build_auxiliary_graph, serve_request


def MGDM_simulation(network, requests):
    G = network.topology
    for request in requests:
        src = request[0]
        dst = request[1]
        rate = request[2]
        auxiliary_graph = build_auxiliary_graph(src, dst, rate, G)
        if src in auxiliary_graph.nodes and dst in auxiliary_graph.nodes:
            if nx.has_path(auxiliary_graph, src, dst):
                path = nx.dijkstra_path(auxiliary_graph, src, dst)
                serve_request(G, request, path, auxiliary_graph)
        else:
            print(f"No path found for {request}")


if __name__ == '__main__':
    network = National_network()
    request_list = gen_request(150000)
    MGDM_simulation(network, request_list)
