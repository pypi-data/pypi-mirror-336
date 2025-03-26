"""
-*- coding: utf-8 -*-
@Author : Cui Jinghao
@Time : 2024/9/11 15:40
@Function: common_decompositions.py
@Contact: cuijinghao@tgqs.net
"""


import tgqSim as tgqs
import numpy as np

# sqrt_x = tgqs.X**0.5
'''
对不同门拆解进行初始化，拆解线路的基础门集采用{Rz, cz, X, SX},以下只选取了一种拆解方式，对不同拆解方式可自行定义。
'''



def H(qubit, width):
    circuit = tgqs.QuantumCircuit(width)
    circuit.append(tgqs.rz(qubit, np.pi/2))
    circuit.append(tgqs.sqrt_x(qubit))
    circuit.append(tgqs.rz(qubit, np.pi/2))
    return circuit


def Y(qubit, width):
    circuit = tgqs.QuantumCircuit(width)
    circuit.append(tgqs.rz(qubit, -np.pi))
    circuit.append(tgqs.x(qubit))
    return circuit


def Z(qubit, width):
    circuit = tgqs.QuantumCircuit(width)
    circuit.append(tgqs.rz(qubit, np.pi))
    return circuit

def Cnot(control_qubit, target_qubit, width):
    circuit = tgqs.QuantumCircuit(width)
    circuit.append(tgqs.rz(target_qubit, np.pi/2))
    circuit.append(tgqs.sqrt_x(target_qubit))
    circuit.append(tgqs.rz(target_qubit, np.pi/2))
    circuit.append(tgqs.cz(control_qubit, target_qubit))
    circuit.append(tgqs.rz(target_qubit, np.pi/2))
    circuit.append(tgqs.sqrt_x(target_qubit))
    circuit.append(tgqs.rz(target_qubit, np.pi/2))
    return circuit

def S(qubit, width):
    circuit = tgqs.QuantumCircuit(width)
    circuit.append(tgqs.rz(qubit, np.pi/2))
    return circuit

def Sdg(qubit, width):
    circuit = tgqs.QuantumCircuit(width)
    circuit.append(tgqs.rz(qubit, -np.pi/2))
    return circuit

def T(qubit, width):
    circuit = tgqs.QuantumCircuit(width)
    circuit.append(tgqs.rz(qubit, np.pi/4))
    return circuit

def Tdg(qubit, width):
    circuit = tgqs.QuantumCircuit(width)
    circuit.append(tgqs.rz(qubit, -np.pi/4))
    return circuit

def Ch(control_qubit, target_qubit, width):
    circuit = tgqs.QuantumCircuit(width)
    circuit.append(tgqs.rz(control_qubit, np.pi))
    circuit.append(tgqs.sqrt_x(control_qubit))
    circuit.append(tgqs.rz(control_qubit, np.pi*3/4))
    # circuit.append(tgqs.CNOT(target_qubit, control_qubit))
    circuit.append(tgqs.rz(target_qubit, np.pi/2))
    circuit.append(tgqs.sqrt_x(target_qubit))
    circuit.append(tgqs.rz(target_qubit, np.pi/2))
    circuit.append(tgqs.cz(control_qubit, target_qubit))
    circuit.append(tgqs.rz(target_qubit, np.pi/2))
    circuit.append(tgqs.sqrt_x(target_qubit))
    circuit.append(tgqs.rz(target_qubit, np.pi/2))
    circuit.append(tgqs.rz(control_qubit, np.pi/4))
    circuit.append(tgqs.sqrt_x(control_qubit))
    return circuit

def Rx(theta, qubit, width):
    circuit = tgqs.QuantumCircuit(width)
    circuit.append(tgqs.rz(qubit, np.pi/2))
    circuit.append(tgqs.sqrt_x(qubit))
    circuit.append(tgqs.rz(qubit, np.pi+theta))
    circuit.append(tgqs.sqrt_x(qubit))
    circuit.append(tgqs.rz(qubit, np.pi*5/2))
    return circuit

def Ry(theta, qubit, width):
    circuit = tgqs.QuantumCircuit(width)
    circuit.append(tgqs.rz(qubit, 0))
    circuit.append(tgqs.sqrt_x(qubit))
    circuit.append(tgqs.rz(qubit, np.pi+theta))
    circuit.append(tgqs.sqrt_x(qubit))
    circuit.append(tgqs.rz(qubit, np.pi*3))
    return circuit

def Swap(qubit1, qubit2, width):
    circuit = tgqs.QuantumCircuit(width)
    # circuit.append(tgqs.CNOT(qubit1, qubit2))
    # circuit.append(tgqs.CNOT(qubit2, qubit1))
    # circuit.append(tgqs.CNOT(qubit1, qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.cz(qubit1, qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))

    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.cz(qubit2, qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))

    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.cz(qubit1, qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    return circuit

def ISwap(qubit1, qubit2, width):
    circuit = tgqs.QuantumCircuit(width)
    circuit.append(tgqs.rz(qubit1, np.pi))
    circuit.append(tgqs.rz(qubit2, np.pi/2))
    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi/2))
    # circuit.append(tgqs.CNOT(qubit1, qubit2))
    # circuit.append(tgqs.CNOT(qubit2, qubit1))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.cz(qubit1, qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))

    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.cz(qubit2, qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.rz(qubit2, np.pi/2))
    circuit.append(tgqs.sqrt_x(qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi/2))
    return circuit

