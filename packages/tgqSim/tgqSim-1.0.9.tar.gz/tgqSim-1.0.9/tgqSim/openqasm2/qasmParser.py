"""
-*- coding: utf-8 -*-
@Author : Cui Jinghao
@Time : 2024/7/18 15:25
@Function: qasmParser.py
@Contact: cuijinghao@tgqs.net
"""


import re
from tgqSim.circuit.QuantumCircuit import QuantumCircuit as qc
from tgqSim.circuit.common_gates import (BASE_SINGLE_GATE,
                                               BASE_DOUBLE_GATE,
                                               BASE_TRIPLE_GATE,
                                               MEASURE,
                                               BASE_SINGLE_GATE_MAP,
                                               BASE_DOUBLE_GATE_MAP,
                                               BASE_TRIPLE_GATE_MAP)
import importlib
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.getcwd())))
# MODULE = importlib.import_module('..common_gates', 'circuit.common_gates')
MODULE = importlib.import_module('.common_gates', 'tgqSim.circuit')
# print(MODULE)
QASM_REG = ['qreg']
QASM_FORMAT = ['openqasm']
ABRV_GATE = {'cphase': 'cp'}


class QASMParser:
    def __init__(self, qasm_code: str):
        self.qasm_code = qasm_code
        self.lines = self.qasm_code.split('\n')
        self.circuit = qc()
        # self.qubits = {}
        # self.bits = {}

    def parse(self):
        # todo: receives an ast string and returns a quantumcircuit object
        # todo: add more operations like if and or in the future
        measure_list = []
        for line in self.lines:
            line = line.strip()
            # todo: change regex method
            # todo: regex for u3 gate
            # get operation from the line
            # this regex get the command
            # e.g. qreg q[5] - > qreg; u3(0.5,0.5,0.5) q[0] -> u3(0.5,0.5,0.5);
            # command = re.match(r'^([a-zA-Z]+\(?[-\d.]*\)?)', line)
            command = re.match(r'^([a-zA-Z]+\d*)(\(?[^)]*\)?)', line)

            qbits = list(map(int, re.findall(r'q\[(\d+)\]', line)))
            # if command:
            #     print('command is : {}'.format(command.group(1)))
            if command and qbits:
                command = command.group(1).lower()
                # print('command initial is {}'.format(command))
                # check whether command has theta parameter, e.g. rz(pi)
                if command in ABRV_GATE.keys():
                    command = ABRV_GATE[command]

                theta_flag = re.match(r'^([a-zA-Z]+\d*)\(([^)]+)\)', line)
                theta = None
                # print('theta flag {}'.format(theta_flag))
                if theta_flag:
                    # command = theta_flag.group(1)
                    # e.g. str: 0.708, 0.708, 0.708
                    theta = theta_flag.group(2)
                    lst = []
                    for _ in theta.split(','):
                        lst.append(float(_.strip()))
                    theta = tuple(lst)

                # print('theta after theta checking is {}'.format(theta))
                # print('theta type after theta checking is {}'.format(type(theta)))
                # print('command after theta checking is {}'.format(command))
                if command in QASM_FORMAT:
                    continue
                elif command in QASM_REG:
                    # e.g. qreg q[10]
                    self.circuit.add_qubits(qbits[0])
                elif command in BASE_SINGLE_GATE_MAP.keys():
                    gate = getattr(MODULE, BASE_SINGLE_GATE_MAP[command])
                    # instantiate
                    gate = gate()
                    if theta:
                        # u1
                        if len(theta) == 1:
                            self.circuit.append(gate(qbits[0], theta[0]))
                        # u2
                        elif len(theta) == 2:
                            self.circuit.append(gate(qbits[0], theta[0], theta[1]))
                        # u3
                        elif len(theta) == 3:
                            self.circuit.append(gate(qbits[0], theta[0], theta[1], theta[2]))
                    else:
                        self.circuit.append(gate(qbits[0]))
                elif command in BASE_DOUBLE_GATE_MAP.keys():
                    gate = getattr(MODULE, BASE_DOUBLE_GATE_MAP[command])
                    gate = gate()
                    if theta is not None:
                        self.circuit.append(gate(qbits[0], qbits[1], theta[0]))
                        print(gate)
                    else:
                        self.circuit.append(gate(qbits[0], qbits[1]))
                elif command in BASE_TRIPLE_GATE_MAP.keys():
                    pass
                elif command in MEASURE:
                    measure_list += qbits
        if measure_list and measure_list != []:
            gate = getattr(MODULE, MEASURE[0])
            gate = gate(measure_list)
            self.circuit.append(gate)
        return self.circuit

    def _parse_measurement(self, line):
        match = re.match(r'measure (\w+) -> (\w+);', line)
        if match:
            qubit_name = match.group(1)
            bit_name = match.group(2)
            self.circuit.append(f"Measure {qubit_name} to {bit_name}")

    def _parse_if_statement(self, line):
        # 示例解析if语句
        pass

    def _parse_for_loop(self, line):
        # 示例解析for循环
        pass

    def _parse_function_definition(self, line):
        # 示例解析函数定义
        pass

# qasm_code =  """
# OPENQASM 2.0;
# qreg q[3];
# h q[0];
# cx q[0], q[1];
# toffoli q[0], q[1], q[2];
# rz(0.708) q[0];
# rz(0) q[0];
# rz(-0.5) q[0];
# u3(0.708, 0.708, 0.708) q[1];
# measure q[0] ;
# measure q[1] ;
# """
# print(QASMParser(qasm_code).parse().gate_list)

