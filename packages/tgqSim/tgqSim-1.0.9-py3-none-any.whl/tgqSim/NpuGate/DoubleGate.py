import torch
import math
import torch_npu
# from tgqSim import QuantumCircuit
# from numba import njit, prange

# 定义复数乘法函数，接受四个实数作为输入，分别代表两个复数的实部和虚部
def complex_mul(a_real, a_imag, b_real, b_imag):
    # print()
    # print("a_real:", a_real)
    # print("a_imag:", a_imag)
    # print("b_real:", b_real)
    # print("b_imag:", b_imag)
    result = [a_real * b_real - a_imag * b_imag, a_real * b_imag + a_imag * b_real]
    # print("complex_mul result:", result)
    return result

def complex_exp(real, imag):
    exp_real = torch.exp(real)
    return [exp_real * torch.cos(imag), exp_real * torch.sin(imag)]

def ActOn_State(psi: list, num_qubits, Gate_type, Gate_pos, *Angles):
    psi_real = torch.tensor(psi, dtype=torch.float32)
    psi_imag = torch.tensor([0]*len(psi), dtype=torch.float32)
    if torch.npu.is_available():
        device = torch.device("npu")
    else:
        device = torch.device("cpu")
    psi_real = psi_real.to(device)
    psi_imag = psi_imag.to(device)
    
    j1, j0 = max(Gate_pos), min(Gate_pos)
    i1_plus = 2 ** j0
    i2_plus = 2 ** j1
    i3_plus = 2 ** j0 + 2 ** j1
    delta2 = 2 ** (j1 + 1)
    delta1 = 2 ** (j0 + 1)
    max2 = 2 ** num_qubits - delta2
    max1 = 2 ** j1 - delta1
    max0 = 2 ** j0 - 1

    for k in range(0, max2 + 1, delta2):
        for l in range(0, max1 + 1, delta1):
            for m in range(0, max0 + 1):
                i0 = m | l | k
                i1 = i0 | i1_plus
                i2 = i0 | i2_plus
                i3 = i0 | i3_plus
                if (i0 != i1) and (i0 != i2) and (i0 != i3) and (i1 != i2) and (i1 != i3) and (i2 != i3):
                    if Gate_type == 'cx':
                        if Gate_pos[0] > Gate_pos[1]:
                            psi_real[i2], psi_real[i3] = psi_real[i3].clone(), psi_real[i2].clone()
                            psi_imag[i2], psi_imag[i3] = psi_imag[i3].clone(), psi_imag[i2].clone()
                        else:
                            psi_real[i1], psi_real[i3] = psi_real[i3].clone(), psi_real[i1].clone()
                            psi_imag[i1], psi_imag[i3] = psi_imag[i3].clone(), psi_imag[i1].clone()
                    elif Gate_type == 'swap':
                        psi_real[i1], psi_real[i2] = psi_real[i2].clone(), psi_real[i1].clone()
                        psi_imag[i1], psi_imag[i2] = psi_imag[i2].clone(), psi_imag[i1].clone()
                    elif Gate_type == 'iswap':
                        psi_real[i1], psi_imag[i1], psi_real[i2], psi_imag[i2] = -psi_imag[i2].clone(), psi_real[i2].clone(), -psi_imag[i1].clone(), psi_real[i1].clone()
                    elif Gate_type == 'cz':
                        psi_real[i3], psi_imag[i3] = -psi_real[i3].clone(), -psi_imag[i3].clone()
                    elif Gate_type == 'cp':
                        angle = torch.tensor(Angles[0])
                        cos_val, sin_val = torch.cos(angle), torch.sin(angle)
                        psi_real[i3], psi_imag[i3] = complex_mul(psi_real[i3], psi_imag[i3], cos_val, sin_val)
                    elif Gate_type == 'syc':
                        psi_real[i1], psi_imag[i1], psi_real[i2], psi_imag[i2] = -psi_imag[i2].clone(), psi_real[i2].clone(), -psi_imag[i1].clone(), psi_real[i1].clone()
                        exp_val = complex_exp(torch.tensor(0.), torch.tensor(-math.pi / 6))
                        psi_real[i3], psi_imag[i3] = complex_mul(psi_real[i3], psi_imag[i3], exp_val[0], exp_val[1])
                    elif Gate_type in ['rxx', 'ryy', 'rzz']:
                        angle = torch.tensor(Angles[0])
                        cos_val, sin_val = torch.cos(angle / 2), torch.sin(angle / 2)
                        # print(cos_val, sin_val)
                        if Gate_type == 'rxx':
                            # print("\nbefore: ", psi_real, psi_imag)
                            psi_real[i0], psi_imag[i0], psi_real[i3], psi_imag[i3] = complex_mul(cos_val, torch.tensor(0.), psi_real[i0], psi_imag[i0])[0] + complex_mul(torch.tensor(0.), -sin_val, psi_real[i3], psi_imag[i3])[0], \
                                                                                    complex_mul(cos_val, torch.tensor(0.), psi_real[i0], psi_imag[i0])[1] + complex_mul(torch.tensor(0.), -sin_val, psi_real[i3], psi_imag[i3])[1], \
                                                                                    complex_mul(cos_val, torch.tensor(0.), psi_real[i3], psi_imag[i3])[0] + complex_mul(torch.tensor(0.), -sin_val, psi_real[i0], psi_imag[i0])[0], \
                                                                                    complex_mul(cos_val, torch.tensor(0.), psi_real[i3], psi_imag[i3])[1] + complex_mul(torch.tensor(0.), -sin_val, psi_real[i0], psi_imag[i0])[1]

                            psi_real[i1], psi_imag[i1], psi_real[i2], psi_imag[i2] = complex_mul(cos_val, torch.tensor(0.), psi_real[i1], psi_imag[i1])[0] + complex_mul(torch.tensor(0.), -sin_val, psi_real[i2], psi_imag[i2])[0], \
                                                                                    complex_mul(cos_val, torch.tensor(0.), psi_real[i1], psi_imag[i1])[1] + complex_mul(torch.tensor(0.), -sin_val, psi_real[i2], psi_imag[i2])[1], \
                                                                                    complex_mul(cos_val, torch.tensor(0.), psi_real[i2], psi_imag[i2])[0] + complex_mul(torch.tensor(0.), -sin_val, psi_real[i1], psi_imag[i1])[0], \
                                                                                    complex_mul(cos_val, torch.tensor(0.), psi_real[i2], psi_imag[i2])[1] + complex_mul(torch.tensor(0.), -sin_val, psi_real[i1], psi_imag[i1])[1]
                            # print("after: ", psi_real, psi_imag)
                            # print(psi_real[i1], psi_imag[i1], psi_real[i2], psi_imag[i2])
                        elif Gate_type == 'ryy':
                            psi_real[i0], psi_imag[i0], psi_real[i3], psi_imag[i3] = complex_mul(cos_val, torch.tensor(0.), psi_real[i0], psi_imag[i0])[0] + complex_mul(torch.tensor(0.), sin_val, psi_real[i3], psi_imag[i3])[0], \
                                                                                    complex_mul(cos_val, torch.tensor(0.), psi_real[i0], psi_imag[i0])[1] + complex_mul(torch.tensor(0.), sin_val, psi_real[i3], psi_imag[i3])[1], \
                                                                                    complex_mul(cos_val, torch.tensor(0.), psi_real[i3], psi_imag[i3])[0] + complex_mul(torch.tensor(0.), sin_val, psi_real[i0], psi_imag[i0])[0], \
                                                                                    complex_mul(cos_val, torch.tensor(0.), psi_real[i3], psi_imag[i3])[1] + complex_mul(torch.tensor(0.), sin_val, psi_real[i0], psi_imag[i0])[1]
                            psi_real[i1], psi_imag[i1], psi_real[i2], psi_imag[i2] = complex_mul(cos_val, torch.tensor(0.), psi_real[i1], psi_imag[i1])[0] + complex_mul(torch.tensor(0.), -sin_val, psi_real[i2], psi_imag[i2])[0], \
                                                                                    complex_mul(cos_val, torch.tensor(0.), psi_real[i1], psi_imag[i1])[1] + complex_mul(torch.tensor(0.), -sin_val, psi_real[i2], psi_imag[i2])[1], \
                                                                                    complex_mul(cos_val, torch.tensor(0.), psi_real[i2], psi_imag[i2])[0] + complex_mul(torch.tensor(0.), -sin_val, psi_real[i1], psi_imag[i1])[0], \
                                                                                    complex_mul(cos_val, torch.tensor(0.), psi_real[i2], psi_imag[i2])[1] + complex_mul(torch.tensor(0.), -sin_val, psi_real[i1], psi_imag[i1])[1]
                        elif Gate_type == 'rzz':
                            exp_pos = complex_exp(torch.tensor(0.), -angle / 2)
                            exp_neg = complex_exp(torch.tensor(0.), angle / 2)
                            psi_real[i0], psi_imag[i0] = complex_mul(psi_real[i0], psi_imag[i0], exp_pos[0], exp_pos[1])
                            psi_real[i1], psi_imag[i1] = complex_mul(psi_real[i1], psi_imag[i1], exp_neg[0], exp_neg[1])
                            psi_real[i2], psi_imag[i2] = complex_mul(psi_real[i2], psi_imag[i2], exp_neg[0], exp_neg[1])
                            psi_real[i3], psi_imag[i3] = complex_mul(psi_real[i3], psi_imag[i3], exp_pos[0], exp_pos[1])

    return psi_real + 1j*psi_imag



