"""
-*- coding: utf-8 -*-
@Author : Cui Jinghao
@Time : 2024/9/11 14:41
@Function: common_merges.py
@Contact: cuijinghao@tgqs.net
"""
import numpy as np
import re
from tgqSim.circuit.common_gates import BASE_SINGLE_GATE, BASE_DOUBLE_GATE, BASE_TRIPLE_GATE
from tgqSim.circuit.common_gates import _CommonGate as CommonGate
from tgqSim.circuit.common_gates import (x, rz, cz, sqrt_x)
from tgqSim.circuit.QuantumCircuit import QuantumCircuit
from tgqSim.transformers.common_decompositions import *

# a set of gates among which, if encountered twice in a circuit on a same qbit, can be merged
GATE_MERGE_SET = ['sqrt_x', 'rz', 'cx']

# decomposition base gates set
DECOMP_GATE_SET = {'rz', 'cz', 'x', 'sqrt_x'}


def two_gates_can_merge(gate1: CommonGate, gate2: CommonGate) -> bool:
    """

    Args:
        gate1:
        gate2:

    Returns: compare two gates' position and check gate type

    """
    return (gate1.name in GATE_MERGE_SET
            and gate2.name in GATE_MERGE_SET
            and gate1.name == gate2.name
            and gate1.qbit == gate2.qbit)


def merge_two_gates_on_base(gate1: CommonGate, gate2: CommonGate):
    """
    Params: original two single bit gates
    Returns: gate after merging

    """
    if two_gates_can_merge(gate1, gate2):
        if gate1.name.lower() == 'sqrt_x' and gate2.name.lower() == 'sqrt_x':
            return x(gate1.qbit)
        elif gate1.name.lower() == 'x' and gate2.name.lower() == 'x':
            return None
        elif gate1.name.lower() == 'cx' and gate2.name.lower() == 'cx':
            return None
        elif gate1.name.lower() == 'rz' and gate2.name.lower() == 'rz':
            return rz(gate1.qbit, gate1.theta + gate2.theta)


def merge_circuit():
    """
    Params: original circuit, merge function
    Returns: merged circuit
    Description: compare each two gates, if can_merge then merge these two gates

    """
    pass


def decompose_circuit_on_base(circuit: QuantumCircuit) -> QuantumCircuit:
    """

    Args:
        circuit: original circuit

    Returns:
        circuit after decomposition

    """
    org_width = circuit.width
    decomposed_circuit = QuantumCircuit(org_width)
    for gate in circuit.gate_list:
        # [(1, ('rx', 1.5707963267948966)), (0, ('sqrt_x',))]
        gate_name = gate[1][0].lower()
        if gate_name in BASE_SINGLE_GATE:
            gate_pos = gate[0]
            #### base single gates
            if gate_name == 'x':
                decomposed_circuit.append(x(gate_pos))
            elif gate_name == 'rz':
                decomposed_circuit.append(rz(gate_pos, gate[1][1]))
            #####
            elif gate_name == 'h':
                decomposed_circuit.append_circuit(H(gate_pos, org_width))
            elif gate_name == 'y':
                decomposed_circuit.append_circuit(Y(gate_pos, org_width))
            elif gate_name == 'z':
                decomposed_circuit.append_circuit(Z(gate_pos, org_width))
            elif gate_name == 's':
                decomposed_circuit.append_circuit(S(gate_pos, org_width))
            elif gate_name == 'sdg':
                decomposed_circuit.append_circuit(Sdg(gate_pos, org_width))
            elif gate_name == 't':
                decomposed_circuit.append_circuit(T(gate_pos, org_width))
            elif gate_name == 'tdg':
                decomposed_circuit.append_circuit(Tdg(gate_pos, org_width))
            elif gate_name == 'rx':
                decomposed_circuit.append_circuit(Rx(gate[1][1], gate_pos, org_width))
            elif gate_name == 'ry':
                decomposed_circuit.append_circuit(Ry(gate[1][1], gate_pos, org_width))

        elif gate_name in BASE_DOUBLE_GATE:
            pos1, pos2 = gate[0][0], gate[0][1]
            #### base double gates
            if gate_name == 'cz':
                decomposed_circuit.append(cz(pos1, pos2))
            ####
            elif gate_name == 'cx':
                decomposed_circuit.append_circuit(Cnot(pos1, pos2, org_width))
            elif gate_name == 'swap':
                decomposed_circuit.append_circuit(Swap(pos1, pos2, org_width))
            elif gate_name == 'iswap':
                decomposed_circuit.append_circuit(ISwap(pos1, pos2, org_width))
            elif gate_name == 'cp':
                decomposed_circuit.append_circuit(Cphase(gate[1][1], pos1, pos2, org_width))
            elif gate_name == 'syc':
                decomposed_circuit.append_circuit(Syc(pos1, pos2, org_width))
            elif gate_name == 'rxx':
                decomposed_circuit.append_circuit(Rxx(gate[1][1], pos1, pos2, org_width))
            elif gate_name == 'ryy':
                decomposed_circuit.append_circuit(Ryy(gate[1][1], pos1, pos2, org_width))
            elif gate_name == 'rzz':
                decomposed_circuit.append_circuit(Rzz(gate[1][1], pos1, pos2, org_width))
        elif gate_name in BASE_TRIPLE_GATE:
            # cswap := fredkin
            if gate_name == 'cswap':
                decomposed_circuit.append_circuit(Fred(gate[0][0], gate[0][1], gate[0][2], org_width))
            # ccx := toffoli
            elif gate_name == 'ccx':
                decomposed_circuit.append_circuit(Toff(gate[0][0], gate[0][1], gate[0][2], org_width))
    return decomposed_circuit
