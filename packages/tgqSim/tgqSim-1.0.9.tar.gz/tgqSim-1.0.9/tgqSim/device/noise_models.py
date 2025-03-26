"""
-*- coding: utf-8 -*-
@Author : Cui Jinghao
@Time : 2024/6/28 14:43
@Function: noise_model.py
@Contact: cuijinghao@tgqs.net
"""


import random
from typing import Union

NOISE_MAPPER = {"bit_flip": "BF",
                "asymmetric_depolarization": "ADP",
                "depolarize": "DP",
                "phase_flip": "PF",
                "phase_damp": "PD",
                "amplitude_damp": "AD",
                "damp_I": "DAMP_I"}

NOISE_TYPE = ["bit_flip",
              # "asymmetric_depolarization",
              "depolarize", "phase_flip", "phase_damp", "amplitude_damp"]


def bit_flip(error_rate: float):
    random_value = random.uniform(0, 1)
    gate_name = "I"
    if random_value < error_rate:
        gate_name = "x"
    return gate_name


def asymmetric_depolarization(error_rate: Union[list, tuple]):
    if len(error_rate) != 3:
        raise ValueError("Length of error must be 3")
    gate_name = "I"
    thredhold = sum(error_rate)
    random_value = random.uniform(0, 1)
    if random_value < thredhold:
        if random_value < error_rate[0]:
            gate_name = "x"
        elif random_value < sum(error_rate[:2]):
            gate_name = "y"
        else:
            gate_name = "z"
    return gate_name


def depolarize(error_rate: float):
    pxyz = [error_rate / 3] * 3
    return asymmetric_depolarization(error_rate=pxyz)


def phase_flip(error_rate: float):
    random_value = random.uniform(0, 1)
    gate_name = "I"
    if random_value < error_rate:
        gate_name = "z"
    return gate_name


def phase_damp(error_rate: float):
    random_value = random.uniform(0, 1)
    gate_name = "damp_I"
    if random_value < error_rate:
        gate_name = "pd"
    return gate_name


def amplitude_damp(error_rate: float):
    random_value = random.uniform(0, 1)
    gate_name = "damp_I"
    if random_value < error_rate:
        gate_name = "ad"
    return gate_name
