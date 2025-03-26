"""
-*- coding: utf-8 -*-
@Author : Cui Jinghao
@Time : 2024/7/23 9:59
@Function: visualization.py
@Contact: cuijinghao@tgqs.net
"""
from tgqSim.circuit.common_gates import (BASE_SINGLE_GATE,
                                         BASE_DOUBLE_GATE,
                                         BASE_TRIPLE_GATE,
                                         CONTROLLED_GATE,
                                         ROTATION_GATE)

# contain all the gates available, grant each gate a symbol to represent
# for controlled gates, one node is 'C', the other node is its symbol string, e.g. 'NOT'
GATE_SYMBOL_DICT = {
    'x': 'X', 'y': 'Y', 'z': 'Z',
    'rzz': 'Z', 'ryy': 'Y', 'rxx': 'X',

                    'cp': 'CPhase',
                    'cx': 'NOT', 'cz': 'Z', 'ccx': 'NOT',
                    's': 'S', 'sdg': 'Sdg', 't': 'T', 'tdg': 'Tdg',
                    'h': 'H', 'u3': 'U3',
                    'rx': 'Rx', 'ry': 'Ry', 'rz': 'Rz',
                    'syc': 'SYC',
                    'swap': 'SWAP', 'cswap': 'SWAP', 'iswap': 'ISWAP'
}


def get_gate_symbol(gatename: str):
    pass


def get_circuit_deep(qubitNum: int, gate_list: list) -> int:
    """
    获取整个线路图最大的深度

    Args:
        qubitNum (int): 线路图中比特数
        gate_list (list): 量子门序列

    Returns:
        int: 量子线路图的深度
    """
    # 初始化，每一个比特位起始值为0
    count = [0 for _ in range(qubitNum)]
    for pos, _, __ in gate_list:
        if isinstance(pos, int):
            # 单比特：若是比特位使用int类型表示，则直接在该比特位计数加一
            count[pos] += 1
        else:
            length = len(pos)
            if 1 == length:
                # 单比特：利用list表示作用比特位时，计数也是直接加一
                count[pos[0]] += 1
            else:
                # 多比特，主要是针对双比特门和三比特门
                # 拿到多比特门跨度所有比特的门计数中最大的门计数
                maxVal = max([count[i] for i in pos])
                # 更新多比特门跨度的所有比特对应的门计数（保证是左对齐）
                for i in range(min(pos), max(pos) + 1):
                    count[i] = maxVal + 1

    return max(count)


def update_index_list(indexList: list, pos: list) -> list:
    """
    获取所有比特位对应的指针位置，保真整个线路图是左对齐

    Args:
        indexList (list): 所有比特中，当前指针所指的位置
        pos (list): 比特门作用的比特位置

    Returns:
        list: 更新后指针的位置
    """
    if 1 == len(pos):
        # 单比特情形
        newCol = indexList[2 * pos[0]] + 1
    else:
        # 多比特情形
        # 拿到多比特门跨度所有比特对应指针最大的位置
        newCol = max([indexList[i] for i in range(2 * min(pos), 2 * max(pos) + 1)]) + 1
    # update indexList
    # 开始更新多比特门跨度所有比特对应指针的值
    for i in range(2 * min(pos), 2 * max(pos) + 1):
        indexList[i] = newCol
    return indexList


def draw_on_quite_gate(diagInfo: list, pos: list, newColIndex: int, diagEle: tuple)->list:
    """
    根据给出来的比特门作用的比特位置、列指针信息以及需要绘画的内容，在对应的比特位置上画出量子门
    这里面仅仅门作用位置的信息，不会更新连线

    Args:
        diagInfo (list): 画板信息，线路形状都会在这个上面呈现
        pos (list): 量子门作用的位置信息，确定行，长度与diagEle保持一致，在定义门确定好
        newColIndex (int): 绘制量子门对应的列索引，确定列
        diagEle (tuple): 绘制图形样子，长度与pos保持一致，由门控制，在定义门确定好

    Returns:
        list: 更新后的画板
    """
    for i, qIndex in enumerate(pos):
        offset = len(diagEle[i])
        # print(pos, diagEle[i])
        diagInfo[2 * qIndex] = diagInfo[2 * qIndex][:newColIndex] + diagEle[i] + diagInfo[2 * qIndex][newColIndex + offset:]
    return diagInfo


