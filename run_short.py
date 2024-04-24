import multiprocessing
import random
import time
from datetime import datetime
import networkx as nx
import winsound
import pythonProject.tools.Shared_Protection as Protection
from pythonProject.tools.Working import build_auxiliary_graph, serve_request
from pythonProject.tools.uilts import gen_request
from tools.Network import National_network


def protection(topology, serve_table, approach, index_protection):
    complexity = 0
    spectrum = 0
    G = topology
    for j, request in enumerate(serve_table):
        src = request[0]
        dst = request[1]
        rate = request[2]
        auxiliary_graph = Protection.build_auxiliary_graph(src, dst, rate, topology, serve_table, request, approach,
                                                           index_protection)
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


def simulation(Germany, requests, serve_table, approach, index_working):
    G = Germany.topology
    complexity = 0
    spectrum = 0
    for request in requests:
        src = request[0]
        dst = request[1]
        rate = request[2]
        auxiliary_graph = build_auxiliary_graph(src, dst, rate, G, approach, index_working)
        if src in auxiliary_graph.nodes and dst in auxiliary_graph.nodes:
            if nx.has_path(auxiliary_graph, src, dst):
                path = nx.dijkstra_path(auxiliary_graph, src, dst)
                consume_complexity, consume_spectrum = serve_request(G, request, path, auxiliary_graph, serve_table,
                                                                     approach, index_working)
                complexity += consume_complexity
                spectrum += consume_spectrum
        else:
            print(f"No path found for {request}")
    # print(serve_table)

    return G, complexity, spectrum


def worker(methods_run, index_list_run, result_run, i, total_traffic):
    request_list_run = gen_request(total_traffic * 1000)
    start_time = time.time()
    print(f"Worker started for {i} process for {len(request_list_run)} requests")
    for method_run in methods_run:
        for index_run in index_list_run:
            # print(method_run, index_run)
            network = National_network()
            route_table = {}
            G, working_complexity, working_spectrum = simulation(network, request_list_run, route_table, method_run,
                                                                 index_run)
            # print(route_table)
            backup_complexity, backup_spectrum = protection(G, route_table, method_run, index_run)
            # print(route_table)
            result_run[method_run][index_run]['backup']['complexity'].append(backup_complexity)
            result_run[method_run][index_run]['working']['complexity'].append(working_complexity)
            result_run[method_run][index_run]['working']['spectrum'].append(working_spectrum)
            result_run[method_run][index_run]['backup']['spectrum'].append(backup_spectrum)
            print(f"Finished {method_run}-{index_run} for {i} running")
    end_time = time.time()
    execution_time = end_time - start_time
    minutes, seconds = divmod(execution_time, 60)
    print(
        f"running time：{int(minutes)} min {seconds:.2f} s  for {i}th running")


if __name__ == '__main__':
    """result = {'backup': {'complexity': [], 'spectrum': []},
              'working': {'complexity': [], 'spectrum': []}}"""
    manager = multiprocessing.Manager()
    result = manager.dict()
    methods = ['SMT', 'MGDM', 'Full-MIMO', 'MF-MGDM']
    index_list = ['Min_complexity', 'Min_spectrum']
    total_traffic = 23.5
    for method in methods:
        result[method] = manager.dict()
        for index in index_list:
            result[method][index] = manager.dict()
            result[method][index]['backup'] = {'complexity': manager.list(), 'spectrum': manager.list()}
            result[method][index]['working'] = {'complexity': manager.list(), 'spectrum': manager.list()}

            """result[method][index] = {'backup': {'complexity': [], 'spectrum': []},
                                     'working': {'complexity': [], 'spectrum': []}}"""
    processed = []
    for i in range(1, 21):
        process = multiprocessing.Process(target=worker,
                                          args=(methods, index_list, result, i, total_traffic))
        processed.append(process)
        process.start()
        time.sleep(random.uniform(0, 1))

    for process in processed:
        process.join()

    winsound.Beep(2000, 5000)

    now = datetime.now()
    current_year = now.year
    current_month = now.month
    current_day = now.day
    current_hour = now.hour
    current_minute = now.minute
    current_second = now.second

    for method in methods:
        for index in index_list:
            with open(f'result\\{method}_short.txt', 'a') as outfile:
                outfile.write(
                    f"##########{index}-----{current_year}-{current_month}-{current_day}-{current_hour}:{current_minute}:{current_second}####################\n")
                # Write the actual content of the dictionary
                outfile.write(f"Backup complexity: {result[method][index]['backup']['complexity']}\n")
                outfile.write(f"Backup spectrum: {result[method][index]['backup']['spectrum']}\n")
                outfile.write(f"Working complexity: {result[method][index]['working']['complexity']}\n")
                outfile.write(f"Working spectrum: {result[method][index]['working']['spectrum']}\n")
                outfile.write("**********Average*********\n")
                # Calculate and write averages
                avg_working_complexity = sum(result[method][index]['working']['complexity']) / len(
                    result[method][index]['working']['complexity']) / total_traffic
                avg_backup_complexity = sum(result[method][index]['backup']['complexity']) / len(
                    result[method][index]['backup']['complexity']) / total_traffic
                avg_working_spectrum = sum(result[method][index]['working']['spectrum']) / len(
                    result[method][index]['working']['spectrum']) / total_traffic
                avg_backup_spectrum = sum(result[method][index]['backup']['spectrum']) / len(
                    result[method][index]['backup']['spectrum']) / total_traffic
                outfile.write(f"Average working path complexity per Tbs: {avg_working_complexity}\n")
                outfile.write(f"Average backup path complexity per Tbs: {avg_backup_complexity}\n")
                outfile.write(f"Average working path spectrum per Tbs: {avg_working_spectrum}\n")
                outfile.write(f"Average backup path spectrum per Tbs: {avg_backup_spectrum}\n")

    # MGDM = 82300 full
