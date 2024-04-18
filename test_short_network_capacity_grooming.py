import networkx as nx
import threading
import time
import pythonProject.tools.Protection as Protection
from pythonProject.tools.Working import build_auxiliary_graph, serve_request
from pythonProject.tools.uilts import gen_request
from tools.Network import National_network
import winsound


def protection(topology, serve_table, approach, index):
    G = topology
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


import multiprocessing
import time


def run_tests(method_list, indexs_list, total_traffic_test, request_list_test, i_test, result):
    for method_test in method_list:
        for index_test in indexs_list:
            start_time = time.time()
            print(
                f"Testing {method_test} {index_test} for {i_test}th with {total_traffic_test / 1000}Tbs num_resuest is {len(request_list_test)}")
            if result[method_test][index_test] == 0:
                network = National_network()
                route_table = {}
                G = simulation(network, request_list_test, route_table, method_test, index_test)
                if G is False:
                    result[method_test][index_test] = total_traffic_test
                    print(f"Failing {method_test} {index_test} for {total_traffic_test / 1000}Tbs in working path")
                    end_time = time.time()
                    execution_time = end_time - start_time
                    minutes, seconds = divmod(execution_time, 60)
                    # print(f"running time：{int(minutes)} min {seconds:.2f} s")
                    break
                G = protection(G, route_table, method_test, index_test)
                if G is False:
                    result[method_test][index_test] = total_traffic_test
                    print(f"Failing {method_test} {index_test} for {total_traffic_test / 1000}Tbs in backup path")
                    end_time = time.time()
                    execution_time = end_time - start_time
                    minutes, seconds = divmod(execution_time, 60)
                    # print(f"running time：{int(minutes)} min {seconds:.2f} s")
                    break
            end_time = time.time()
            execution_time = end_time - start_time
            minutes, seconds = divmod(execution_time, 60)
            print(
                f"running time：{int(minutes)} min {seconds:.2f} s {method_test} {index_test} for {i_test}th with {total_traffic_test / 1000}Tbs")


def worker(methods, index_list, total_traffic, i, result):
    request_list = gen_request(total_traffic)
    run_tests(methods, index_list, total_traffic, request_list, i, result)


if __name__ == '__main__':
    result = {}
    methods = ['SMT', 'MGDM', 'Full-MIMO', 'MF-MGDM']
    index_list = ['Min_complexity', 'Min_spectrum']
    total_traffic = 43000
    for method in methods:
        manager = multiprocessing.Manager()
        result[method] = manager.dict()
        for index in index_list:
            result[method][index] = 0
    result['SMT']['Min_complexity'] = 25000
    result['SMT']['Min_spectrum'] = 35000
    result['MGDM']['Min_complexity'] = 'Waiting'
    result['MGDM']['Min_spectrum'] = 'Waiting'
    result['Full-MIMO']['Min_complexity'] = 'Waiting'
    result['Full-MIMO']['Min_spectrum'] = 'Waiting'
    result['MF-MGDM']['Min_complexity'] = 51000
    result['MF-MGDM']['Min_spectrum'] = 57000

    while True:
        processes = []
        for i in range(10):
            process = multiprocessing.Process(target=worker,
                                              args=(methods, index_list, total_traffic, i, result))
            processes.append(process)
            process.start()
        for process in processes:
            process.join()

        for i, method in enumerate(result):
            for j, index in enumerate(result[method]):
                print(f'***{method}-{index}_{result[method][index]}-{total_traffic/1000}Tbs***')
        total_traffic += 1000
        flag = True
        for method in methods:
            for index in index_list:
                if result[method][index] == 0:
                    flag = False
        if flag:
            break

    with open(f'result\\capacity\\short_capacity.txt', 'a') as outfile:
        for i, method in enumerate(result):
            for j, index in enumerate(result[method]):
                outfile.write(f'Capacity: {method}-{index}-{result[method][index]}Tbs')
    winsound.Beep(2000, 5000)