def draw_vertical_line(diagInfo: list, pos: list, newColIndex: int)->list:
    """
    依据门信息，画出对应的连线

    Args:
        diagInfo (list): 画板信息，线路形状都会在这个上面呈现
        pos (list): 量子门作用的位置信息，确定行
        newColIndex (int):  绘制量子门对应的列索引，确定列

    Returns:
        list: 更新后的画板
    """
    for i in range(2 * min(pos), 2 * max(pos) + 1):
        if i % 2 == 0:
            qIndex = i // 2
            if qIndex in pos:
                # 这个位置是门作用的位置，不能覆盖
                continue
            else:
                # 若是当前位置比特位，则利用垂直线替代┼
                diagInfo[i] = diagInfo[i][:newColIndex] + "┼" + diagInfo[i][newColIndex + 1:]
        else:
            # 若是当前位置是两个相邻比特之间的空隙，直接用│替代
            diagInfo[i] = diagInfo[i][:newColIndex] + "│" + diagInfo[i][newColIndex + 1:]
    return diagInfo


def draw_gate(diagInfo: list, pos: list, newColIndex: int, diagEle: tuple)->list:
    """
    在线路图中绘制量子门
    绘制方法：
    首先在量子门作用位置进行绘制，即先绘制从控制比特和目标比特的图形
    其次再绘制之间的连线

    Args:
        diagInfo (list): 画板信息，线路形状都会在这个上面呈现
        pos (list): 量子门作用的位置信息，确定行，长度与diagEle保持一致，在定义门确定好
        newColIndex (int): 绘制量子门对应的列索引，确定列
        diagEle (tuple): 绘制图形样子，长度与pos保持一致，由门控制，在定义门确定好

    Returns:
        list: 更新后的画板
    """
    diagInfo = draw_on_quite_gate(diagInfo=diagInfo, pos=pos, newColIndex=newColIndex, diagEle=diagEle)
    diagInfo = draw_vertical_line(diagInfo=diagInfo, pos=pos, newColIndex=newColIndex)
    return diagInfo


def to_text_diag(gates: list, width: int) -> str:
    """
    绘制量子线路图

    Args:
        circuit (tgqSim.QuantumCircuit): 量子线路图信息

    Returns:
        str: 可供打印的线路图信息
    """
    # use displayname_list element of quantumcircuit
    gateList = gates
    qubitNum = width
    indexList = [0 for _ in range(2 * qubitNum - 1)]
    circuit_deep = get_circuit_deep(qubitNum, gateList)
    # print(circuit_deep)
    # 奇数行绘制横线，偶数行绘制空格
    base_line, base_space = "───────────", "           "
    # 初始化画板样式
    diagInfo = [f"{i // 2}: " + base_line * circuit_deep if i % 2 == 0 else base_space * circuit_deep for i in range(2 * qubitNum - 1)]
    # e.g. gate_pos: Union[int, str], display_name: tuple, *gate_info
    for pos, display_name, gate in gateList:
        if isinstance(pos, int):
            pos = [pos]
        newColIndex = max([indexList[ele] * len(base_space) + 4 for ele in range(2 * min(pos), 2 * max(pos) + 1)])
        indexList = update_index_list(indexList=indexList, pos=pos)
        # todo: use mapping instead of element of gatelist, gatelist will not contain symbol
        diagInfo = draw_gate(diagInfo=diagInfo, pos=pos, newColIndex=newColIndex, diagEle=display_name)
    return "\n".join(diagInfo)

