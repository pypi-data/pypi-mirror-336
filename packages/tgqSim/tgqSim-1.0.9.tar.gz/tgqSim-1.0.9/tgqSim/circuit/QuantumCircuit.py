#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Modifider: Cui Jinghao
@contact: cuijinghao@tgqs.net
@file: QuantumCircuit.py
@time: 2024/06/28 14:40

reconstructed quantum circuit file
"""
import tgqSim
from tgqSim.circuit.common_gates import CommonGate
from tgqSim.circuit.param_gates import ParamGates
import tgqSim.draw_circuit_tools as tools
from tgqSim.circuit.common_gates import (BASE_SINGLE_GATE,
                                               BASE_DOUBLE_GATE,
                                               BASE_TRIPLE_GATE,
                                               MEASURE, )
from tgqSim.device.noise_models import NOISE_MAPPER
from tgqSim.utils.visualization import to_text_diag
from tgqSim.utils.logger import Logger
import logging
from typing import Union
import random, os, ctypes
import numpy as np
import matplotlib.pyplot as plt
import importlib
from enum import Enum
# import GPUtil, datetime
# from numba import njit, prange

# log = Logger(name="tgqsim", level=logging.DEBUG, log_file="app.log")

MODULE = importlib.import_module('.common_gates', 'tgqSim.circuit')


class Float2(ctypes.Structure):
    _fields_ = [("x", ctypes.c_float),
                ("y", ctypes.c_float)]

class Double2(ctypes.Structure):
    _fields_ = [("x", ctypes.c_double),
                ("y", ctypes.c_double)]

class GateInfo(ctypes.Structure):
    _fields_ = [
        ("gateName", ctypes.c_char_p),
        ("actionPos", ctypes.POINTER(ctypes.c_int)),
        ("theta", ctypes.c_double)
    ]

class NoiseType(str, Enum):
    BIT_FLIP = "bit_flip"
    DEPOLARIZE = "depolarize"
    PHASE_FLIP = "phase_flip"
    PHASE_DAMP = "phase_damp"
    AMPLITUDE_DAMP = "amplitude_damp"


class Qubit:
    def __init__(self, name=None, idx=None, pos=None):
        self.label = 'p' if not name else name
        self.name = f'p_{idx+100}' if not name else f"{name}_{idx}"
        self.pos = pos + idx
        self.idx = idx

    # def __getattr__(self, item):
    #     if item == self.name:
    #         return self.idx
    #     if item == self.label+"["+str(self.pos)+"]":
    #         return self.idx

    def __str__(self):
        return str(self.name)


class QuantumCircuit:
    def __init__(self, qbit_number=0):
        self.qbit_list = []
        self.cbit_list = []
        self.gate_list = []
        self.qbit_register = {}
        self.width = qbit_number
        self.state = []
        self.circuit_diag = []
        # self.isgpu = False
        # self.isnpu = False
        self.noise_circuit = []
        self.current_gate_info = ()
        self.diagram_str = []
        # contains gates's display_names
        self.displayname_list = []
        self.measure_pos_list = [[], [], []]

    # todo: implement a visualization method for circuit, use displayname_list to denote
    def __str__(self):
        # sum up gate list and measure list
        # all_display_name_list = self.displayname_list + [
        #     (
        #         self.measure_pos_list[0],
        #         tuple(self.measure_pos_list[1]),
        #         (self.measure_pos_list[2],)
        #     )
        # ] if self.measure_pos_list else self.displayname_list and len(self.displayname_list[0]) > 0
        if self.measure_pos_list and len(self.measure_pos_list[0]) > 0:
            new_entry = (
                self.measure_pos_list[0],
                tuple(self.measure_pos_list[1]),
                (self.measure_pos_list[2],)
            )
            all_display_name_list = self.displayname_list + [new_entry]
        else:
            if self.displayname_list and len(self.displayname_list[0]) > 0:
                all_display_name_list = self.displayname_list
            else:
                all_display_name_list = []
        # print('all display name list: ', all_display_name_list)
        return to_text_diag(all_display_name_list, self.width)

    def _add_single_gate(self, gate_pos: Union[int, str], display_name: tuple, *gate_info):
        """
        添加单比特门序列
        :param gate_pos:
        :param gate_info: 门类型，门参数
        :param display_name:
        :return:
        """
        tmp_pos = gate_pos
        if isinstance(gate_pos, list):
            tmp_pos = gate_pos[0]
        if tmp_pos < 0 or tmp_pos >= self.width:
            raise ValueError("添加的位置不能为负数或不能超过线路设置的比特数")
        if len(gate_info) >= 1:
            if gate_info[0] not in BASE_SINGLE_GATE:
                raise ValueError("添加的门名称在框架支持中，请检查添加门的名称")
        if isinstance(gate_pos, int):
            gatename = gate_info[0].upper()
            self.circuit_diag.append([(gatename, gate_pos)])
        else:
            gatename = gate_info[0].upper()
            self.circuit_diag.append([(gatename, int(gate_pos))])

        self.current_gate_info = (gate_pos, gate_info)
        self.noise_circuit.append((gate_pos, gate_info))
        self.gate_list.append((gate_pos, gate_info))
        self.displayname_list.append((gate_pos, display_name, gate_info))
        # print("over")
        return self
        # todo 通过比特名称访问
        # if isinstance(gate_pos, str):
        #     return self.gate_list.append((gate_pos, gate_type))

    def _add_double_gate(self, gate_pos_0:int, gate_pos_1: int, display_name: str, *gate_info):
        """
        添加两比特门序列
        :param gate_pos_0: 控制位
        :param gate_pos_1: 目标位
        :param gate_info: 门类型，门参数
        :param display_name:
        :return:
        """
        # print('actual displayname: ', display_name)
        # print('actual gate name: ', gate_info)
        min_pos, max_pos = min([gate_pos_0, gate_pos_1]), max([gate_pos_0, gate_pos_1])
        if min_pos < 0 or max_pos >= self.width:
            raise ValueError("添加的位置不能为负数或不能超过线路设置的比特数")
        if len(gate_info) >= 1:
            if gate_info[0] not in BASE_DOUBLE_GATE:
                raise ValueError("添加的门名称在框架支持中，请检查添加门的名称")
        if gate_info[0] in ["rxx", 'ryy', 'rzz', 'iswap', 'syc']:
            self.circuit_diag.append([(gate_info[0].upper(), (gate_pos_1, gate_pos_0))])
        else:
            self.circuit_diag.append([(gate_info[0].upper(), gate_pos_1, gate_pos_0)])
        self.current_gate_info = ([gate_pos_0, gate_pos_1], gate_info)
        self.noise_circuit.append(([gate_pos_0, gate_pos_1], gate_info))
        self.gate_list.append(([gate_pos_0, gate_pos_1], gate_info))
        self.displayname_list.append(([gate_pos_0, gate_pos_1], display_name, gate_info))
        return self

    def _add_triple_gate(self, gate_pos: list, display_name: str, *gate_info):
        """
        添加三比特门序列
        :param gate_pos:
        :param gate_info:
        :param display_name:
        :return:
        """
        min_pos, max_pos = min(gate_pos), max(gate_pos)
        if min_pos < 0 or max_pos >= self.width:
            raise ValueError("添加的位置不能为负数或不能超过线路设置的比特数")
        if len(gate_info) >= 1:
            if gate_info[0] not in BASE_TRIPLE_GATE:
                raise ValueError("添加的门名称在框架支持中，请检查添加门的名称")
        self.circuit_diag.append([(gate_info[0].upper(), gate_pos[2], gate_pos[0], gate_pos[1])])
        self.current_gate_info = (gate_pos, gate_info)
        self.noise_circuit.append((gate_pos, gate_info))
        self.gate_list.append((gate_pos, gate_info))
        self.displayname_list.append((gate_pos, display_name, gate_info))
        return self

    def _add_measure_gate(self, gate_pos: Union[list, int], display_name: tuple, *gate_info):
        if isinstance(gate_pos, list):
            min_pos, max_pos = min(gate_pos), max(gate_pos)
        else:
            min_pos, max_pos = gate_pos, gate_pos
        if min_pos < 0 or max_pos >= self.width:
            raise ValueError("添加的位置不能为负数或不能超过线路设置的比特数")
        if len(gate_info) >= 1:
            if gate_info[0] not in MEASURE:
                raise ValueError("添加的门名称在框架支持中，请检查添加门的名称")
        if isinstance(gate_pos, int):
            gate_pos = [gate_pos]
        # todo: 每次加新的测量门时候，先检测线路是否已经有测量门，如果不存在就直接加，如果已经存在，那么需要把measuregate的pos加长，displayname也得加长，并且需要去重
        # # self._add_measure_gate(gate['qbit'], gate['name'])
        # [[0,2,3], ['Measure', 'Measure', 'Measure'], 'measure']
        if self.measure_pos_list and self.measure_pos_list[0] and len(self.measure_pos_list[0]) > 0:
            self.measure_pos_list[0] += gate_pos
            self.measure_pos_list[0] = list(set(self.measure_pos_list[0]))
            self.measure_pos_list[1] = [display_name[0]] * len(self.measure_pos_list[0])
        else:
            self.measure_pos_list = [gate_pos, list(display_name), gate_info]
        # todo: save measure position list to measure_pos_list attribute
        self.gate_list.append((gate_pos, gate_info))
        # self.displayname_list.append((gate_pos, display_name, gate_info))
        return self

    def append_with_params(self, gate: ParamGates):
        if isinstance(gate.gate_pos, int):
            gate_pos = (gate.gate_pos,)
        else:
            gate_pos = gate.gate_pos
        if gate.gate_name in BASE_SINGLE_GATE:
            gate_instance = getattr(MODULE, gate.gate_name)
            if gate.gate_params is None:
                self.append(gate_instance(gate_pos[0]))
            else:
                self.append(gate_instance(gate.gate_pos[0], gate.gate_params))
        elif gate.gate_name in BASE_DOUBLE_GATE:
            gate_instance = getattr(MODULE, gate.gate_name)
            # print('gate name: {}, gate pos: {}'.format(gate))

            if gate.gate_params is None:
                self.append(gate_instance(gate_pos[0], gate_pos[1]))
            else:
                self.append(gate_instance(gate_pos[0], gate_pos[1], gate.gate_params))
        else:
            raise Exception('gate type not supported yet')

    def append(self, gate: CommonGate):
        """
        append gate to circuit
        Returns:
        three options: single,double and triple

        """
        # print(gate)

        # if gate['name'] in MEASURE:
        # print('actual gate: name {}, displayname {}'.format(gate.name, gate.display_name))
        if gate.name in MEASURE:
            self._add_measure_gate(gate.qbit, gate.display_name, gate.name)

        # elif gate['name'] in BASE_SINGLE_GATE:
        elif gate.name in BASE_SINGLE_GATE:

            # if gate['theta'] is None:
            if gate.theta is None:

                self._add_single_gate(gate.qbit, gate.display_name, gate.name)

            else:
                if isinstance(gate.theta, tuple):
                    self._add_single_gate(gate.qbit,
                                         gate.display_name,
                                         gate.name,
                                         *gate.theta)
                else:
                    # print('gate theta before append is {}'.format(gate['theta']))
                    self._add_single_gate(gate.qbit, gate.display_name ,gate.name, gate.theta)

        elif gate.name in BASE_DOUBLE_GATE:
            if not gate.theta:
                self._add_double_gate(gate.qbit[0], gate.qbit[1], gate.display_name, gate.name)
            else:
                self._add_double_gate(gate.qbit[0], gate.qbit[1], gate.display_name,
                                     gate.name, gate.theta)

        elif gate.name in BASE_TRIPLE_GATE:
            if not gate.theta:
                self._add_triple_gate(gate.qbit, gate.display_name, gate.name)
        # if gate.noise is not None:
        #     pass
        #     # noise looks like this [(qbit, (noise_type, error_rate))
        #     self.with_noise(gate.noise[0], gate.noise[1][0], gate.noise[1,1])

    def append_circuit(self, circuit: "QuantumCircuit"):
        """compose: append circuit to current circuit"""
        self.gate_list += circuit.gate_list
        self.noise_circuit += circuit.noise_circuit
        self.displayname_list += circuit.displayname_list
        self.width = max(self.width, circuit.width)
        if circuit.measure_pos_list and  len(circuit.measure_pos_list[0]) > 0:
            self.measure_pos_list[0] = list(set(self.measure_pos_list[0] + circuit.measure_pos_list[0]))
            # [[0,2,3], ['Measure', 'Measure', 'Measure'], 'measure']
            self.measure_pos_list[1] = [circuit.measure_pos_list[1][0]] * len(self.measure_pos_list[0])
            self.measure_pos_list[2] = circuit.measure_pos_list[2]

    def add_qubits(self, number: int, name: str = 'p'):
        """
        添加量子比特
        :param number: 比特数量
        :param name: 比特名称
        :return:
        """
        self.width += number
        if name not in self.qbit_register:
            self.qbit_register.update({name: number})
            sub_list = [Qubit(name=name, idx=i, pos=i+self.width) for i in range(number)]
        else:
            former_number = self.qbit_register[name]
            self.qbit_register.update({name: number+former_number})
            sub_list = [Qubit(name=name, idx=i+former_number, pos=i+self.width) for i in range(number)]
        self.qbit_list.append(sub_list)

    # moved setdevice method to simulator class

    # todo: add noise to each gate instead of to the whole circuit
    def with_noise(self, qbit:Union[list, int], noise_type: NoiseType, error_rate:Union[float, list]):
        """
        将当前的所有控制门都加上noise_type类型的噪声

        Args:
            noise_type (str): 噪声类型: "bit_flip","depolarize", "phase_flip", "phase_damp", "amplitude_damp"
            error_rate (Union[float, list]): 错误率
        """
        # self.noise_circuit += [self.current_gate_info]
        # gate_pos = self.current_gate_info[0]
        gate_pos = qbit
        if isinstance(gate_pos, int):
            self.noise_circuit += [(gate_pos, (noise_type, error_rate))]
            # self.circuit_diag.append([(NOISE_MAPPER[noise_type], gate_pos)])
        else:
            for gate in gate_pos:
                self.noise_circuit += [(gate, (noise_type, error_rate))]
                # self.circuit_diag.append([(NOISE_MAPPER[noise_type], gate)])

    def reserve_circuit(self):
        """
        反转线路
        :return:
        """
        self.gate_list = self.gate_list[::-1]
        self.displayname_list = self.displayname_list[::-1]
        self.noise_circuit = self.noise_circuit[::-1]
        return self



    def random_circuit(self, num_qubits, num_gates: Union[int, list]):
        """
        生成随机线路
        :param num_qubits:
        :param num_gates: 门数量，列表表示单比特，多比特门数量
        :return:
        """
        self.width = num_qubits
        if isinstance(num_gates, int):
            base_gate_list = BASE_SINGLE_GATE + BASE_DOUBLE_GATE + BASE_TRIPLE_GATE
            for _ in range(num_gates):
                gate_type = np.random.choice(base_gate_list)
                angle = np.random.uniform(-2*np.pi, 2*np.pi, size=3)
                if gate_type in BASE_SINGLE_GATE:
                    gate_pos = np.random.choice(np.array(range(num_qubits)), size=1)[0]
                elif gate_type in BASE_DOUBLE_GATE:
                    gate_pos = random.sample(range(num_qubits), 2)
                    gate_pos = list(gate_pos)
                elif gate_type in BASE_TRIPLE_GATE:
                    gate_pos = random.sample(range(num_qubits), 3)
                    gate_pos = list(gate_pos)
                else:
                    gate_pos = None
                self.gate_list.append([gate_pos, tuple([gate_type]) + tuple(angle)])
        elif isinstance(num_gates, list):
            single_gate_num = num_gates[0]
            multiple_gate_num = num_gates[1]
            for _ in range(single_gate_num):
                gate_type = np.random.choice(BASE_DOUBLE_GATE)
                angle = np.random.uniform(-2*np.pi, 2*np.pi, size=3)
                gate_pos = np.random.choice(np.array(range(num_qubits)), size=1)[0]
                self.gate_list.append([gate_pos, tuple([gate_type]) + tuple(angle)])
            for _ in range(multiple_gate_num):
                base_gate_list = BASE_DOUBLE_GATE+BASE_TRIPLE_GATE
                gate_type = np.random.choice(base_gate_list)
                angle = np.random.uniform(-2 * np.pi, 2 * np.pi, size=3)
                if gate_type in BASE_DOUBLE_GATE:
                    gate_pos = random.sample(range(num_qubits), 2)
                    gate_pos = list(gate_pos)
                elif gate_type in BASE_TRIPLE_GATE:
                    gate_pos = random.sample(range(num_qubits), 3)
                    gate_pos = list(gate_pos)
                else:
                    gate_pos = None
                self.gate_list.append([gate_pos, tuple([gate_type]) + tuple(angle)])
                random.shuffle(self.gate_list)

    # def show_quantum_circuit(self, plot_labels=True, **kwargs):
    #     """Use Matplotlib to plot a quantum circuit.
    #     kwargs    Can override plot_parameters
    #     """
    #     labels = []
    #     inits = {}
    #     for i in range(self.width):
    #         labels.append(f"q_{i}")
    #         inits[f"q_{i}"] = i
    #     plot_params = dict(scale = 1.0, fontsize = 14.5, linewidth = 2.0,
    #                         control_radius = 0.05, not_radius = 0.15,
    #                         swap_delta = 0.08, label_buffer = 0.8,
    #                         rectangle_delta = 0.3, box_pad=0.2)
    #     plot_params.update(kwargs)
    #     scale = plot_params['scale']
    #
    #     # Create labels from gates. This will become slow if there are a lot
    #     #  of gates, in which case move to an ordered dictionary
    #     if not labels:
    #         labels = []
    #         for i,gate in tools.enumerate_gates(self.circuit_diag, schedule=True):
    #             for label in gate[1:]:
    #                 if label not in labels:
    #                     labels.append(label)
    #
    #     nq = len(labels)
    #     nt = len(self.circuit_diag)
    #     wire_grid = np.arange(0.0, nq*scale, scale, dtype=float)
    #     gate_grid = np.arange(0.0, nt*scale, scale, dtype=float)
    #     gate_grid_index = [0.0 for _ in range(nq)]
    #     # print(gate_grid_index)
    #
    #     fig,ax = tools.setup_figure(nq,nt,gate_grid,wire_grid,plot_params)
    #
    #     measured = tools.measured_wires(self.circuit_diag, labels, schedule=True)
    #     tools.draw_wires(ax, nq, gate_grid, wire_grid, plot_params, 'k', measured)
    #
    #     if plot_labels:
    #         tools.draw_labels(ax, labels, inits, gate_grid, wire_grid, plot_params, 'k')
    #
    #     tools.draw_gates(ax, self.circuit_diag, labels, gate_grid_index, wire_grid, plot_params, measured, schedule=True)
    #     plt.show()
        # return ax

    def show_quantum_circuit(self, plot_labels=True, **kwargs):
        """Use Matplotlib to plot a quantum circuit.
        kwargs    Can override plot_parameters
        """
        labels = []
        inits = {}
        for i in range(self.width):
            labels.append(f"q_{i}")
            inits[f"q_{i}"] = i
        plot_params = dict(scale=1.0, fontsize=14.5, linewidth=2.0,
                           control_radius=0.05, not_radius=0.15,
                           swap_delta=0.08, label_buffer=0.8,
                           rectangle_delta=0.3, box_pad=0.2)
        plot_params.update(kwargs)
        scale = plot_params['scale']

        # Create labels from gates. This will become slow if there are a lot
        #  of gates, in which case move to an ordered dictionary
        if not labels:
            labels = []
            for i, gate in tools.enumerate_gates(self.circuit_diag, schedule=True):
                for label in gate[1:]:
                    if label not in labels:
                        labels.append(label)

        nq = len(labels)
        nt = len(self.circuit_diag)
        wire_grid = np.arange(0.0, nq * scale, scale, dtype=float)
        gate_grid = np.arange(0.0, nt * scale, scale, dtype=float)
        gate_grid_index = [0.0 for _ in range(nq)]
        # print(gate_grid_index)

        fig, ax = tools.setup_figure(nq, nt, gate_grid, wire_grid, plot_params)

        measured = tools.measured_wires(self.circuit_diag, labels, schedule=True)
        tools.draw_wires(ax, nq, gate_grid, wire_grid, plot_params, 'k', measured)

        if plot_labels:
            tools.draw_labels(ax, labels, inits, gate_grid, wire_grid, plot_params, 'k')

        tools.draw_gates(ax, self.circuit_diag, labels, gate_grid_index, wire_grid, plot_params, measured,
                         schedule=True)
        plt.show()
        # return ax

