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
SMT_REACH_TABLE = {
    ('A'): {'Spatial modes': (1),
            '4QAM': {'capacity': 104,
                     'reach': 7830},
            '16QAM': {'capacity': 268,
                      'reach': 1686},
            '64QAM': {'capacity': 312,
                      'reach': 426},
            'MIMO complexity': 1},
}
FULL_MIMO_REACH_TABLE = {
    ('A', 'B', 'C', 'D', 'E'): {'Spatial modes': (1, 2, 3, 4, 5),
                                '4QAM': {'capacity': 1562,
                                         'reach': 7830},
                                '16QAM': {'capacity': 3125,
                                          'reach': 1686},
                                '64QAM': {'capacity': 4687,
                                          'reach': 426},
                                'MIMO complexity': 225},
}
MF_MGDM_REACH_TABLE = {
    ('A'): {'Spatial modes': (1),
            '4QAM': {'capacity': 100,
                     'reach': 21},
            '16QAM': {'capacity': 200,
                      'reach': 21},
            'MIMO complexity': 1},
    ('A', 'E'): {'Spatial modes': (1, 1),
                 '4QAM': {'capacity': 200,
                          'reach': 21},
                 '16QAM': {'capacity': 400,
                           'reach': 21},
                 'MIMO complexity': 2},
    ('A', 'C', 'E'): {'Spatial modes': (1, 1, 1),
                      '16QAM': {'capacity': 600,
                                'reach': 3},
                      'MIMO complexity': 3},
}


def build_virtual_edge(G, path, mode, modulation, approach, index):
    virtual_edge = []
    distance = 0
    path_edge = []
    src = path[0]
    dst = path[-1]
    spectrum = 0
    if approach == 'SMT':
        reach_table = SMT_REACH_TABLE
    if approach == 'MGDM':
        reach_table = MGDM_REACH_TABLE
    if approach == 'Full-MIMO':
        reach_table = FULL_MIMO_REACH_TABLE
    if approach == 'MF-MGDM':
        reach_table = MF_MGDM_REACH_TABLE
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

    if distance <= reach_table[mode][modulation]['reach']:
        virtual_edge = [src, dst, path_edge, distance, spectrum]
    else:
        return None

    return virtual_edge


def check_wavelength(G, reach, modulation, mode, rate, approach, index):
    remove_edge_list = []
    if approach == 'SMT':
        reach_table = SMT_REACH_TABLE
    if approach == 'MGDM':
        reach_table = MGDM_REACH_TABLE
    if approach == 'Full-MIMO':
        reach_table = FULL_MIMO_REACH_TABLE
    if approach == 'MF-MGDM':
        reach_table = MF_MGDM_REACH_TABLE
    for u, v, key, data in G.edges(data=True, keys=True):
        if data['occupied_modulation'] != modulation and data['occupied_modulation'] is not None:
            if [u, v, key] not in remove_edge_list:
                remove_edge_list.append([u, v, key])
        if set(set(data['occupied_mode'])).issubset(set(set(mode))) is False and len(data['occupied_mode']) != 0:
            #print(set(data['occupied_mode']), set(mode))
            if [u, v, key] not in remove_edge_list:
                remove_edge_list.append([u, v, key])
        if data['min_distance'] > reach:
            if [u, v, key] not in remove_edge_list:
                remove_edge_list.append([u, v, key])

        if len(data['occupied_mode']) != 0 or data['occupied_modulation'] is not None:
            if reach_table[mode][modulation]['capacity'] - data['occupied_rate'] < rate:
                if [u, v, key] not in remove_edge_list:
                    remove_edge_list.append([u, v, key])
    for edge in remove_edge_list:
        G.remove_edge(edge[0], edge[1], edge[2])

    return G


def build_virtual_graph(G, reach, modulation, mode, rate, approach, index):
    if approach == 'SMT':
        reach_table = SMT_REACH_TABLE
    if approach == 'MGDM':
        reach_table = MGDM_REACH_TABLE
    if approach == 'Full-MIMO':
        reach_table = FULL_MIMO_REACH_TABLE
    if approach == 'MF-MGDM':
        reach_table = MF_MGDM_REACH_TABLE
    virtual_graph = nx.MultiGraph()
    for u, v, key, data in G.edges(data=True, keys=True):
        if 'wavelength' in data['type']:
            # print("adding {} to {}".format(u, v))
            if index == 'Min_complexity':
                virtual_graph.add_edge(u, v, key=key, **data,
                                       weight=data['distance'] + 0.0000001 * reach_table[mode]["MIMO complexity"])
            if index == 'Min_spectrum':
                virtual_graph.add_edge(u, v, key=key, **data,
                                       weight=data['distance'] + 0.0000001 * data['spectrum'])

    virtual_graph = check_wavelength(virtual_graph, reach,
                                     modulation, mode, rate, approach, index)
    return virtual_graph


