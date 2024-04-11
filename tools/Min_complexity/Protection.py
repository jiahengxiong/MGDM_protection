import uuid

import networkx as nx

MGDM_REACH_TABLE = {
    ('A'): {'Spatial modes': (1),
            '4QAM': {'capacity': 104,
                     'reach': 7830},
            '16QAM': {'capacity': 268,
                      'reach': 1686},
            '64QAM': {'capacity': 312,
                      'reach': 426},
            'MIMO complexity': 1},
    ('A', 'C'): {'Spatial modes': (1, 3),
                 '4QAM': {'capacity': 417,
                          'reach': 426},
                 '16QAM': {'capacity': 833,
                           'reach': 84},
                 '64QAM': {'capacity': 1250,
                           'reach': 12},
                 'MIMO complexity': 10},
    ('A', 'D'): {'Spatial modes': (1, 4),
                 '4QAM': {'capacity': 521,
                          'reach': 7578},
                 '16QAM': {'capacity': 1042,
                           'reach': 1434},
                 '64QAM': {'capacity': 1562,
                           'reach': 174},
                 'MIMO complexity': 17},

    ('A', 'E'): {'Spatial modes': (1, 5),
                 '4QAM': {'capacity': 625,
                          'reach': 7554},
                 '16QAM': {'capacity': 1250,
                           'reach': 1416},
                 '64QAM': {'capacity': 1875,
                           'reach': 156},
                 'MIMO complexity': 26},
    ('B', 'D'): {'Spatial modes': (2, 4),
                 '4QAM': {'capacity': 625,
                          'reach': 306},
                 '16QAM': {'capacity': 1250,
                           'reach': 42},
                 'MIMO complexity': 20},
    ('B', 'E'): {'Spatial modes': (2, 5),
                 '4QAM': {'capacity': 729,
                          'reach': 7248},
                 '16QAM': {'capacity': 1458,
                           'reach': 640},
                 'MIMO complexity': 29},

    ('C', 'E'): {'Spatial modes': (3, 5),
                 '4QAM': {'capacity': 833,
                          'reach': 228},
                 '16QAM': {'capacity': 1667,
                           'reach': 12},
                 'MIMO complexity': 34},

    ('A', 'C', 'E'): {'Spatial modes': (1, 3, 5),
                      '4QAM': {'capacity': 937,
                               'reach': 186},
                      '16QAM': {'capacity': 1875,
                                'reach': 6},
                      'MIMO complexity': 35},

}


def build_virtual_edge(G, path, mode, modulation):
    virtual_edge = []
    distance = 0
    path_edge = []
    src = path[0]
    dst = path[-1]
    spectrum = 1
    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]
        valid_edges = []
        for key, edge_attr in G[u][v].items():
            valid_edges.append([u, v, key, edge_attr])
        path_edge.append(min(valid_edges, key=lambda e: e[3]['weight']))
    for edge in path_edge:
        distance += edge[3]['distance']
        spectrum += edge[3]['spectrum']

    if distance <= MGDM_REACH_TABLE[mode][modulation]['reach']:
        virtual_edge = [src, dst, path_edge, distance, spectrum]
    else:
        return None

    return virtual_edge


def check_wavelength(G, reach, modulation, mode, serve_table, request, rate):
    """
    Rewrite this function to satisfy
    1. if served request's work path overlap current request, the backup paths can
    not share the same mode group. To develop this function we should read the backup path of overlapped requests and
    if current request want to use the wavelength which is used by requests with overlapped working path, add mode.
    2. if current request's backup path will across the wavelength exiting work path:
    2.1 if there is another request's backup path, do not need to add mode
    2.2 if there is not  another request's backup path, add mode
    """
    remove_edge_list = []
    add_mode_wavelength = []
    overlapped_request = []

    working_path = serve_table[request]['working_path']
    for i, key in enumerate(serve_table):
        if len(serve_table[key]['backup_path']) != 0 and key != request:
            for edge in working_path:
                if edge in serve_table[key]['working_path']:
                    add_mode_wavelength.extend(serve_table[key]['backup_path'])
                    overlapped_request.append(key)
                    break

    for u, v, key, data in G.edges(data=True, keys=True):
        if data['occupied_modulation'] != modulation and data['occupied_modulation'] is not None:
            if [u, v, key] not in remove_edge_list:
                remove_edge_list.append([u, v, key])
        if (set(data['occupied_mode']) not in set(mode) and len(data['occupied_mode']) != 0) or (
                set(data['occupied_mode']) == mode):
            if [u, v, key] not in remove_edge_list:
                remove_edge_list.append([u, v, key])
        if data['min_distance'] > reach:
            if [u, v, key] not in remove_edge_list:
                remove_edge_list.append([u, v, key])

        if len(data['occupied_mode']) != 0 or data['occupied_modulation'] is not None:
            if MGDM_REACH_TABLE[mode][modulation]['capacity'] - \
                    MGDM_REACH_TABLE[data["occupied_mode"]][data["occupied_modulation"]]['capacity'] < rate:
                if [u, v, key] not in remove_edge_list:
                    remove_edge_list.append([u, v, key])
        backup_requests = data['protection_requests']
        if backup_requests is not None:
            overlapped_mode = []
            overlapped_distance = []
            overlapped_rate = []
            for i in range(len(backup_requests)):
                request = backup_requests[i]
                if request in overlapped_request:
                    overlapped_mode.append(data['backup_mode'][i])
                    overlapped_distance.append(data['backup_distance'][i])
                    overlapped_rate.append(data['backup_rate'][i])
            if len(overlapped_mode) != 0:
                min_distance = max(overlapped_distance)
                max_mode = max(overlapped_mode, key=len)
                if min_distance > reach:
                    if [u, v, key] not in remove_edge_list:
                        remove_edge_list.append([u, v, key])
                if (set(max_mode) not in set(mode) and len(max_mode) != 0) or (
                        set(max_mode) == mode):
                    if [u, v, key] not in remove_edge_list:
                        remove_edge_list.append([u, v, key])
                if len(data['occupied_mode']) != 0 or data['occupied_modulation'] is not None:
                    if MGDM_REACH_TABLE[mode][modulation]['capacity'] - \
                            MGDM_REACH_TABLE[max_mode][data["occupied_modulation"]]['capacity'] < rate:
                        if [u, v, key] not in remove_edge_list:
                            remove_edge_list.append([u, v, key])

    for edge in remove_edge_list:
        G.remove_edge(edge[0], edge[1], edge[2])

    return G


