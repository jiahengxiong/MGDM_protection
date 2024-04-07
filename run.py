from tools.Network import National_network
import numpy as np
import networkx as nx
from tools.uilts import gen_request
from tools.MGDM import build_auxiliary_graph, serve_request
import tools.Protection as Protection


def protection(topology, serve_table):
    for i, request in enumerate(serve_table):
        src = request[0]
        dst = request[1]
        rate = request[2]
        auxiliary_graph = Protection.build_auxiliary_graph(src, dst, rate, topology, serve_table, request)
        if src in auxiliary_graph.nodes and dst in auxiliary_graph.nodes:
            if nx.has_path(auxiliary_graph, src, dst):
                path = nx.dijkstra_path(auxiliary_graph, src, dst)
                Protection.serve_request(G, request, path, auxiliary_graph, serve_table)
        else:
            print(f"No back up path found for {request}")


def MGDM_simulation(network, requests, serve_table):
    G = network.topology
    for request in requests:
        src = request[0]
        dst = request[1]
        rate = request[2]
        auxiliary_graph = build_auxiliary_graph(src, dst, rate, G)
        if src in auxiliary_graph.nodes and dst in auxiliary_graph.nodes:
            if nx.has_path(auxiliary_graph, src, dst):
                path = nx.dijkstra_path(auxiliary_graph, src, dst)
                serve_request(G, request, path, auxiliary_graph, serve_table)
        else:
            print(f"No path found for {request}")
    # print(serve_table)

    return G


if __name__ == '__main__':
    network = National_network()
    request_list = gen_request(100000)
    route_table = {}
    G = MGDM_simulation(network, request_list, route_table)
    print(route_table)
    protection(G, route_table)
    print(route_table)
