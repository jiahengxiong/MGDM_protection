import networkx as nx

import pythonProject.tools.Protection as Protection
from pythonProject.tools.Working import build_auxiliary_graph, serve_request
from pythonProject.tools.uilts import gen_request
from tools.Network import Continental_network


def protection(topology, serve_table, approach, index):
    complexity = 0
    spectrum = 0
    for i, request in enumerate(serve_table):
        src = request[0]
        dst = request[1]
        rate = request[2]
        auxiliary_graph = Protection.build_auxiliary_graph(src, dst, rate, topology, serve_table, request, approach,
                                                           index)
        if src in auxiliary_graph.nodes and dst in auxiliary_graph.nodes:
            if nx.has_path(auxiliary_graph, src, dst):
                path = nx.dijkstra_path(auxiliary_graph, src, dst)
                consume_complexity, consume_spectrum = Protection.serve_request(G, request, path, auxiliary_graph,
                                                                                serve_table, approach)
                complexity += consume_complexity
                spectrum += consume_spectrum
        else:
            print(f"No backup path found for {request}")

    return complexity, spectrum


def simulation(Germany, requests, serve_table, approach, index):
    G = Germany.topology
    complexity = 0
    spectrum = 0
    for request in requests:
        src = request[0]
        dst = request[1]
        rate = request[2]
        auxiliary_graph = build_auxiliary_graph(src, dst, rate, G, approach, index)
        if src in auxiliary_graph.nodes and dst in auxiliary_graph.nodes:
            if nx.has_path(auxiliary_graph, src, dst):
                path = nx.dijkstra_path(auxiliary_graph, src, dst)
                consume_complexity, consume_spectrum = serve_request(G, request, path, auxiliary_graph, serve_table,
                                                                     approach, index)
                complexity += consume_complexity
                spectrum += consume_spectrum
        else:
            print(f"No path found for {request}")
    # print(serve_table)

    return G, complexity, spectrum


if __name__ == '__main__':
    """result = {'backup': {'complexity': [], 'spectrum': []},
              'working': {'complexity': [], 'spectrum': []}}"""
    result = {}
    methods = ['SMT', 'MGDM', 'Full-MIMO', 'MF-MGDM']
    index_list = ['Min_complexity', 'Min_spectrum']
    total_traffic = 30
    for method in methods:
        result[method] = {}
        for index in index_list:
            result[method][index] = {'backup': {'complexity': [], 'spectrum': []},
                                     'working': {'complexity': [], 'spectrum': []}}
    for i in range(100):
        request_list = gen_request(total_traffic * 1000)
        for method in methods:
            for index in index_list:
                print(method, index)
                network = Continental_network()
                route_table = {}
                G, working_complexity, working_spectrum = simulation(network, request_list, route_table, method,
                                                                     index)
                print(route_table)
                backup_complexity, backup_spectrum = protection(G, route_table, method, index)
                print(route_table)
                result[method][index]['backup']['complexity'].append(backup_complexity)
                result[method][index]['working']['complexity'].append(working_complexity)
                result[method][index]['working']['spectrum'].append(working_spectrum)
                result[method][index]['backup']['spectrum'].append(backup_spectrum)

    for i, method in enumerate(result):
        for j, index in enumerate(result[method]):
            with open(f'result\\{method}.txt', 'a') as outfile:
                outfile.write(f"##########{index}####################\n")
                outfile.write(str(result))
                outfile.write("\n**********Average*********\n")
                outfile.write(
                    f"Average working path complexity: {sum(result[method][index]['working']['complexity']) / len(result[method][index]['working']['complexity'])}\n")
                outfile.write(
                    f"Average backup path complexity: {sum(result[method][index]['backup']['complexity']) / len(result[method][index]['backup']['complexity'])}\n")
                outfile.write(
                    f"Average working path spectrum: {sum(result[method][index]['working']['spectrum']) / len(result[method][index]['working']['spectrum'])}\n")
                outfile.write(
                    f"Average backup path spectrum: {sum(result[method][index]['backup']['spectrum']) / len(result[method][index]['backup']['spectrum'])}\n")

    # MGDM = 82300 full
