"""
-*- coding: utf-8 -*-
@Author : Cui Jinghao
@Time : 2024/6/28 15:49
@Function: common_gates
@Contact: cuijinghao@tgqs.net
"""
from typing import Union
from abc import abstractmethod
from copy import deepcopy

# global parameters
BASE_SINGLE_GATE = ['h', 'x', 'y', 'z', 'rx', 'ry', 'rz', 'u3', 's', 'sdg', 't', 'tdg', "damp_I", "pd", "ad", 'sqrt_x']
BASE_DOUBLE_GATE = ['cx', 'swap', 'iswap', 'cz', 'cp', 'rxx', 'ryy', 'rzz', 'syc']
BASE_TRIPLE_GATE = ['ccx', 'cswap']
CONTROLLED_GATE = ['cx', 'cz', 'cp', 'ccx', 'cswap']
ROTATION_GATE = ['rxx', 'ryy', 'rzz']
MEASURE = ['measure']
BASE_SINGLE_GATE_MAP = {'h': '_H', 'x': '_X', 'y': '_Y', 'z': '_Z',
                        'rx': '_RX', 'ry': '_RY', 'rz': '_RZ',
                        'u3': '_U3',
                        's': '_S', 'sdg': '_SDG', 't': '_T', 'tdg': '_TDG', 'sqrt_x': '_SQRT_X'}
BASE_DOUBLE_GATE_MAP = {'cx': '_CX', 'swap': '_SWAP', 'iswap': '_ISWAP',
                        'cz': '_CZ', 'cp': '_CP', 'rxx': '_RXX', 'ryy': '_RYY', 'rzz': '_RZZ', 'syc': '_SYC'}

BASE_TRIPLE_GATE_MAP = {'cswap': '_CSWAP', 'ccx': '_CCX'}

MEASURE_MAP = {'measure': '_Measure'}


# will implement more gates classes later
# will further abstract classes
class _CommonGate:
    def __init__(self, qbit=None, name=None, theta=None):
        self.qbit = qbit
        self.name = name
        self.theta = theta
    @abstractmethod
    def gate(self, *args, **kwargs):
        gate_instance = deepcopy(self)
        return gate_instance


CommonGate = _CommonGate()


class _Measure(_CommonGate):
    def __init__(self, qbit: Union[list, int] = 0, name: str = 'measure', theta=None):
        self.qbit = qbit
        self.name = name
        self.theta = theta
        if isinstance(qbit, int):
            self.display_name = ('Measure',)
        else:
            self.display_name = tuple(['Measure'] * len(self.qbit))

    def __call__(self, qbit):
        return self.gate(qbit)

    def gate(self, qbit):
        gate_instance = deepcopy(self)
        gate_instance.qbit = qbit
        if isinstance(qbit, int):
            gate_instance.display_name = ('Measure',)
        else:
            gate_instance.display_name = tuple(['Measure'] * len(gate_instance.qbit))
        return gate_instance


measure = _Measure()


class _I(_CommonGate):
    """
    eye matrix
    """
    def __init__(self, qbit: int = 0, name='I', theta=None):
        self.qbit = qbit
        self.name = name
        self.theta = theta
        self.display_name = ("I", )

    def __call__(self, qbit):
        return self.gate(qbit)

    def gate(self, qbit):
        gate_instance = deepcopy(self)
        gate_instance.qbit = qbit
        return gate_instance


I = _I()


class _Pauli(_CommonGate):
    def __init__(self):
        pass

    def __call__(self):
        return

    def gate(self):
        pass


class _X(_Pauli):
    # todo: add attribute noise
    def __init__(self, qbit: int = 0, name='x', theta=None):
        self.qbit = qbit
        self.name = name
        self.theta = theta
        self.display_name = ("X", )

    def __call__(self, qbit):
        return self.gate(qbit)

    def gate(self, qbit):
        gate_instance = deepcopy(self)
        gate_instance.qbit = qbit
        return gate_instance


x = _X()


class _SQRT_X(_Pauli):
    def __init__(self, qbit: int = 0, name='sqrt_x', theta=None):
        self.qbit = qbit
        self.name = name
        self.theta = theta
        self.display_name = ("X^½", )

    def __call__(self, qbit):
        return self.gate(qbit)

    def gate(self, qbit):
        gate_instance = deepcopy(self)
        gate_instance.qbit = qbit
        return gate_instance


sqrt_x = _SQRT_X


class _Y(_Pauli):
    def __init__(self, qbit=0, name='y', theta=None):
        self.qbit = qbit
        self.name = name
        self.theta = theta
        self.display_name = ("Y",)

    def __call__(self, qbit):
        return self.gate(qbit)

    def gate(self, qbit):
        gate_instance = deepcopy(self)
        gate_instance.qbit = qbit
        return gate_instance