def Cphase(theta, control_qubit, target_qubit, width):
    circuit = tgqs.QuantumCircuit(width)
    circuit.append(tgqs.rz(control_qubit, theta/2))
    # circuit.append(tgqs.CNOT(control_qubit, target_qubit))
    circuit.append(tgqs.rz(target_qubit, np.pi/2))
    circuit.append(tgqs.sqrt_x(target_qubit))
    circuit.append(tgqs.rz(target_qubit, np.pi/2))
    circuit.append(tgqs.cz(control_qubit, target_qubit))
    circuit.append(tgqs.rz(target_qubit, np.pi/2))
    circuit.append(tgqs.sqrt_x(target_qubit))
    circuit.append(tgqs.rz(target_qubit, np.pi/2))
    circuit.append(tgqs.rz(target_qubit, -(theta/2)))
    # circuit.append(tgqs.CNOT(control_qubit, target_qubit))
    circuit.append(tgqs.rz(target_qubit, np.pi/2))
    circuit.append(tgqs.sqrt_x(target_qubit))
    circuit.append(tgqs.rz(target_qubit, np.pi/2))
    circuit.append(tgqs.cz(control_qubit, target_qubit))
    circuit.append(tgqs.rz(target_qubit, np.pi/2))
    circuit.append(tgqs.sqrt_x(target_qubit))
    circuit.append(tgqs.rz(target_qubit, np.pi/2))
    circuit.append(tgqs.rz(target_qubit, theta/2))
    return circuit

def Fred(control_qubit, qubit1, qubit2, width):
    circuit = tgqs.QuantumCircuit(width)
    # circuit.append(tgqs.CNOT(qubit1, control_qubit))
    circuit.append(tgqs.rz(control_qubit, np.pi / 2))
    circuit.append(tgqs.sqrt_x(control_qubit))
    circuit.append(tgqs.rz(control_qubit, np.pi / 2))
    circuit.append(tgqs.cz(qubit1, control_qubit))
    circuit.append(tgqs.rz(control_qubit, np.pi / 2))
    circuit.append(tgqs.sqrt_x(control_qubit))
    circuit.append(tgqs.rz(control_qubit, np.pi / 2))

    circuit.append(tgqs.rz(qubit1, np.pi/2))
    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi/2))
    # circuit.append(tgqs.CNOT(control_qubit, qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.cz(control_qubit, qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))

    circuit.append(tgqs.rz(qubit1, -(np.pi/4)))
    # circuit.append(tgqs.CNOT(qubit2, qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.cz(qubit2, qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))

    circuit.append(tgqs.rz(qubit1, np.pi/4))
    # circuit.append(tgqs.CNOT(control_qubit, qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.cz(control_qubit, qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))

    circuit.append(tgqs.rz(control_qubit, np.pi/4))
    circuit.append(tgqs.rz(qubit1, -(np.pi/4)))
    # circuit.append(tgqs.CNOT(qubit2, qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.cz(qubit2, qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))

    circuit.append(tgqs.rz(qubit1, np.pi*3/4))
    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi/2))
    # circuit.append(tgqs.CNOT(control_qubit, qubit1))
    # circuit.append(tgqs.CNOT(qubit1, control_qubit))
    # circuit.append(tgqs.CNOT(control_qubit, qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.cz(control_qubit, qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))

    circuit.append(tgqs.rz(control_qubit, np.pi / 2))
    circuit.append(tgqs.sqrt_x(control_qubit))
    circuit.append(tgqs.rz(control_qubit, np.pi / 2))
    circuit.append(tgqs.cz(qubit1, control_qubit))
    circuit.append(tgqs.rz(control_qubit, np.pi / 2))
    circuit.append(tgqs.sqrt_x(control_qubit))
    circuit.append(tgqs.rz(control_qubit, np.pi / 2))

    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.cz(control_qubit, qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))

    # circuit.append(tgqs.CNOT(qubit2, qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.cz(qubit2, qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.rz(qubit1, -(np.pi/4)))
    circuit.append(tgqs.rz(qubit2, np.pi/4))
    # circuit.append(tgqs.CNOT(qubit2, qubit1))
    # circuit.append(tgqs.CNOT(control_qubit, qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.cz(qubit2, qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))

    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.cz(control_qubit, qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    return circuit

def Syc(qubit1, qubit2, width):
    circuit = tgqs.QuantumCircuit(width)
    circuit.append(tgqs.rz(qubit1, -np.pi))
    circuit.append(tgqs.rz(qubit2, -np.pi/2))
    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.sqrt_x(qubit2))
    circuit.append(tgqs.rz(qubit1, np.pi/2))
    circuit.append(tgqs.rz(qubit2, -np.pi))
    # circuit.append(tgqs.CNOT(qubit1, qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.cz(qubit1, qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))

    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.rz(qubit2, np.pi/2))
    circuit.append(tgqs.rz(qubit1, np.pi))
    # circuit.append(tgqs.CNOT(qubit1, qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.cz(qubit1, qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))

    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.rz(qubit2, np.pi/2))
    # circuit.append(tgqs.CNOT(qubit1, qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.cz(qubit1, qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.x(qubit1))
    circuit.append(tgqs.x(qubit2))
    circuit.append(tgqs.rz(qubit1, np.pi*11/12))
    circuit.append(tgqs.rz(qubit2, np.pi*11/12))
    return circuit

