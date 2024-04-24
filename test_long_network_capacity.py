import networkx as nx

import pythonProject.tools.Shared_Protection as Protection
from pythonProject.tools.Working import build_auxiliary_graph, serve_request
from pythonProject.tools.uilts import gen_request
from tools.Network import National_network, Continental_network


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
            return False

    return G


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
            return False
    # print(serve_table)

    return G


if __name__ == '__main__':
    """result = {'backup': {'complexity': [], 'spectrum': []},
              'working': {'complexity': [], 'spectrum': []}}"""
    result = {}
    methods = ['SMT', 'MGDM', 'Full-MIMO']
    index_list = ['Min_complexity', 'Min_spectrum']
    total_traffic = 14000
    for method in methods:
        result[method] = {}
        for index in index_list:
            result[method][index] = 0
    while 1 == 1:
        for i in range(10):
            request_list = gen_request(total_traffic)
            for method in methods:
                for index in index_list:
                    if result[method][index] == 0:
                        network = Continental_network()
                        route_table = {}
                        G = simulation(network, request_list, route_table, method, index)
                        if G is False:
                            result[method][index] = total_traffic
                            break
                        G = protection(G, route_table, method, index)
                        if G is False:
                            result[method][index] = total_traffic
                            break
        total_traffic = total_traffic + 1000
        print(f"******{result}-total_traffic={total_traffic}******")
        flag = True
        for method in methods:
            for index in index_list:
                if result[method][index] == 0:
                    flag = False
        if flag is True:
            break
    with open(f'result\\capacity\\long_capacity.txt', 'w') as outfile:
        outfile.write(str(result))
