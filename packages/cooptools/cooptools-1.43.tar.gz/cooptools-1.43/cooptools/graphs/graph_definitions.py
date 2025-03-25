from cooptools.graphs import graph as gr
import random as rnd
from typing import Callable, Tuple
import string
import math
from cooptools.geometry_utils import vector_utils as vec

def random_dict(index_provider: Callable[[], str], max_x: int, max_y: int):
    nodes = []
    for ii in range(0, 5):
        nodes.append(gr.Node(name=f"{index_provider()}",
                          pos=(rnd.randint(0, max_x), rnd.randint(0, max_y))))

    graph_dict = {node: [] for node in nodes}
    for node in nodes:
        n_connections = rnd.randint(1, len(nodes)//2)
        samples = rnd.sample(nodes, n_connections)

        graph_dict[node] += [sample for sample in samples if sample not in graph_dict[node]]
        for sample in samples:
            graph_dict[sample].append(node)

    return graph_dict

def small_test():
    a = gr.Node('a', (100, 100))
    b = gr.Node('b', (200, 100))
    c = gr.Node('c', (100, 200))
    d = gr.Node('d', (200, 200))
    e = gr.Node('e', (300, 300))
    graph_dict = {
        a: [b, c],
        b: [a, d, e],
        c: [a, d],
        d: [b, c, e],
        e: [b, d]
    }

    return graph_dict

def test_circuit():
    a = gr.Node('a', (200, 200))
    b = gr.Node('b', (250, 250))
    c = gr.Node('c', (250, 300))
    d = gr.Node('d', (300, 300))
    e = gr.Node('e', (350, 150))
    f = gr.Node('f', (300, 200))
    g = gr.Node('g', (250, 100))
    h = gr.Node('h', (200, 100))
    graph_dict = {
        a: [b, c],
        b: [c, d],
        c: [d],
        d: [e],
        e: [f, g],
        f: [h],
        h: [a],
        g: [a]
    }

    return graph_dict

def large_circuit(x_bounds: Tuple[float, float], y_bounds: Tuple[float, float], spread: int = 100):
    alphabet=string.ascii_lowercase

    nodes = []
    rnd.seed(0)
    for ii in range(0, 26):
        nodes.append(
            gr.Node(name=alphabet[ii],
                 pos=((x_bounds[1] - x_bounds[0]) / 2 + x_bounds[0] + (x_bounds[1] - x_bounds[0]) * math.sin(ii / 26 * 2 * math.pi) + rnd.randint(-spread, spread),
                     (y_bounds[1] - y_bounds[0]) / 2 + y_bounds[0] + (y_bounds[1] - y_bounds[0])  * math.cos(ii / 26 * 2 * math.pi) + rnd.randint(-spread, spread))))

    graph_dict = {}

    for ii, node in enumerate(nodes):
        n_connections = rnd.randint(1, 4)

        for n in range(1, n_connections + 1):
            if ii + n >= 26:
                index = ii + n - 26
            else:
                index = ii + n
            graph_dict.setdefault(node, []).append(nodes[index])
    return graph_dict


def basic_intersection():
    a = gr.Node('a', (200, 200))
    b = gr.Node('b', (200, 300))
    c = gr.Node('c', (300, 300))
    d = gr.Node('d', (300, 300))
    e = gr.Node('e', (350, 150))
    f = gr.Node('f', (300, 200))
    g = gr.Node('g', (250, 100))
    h = gr.Node('h', (200, 100))
    graph_dict = {
        a: [b, c],
        b: [c, d],
        c: [d],
        d: [e],
        e: [f, g],
        f: [h],
        h: [a],
        g: [a]
    }

    return graph_dict


def intersection(pos: vec.FloatVec, offset_val: float = None):

    if offset_val is None:
        offset_val = 0

    L_Out = gr.Node('L_Out', pos=vec.add_vectors([pos, (-offset_val, offset_val / 2)]))
    L_In  = gr.Node('L_In', pos=vec.add_vectors([pos, (offset_val, offset_val / 2)]))
    R_Out = gr.Node('R_Out', pos=vec.add_vectors([pos, (offset_val, -offset_val / 2)]))
    R_In  = gr.Node('R_In', pos=vec.add_vectors([pos, (-offset_val, -offset_val / 2)]))
    U_Out = gr.Node('U_Out', pos=vec.add_vectors([pos, (offset_val / 2, offset_val)]))
    U_In  = gr.Node('U_In', pos=vec.add_vectors([pos, (offset_val / 2, -offset_val)]))
    D_Out = gr.Node('D_Out', pos=vec.add_vectors([pos, (-offset_val / 2, -offset_val)]))
    D_In  = gr.Node('D_In', pos=vec.add_vectors([pos, (-offset_val / 2, offset_val)]))
    Rot_0_270 = gr.Node('Rot_0_270', pos=vec.add_vectors([pos, (-offset_val * 2 / 3, -offset_val * 2 / 3)]))
    Rot_90_0 = gr.Node('Rot_90_0', pos=vec.add_vectors([pos, (offset_val * 2 / 3, -offset_val * 2 / 3)]))
    Rot_180_90 = gr.Node('Rot_180_90', pos=vec.add_vectors([pos, (offset_val * 2 / 3, offset_val * 2 / 3)]))
    Rot_270_180 = gr.Node('Rot_270_180', pos=vec.add_vectors([pos, (-offset_val * 2 / 3, offset_val * 2 / 3)]))
    Rot_270_0 = gr.Node('Rot_270_0', pos=vec.add_vectors([pos, (-offset_val * 1 / 3, -offset_val * 1 / 3)]))
    Rot_0_90 = gr.Node('Rot_0_90', pos=vec.add_vectors([pos, (offset_val * 1 / 3, -offset_val * 1 / 3)]))
    Rot_90_180 = gr.Node('Rot_90_180', pos=vec.add_vectors([pos, (offset_val * 1 / 3, offset_val * 1 / 3)]))
    Rot_180_270 = gr.Node('Rot_180_270', pos=vec.add_vectors([pos, (-offset_val * 1 / 3, offset_val * 1 / 3)]))

    graph_dict = {
        L_Out: [],
        L_In: [L_Out, Rot_180_90, Rot_180_270],
        R_Out: [],
        R_In: [R_Out, Rot_0_270, Rot_0_90],
        U_Out: [],
        U_In: [U_Out, Rot_90_0, Rot_90_180],
        D_Out: [],
        D_In: [D_Out, Rot_270_180, Rot_270_0],
        Rot_0_270: [Rot_270_180, D_Out],
        Rot_90_0: [Rot_0_270, R_Out],
        Rot_180_90: [Rot_90_0, U_Out],
        Rot_270_180: [Rot_180_90, L_Out],
        Rot_270_0: [Rot_0_90, R_Out],
        Rot_0_90: [Rot_90_180, U_Out],
        Rot_90_180: [Rot_180_270, L_Out],
        Rot_180_270: [Rot_270_0, D_Out]
    }

    return graph_dict

if __name__ == "__main__":
    from cooptools.graphs import draw as d
    from matplotlib import pyplot as plt

    def test_intersection():
        grp = gr.Graph(intersection((0, 0), offset_val=0.5))

        fig, ax = plt.subplots()

        d.plot_graph(grp,
                     fig=fig,
                     ax=ax,
                     routes=[grp.astar(grp.Nodes["R_In"], grp.Nodes["D_Out"])])

        plt.show()


    test_intersection()