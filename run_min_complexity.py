import networkx as nx

import pythonProject.tools.Min_complexity.Protection as Protection
from pythonProject.tools.Min_complexity.MGDM import build_auxiliary_graph, serve_request
from tools.Network import National_network
from tools.uilts import gen_request


def protection(topology, serve_table):
    complexity = 0
    spectrum = 0
    for i, request in enumerate(serve_table):
        src = request[0]
        dst = request[1]
        rate = request[2]
        auxiliary_graph = Protection.build_auxiliary_graph(src, dst, rate, topology, serve_table, request)
        if src in auxiliary_graph.nodes and dst in auxiliary_graph.nodes:
            if nx.has_path(auxiliary_graph, src, dst):
                path = nx.dijkstra_path(auxiliary_graph, src, dst)
                consume_complexity, consume_spectrum = Protection.serve_request(G, request, path, auxiliary_graph,
                                                                                serve_table)
                complexity += consume_complexity
                spectrum += consume_spectrum
        else:
            print(f"No backup path found for {request}")

    return complexity, spectrum


def MGDM_simulation(Germany, requests, serve_table):
    G = Germany.topology
    complexity = 0
    spectrum = 0
    for request in requests:
        src = request[0]
        dst = request[1]
        rate = request[2]
        auxiliary_graph = build_auxiliary_graph(src, dst, rate, G)
        if src in auxiliary_graph.nodes and dst in auxiliary_graph.nodes:
            if nx.has_path(auxiliary_graph, src, dst):
                path = nx.dijkstra_path(auxiliary_graph, src, dst)
                consume_complexity, consume_spectrum = serve_request(G, request, path, auxiliary_graph, serve_table)
                complexity += consume_complexity
                spectrum += consume_spectrum
        else:
            print(f"No path found for {request}")
    # print(serve_table)

    return G, complexity, spectrum


if __name__ == '__main__':
    result = {'backup': {'complexity': [], 'spectrum': []},
              'working': {'complexity': [], 'spectrum': []}}
    for i in range(100):
        network = National_network()
        request_list = gen_request(41000)
        route_table = {}
        G, working_complexity, working_spectrum = MGDM_simulation(network, request_list, route_table)
        print(route_table)
        backup_complexity, backup_spectrum = protection(G, route_table)
        print(route_table)
        result['backup']['complexity'].append(backup_complexity)
        result['working']['complexity'].append(working_complexity)
        result['working']['spectrum'].append(working_spectrum)
        result['backup']['spectrum'].append(backup_spectrum)

    with open('result\\MGDM.txt', 'a') as outfile:
        outfile.write("\n##########MIN complexity####################\n")
        outfile.write(str(result))
        outfile.write("\n**********Average*********\n")
        outfile.write(
            f"Average working path complexity: {sum(result['working']['complexity']) / len(result['working']['complexity'])}\n")
        outfile.write(
            f"Average backup path complexity: {sum(result['backup']['complexity']) / len(result['backup']['complexity'])}\n")
        outfile.write(
            f"Average working path spectrum: {sum(result['working']['spectrum']) / len(result['working']['spectrum'])}\n")
        outfile.write(
            f"Average backup path spectrum: {sum(result['backup']['spectrum']) / len(result['backup']['spectrum'])}")


# MGDM = 82300 full
