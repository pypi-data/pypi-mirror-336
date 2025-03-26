"""
-*- coding: utf-8 -*-
@Author : XerCis
@Time : 2024/6/28 16:38
@Function:
@Contact: 
"""
import tgqSim.device.noise_models as noise_model
from typing import Union


def parse_noise(noise_type: str, gate_pos: int, error_rate: Union[float, list]):
    """
    对于不同的噪声类型，返回不同的信息

    Args:
        noise_type (str): 噪声类型
        error_rate Union[float, list]: 门错误率信息
    """
    gate_name = "I"
    if "bit_flip" == noise_type:
        gate_name = noise_model.bit_flip(error_rate)
    elif "asymmetric_depolarization" == noise_type:
        gate_name = noise_model.asymmetric_depolarization(error_rate)
    elif "depolarize" == noise_type:
        gate_name = noise_model.depolarize(error_rate)
    elif "phase_flip" == noise_type:
        gate_name = noise_model.phase_flip(error_rate)
    elif "phase_damp" == noise_type:
        gate_name = noise_model.phase_damp(error_rate)
    elif "amplitude_damp" == noise_type:
        gate_name = noise_model.amplitude_damp(error_rate)
    else:
        raise ValueError("Please check noise model name")
    if gate_name == "I":
        return None
    return (gate_pos, (gate_name,error_rate))