y = _Y()


class _Z(_Pauli):
    def __init__(self, qbit=0, name='z', theta=None):
        self.qbit = qbit
        self.name = name
        self.theta = theta
        self.display_name = ("Z",)

    def __call__(self, qbit):
        return self.gate(qbit)

    def gate(self, qbit):
        gate_instance = deepcopy(self)
        gate_instance.qbit = qbit
        return gate_instance


z = _Z()


class _RX(_CommonGate):
    def __init__(self, qbit=0, name='rx', theta=0):
        self.qbit = qbit
        self.name = name
        self.theta = float(theta)
        self.display_name = (f"Rx({round(self.theta, 2)})",)

    def __call__(self, qbit, theta):
        return self.gate(qbit, theta)

    def gate(self, qbit, theta):
        gate_instance = deepcopy(self)
        gate_instance.qbit = qbit
        gate_instance.theta = float(theta)
        gate_instance.display_name = (f"Rx({round(gate_instance.theta, 2)})",)
        return gate_instance


rx = _RX()


class _RY(_CommonGate):
    def __init__(self, qbit=0, name='ry', theta=0):
        self.qbit = qbit
        self.name = name
        self.theta = float(theta)
        self.display_name = (f"Ry({round(self.theta, 2)})",)

    def __call__(self, qbit, theta):
        return self.gate(qbit, theta)

    def gate(self, qbit, theta):
        gate_instance = deepcopy(self)
        gate_instance.qbit = qbit
        gate_instance.theta = float(theta)
        gate_instance.display_name = (f"Ry({round(gate_instance.theta, 2)})",)
        return gate_instance


ry = _RY()


class _RZ(_CommonGate):
    def __init__(self, qbit=0, name='rz', theta=0):
        self.qbit = qbit
        self.name = name
        self.theta = float(theta)
        self.display_name = (f"Rz({round(self.theta, 2)})",)

    def __call__(self, qbit, theta):
        return self.gate(qbit, theta)

    def gate(self, qbit, theta):
        gate_instance = deepcopy(self)
        gate_instance.qbit = qbit
        gate_instance.theta = float(theta)
        gate_instance.display_name = (f"Rz({round(gate_instance.theta, 2)})",)
        return gate_instance


rz = _RZ()


# class _U3(_CommonGate):
#     def __init__(self, qbit=0, name='u3', *theta):
#         self.qbit = qbit
#         self.name = name
#         self.theta = theta
#
#     def __call__(self, qbit, *theta):
#
#         # print('len of theta tuple is {}, tuple is {}'.format(len(theta), theta))
#         if not theta or (theta and len(theta) != 3):
#             raise Exception('U3 gate requires 3 parameters, please check!')
#         # print('theta before calling gate is {}'.format(theta))
#         return self.gate(qbit, theta[0], theta[1], theta[2])
#
#     def gate(self, qbit, *theta):
#         # print('theta after initialization is {}'.format(theta))
#         self.qbit = qbit
#         self.theta = theta
#         return self
#
#
# u3 = _U3()


# class

class _H(_CommonGate):
    def __init__(self, qbit=0, name='h', theta=None):
        self.qbit = qbit
        self.name = name
        self.theta = theta
        self.display_name = ('H',)

    def __call__(self, qbit):
        return self.gate(qbit)

    def gate(self, qbit):
        gate_instance = deepcopy(self)
        gate_instance.qbit = qbit
        return gate_instance


h = _H()


class _S(_CommonGate):
    def __init__(self, qbit=0, name='s', theta=None):
        self.qbit = qbit
        self.name = name
        self.theta = theta
        self.display_name = ("S",)

    def __call__(self, qbit):
        return self.gate(qbit)

    def gate(self, qbit):
        gate_instance = deepcopy(self)
        gate_instance.qbit = qbit
        return gate_instance


s = _S()


class _SDG(_CommonGate):
    def __init__(self, qbit=0, name='sdg', theta=None):
        self.qbit = qbit
        self.name = name
        self.theta = theta
        self.display_name = ("SDG",)

    def __call__(self, qbit):
        return self.gate(qbit)

    def gate(self, qbit):
        gate_instance = deepcopy(self)
        gate_instance.qbit = qbit
        return gate_instance


sdg = _SDG()


class _T(_CommonGate):
    def __init__(self, qbit=0, name='t', theta=None):
        self.qbit = qbit
        self.name = name
        self.theta = theta
        self.display_name = ("T",)

    def __call__(self, qbit):
        return self.gate(qbit)

    def gate(self, qbit):
        gate_instance = deepcopy(self)
        gate_instance.qbit = qbit
        return gate_instance


