#!/usr/bin/env python3

from mlreferences.fx import DMatrixModel
import pytest
import torch
from torch import Tensor
import torch.nn.functional as F
import torch.nn as nn
from mltools import dmx
from mltools.fx.tracer import QuantTracer
from mltools.fx.transform import cast_input_output_transform
from mltools.sparse import Sparsify
from mltools.approximate import Approximate
import torch.fx as fx
from torch.fx import Node, Graph
from typing import List, Tuple


RANDOM_SEED = 0

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

torch.manual_seed(RANDOM_SEED)
import pytest
import torch
from torch import nn

from collections import namedtuple

from mlreferences.mnist import Lenet5, MNISTWorkload


def test_indempotence_law():
    # Create a simple PyTorch module for testing

    # Initialize the module and some sample input

    # dmx.aware()
    model = Lenet5()
    orig_lenet_workload = MNISTWorkload(
        name="lenet5",
        model=model,
        resize_image=True,
        data_dir="./data")

    dmxmodel_lenet_workload = MNISTWorkload(
        name="lenet5",
        model=DMatrixModel(model),
        resize_image=True,
        data_dir="./data")

    simple_module = orig_lenet_workload.model
    transformed_module = dmxmodel_lenet_workload.model

    sample_input = orig_lenet_workload.create_batch(1)

    original_output = simple_module(sample_input)
    transformed_output = transformed_module(sample_input)

    assert torch.allclose(original_output, transformed_output)
    breakpoint()

def compare_code_diff(graph1: Graph, graph2: Graph) -> List[str]:
    import difflib
    d = difflib.Differ()
    c1 = graph1.python_code(graph1)
    c2 = graph2.python_code(graph2)
    result = list(d.compare(c1.src.splitlines(), c2.src.splitlines()))
    html_d = difflib.HtmlDiff()
    with open("demofile2.html", "a") as f:
        output = html_d.make_file(fromlines=c1.src.splitlines(), tolines=c2.src.splitlines())
        f.write(output)
    return result

def nodes_are_equal(node1: Node, node2: Node) -> bool:
    return (
        node1.op == node2.op and
        node1.target == node2.target and
        len(node1.args) == len(node2.args) and
        len(node1.kwargs) == len(node2.kwargs))

def compare_graphs(graph1: Graph,
                   graph2: Graph) -> Tuple[List[Graph], List[List[Graph]]]:
    nodes1 = list(graph1.nodes)
    nodes2 = list(graph2.nodes)

    mismatched_segments1 = []
    mismatched_segments2 = []
    current_segment1 = []
    current_segment2 = []


    for node1, node2 in zip(nodes1, nodes2):

        if not nodes_are_equal:
            current_segment1.append(node1)
            current_segment2.append(node2)
        else:
            if current_segment1 and current_segment2:
                mismatched_segments1.append(current_segment1)
                mismatched_segments2.append(current_segment2)
                current_segment1 = []
                current_segment2 = []

    if current_segment1 and current_segment2:
        mismatched_segments1.append(current_segment1)
        mismatched_segments2.append(current_segment2)

    return mismatched_segments1, mismatched_segments2

Frontier = namedtuple('Frontier', ['x', 'history'])
Insert = namedtuple('Insert', ['line'])
Remove = namedtuple('Remove', ['line'])
def myers_diff(a_nodes: List[Node], b_nodes: List[Node]) -> Tuple[List[Node], List[Node]]:
    # This marks the farthest-right point along each diagonal in the edit
    # graph, along with the history that got it there
    frontier = {1: Frontier(0, [])}

    def one(idx):
        """
        The algorithm Myers presents is 1-indexed; since Python isn't, we
        need a conversion.
        """
        return idx - 1

    a_max = len(a_nodes)
    b_max = len(b_nodes)
    for d in range(0, a_max + b_max + 1):
        for k in range(-d, d + 1, 2):
            # This determines whether our next search point will be going down
            # in the edit graph, or to the right.
            #
            # The intuition for this is that we should go down if we're on the
            # left edge (k == -d) to make sure that the left edge is fully
            # explored.
            #
            # If we aren't on the top (k != d), then only go down if going down
            # would take us to territory that hasn't sufficiently been explored
            # yet.
            go_down = (k == -d or
                    (k != d and frontier[k - 1].x < frontier[k + 1].x))

            # Figure out the starting point of this iteration. The diagonal
            # offsets come from the geometry of the edit grid - if you're going
            # down, your diagonal is lower, and if you're going right, your
            # diagonal is higher.
            if go_down:
                old_x, history = frontier[k + 1]
                x = old_x
            else:
                old_x, history = frontier[k - 1]
                x = old_x + 1

            # We want to avoid modifying the old history, since some other step
            # may decide to use it.
            history = history[:]
            y = x - k

            # We start at the invalid point (0, 0) - we should only start building
            # up history when we move off of it.
            if 1 <= y <= b_max and go_down:
                history.append(Insert(b_nodes[one(y)]))
            elif 1 <= x <= a_max:
                history.append(Remove(a_nodes[one(x)]))

            # Chew up as many diagonal moves as we can - these correspond to common lines,
            # and they're considered "free" by the algorithm because we want to maximize
            # the number of these in the output.
            while x < a_max and y < b_max and a_nodes[one(x + 1)] == b_nodes[one(y + 1)]:
                x += 1
                y += 1
                history.append(Keep(a_nodes[one(x)]))

            if x >= a_max and y >= b_max:
                # If we're here, then we've traversed through the bottom-left corner,
                # and are done.
                return history
            else:
                frontier[k] = Frontier(x, history)

    assert False, 'Could not find edit script'
