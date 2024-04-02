import uuid

import networkx as nx


class National_network:
    def __init__(self):
        self.distance = [200, 300, 400, 500, 600, 700, 600, 500, 400, 300, 200]
        self.topology = self.get_topology()

    def get_topology(self):
        G = nx.MultiGraph()
        for i in range(1, 51):
            G.add_edge(1, 7, distance=306,
                       occupied_mode=(), occupied_requests=(), type=f'wavelength{i}', occupied_modulation=None,
                       min_distance=0,
                       key=uuid.uuid4().hex)
            G.add_edge(1, 8, distance=298,
                       occupied_mode=(), occupied_requests=(), type=f'wavelength{i}', occupied_modulation=None,
                       min_distance=0,
                       key=uuid.uuid4().hex)
            G.add_edge(1, 11, distance=174,
                       occupied_mode=(), occupied_requests=(), type=f'wavelength{i}', occupied_modulation=None,
                       min_distance=0,
                       key=uuid.uuid4().hex)
            G.add_edge(2, 7, distance=114,
                       occupied_mode=(), occupied_requests=(), type=f'wavelength{i}', occupied_modulation=None,
                       min_distance=0,
                       key=uuid.uuid4().hex)
            G.add_edge(2, 8, distance=120,
                       occupied_mode=(), occupied_requests=(), type=f'wavelength{i}', occupied_modulation=None,
                       min_distance=0,
                       key=uuid.uuid4().hex)
            G.add_edge(2, 14, distance=144,
                       occupied_mode=(), occupied_requests=(), type=f'wavelength{i}', occupied_modulation=None,
                       min_distance=0,
                       key=uuid.uuid4().hex)
            G.add_edge(3, 5, distance=37,
                       occupied_mode=(), occupied_requests=(), type=f'wavelength{i}', occupied_modulation=None,
                       min_distance=0,
                       key=uuid.uuid4().hex)
            G.add_edge(3, 8, distance=208,
                       occupied_mode=(), occupied_requests=(), type=f'wavelength{i}', occupied_modulation=None,
                       min_distance=0,
                       key=uuid.uuid4().hex)
            G.add_edge(3, 10, distance=88,
                       occupied_mode=(), occupied_requests=(), type=f'wavelength{i}', occupied_modulation=None,
                       min_distance=0,
                       key=uuid.uuid4().hex)
            G.add_edge(3, 14, distance=278,
                       occupied_mode=(), occupied_requests=(), type=f'wavelength{i}', occupied_modulation=None,
                       min_distance=0,
                       key=uuid.uuid4().hex)
            G.add_edge(4, 5, distance=36,
                       occupied_mode=(), occupied_requests=(), type=f'wavelength{i}', occupied_modulation=None,
                       min_distance=0,
                       key=uuid.uuid4().hex)
            G.add_edge(4, 10, distance=41,
                       occupied_mode=(), occupied_requests=(), type=f'wavelength{i}', occupied_modulation=None,
                       min_distance=0,
                       key=uuid.uuid4().hex)
            G.add_edge(6, 8, distance=316,
                       occupied_mode=(), occupied_requests=(), type=f'wavelength{i}', occupied_modulation=None,
                       min_distance=0,
                       key=uuid.uuid4().hex)
            G.add_edge(6, 10, distance=182,
                       occupied_mode=(), occupied_requests=(), type=f'wavelength{i}', occupied_modulation=None,
                       min_distance=0,
                       key=uuid.uuid4().hex)
            G.add_edge(6, 11, distance=400,
                       occupied_mode=(), occupied_requests=(), type=f'wavelength{i}', occupied_modulation=None,
                       min_distance=0,
                       key=uuid.uuid4().hex)
            G.add_edge(6, 12, distance=85,
                       occupied_mode=(), occupied_requests=(), type=f'wavelength{i}', occupied_modulation=None,
                       min_distance=0,
                       key=uuid.uuid4().hex)
            G.add_edge(6, 15, distance=224,
                       occupied_mode=(), occupied_requests=(), type=f'wavelength{i}', occupied_modulation=None,
                       min_distance=0,
                       key=uuid.uuid4().hex)
            G.add_edge(7, 8, distance=157,
                       occupied_mode=(), occupied_requests=(), type=f'wavelength{i}', occupied_modulation=None,
                       min_distance=0,
                       key=uuid.uuid4().hex)
            G.add_edge(8, 11, distance=258,
                       occupied_mode=(), occupied_requests=(), type=f'wavelength{i}', occupied_modulation=None,
                       min_distance=0,
                       key=uuid.uuid4().hex)
            G.add_edge(9, 12, distance=64,
                       occupied_mode=(), occupied_requests=(), type=f'wavelength{i}', occupied_modulation=None,
                       min_distance=0,
                       key=uuid.uuid4().hex)
            G.add_edge(9, 16, distance=74,
                       occupied_mode=(), occupied_requests=(), type=f'wavelength{i}', occupied_modulation=None,
                       min_distance=0,
                       key=uuid.uuid4().hex)
            G.add_edge(11, 15, distance=275,
                       occupied_mode=(), occupied_requests=(), type=f'wavelength{i}', occupied_modulation=None,
                       min_distance=0,
                       key=uuid.uuid4().hex)
            G.add_edge(13, 15, distance=179,
                       occupied_mode=(), occupied_requests=(), type=f'wavelength{i}', occupied_modulation=None,
                       min_distance=0,
                       key=uuid.uuid4().hex)
            G.add_edge(13, 17, distance=143,
                       occupied_mode=(), occupied_requests=(), type=f'wavelength{i}', occupied_modulation=None,
                       min_distance=0,
                       key=uuid.uuid4().hex)
            G.add_edge(15, 16, distance=187,
                       occupied_mode=(), occupied_requests=(), type=f'wavelength{i}', occupied_modulation=None,
                       min_distance=0,
                       key=uuid.uuid4().hex)
            G.add_edge(16, 17, distance=86,
                       occupied_mode=(), occupied_requests=(), type=f'wavelength{i}', occupied_modulation=None,
                       min_distance=0,
                       key=uuid.uuid4().hex)

        for u, v, key, data in G.edges(data=True, keys=True):
            G[u][v][key]['distance'] = data['distance'] - 31

        return G
