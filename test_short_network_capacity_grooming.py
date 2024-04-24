import copy

import networkx as nx
import winsound

import pythonProject.tools.Dadicated_Protection as Dadicated_Protection
import pythonProject.tools.Shared_Protection as Shared_Protection
from pythonProject.tools.Working import build_auxiliary_graph, serve_request
from pythonProject.tools.uilts import gen_request
from tools.Network import Continental_network, National_network


def share_protection(topology, serve_table, approach, index):
    G = topology
    complexity = 0
    spectrum = 0
    no_serve = []
    for i, request in enumerate(serve_table):
        src = request[0]
        dst = request[1]
        rate = request[2]
        auxiliary_graph = Shared_Protection.build_auxiliary_graph(src, dst, rate, topology, serve_table, request,
                                                                  approach,
                                                                  index)
        if src in auxiliary_graph.nodes and dst in auxiliary_graph.nodes:
            if nx.has_path(auxiliary_graph, src, dst):
                path = nx.dijkstra_path(auxiliary_graph, src, dst)
                consume_complexity, consume_spectrum = Shared_Protection.serve_request(G, request, path,
                                                                                       auxiliary_graph,
                                                                                       serve_table, approach)
                complexity += consume_complexity
                spectrum += consume_spectrum
        else:
            no_serve.append(request)

    return G, no_serve


def dadicate_protection(Germany, requests, serve_table, approach, index):
    G = Germany
    complexity = 0
    spectrum = 0
    no_serve = []
    for request in requests:
        src = request[0]
        dst = request[1]
        rate = request[2]
        auxiliary_graph = Dadicated_Protection.build_auxiliary_graph(src, dst, rate, G, approach, index, serve_table,
                                                                     request)
        if src in auxiliary_graph.nodes and dst in auxiliary_graph.nodes:
            if nx.has_path(auxiliary_graph, src, dst):
                path = nx.dijkstra_path(auxiliary_graph, src, dst)
                consume_complexity, consume_spectrum = Dadicated_Protection.serve_request(G, request, path,
                                                                                          auxiliary_graph, serve_table,
                                                                                          approach, index)
                complexity += consume_complexity
                spectrum += consume_spectrum
        else:
            no_serve.append(request)
    # print(serve_table)

    return G, no_serve


def simulation(Germany, requests, serve_table, approach, index):
    G = Germany.topology
    complexity = 0
    spectrum = 0
    no_serve = []
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
            no_serve.append(request)
    # print(serve_table)

    return G, no_serve


import multiprocessing
import time


def run_tests(method, index, total_traffic_test, request_list_test, i_test, result):
    no_serve_dadicated = []
    no_serve_shared = []
    no_serve_working = []
    start_time = time.time()
    print(
        f"Testing {method} {index} for {i_test}th with {total_traffic_test / 1000}Tbs num_resuest is {len(request_list_test)}")
    network = National_network()
    route_table = {}
    G, no_serve_working = simulation(network, request_list_test, route_table, method, index)
    D = copy.deepcopy(G)
    if G is False:
        print(f"Failing {method} {index} for {total_traffic_test / 1000}Tbs in working path")
        end_time = time.time()
        execution_time = end_time - start_time
        minutes, seconds = divmod(execution_time, 60)
        # print(f"running time：{int(minutes)} min {seconds:.2f} s")
    else:
        G, no_serve_shared = share_protection(G, route_table, method, index)
        D, no_serve_dadicated = dadicate_protection(D, request_list_test, route_table, method, index)
    if G is False:
        print(f"Failing {method} {index} for {total_traffic_test / 1000}Tbs in shared")
        end_time = time.time()
        execution_time = end_time - start_time
        minutes, seconds = divmod(execution_time, 60)
        # print(f"running time：{int(minutes)} min {seconds:.2f} s")
    if D is False:
        print(f"Failing {method} {index} for {total_traffic_test / 1000}Tbs in dadicated")
        end_time = time.time()
        execution_time = end_time - start_time
        minutes, seconds = divmod(execution_time, 60)
        # print(f"running time：{int(minutes)} min {seconds:.2f} s")
    no_serve_Shared = no_serve_working + no_serve_shared
    no_serve_Dadicated = no_serve_working + no_serve_dadicated
    no_serve_share_set = set(no_serve_Shared)
    no_serve_dadicate_set = set(no_serve_Dadicated)
    no_serve_share_final = list(no_serve_share_set)
    no_serve_dadicate_final = list(no_serve_dadicate_set)

    no_serve_share_rate = 0
    no_serve_dadicate_rate = 0
    for request in no_serve_share_final:
        no_serve_share_rate = no_serve_share_rate + request[2]
    for request in no_serve_dadicate_final:
        no_serve_dadicate_rate = no_serve_dadicate_rate + request[2]

    end_time = time.time()
    execution_time = end_time - start_time
    minutes, seconds = divmod(execution_time, 60)
    print(
        f"running time：{int(minutes)} min {seconds:.2f} s {method} {index} for {i_test}th with {total_traffic_test / 1000}Tbs")

    return no_serve_share_rate / total_traffic_test, no_serve_dadicate_rate / total_traffic_test