# class Visualizer:
#     def __init__(self):
#         self.diagram_str = ''
#         self.diagram = ''


def to_text_diagram(gates: list, width: int):
    # [(0, ('h',)), ([0, 1], ('cx',)), (0, ('rz', 0.708)), (0, ('rz', 0.0)), (0, ('rz', -0.5)),
    #  (1, ('u3', 0.708, 0.708, 0.708)), ([0, 1], ('measure',))]
    max_gate_length = max(len(GATE_SYMBOL_DICT[gate[1][0]]) for gate in gates) if gates else 1
    # colum_width refers to gate width, while width refers to the number of qubits
    column_width = max_gate_length + 2
    diagram_str = ['-' * (len(gates) * column_width + 1) for _ in range(width)]
    for col, (qubits, gate) in enumerate(gates):
        print(col, gate, qubits)
        gate = gate[0].lower()
        if isinstance(qubits, int):
            qubits = [qubits]
        # todo: not all two bit gates are control gates, need to consider gates like RXX, ISWAP etc
        # single gate
        if gate in BASE_SINGLE_GATE:
            for q in range(width):
                if q in qubits:
                    diagram_str[q] = (diagram_str[q][:col * column_width + 1]
                                      + f'{GATE_SYMBOL_DICT[gate]}'.center(column_width)
                                      + diagram_str[q][col * column_width + column_width + 1:])
                else:
                    diagram_str[q] = diagram_str[q][:col * column_width + 1] + '|'.center(column_width) + \
                                     diagram_str[q][
                                     col * column_width + column_width + 1:]
        # double gate
        elif gate in BASE_DOUBLE_GATE:
            # for controlled gates
            if gate in CONTROLLED_GATE:
                # by default, first returned result is control bit
                control, target = qubits
                for q in range(width):
                    if q == control:
                        diagram_str[q] = diagram_str[q][:col * column_width + 1] + f'@'.center(column_width) + \
                                         diagram_str[q][
                                         col * column_width + column_width + 1:]
                    elif q == target:
                        diagram_str[q] = diagram_str[q][:col * column_width + 1] + f'{GATE_SYMBOL_DICT[gate]}'.center(
                            column_width) + \
                                         diagram_str[q][
                                         col * column_width + column_width + 1:]
                    elif control < q < target or target < q < control:
                        diagram_str[q] = diagram_str[q][:col * column_width + 1] + '|'.center(column_width) + \
                                         diagram_str[q][
                                         col * column_width + column_width + 1:]
                    else:
                        diagram_str[q] = diagram_str[q][:col * column_width + 1] + ' '.center(column_width) + \
                                         diagram_str[q][
                                         col * column_width + column_width + 1:]
            # for non controlled gates
            else:
                bit0, bit1 = qubits
                for q in range(width):
                    if q == bit0:
                        diagram_str[q] = (diagram_str[q][:col * column_width + 1] +
                                          f'{GATE_SYMBOL_DICT[gate]}'.center(column_width) +
                                         diagram_str[q][col * column_width + column_width + 1:])
                    elif q == bit1:
                        diagram_str[q] = (diagram_str[q][:col * column_width + 1] +
                                          f'{GATE_SYMBOL_DICT[gate]}'.center(column_width) +
                                         diagram_str[q][col * column_width + column_width + 1:])
                    elif bit0 < q < bit1 or bit1 < q < bit0:
                        diagram_str[q] = diagram_str[q][:col * column_width + 1] + '|'.center(column_width) + \
                                         diagram_str[q][
                                         col * column_width + column_width + 1:]
                    else:
                        diagram_str[q] = diagram_str[q][:col * column_width + 1] + ' '.center(column_width) + \
                                         diagram_str[q][
                                         col * column_width + column_width + 1:]
        elif gate in BASE_TRIPLE_GATE:
            pass
    diagram = '\n'.join(diagram_str)
    return diagram