def Rxx(theta, qubit1, qubit2, width):
    circuit = tgqs.QuantumCircuit(width)
    circuit.append(tgqs.rz(qubit1, np.pi/2))
    circuit.append(tgqs.rz(qubit2, np.pi/2))
    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.sqrt_x(qubit2))
    circuit.append(tgqs.rz(qubit1, np.pi/2))
    circuit.append(tgqs.rz(qubit2, np.pi))
    # circuit.append(tgqs.CNOT(qubit2, qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.cz(qubit2, qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))

    circuit.append(tgqs.rz(qubit1, theta))
    # circuit.append(tgqs.CNOT(qubit2, qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.cz(qubit2, qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))

    circuit.append(tgqs.rz(qubit1, np.pi/2))
    circuit.append(tgqs.sqrt_x(qubit2))
    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.rz(qubit2, np.pi/2))
    circuit.append(tgqs.rz(qubit1, np.pi/2))
    return circuit

def Ryy(theta, qubit1, qubit2, width):
    circuit = tgqs.QuantumCircuit(width)
    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.sqrt_x(qubit2))
    # circuit.append(tgqs.CNOT(qubit1, qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.cz(qubit1, qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))

    circuit.append(tgqs.rz(qubit2, theta))
    # circuit.append(tgqs.CNOT(qubit1, qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.cz(qubit1, qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))

    circuit.append(tgqs.rz(qubit1, -np.pi))
    circuit.append(tgqs.rz(qubit2, -np.pi))
    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.sqrt_x(qubit2))
    circuit.append(tgqs.rz(qubit1, -np.pi))
    circuit.append(tgqs.rz(qubit2, -np.pi))
    return circuit

def Rzz(theta, qubit1, qubit2, width):
    circuit = tgqs.QuantumCircuit(width)
    # circuit.append(tgqs.CNOT(qubit1, qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.cz(qubit1, qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.rz(qubit2, theta))
    # circuit.append(tgqs.CNOT(qubit1, qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.cz(qubit1, qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    return circuit

def Toff(qubit1, qubit2, qubit3, width):
    circuit = tgqs.QuantumCircuit(width)
    circuit.append(tgqs.rz(qubit2, np.pi/2))
    circuit.append(tgqs.sqrt_x(qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi/2))
    # circuit.append(tgqs.CNOT(qubit1, qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.cz(qubit1, qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))

    circuit.append(tgqs.rz(qubit2, -np.pi/4))
    # circuit.append(tgqs.CNOT(qubit3, qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.cz(qubit3, qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))

    circuit.append(tgqs.rz(qubit2, np.pi/4))
    # circuit.append(tgqs.CNOT(qubit1, qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.cz(qubit1, qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))

    circuit.append(tgqs.rz(qubit1, np.pi/4))
    circuit.append(tgqs.rz(qubit2, -np.pi/4))
    # circuit.append(tgqs.CNOT(qubit3, qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.cz(qubit3, qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))

    circuit.append(tgqs.rz(qubit2, np.pi*3/4))
    circuit.append(tgqs.sqrt_x(qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi/2))
    # circuit.append(tgqs.CNOT(qubit3, qubit2))
    # circuit.append(tgqs.CNOT(qubit2, qubit3))
    # circuit.append(tgqs.CNOT(qubit3, qubit2))
    # circuit.append(tgqs.CNOT(qubit2, qubit1))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.cz(qubit3, qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))

    circuit.append(tgqs.rz(qubit3, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit3))
    circuit.append(tgqs.rz(qubit3, np.pi / 2))
    circuit.append(tgqs.cz(qubit2, qubit3))
    circuit.append(tgqs.rz(qubit3, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit3))
    circuit.append(tgqs.rz(qubit3, np.pi / 2))

    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.cz(qubit3, qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit2))
    circuit.append(tgqs.rz(qubit2, np.pi / 2))

    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.cz(qubit2, qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.rz(qubit1, -np.pi/4))
    circuit.append(tgqs.rz(qubit2, np.pi/4))
    # circuit.append(tgqs.CNOT(qubit2, qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.cz(qubit2, qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    circuit.append(tgqs.sqrt_x(qubit1))
    circuit.append(tgqs.rz(qubit1, np.pi / 2))
    return circuit