def build_virtual_graph(G, reach, modulation, mode, serve_table, request):
    virtual_graph = nx.MultiGraph()
    working_path = serve_table[request]["working_path"]
    rate = request[2]
    for u, v, key, data in G.edges(data=True, keys=True):
        if 'wavelength' in data['type'] and (u, v) not in working_path and (v, u) not in working_path:
            # print("adding {} to {}".format(u, v))
            virtual_graph.add_edge(u, v, key=key, **data,
                                   weight=data['distance'] + 0.0000001 * MGDM_REACH_TABLE[mode]["MIMO complexity"])

    virtual_graph = check_wavelength(G=virtual_graph, reach=reach, rate=rate,
                                     modulation=modulation, mode=mode, serve_table=serve_table, request=request)
    return virtual_graph


def build_auxiliary_graph(src, dst, rate, G, serve_table, request):
    modulation_list = ['4QAM', '16QAM', '64QAM']
    auxiliary_graph = nx.MultiGraph()
    for i, mode in enumerate(MGDM_REACH_TABLE):
        for j, modulation in enumerate(MGDM_REACH_TABLE[mode]):
            if modulation in modulation_list:
                if MGDM_REACH_TABLE[mode][modulation]['capacity'] < rate:
                    continue
                virtual_graph = build_virtual_graph(G, MGDM_REACH_TABLE[mode][modulation]['reach'], modulation, mode,
                                                    serve_table, request)

                for u in virtual_graph.nodes():
                    for v in virtual_graph.nodes():
                        virtual_edge = None
                        if u != v and nx.has_path(virtual_graph, u, v):
                            path = nx.dijkstra_path(virtual_graph, u, v, weight='weight')
                            if path is not None:
                                virtual_edge = build_virtual_edge(virtual_graph, path, mode, modulation)
                            if virtual_edge is not None:
                                auxiliary_graph.add_edge(virtual_edge[0], virtual_edge[1], mode=mode,
                                                         modulation=modulation, dependency=virtual_edge[2],
                                                         distance=virtual_edge[3], key=uuid.uuid4().hex,
                                                         weight=virtual_edge[3] + 0.0000001 * MGDM_REACH_TABLE[mode]["MIMO complexity"], spectrum=virtual_edge[4])

    return auxiliary_graph


def serve_request(G, request, path, auxiliary_graph, serve_table):
    print(f"request = {request}, backup path = {path}")
    complexity = 0
    spectrum = 0
    for i in range(0, len(path) - 1):
        valid_edges = []
        u = path[i]
        v = path[i + 1]
        for key, edge_attr in auxiliary_graph[u][v].items():
            valid_edges.append([u, v, key, edge_attr])
        wavelength = (min(valid_edges, key=lambda e: e[3]['weight']))
        data = wavelength[3]
        path_edge = data['dependency']
        mode = data['mode']
        modulation = data['modulation']
        complexity += MGDM_REACH_TABLE[mode]['MIMO complexity']
        print(mode, modulation)
        for edge in path_edge:
            spectrum += G.edges[edge[0], edge[1], edge[2]]['spectrum']
            G.edges[edge[0], edge[1], edge[2]]['backup_mode'].append(mode)
            G.edges[edge[0], edge[1], edge[2]]['backup_distance'].append(edge[3]["distance"])
            G.edges[edge[0], edge[1], edge[2]]['spectrum'] = 0
            G.edges[edge[0], edge[1], edge[2]]['protection_requests'].append(request)
            G.edges[edge[0], edge[1], edge[2]]['backup_rate'].append(request[2])
            serve_table[(request[0], request[1], request[2], request[3])]["backup_path"].append(
                (edge[0], edge[1], edge[2]))

    return complexity, spectrum
