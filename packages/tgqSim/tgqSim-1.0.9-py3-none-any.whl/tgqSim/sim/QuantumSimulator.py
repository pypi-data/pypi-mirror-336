"""
-*- coding: utf-8 -*-
@Author : Cui Jinghao
@Time : 2024/6/28 14:43
@Function: quantum simulator.py
@Contact: cuijinghao@tgqs.net
"""

import tgqSim.utils.dev_tools as dev_tools
from tgqSim.circuit.common_gates import (BASE_SINGLE_GATE,
                                               BASE_DOUBLE_GATE,
                                               BASE_TRIPLE_GATE,
                                               MEASURE,
                                               BASE_SINGLE_GATE_MAP,
                                               BASE_DOUBLE_GATE_MAP,
                                               BASE_TRIPLE_GATE_MAP)
from tgqSim.device.noise_models import NOISE_MAPPER, NOISE_TYPE

import tgqSim.device.noise_util as noise_util
from tgqSim.circuit.QuantumCircuit import QuantumCircuit
# import simulator_utils
import os
from typing import Union
import GPUtil
import ctypes
import numpy as np


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


class SimulationError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class QuantumSimulator:

    def __init__(self):
        self.qbit_list = []
        self.state = []
        self.deviceid = []
        self.prob_result = {}

    def set_gpu_device_withlist(self, deviceList: Union[int, list]):
        gpus = GPUtil.getGPUs()
        gpuidList = [gpu.id for gpu in gpus]
        if isinstance(deviceList, int):
            deviceList = [deviceList]
        for deviceid in deviceList:
            if deviceid not in gpuidList:
                raise ValueError("设置设备ID不存在")
        # self.isgpu = True
        # todo: can only run with one kind of device at a time?
        # self.isnpu = False
        self.deviceid = deviceList

    # todo: add a function that does not need devicelist input?
    # todo: expose gpu device list to user?
    def set_gpu_device(self):
        gpus = GPUtil.getGPUs()
        self.deviceid = [gpu.id for gpu in gpus]

    # todo: add set npu device method later
    def set_npu_device(self):
        pass
        # self.isnpu = True
        # self.isgpu = False

    # def validate_obj(self):
    #     if isinstance(self.circuit, QuantumCircuit):
    #         pass

    def _run_with_dcu_device(self, circuit: QuantumCircuit):
        lib = dev_tools.get_dcu_lib()
        lib.execute_circuit.argtypes = [
            ctypes.POINTER(ctypes.POINTER(Double2)),
            ctypes.POINTER(GateInfo),
            ctypes.c_int,
            ctypes.c_int,
            ctypes.POINTER(ctypes.c_int)
        ]
        lib.execute_circuit.restype = None
        gateInfo = []
        for (gate_pos, gate_info) in circuit.gate_list:
            # todo: add an if to check whether gate is measure gate
            if gate_info[0].lower() in MEASURE:
                continue
            elif isinstance(gate_pos, int):
                length = 2
                gate_pos = [gate_pos]
            elif isinstance(gate_pos, list):
                length = len(gate_pos) + 1
            else:
                raise TypeError("Type of gate_pos must be int or list")
            gate_obj = GateInfo()
            actionPos = gate_pos + [-1]
            gate_obj.actionPos = (ctypes.c_int * length)(*actionPos)
            if len(gate_info) > 0:
                gate_obj.gateName = gate_info[0].encode(encoding='utf-8')
            if len(gate_info) > 1:
                gate_obj.theta = gate_info[1]
            gateInfo.append(gate_obj)
        gateInfoCData = (GateInfo * len(gateInfo))(*gateInfo)
        deviceIdCData = (ctypes.c_int * len(self.deviceid))(*self.deviceid)
        # 申请内存首地址，不在Python端申请内存
        # 在C语言中申请统一内存，减少多次拷贝动作
        # todo: separate pointer applying out or not?
        state = ctypes.POINTER(Double2)()
        lib.execute_circuit(ctypes.byref(state), gateInfoCData, len(gateInfo), circuit.width, deviceIdCData)
        # iStart = datetime.datetime.now()
        # print(f"start time is {iStart}")
        state = np.ctypeslib.as_array(state, shape=(2 ** circuit.width,))
        py_state = state.view(np.complex128)
        # clear mem for C++ side
        # lib.freeAllMem(state)
        # print(f"total time of changing type is {(datetime.datetime.now() - iStart).total_seconds()} secs")
        return py_state

    # todo: add run with npu device later
    def _run_with_gpu_device(self, circuit: QuantumCircuit):
        self.set_gpu_device()
        lib = dev_tools.get_cuda_lib()
        lib.execute_circuit.argtypes = [
            ctypes.POINTER(ctypes.POINTER(Double2)),
            ctypes.POINTER(GateInfo),
            ctypes.c_int,
            ctypes.c_int,
            ctypes.POINTER(ctypes.c_int)
        ]
        lib.execute_circuit.restype = None
        gateInfo = []
        for (gate_pos, gate_info) in circuit.gate_list:
            # todo: add an if to check whether gate is measure gate
            if gate_info[0].lower() in MEASURE:
                continue
            elif isinstance(gate_pos, int):
                length = 2
                gate_pos = [gate_pos]
            elif isinstance(gate_pos, list):
                length = len(gate_pos) + 1
            else:
                raise TypeError("Type of gate_pos must be int or list")
            gate_obj = GateInfo()
            actionPos = gate_pos + [-1]
            gate_obj.actionPos = (ctypes.c_int * length)(*actionPos)
            if len(gate_info) > 0:
                gate_obj.gateName = gate_info[0].encode(encoding='utf-8')
            if len(gate_info) > 1:
                gate_obj.theta = gate_info[1]
            gateInfo.append(gate_obj)
        gateInfoCData = (GateInfo * len(gateInfo))(*gateInfo)
        # 以-1作为结尾
        deviceId = self.deviceid + [-1]
        deviceIdCData = (ctypes.c_int * len(deviceId))(*deviceId)
        # 申请内存首地址，不在Python端申请内存
        # 在C语言中申请统一内存，减少多次拷贝动作
        # todo: separate pointer applying out or not?
        state = ctypes.POINTER(Double2)()
        lib.execute_circuit(ctypes.byref(state), gateInfoCData, len(gateInfo), circuit.width, deviceIdCData)
        # iStart = datetime.datetime.now()
        # print(f"start time is {iStart}")
        state = np.ctypeslib.as_array(state, shape=(2 ** circuit.width,))
        py_state = state.view(np.complex128)
        # clear mem for C++ side
        # lib.freeAllMem(state)
        # print(f"total time of changing type is {(datetime.datetime.now() - iStart).total_seconds()} secs")
        return py_state

    # def _run_in_python(self, circuit: QuantumCircuit):

    def _run_with_npu_device(self, circuit: QuantumCircuit):
        import torch
        from tgqSim.NpuGate import SingleGate, DoubleGate, TripleGate
        state = [1 if a == 0 else 0 for a in range(2 ** circuit.width)]
        for (gate_pos, gate_info) in circuit.gate_list:
            # if it is a measure gate, then continue
            if gate_info[0].lower() in MEASURE:
                continue
            gate_type = gate_info[0]
            # last position of gate_info is display_name
            angle = tuple(gate_info[1:])
            if gate_type in BASE_SINGLE_GATE_MAP.keys() or gate_type.upper() in NOISE_MAPPER.values():
                state = SingleGate.ActOn_State(state,
                                                circuit.width,
                                                gate_type,
                                                gate_pos,
                                                *angle)

            elif gate_type in BASE_DOUBLE_GATE_MAP.keys():
                set_gate_pos = set(gate_pos)
                if len(set_gate_pos) != len(gate_pos):
                    raise SimulationError(f"Gate position cannot be the same: {gate_pos[0]}, {gate_pos[1]}")
                state = DoubleGate.ActOn_State(state,
                                                    circuit.width,
                                                    gate_type,
                                                    gate_pos,
                                                    *angle)
            elif gate_type in BASE_TRIPLE_GATE_MAP.keys():
                set_gate_pos = set(gate_pos)
                if len(set_gate_pos) != len(gate_pos):
                    raise SimulationError(f"Gate position cannot be the same: "
                                          f"{gate_pos[0]}, {gate_pos[1]} and {gate_pos[2]}")
                state = TripleGate.ActOn_State(state,
                                                    circuit.width,
                                                    gate_type,
                                                    gate_pos,
                                                    *angle)
            else:
                raise SimulationError(f"Unkown gate type: {gate_type}")
        # tensor to cpu
        state = torch.Tensor.cpu(state)
        return state


    def _run_with_cpu_device(self, circuit: QuantumCircuit):
        from tgqSim.CpuGate import SingleGate, DoubleGate, TripleGate
        # todo: watch out that length of state list grows exponentially with circuit width
        state = [1 if a == 0 else 0 for a in range(2 ** circuit.width)]
        for (gate_pos, gate_info) in circuit.gate_list:
            gate_type = gate_info[0]
            angle = tuple(gate_info[1:])
            # todo: if it is a measure gate, then continue
            if gate_info[0].lower() in MEASURE:
                continue

            # todo: check mapped noise gate
            elif gate_type in BASE_SINGLE_GATE_MAP.keys() or gate_type.upper() in NOISE_MAPPER.values():
                # todo: for noise gate gatetype should coordinate with CpuGate/SingleGate
                state = SingleGate.ActOn_State(state,
                                                circuit.width,
                                                gate_type,
                                                gate_pos,
                                                *angle)
                # if gate_type in NOISE_TYPE:
                #     state = SingleGate.ActOn_State()

            elif gate_type in BASE_DOUBLE_GATE_MAP.keys():
                set_gate_pos = set(gate_pos)
                if len(set_gate_pos) != len(gate_pos):
                    raise SimulationError(f"Gate position cannot be the same: {gate_pos[0]}, {gate_pos[1]}")
                state = DoubleGate.ActOn_State(state,
                                                    circuit.width,
                                                    gate_type,
                                                    gate_pos,
                                                    *angle)
            elif gate_type in BASE_TRIPLE_GATE_MAP.keys():
                set_gate_pos = set(gate_pos)
                if len(set_gate_pos) != len(gate_pos):
                    raise SimulationError(f"Gate position cannot be the same: "
                                          f"{gate_pos[0]}, {gate_pos[1]} and {gate_pos[2]}")
                state = TripleGate.ActOn_State(state,
                                                    circuit.width,
                                                    gate_type,
                                                    gate_pos,
                                                    *angle)
            else:
                raise SimulationError(f"Unkown gate type: {gate_type}")
        return state

    def run_with_noise(self, circuit: QuantumCircuit, shots:int=1000, device: str='cpu'):
        result_dict = {}
        tmp_circuit = circuit.gate_list
        for _ in range(shots):
            new_circuit = []
            for (gate_pos, gate_info) in circuit.noise_circuit:
                # todo: original noise type name
                if gate_info[0] in NOISE_TYPE:
                    # todo: parsed noise type name
                    noise_gate = noise_util.parse_noise(noise_type=gate_info[0], gate_pos=gate_pos, error_rate=gate_info[1])
                    # print(noise_gate)
                    if noise_gate is not None:
                        # new_circuit looks like this [(1, ('h',)), (1, ('amplitude_damp', 0.5))]
                        new_circuit.append(noise_gate)
                else:
                    new_circuit.append((gate_pos, gate_info))
            # print("new_circuit:", new_circuit)
            # todo: check last element of original gate_list, if not measure all bit position
            if tmp_circuit[-1][1][0].lower() == 'measure':
                circuit.gate_list = new_circuit + [(tmp_circuit[-1][0], ('measure', ))]
            else:
                circuit.gate_list = new_circuit
            result = self.execute(circuit, shots=1000, device=device)
            # print(result)
            # print(self.state)
            for key in result.keys():
                if key in result_dict:
                    result_dict[key] += result[key]
                else:
                    result_dict[key] = result[key]
        circuit.gate_list = tmp_circuit

        prob_result = dev_tools.get_normalization(frequency=result_dict)
        # freq_result = self.prob_to_freq(prob_result, shots)
        freq_result = result_dict
        return prob_result, freq_result

    # added npu option
    # todo: add a parameter to identify which device to use
    def run_statevector(self, circuit: QuantumCircuit, device: str = 'cpu'):
        """
        根据线路的门序列计算末态的量子态
        :return:
        """
        if device.upper() == 'GPU':
            return self._run_with_gpu_device(circuit)
        if device.upper() == 'NPU':
            return self._run_with_npu_device(circuit)
        if device.upper() == 'CPU':
            return self._run_with_cpu_device(circuit)
        if device.upper() == 'DCU':
            return self._run_with_dcu_device(circuit)

    @staticmethod
    def freq_to_prob(result: dict):
        shots = sum(result.values())
        prob = {}
        for res, freq in result.items():
            prob[res] = float(freq/shots)
        return prob

    @staticmethod
    def prob_to_freq(result: dict, shots: int):
        freq = {}
        for state, prob in result.items():
            freq[state] = int(prob * shots)
        return freq

    # add device parameter to measure function to identify which device to use
    def execute(self, circuit: QuantumCircuit, shots: int = 1000, device:str='cpu') -> dict:
        """
        execute simulation
        Args:
            circuit:
            # measure_bits_list: 测量比特列表，传入比特位置或列表位置
            shots: 测量次数
            device: cpu, npu or gpu
        Returns:
            result: 返回测量结果
        """
        if shots <= 0:
            raise Exception("Experiment shots cannot be less than or equal to 0!")
        # 首先通过执行操作得到所有的状态
        # print(self.gate_list)
        state = self.run_statevector(circuit, device)
        state = np.array(state)
        # print(state)
        prob = np.real(state.conjugate() * state)
        # e.g. count = {'000': 0, '001': 0, '010': 1, '011': 0, '100': 0, '101': 0, '110': 0, '111': 0}
        count = {format(i, f'0{circuit.width}b'): prob[i] for i in range(len(prob))}
        # print('new count {}'.format(count))
        distribution = {}
        measure_bits_list = None
        # {gatename: position}
        if circuit.measure_pos_list and len(circuit.measure_pos_list[0]) > 0:
            # print(gate_dict)
            measure_bits_list = sorted(circuit.width - 1 - i for i in circuit.measure_pos_list[0])
        if measure_bits_list is None or measure_bits_list == []:  # 若为空默认测量所有可能
            # bugfix, comment this line
            # distribution = count
            measure_bits_list = sorted([_ for _ in range(circuit.width)])
            # print(measure_bits_list)
        if isinstance(measure_bits_list, int):
            measure_bits_list = [measure_bits_list]

        # print('new measure bit {}'.format(measure_bits_list))
        # 计算测量分布
        for p in count.keys():
            # key = ''.join(p[pos - 1] for pos in measure_bits_list)
            key = ''.join(p[pos] for pos in measure_bits_list)
            if count[p] == 0:
                continue
            if key not in distribution:
                distribution[key] = count[p]
            else:
                distribution[key] += count[p]
        # print('new distribution {}'.format(distribution))
        # 根据分布抽样概率
        result = {}
        cumulate = 0
        sample = np.random.uniform(0, 1, size=shots)
        for key in distribution.keys():
            new_cumulate = cumulate + distribution[key]
            result[key] = sum((cumulate <= sample) & (sample < new_cumulate))
            cumulate = new_cumulate
        return result