if __name__ == '__main__':
    psi_real = torch.tensor([0, 0, 0, 1, 0, 0, 0, 0], dtype=torch.float32)
    psi_imag = torch.tensor([0, 0, 0, 0, 0, 0, 0, 0], dtype=torch.float32)
    num_qubits = 3
    circuit = QuantumCircuit(num_qubits)
    circuit.add_single_gate(0, 'x')
    circuit.add_single_gate(1, 'x')
    circuit.add_double_gate(0, 1, 'cx')
    circuit.add_double_gate(0, 1, 'swap')
    circuit.add_double_gate(0, 1, 'iswap')
    circuit.add_double_gate(1, 2, 'cz')
    circuit.add_double_gate(1, 2, 'cp', 1.78)
    circuit.add_double_gate(0, 1, 'syc')
    circuit.add_double_gate(1, 2, 'rxx', 1.78)
    circuit.add_double_gate(1, 2, 'ryy', 1.78)
    circuit.add_double_gate(1, 2, 'rzz', 1.78)
    # print(circuit.gate_list)
    circuit.run_statevector()
    print(circuit.state)
    # gate_list = [([0, 1], ('cx',)), ([0, 1], ('swap',)), ([0, 1], ('iswap',)), ([1, 2], ('cz', )), ([1, 2], ('cp', 1.78)), ([0, 1], ('syc', )), 
    #              ([1, 2], ('rxx', 1.78)), ([1, 2], ('ryy', 1.78)), ([1, 2], ('rzz', 1.78))]
    gate_list = [([0, 1], ('cx',)), ([0, 1], ('swap',)), ([0, 1], ('iswap',)), ([1, 2], ('cz', )), ([1, 2], ('cp', 1.78)), ([0, 1], ('syc', )),
                 ([1, 2], ('rxx', 1.78)), ([1, 2], ('ryy', 1.78)), ([1, 2], ('rzz', 1.78))]
    for ele in gate_list:
        Gate_type = ele[1][0]
        Gate_pos = ele[0]
        Angles = tuple()
        if len(ele[1]) > 1:
            Angles = tuple(ele[1][1:])
        psi_real, psi_imag = ActOn_State(psi_real, psi_imag, num_qubits, Gate_type, Gate_pos, *Angles)
    final_psi = psi_real + 1j * psi_imag
    print("final_psi:", final_psi)