t = _T()


class _TDG(_CommonGate):
    def __init__(self, qbit=0, name='tdg', theta=None):
        self.qbit = qbit
        self.name = name
        self.theta = theta
        self.display_name = ("TDG",)

    def __call__(self, qbit):
        return self.gate(qbit)

    def gate(self, qbit):
        gate_instance = deepcopy(self)
        gate_instance.qbit = qbit
        return gate_instance


tdg = _TDG()


# double gates ['cx', 'swap', 'iswap', 'cz', 'cp', 'rxx', 'ryy', 'rzz', 'syc']
class _CX(_CommonGate):
    """
    @explain: CNOT gate
    @params: by default, qbit0 is the controll bit
    @return: CNOT gate
    """
    # by default, qbit0 is the controll bit
    def __init__(self, qbit0=0, qbit1=1, name='cx', theta=None):
        self.qbit0 = qbit0
        self.qbit1 = qbit1
        self.qbit = None
        self.name = name
        self.theta = theta
        self.display_name = ("@", "X")

    def __call__(self, qbit0, qbit1):
        return self.gate(qbit0, qbit1)

    def gate(self, qbit0, qbit1):
        gate_instance = deepcopy(self)
        gate_instance.qbit = [qbit0, qbit1]
        return gate_instance


cx = _CX()


class _CZ(_CommonGate):
    def __init__(self, qbit0=0, qbit1=1, name='cz', theta=None):
        self.qbit0 = qbit0
        self.qbit1 = qbit1
        self.qbit = None
        self.name = name
        self.theta = theta
        self.display_name = ("@", "@")

    def __call__(self, qbit0, qbit1, theta=None):
        return self.gate(qbit0, qbit1, theta)

    def gate(self, qbit0, qbit1, theta=None):
        gate_instance = deepcopy(self)
        gate_instance.qbit = [qbit0, qbit1]
        return gate_instance


cz = _CZ()


class _CP(_CommonGate):
    """
    @params: first control, second target, third theta
    @returns: cphase gate
    @explanation: cphase gate

    """
    def __init__(self, qbit0=0, qbit1=1, name='cp', theta=0):
        self.qbit0 = qbit0
        self.qbit1 = qbit1
        self.qbit = None
        self.name = name
        self.theta = float(theta)
        self.display_name = ("@", f"@^{round(self.theta, 2)}")

    def __call__(self, qbit0, qbit1, theta):
        return self.gate(qbit0, qbit1, theta)

    def gate(self, qbit0, qbit1, theta):
        gate_instance = deepcopy(self)
        gate_instance.qbit = [qbit0, qbit1]
        gate_instance.theta = float(theta)
        gate_instance.display_name = ("@", f"@^{round(gate_instance.theta, 2)}")
        return gate_instance


cp = _CP()


class _SWAP(_CommonGate):
    def __init__(self, qbit0=0, qbit1=1, name='swap', theta=None):
        self.qbit0 = qbit0
        self.qbit1 = qbit1
        self.qbit = None
        self.name = name
        self.theta = theta
        self.display_name = ("x", "x")

    def __call__(self, qbit0, qbit1):
        return self.gate(qbit0, qbit1)

    def gate(self, qbit0, qbit1):
        gate_instance = deepcopy(self)
        gate_instance.qbit = [qbit0, qbit1]
        return gate_instance


swap = _SWAP()


class _ISWAP(_CommonGate):
    def __init__(self, qbit0: int = 0, qbit1: int = 1, name='iswap', theta=None):
        self.qbit0 = qbit0
        self.qbit1 = qbit1
        self.qbit = None
        self.name = name
        self.theta = theta
        self.display_name = ("iSwap", "iSwap")

    def __call__(self, qbit0, qbit1):
        return self.gate(qbit0, qbit1)

    def gate(self, qbit0, qbit1):
        gate_instance = deepcopy(self)
        gate_instance.qbit = [qbit0, qbit1]
        return gate_instance


iswap = _ISWAP()


class _RXX(_CommonGate):
    def __init__(self, qbit0=0, qbit1=1, name='rxx', theta=0):
        self.qbit0 = qbit0
        self.qbit1 = qbit1
        self.qbit = None
        self.name = name
        self.theta = float(theta)
        self.display_name = (f"Rxx({round(self.theta, 2)})", f"Rxx({round(self.theta, 2)})")

    def __call__(self, qbit0, qbit1, theta):
        return self.gate(qbit0, qbit1, theta)

    def gate(self, qbit0, qbit1, theta):
        gate_instance = deepcopy(self)
        gate_instance.theta = float(theta)
        gate_instance.qbit = [qbit0, qbit1]
        gate_instance.display_name = (f"Rxx({round(gate_instance.theta, 2)})", f"Rxx({round(gate_instance.theta, 2)})")
        return gate_instance


