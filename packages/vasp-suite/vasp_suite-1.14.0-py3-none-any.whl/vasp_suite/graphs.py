import xyz_py
import numpy as np
import matplotlib.pyplot as plt
from ase.data import covalent_radii, atomic_numbers, atomic_masses
from scipy.spatial.distance import cdist
import sys

# from .structure import Structure


class Node:

    def __init__(self, coordinate: np.ndarray, symbol: str, radius: float, idx: int, mass: float, scaler=1.1):
        self.coordinate = coordinate
        self.symbol = symbol
        self.radius = radius
        self.idx = idx
        self.mass = mass
        self.scaler = scaler

    def __sub__(self, other):
        return np.linalg.norm(self.coordinate - other.coordinate)

    def is_connected(self, other) -> bool:
        return self - other <= self.scaler * (self.radius + other.radius)

    @property
    def xy_project(self) -> np.ndarray:
        return self.coordinate @ np.array([
            [1, 0],
            [0, 1],
            [0, 0]
        ])


class MolGraph:
    def __init__(self, scaler=1.1):
        self.nodes = []
        self.edges = {}
        self.crystal = False
        self.scaler = scaler

    def add_node(self, node):
        if type(node) is Node:
            self.nodes.append(node)
        elif type(node) is list:
            for n in node:
                self.nodes.append(n)
        else:
            raise ValueError('Invalid node type')

    def remove_node(self, node: Node):
        self.nodes.remove(node)
        if node in self.edges:
            for neighbor in self.edges[node]:
                self.edges[neighbor].remove(node)
            del self.edges[node]

    @property
    def is_crystal(self):
        self.crystal = True

    def add_edge(self, node1: Node, node2: Node):
        if node1 not in self.edges:
            self.edges[node1] = []
            self.edges[node1].append(node2)
        else:
            if node2 not in self.edges[node1]:
                self.edges[node1].append(node2)

        if node2 not in self.edges:
            self.edges[node2] = []
            self.edges[node2].append(node1)
        else:
            if node1 not in self.edges[node2]:
                self.edges[node2].append(node1)

    @property
    def graph_formula(self):
        symbols = list(map(lambda x: x.symbol, self.nodes))
        symb, count = np.unique(symbols, return_counts=True)
        return ''.join(map(lambda x: x[0] + str(x[1]), zip(symb, count)))

    @property
    def construct_graph(self) -> None:
        coordinates = np.array(list(map(lambda x: x.coordinate, self.nodes)))
        radii = np.array(list(map(lambda x: x.radius, self.nodes)))
        radii = np.tile(radii, (len(radii), 1))
        radii = self.scaler * (radii + radii.T)
        distances = cdist(coordinates, coordinates)
        distances -= radii
        # find the indexes of distances that are less than 0
        idx = np.where(distances <= 0)
        idx = list(zip(idx[0], idx[1]))
        idx = list(filter(lambda x: x[0] != x[1], idx))
        list(map(lambda x: self.add_edge(self.nodes[x[0]], self.nodes[x[1]]), idx))

    def _edge_vector_2d(self, node1: Node, node2: Node) -> np.ndarray:
        return np.array([node1.xy_project, node2.xy_project])

    def _edge_vector_3d(self, node1: Node, node2: Node) -> np.ndarray:
        return np.array([node1.coordinate, node2.coordinate])

    @property
    def plot(self):
        self.construct_graph
        nodes = np.array(list(map(lambda x: x.xy_project, self.nodes)))
        edges = list(map(lambda x: list(map(lambda y: self._edge_vector_2d(x, y), self.edges[x])), self.edges))
        edges = np.array([item for sublist in edges for item in sublist]).reshape(-1, 2, 2)
        idcs = np.array(list(map(lambda x: x.idx, self.nodes)))

        fig, ax = plt.subplots(figsize=(5, 5))
        for edge in edges:
            ax.plot(edge[:, 0], edge[:, 1], c='k', zorder=1)
        for node, idx in zip(nodes, idcs):
            ax.scatter(node[0], node[1], s=100, c='w', zorder=2, edgecolors='k')
            ax.text(node[0], node[1], str(idx), fontsize=6, ha='center', va='center', zorder=2)
        ax.set_aspect('equal')
        ax.set_xlabel('x (Å)')
        ax.set_ylabel('y (Å)')
        fig.tight_layout()
        fig.savefig('molecular_graph.png', dpi=600)

    @property
    def plot3d(self):
        self.construct_graph
        nodes = np.array(list(map(lambda x: x.coordinate, self.nodes)))
        edges = list(map(lambda x: list(map(lambda y: self._edge_vector_3d(x, y), self.edges[x])), self.edges))
        edges = np.array([item for sublist in edges for item in sublist]).reshape(-1, 2, 3)

        # 3d plot
        fig, ax = plt.subplots(subplot_kw={'projection': '3d'}, figsize=(5, 5))
        for node in nodes:
            ax.scatter(node[0], node[1], node[2], s=30, c='w', edgecolors='k', zorder=2)
        for edge in edges:
            ax.plot(edge[:, 0], edge[:, 1], edge[:, 2], c='k', zorder=1)
        ax.set_xlabel('x (Å)')
        ax.set_ylabel('y (Å)')
        ax.set_zlabel('z (Å)')
        plt.show()

    @property
    def get_centered_node(self) -> Node:
        for node in self.nodes:
            if np.allclose(node.coordinate, np.zeros(3)):
                return node
        raise ValueError('No centered node found')

    def extract_fragment(self, node: Node):
        seen = {node}
        mol_graph = MolGraph()
        sys.setrecursionlimit(1000000)

        if len(self.edges) == 0:
            raise ValueError('Graph is not constructed')

        def dfs(node):
            mol_graph.add_node(node)
            if node in self.edges:
                for neighbor in self.edges[node]:
                    if neighbor not in seen:
                        seen.add(neighbor)
                        dfs(neighbor)

        dfs(node)
        mol_graph.construct_graph
        return mol_graph

    def coordination_sphere(self, node: Node, cs_number: int):
        seen = {node}
        sphere_region = MolGraph()

        if len(self.edges) == 0:
            raise ValueError('Graph is not constructed')

        def add_coordination(node, rucursive_depth=0):
            sphere_region.add_node(node)

            if rucursive_depth == cs_number:
                return

            if node in self.edges:
                for neighbor in self.edges[node]:
                    if neighbor not in seen:
                        seen.add(neighbor)
                        add_coordination(neighbor, rucursive_depth + 1)

        add_coordination(node)
        sphere_region.construct_graph
        return sphere_region

    def bridge_nodes(self, node1: Node, node2: Node):
        seen = {node1, node2}
        fragment = []
        atom_dist = node1 - node2
        print("distance between node1 and node2: ", atom_dist)
        symbol = node1.symbol

        fragment.append(node1)
        fragment.append(node2)

        fcs1 = self.edges[node1]
        fcs2 = self.edges[node2]

        fcs1 = list(filter(lambda x: x.symbol != symbol, fcs1))
        fcs2 = list(filter(lambda x: x.symbol != symbol, fcs2))

        fragment.extend(fcs1)
        fragment.extend(fcs2)
        seen.update(fcs1)
        seen.update(fcs2)

        mol_graph = MolGraph()
        for node in fragment:
            mol_graph.add_node(node)
        mol_graph.construct_graph
        return mol_graph

    def _shift_node(self, node: Node):
        x, y, z = node.coordinate
        x_lim, y_lim, z_lim = self.boundaries / 2
        tol = 1.5
        if np.allclose(x, -x_lim, atol=tol) or np.allclose(x, x_lim, atol=tol):
            x = -x
        if np.allclose(y, -y_lim, atol=tol) or np.allclose(y, y_lim, atol=tol):
            y = -y
        if np.allclose(z, -z_lim, atol=tol) or np.allclose(z, z_lim, atol=tol):
            z = -z

        new_node = Node(np.array([x, y, z]), node.symbol, node.radius, node.idx, node.mass)
        self.add_node(new_node)
        self.remove_node(node)

    @property
    def fragment_graph(self):
        fragments = []
        seen = set()
        for node in self.nodes:
            if node.idx not in seen:
                graph = self.extract_fragment(node)
                nodes = graph.nodes
                idx = set(map(lambda x: x.idx, nodes))
                seen.update(idx)
                fragments.append(graph)
            else:
                continue
        return fragments

    @staticmethod
    def mass_center(coords: np.ndarray, masses: np.ndarray) -> np.ndarray:
        center = np.sum(coords * masses[:, None], axis=0) / np.sum(masses)
        coords -= center
        tensor = coords.T @ np.diag(masses) @ coords
        eigval, eigvec = np.linalg.eigh(tensor)
        idx = eigval.argsort()[::-1]
        idx = idx[::-1]
        eigval = eigval[idx]
        prin_axes = eigvec[:, idx]
        coords = coords @ prin_axes
        return coords

    def to_xyz(self, filename: str=None, mass_centered: bool=False):
        if filename is None:
            filename = self.graph_formula + '.xyz'
        coordinates = np.array(list(map(lambda x: x.coordinate, self.nodes)))
        symbols = list(map(lambda x: x.symbol, self.nodes))
        if mass_centered:
            masses = np.array(list(map(lambda x: x.mass, self.nodes)))
            coordinates = self.mass_center(coordinates, masses)
        xyz_py.save_xyz(filename, symbols, coordinates)

    def graph_compare(self, other: 'MolGraph') -> bool:
        if len(self.nodes) != len(other.nodes):
            return False

        symbols1 = list(map(lambda x: x.symbol, self.nodes))
        symbols2 = list(map(lambda x: x.symbol, other.nodes))
        s1, c1 = np.unique(symbols1, return_counts=True)
        s1dict = dict(zip(s1, c1))
        s2, c2 = np.unique(symbols2, return_counts=True)
        s2dict = dict(zip(s2, c2))

        if s1dict != s2dict:
            return False

        mass1 = np.array(list(map(lambda x: x.mass, self.nodes)))
        coords1 = np.array(list(map(lambda x: x.coordinate, self.nodes)))
        coords1 = self.mass_center(coords1, mass1)

        mass2 = np.array(list(map(lambda x: x.mass, other.nodes)))
        coords2 = np.array(list(map(lambda x: x.coordinate, other.nodes)))
        coords2 = self.mass_center(coords2, mass2)

        rmsd = xyz_py.minimise_rmsd(coords1, coords2)[0]
        if rmsd < 1:
            return True
        else:
            return False