def build_auxiliary_graph(src, dst, rate, G, approach, index):
    modulation_list = ['4QAM', '16QAM', '64QAM']
    auxiliary_graph = nx.MultiGraph()
    if approach == 'SMT':
        reach_table = SMT_REACH_TABLE
    if approach == 'MGDM':
        reach_table = MGDM_REACH_TABLE
    if approach == 'Full-MIMO':
        reach_table = FULL_MIMO_REACH_TABLE
    if approach == 'MF-MGDM':
        reach_table = MF_MGDM_REACH_TABLE
    for i, mode in enumerate(reach_table):
        for j, modulation in enumerate(reach_table[mode]):
            if modulation in modulation_list:
                if reach_table[mode][modulation]['capacity'] < rate:
                    continue
                virtual_graph = build_virtual_graph(G, reach_table[mode][modulation]['reach'], modulation, mode,
                                                    rate, approach, index)

                for u in virtual_graph.nodes():
                    for v in virtual_graph.nodes():
                        virtual_edge = None
                        if u != v and nx.has_path(virtual_graph, u, v):
                            path = nx.dijkstra_path(virtual_graph, u, v, weight='weight')
                            if path is not None:
                                virtual_edge = build_virtual_edge(virtual_graph, path, mode, modulation, approach,
                                                                  index)
                            if virtual_edge is not None:
                                if index == 'Min_complexity':
                                    auxiliary_graph.add_edge(virtual_edge[0], virtual_edge[1], mode=mode,
                                                             modulation=modulation, dependency=virtual_edge[2],
                                                             distance=virtual_edge[3], key=uuid.uuid4().hex,
                                                             weight=virtual_edge[3] + 0.000001*reach_table[mode]["MIMO complexity"],
                                                             spectrum=virtual_edge[4])
                                else:
                                    auxiliary_graph.add_edge(virtual_edge[0], virtual_edge[1], mode=mode,
                                                             modulation=modulation, dependency=virtual_edge[2],
                                                             distance=virtual_edge[3], key=uuid.uuid4().hex,
                                                             weight=virtual_edge[3] + 0.000001 * virtual_edge[4],
                                                             spectrum=virtual_edge[4])

    return auxiliary_graph


def serve_request(G, request, path, auxiliary_graph, serve_table, approach, index):
    serve_table[(request[0], request[1], request[2], request[3])] = {"working_path": [],
                                                                     "backup_path": []}
    if approach == 'SMT':
        reach_table = SMT_REACH_TABLE
    if approach == 'MGDM':
        reach_table = MGDM_REACH_TABLE
    if approach == 'Full-MIMO':
        reach_table = FULL_MIMO_REACH_TABLE
    if approach == 'MF-MGDM':
        reach_table = MF_MGDM_REACH_TABLE

    print(f"request = {request}, path = {path}")
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
        complexity += reach_table[mode]['MIMO complexity']
        print(mode, modulation)
        for edge in path_edge:
            spectrum += G.edges[edge[0], edge[1], edge[2]]['spectrum']
            G.edges[edge[0], edge[1], edge[2]]['occupied_mode'] = mode
            G.edges[edge[0], edge[1], edge[2]]['occupied_modulation'] = modulation
            G.edges[edge[0], edge[1], edge[2]]['min_distance'] = max(edge[3]['distance'],
                                                                     G.edges[edge[0], edge[1], edge[2]]['min_distance'])
            G.edges[edge[0], edge[1], edge[2]]['spectrum'] = 0
            G.edges[edge[0], edge[1], edge[2]]['working_requests'].append(request)
            G.edges[edge[0], edge[1], edge[2]]['occupied_rate'] = G.edges[edge[0], edge[1], edge[2]]['occupied_rate'] + \
                                                                  request[2]
            serve_table[(request[0], request[1], request[2], request[3])]["working_path"].append((edge[0], edge[1]))

    return complexity, spectrum
