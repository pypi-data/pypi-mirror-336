"""
-*- coding: utf-8 -*-
@Author : Cui Jinghao
@Time : 2024/10/21 11:08
@Function: param_gates.py
@Contact: cuijinghao@tgqs.net
"""
from typing import Union


class ParamGates:
    def __init__(self, gate_pos: Union[int, tuple, list], gate_info: tuple):
        self.gate_pos = gate_pos
        if len(gate_info) == 1:
            self.gate_name = gate_info[0]
            self.gate_params = None
        elif len(gate_info) == 2:
            self.gate_name = gate_info[0]
            self.gate_params = gate_info[1]
        else:
            raise Exception('not support gate type, too many gate params')



