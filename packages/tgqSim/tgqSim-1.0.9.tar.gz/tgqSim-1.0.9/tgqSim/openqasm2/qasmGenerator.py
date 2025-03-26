"""
-*- coding: utf-8 -*-
@Author : Cui Jinghao
@Time : 2024/8/22 15:25
@Function: qasmGenerator.py
@Contact: cuijinghao@tgqs.net
"""
from pygments.lexer import RegexLexer
from pygments.token import Comment, String, Keyword, Name, Number, Text
from pygments.style import Style
from pygments.formatters import Terminal256Formatter
import pygments

ABV_GATE = {'cp': 'cphase'}


class QasmTerminalStyle(Style):
    """A style for OpenQasm in a Terminal env (e.g. Jupyter print)."""

    styles = {
        String: "ansibrightred",
        Number: "ansibrightcyan",
        Keyword.Reserved: "ansibrightgreen",
        Keyword.Declaration: "ansibrightgreen",
        Keyword.Type: "ansibrightmagenta",
        Name.Builtin: "ansibrightblue",
        Name.Function: "ansibrightyellow",
    }


class QasmHTMLStyle(Style):
    """A style for OpenQasm in a HTML env (e.g. Jupyter widget)."""

    styles = {
        String: "ansired",
        Number: "ansicyan",
        Keyword.Reserved: "ansigreen",
        Keyword.Declaration: "ansigreen",
        Keyword.Type: "ansimagenta",
        Name.Builtin: "ansiblue",
        Name.Function: "ansiyellow",
    }


class OpenQASMLexer(RegexLexer):
    """A pygments lexer for OpenQasm."""

    name = "OpenQASM"
    aliases = ["qasm"]
    filenames = ["*.qasm"]

    gates = [
        "id",
        "cx",
        "x",
        "y",
        "z",
        "s",
        "sdg",
        "h",
        "t",
        "tdg",
        "ccx",
        "c3x",
        "c4x",
        "c3sqrtx",
        "rx",
        "ry",
        "rz",
        "cz",
        "cy",
        "ch",
        "cp",
        "swap",
        "syc",
        "cswap",
        "crx",
        "cry",
        "crz",
        "cu1",
        "cu3",
        "rxx",
        "rzz",
        "rccx",
        "rc3x",
        "u1",
        "u2",
        "u3",
    ]

    tokens = {
        "root": [
            (r"\n", Text),
            (r"[^\S\n]+", Text),
            (r"//\n", Comment),
            (r"//.*?$", Comment.Single),
            # Keywords
            (r"(OPENQASM|include)\b", Keyword.Reserved, "keywords"),
            (r"(qreg|creg)\b", Keyword.Declaration),
            # Treat 'if' special
            (r"(if)\b", Keyword.Reserved, "if_keywords"),
            # Constants
            (r"(pi)\b", Name.Constant),
            # Special
            (r"(barrier|measure|reset)\b", Name.Builtin, "params"),
            # Gates (Types)
            ("(" + "|".join(gates) + r")\b", Keyword.Type, "params"),
            (r"[unitary\d+]", Keyword.Type),
            # Functions
            (r"(gate)\b", Name.Function, "gate"),
            # Generic text
            (r"[a-zA-Z_][a-zA-Z0-9_]*", Text, "index"),
        ],
        "keywords": [
            (r'\s*("([^"]|"")*")', String, "#push"),
            (r"\d+", Number, "#push"),
            (r".*\(", Text, "params"),
        ],
        "if_keywords": [
            (r"[a-zA-Z0-9_]*", String, "#pop"),
            (r"\d+", Number, "#push"),
            (r".*\(", Text, "params"),
        ],
        "params": [
            (r"[a-zA-Z_][a-zA-Z0-9_]*", Text, "#push"),
            (r"\d+", Number, "#push"),
            (r"(\d+\.\d*|\d*\.\d+)([eEf][+-]?[0-9]+)?", Number, "#push"),
            (r"\)", Text),
        ],
        "gate": [(r"[unitary\d+]", Keyword.Type, "#push"), (r"p\d+", Text, "#push")],
        "index": [(r"\d+", Number, "#pop")],
    }


def qasm(gate_list: list, nqubit: int, formatted=False)->str:
    mapping = {
        "iswap": "gate iswap q0,q1 { s q0; s q1; h q0; cx q0,q1; cx q1,q0; h q1; }",
        "ryy": "gate ryy(param0) q0,q1 { rx(pi/2) q0; rx(pi/2) q1; cx q0,q1; rz(param0) q1; cx q0,q1; rx(-pi/2) q0; rx(-pi/2) q1; }",
        "syc": "gate syc q0,q1 { rxx(-pi/2) q0,q1; ryy(-pi/2) q0,q1; cp(-pi/6) q0,q1; }",
        "syc": "gate syc q0,q1 { rxx(-pi/2) q0,q1; ryy(-pi/2) q0,q1; cp(-pi/6) q0,q1; }"
    }
    version_lib = "OPENQASM 2.0;\ninclude \"qelib1.inc\";\n"
    bytes_pos = [f"qreg q[{nqubit}]", f"creg c[{nqubit}]"]
    other_gate_define = []
    normal_gate_list = []
    is_define = {"iswap": False, "ryy": False, "syc": False}
    measure_gate = []
    for pos, gate_info in gate_list:
        gate_name = gate_info[0].lower()
        if gate_name == "measure":
            if isinstance(pos, int):
                measure_gate.append(f"{gate_name} q[{pos}] -> c[{pos}]")
            elif isinstance(pos, list):
                for pos_idx in pos:
                    measure_gate.append(f"{gate_name} q[{pos_idx}] -> c[{pos_idx}]")
            continue
        if isinstance(pos, int):
            normal_gate_list.append(f"{gate_name} q[{pos}]")
        elif isinstance(pos, list):
            length = len(pos)
            if 1 == length:
                normal_gate_list.append(f"{gate_info[0].lower()} q[{pos[0]}]")
            elif 2 == length:
                need_redefine_gate = ["iswap", "ryy", "syc"]
                if gate_name in need_redefine_gate and not is_define[gate_name]:
                    other_gate_define.append(mapping[gate_name])
                    is_define[gate_name] = True
                if len(gate_info) >= 2:
                    if gate_name in ABV_GATE:
                        gate_name = ABV_GATE[gate_name]
                    if isinstance(gate_info[1], float):
                        normal_gate_list.append(f"{gate_name}({gate_info[1]}) q[{pos[0]}] q[{pos[1]}]")
                    else:
                        normal_gate_list.append(f"{gate_name} q[{pos[0]}] q[{pos[1]}]")
            elif 3 == length:
                if len(gate_info) >= 2:
                    if isinstance(gate_info[1], float):
                        normal_gate_list.append(f"{gate_name}({gate_info[1]}) q[{pos[0]}] q[{pos[1]}]")
                    else:
                        normal_gate_list.append(f"{gate_name} q[{pos[0]}] q[{pos[1]}]")
    qasm_code = version_lib + "\n".join(other_gate_define) + "\n" + "\n".join(bytes_pos) + "\n" + \
        "\n".join(normal_gate_list) + "\n" + "\n".join(measure_gate)
    if formatted:
        code = pygments.highlight(
            qasm_code,
            OpenQASMLexer(),
            Terminal256Formatter(style=QasmTerminalStyle)
        )
        print(code)
        return None
    return qasm_code