def worker(methods, index_list, request_list, i, result, protection_policy, total_traffic, no_serve_rate_dict):
    for method in methods:
        for index in index_list:
            if result['shared'][method][index] == 0 or result['dadicated'][method][index] == 0:
                no_serve_shar_rate, no_serve_dadicate_rate = run_tests(method, index, total_traffic, request_list, i,
                                                                       result)
                no_serve_rate_dict['shared'][method][index].append(no_serve_shar_rate)
                no_serve_rate_dict['dadicated'][method][index].append(no_serve_dadicate_rate)


if __name__ == '__main__':
    result = {}
    no_serve_dict = {}
    protection_policy = ['shared', 'dadicated']
    methods = ['SMT', 'MGDM', 'Full-MIMO', 'MF-MGDM']
    index_list = ['Min_complexity']
    total_traffic = 150000  # 100000
    for protection in protection_policy:
        manager = multiprocessing.Manager()
        result[protection] = manager.dict()

        for method in methods:
            result[protection][method] = manager.dict()  # 这里初始化每个方法的字典

            for index in index_list:
                result[protection][method][index] = 0
    """result['SMT']['Min_complexity'] = 0
    result['SMT']['Min_spectrum'] = 0
    result['MGDM']['Min_complexity'] = 0
    result['MGDM']['Min_spectrum'] = 0
    result['Full-MIMO']['Min_complexity'] = 0
    result['Full-MIMO']['Min_spectrum'] = 0
    result['MF-MGDM']['Min_complexity'] = 0
    result['MF-MGDM']['Min_spectrum'] = 0"""

    result['dadicated']['Full-MIMO']['Min_complexity'] = 170000
    result['shared']['Full-MIMO']['Min_complexity'] = 249000  # 250-240
    result['shared']['SMT']['Min_complexity'] = 26000
    result['dadicated']['SMT']['Min_complexity'] = 23000
    result['shared']['MGDM']['Min_complexity'] = 'waiting'
    result['dadicated']['MGDM']['Min_complexity'] = 0
    result['shared']['MF-MGDM']['Min_complexity'] = 68000  # 70000
    result['dadicated']['MF-MGDM']['Min_complexity'] = 51000  # 60000

    while True:
        """result['shared']['SMT']['Min_complexity'] = 20000
        result['dadicated']['SMT']['Min_complexity'] = 20000"""
        processes = []
        for protection in protection_policy:
            manager = multiprocessing.Manager()
            no_serve_dict[protection] = manager.dict()

            for method in methods:
                no_serve_dict[protection][method] = manager.dict()  # 初始化每个方法的字典

                for index in index_list:
                    no_serve_dict[protection][method][index] = manager.list()

        for i in range(10):
            request_list = gen_request(total_traffic)
            process = multiprocessing.Process(target=worker,
                                              args=(methods, index_list, request_list, i, result, protection_policy,
                                                    total_traffic, no_serve_dict))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        for protection in protection_policy:
            for method in methods:
                for index in index_list:
                    print(
                        f'***{protection}-{method}-{index}-{result[protection][method][index]}-{total_traffic / 1000}Tbs***')

        for protection in protection_policy:
            for method in methods:
                for index in index_list:
                    if result[protection][method][index] == 0:
                        print(f"***{protection}-{method}-{index}")
                        if 1 - sum(no_serve_dict[protection][method][index]) / len(
                                no_serve_dict[protection][method][index]) <= 0.99:
                            print(1 - sum(no_serve_dict[protection][method][index]) / len(
                                no_serve_dict[protection][method][index]))
                            result[protection][method][index] = total_traffic

        total_traffic += 10000  # 确保每次循环都更新

        # 检查所有进程是否已完成，如果是，则退出循环
        flag = True
        for protection in protection_policy:
            for method in methods:
                for index in index_list:
                    if result[protection][method][index] == 0:
                        flag = False
        if flag:
            break

    winsound.Beep(2000, 5000)

    with open(f'result\\capacity\\short_capacity.txt', 'a') as outfile:
        outfile.write("\n*******************************************\n")
        for protection in protection_policy:
            for method in methods:
                for index in index_list:
                    outfile.write(f'Capacity: {protection}-{method}-{index}-{result[protection][method][index]}\n')