rxx = _RXX()


class _RYY(_CommonGate):
    def __init__(self, qbit0=0, qbit1=1, name='ryy', theta=0):
        self.qbit0 = qbit0
        self.qbit1 = qbit1
        self.qbit = None
        self.name = name
        self.theta = float(theta)
        self.display_name = (f"Ryy({round(theta, 2)})", f"Ryy({round(theta, 2)})")

    def __call__(self, qbit0, qbit1, theta):
        return self.gate(qbit0, qbit1, theta)

    def gate(self, qbit0, qbit1, theta):
        gate_instance = deepcopy(self)
        gate_instance.theta = float(theta)
        gate_instance.qbit = [qbit0, qbit1]
        gate_instance.display_name = (f"Ryy({round(gate_instance.theta, 2)})", f"Ryy({round(gate_instance.theta, 2)})")
        return gate_instance


ryy = _RYY()


class _RZZ(_CommonGate):
    """
    @params: first two params are qbit positions, third param is theta;
    @return: rzz gate
    """
    def __init__(self, qbit0=0, qbit1=1, name='rzz', theta=0):
        self.qbit0 = qbit0
        self.qbit1 = qbit1
        self.qbit = None
        self.name = name
        self.theta = float(theta)
        self.display_name = (f"Rzz({round(self.theta, 2)})", f"Rzz({round(self.theta, 2)})")

    def __call__(self, qbit0, qbit1, theta):
        return self.gate(qbit0, qbit1, theta)

    def gate(self, qbit0, qbit1, theta):
        gate_instance = deepcopy(self)
        gate_instance.theta = float(theta)
        gate_instance.qbit = [qbit0, qbit1]
        gate_instance.display_name = (f"Rzz({round(gate_instance.theta, 2)})", f"Rzz({round(gate_instance.theta, 2)})")
        return gate_instance


rzz = _RZZ()


class _SYC(_CommonGate):
    def __init__(self, qbit0: int = 0, qbit1: int = 1, name='syc', theta=None):
        self.qbit0 = qbit0
        self.qbit1 = qbit1
        self.qbit = None
        self.name = name
        self.theta = theta
        self.display_name = ('SYC', 'SYC')

    def __call__(self, qbit0, qbit1):
        return self.gate(qbit0, qbit1)

    def gate(self, qbit0, qbit1):
        gate_instance = deepcopy(self)
        gate_instance.qbit = [qbit0, qbit1]
        return gate_instance


syc = _SYC()


class _CCX(_CommonGate):
    """
    @params: control_qbit control qbits: list, target_qbit target qbit: int
    """
    def __init__(self, control_qbit: Union[list, int] = None, target_qbit: Union[list, int] = None, name='ccx', theta=None):
        self.control_qbit = control_qbit if isinstance(control_qbit, list) else [control_qbit]
        self.target_qbit = target_qbit if isinstance(target_qbit, list) else [target_qbit]
        self.qbit = None
        self.name = name
        self.theta = theta
        self.display_name = ("@", "@", "X")

    def __call__(self, control_qbit, target_qbit):
        return self.gate(control_qbit, target_qbit)

    def gate(self, control_qbit, target_qbit):
        gate_instance = deepcopy(self)
        gate_instance.control = control_qbit if isinstance(control_qbit, list) else [control_qbit]
        gate_instance.target = target_qbit if isinstance(target_qbit, list) else [target_qbit]
        gate_instance.qbit = gate_instance.control + gate_instance.target
        return gate_instance


ccx = _CCX()


class _CSWAP(_CommonGate):
    """
    @params: control_qbit control qbit: int, target_qbit target qbits: list
    """
    def __init__(self, control_qbit: Union[list, int] = None, target_qbit: Union[list, int] = None, name='cswap', theta=None):
        self.control_qbit = control_qbit if isinstance(control_qbit, list) else [control_qbit]
        self.target_qbit = target_qbit if isinstance(target_qbit, list) else [target_qbit]
        self.qbit = None
        self.name = name
        self.theta = theta
        self.display_name = ("@", "x", "x")

    def __call__(self, control_qbit, target_qbit):
        return self.gate(control_qbit, target_qbit)

    def gate(self, control_qbit, target_qbit):
        gate_instance = deepcopy(self)
        gate_instance.control = control_qbit if isinstance(control_qbit, list) else [control_qbit]
        gate_instance.target = target_qbit if isinstance(target_qbit, list) else [target_qbit]
        gate_instance.qbit = gate_instance.control + gate_instance.target
        return gate_instance


cswap = _CSWAP()



