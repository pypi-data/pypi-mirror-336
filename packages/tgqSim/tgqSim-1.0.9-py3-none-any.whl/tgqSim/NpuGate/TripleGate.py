import torch
import math
import torch_npu
# from tgqSim import QuantumCircuit

# def ActOn_State_PyTorch(psi_real, psi_imag, num_qubits, Gate_type, Gate_pos, *Angles):
#     if torch.npu.is_available():
#         device = torch.device("npu")
#     else:
#         device = torch.device("cpu")

def ActOn_State(psi: list, num_qubits, Gate_type, Gate_pos):
    """
    Apply quantum gates on the state vector using PyTorch.

    :param psi_real: Real part of the state vector
    :param psi_imag: Imaginary part of the state vector
    :param num_qubits: Number of qubits
    :param Gate_type: Type of the gate ('ccx' or 'cswap')
    :param Gate_pos: Positions of the qubits the gate acts on
    :return: Updated real and imaginary parts of the state vector
    """
    psi_real = torch.tensor(psi, dtype=torch.float32)
    psi_imag = torch.tensor([0]*len(psi), dtype=torch.float32)
    device = torch.device("npu" if torch.npu.is_available() else "cpu")
    psi_real = psi_real.to(device)
    psi_imag = psi_imag.to(device)
    
    j2, j1, j0 = sorted(Gate_pos, reverse=True)
    i1_plus = 2 ** j0
    i2_plus = 2 ** j1
    i3_plus = 2 ** j2
    i4_plus = 2 ** j0 + 2 ** j1
    i5_plus = 2 ** j0 + 2 ** j2
    i6_plus = 2 ** j1 + 2 ** j2
    i7_plus = 2 ** j0 + 2 ** j1 + 2 ** j2
    delta3 = 2 ** (j2 + 1)
    delta2 = 2 ** (j1 + 1)
    delta1 = 2 ** (j0 + 1)
    max3 = 2 ** num_qubits - delta3
    max2 = 2 ** j2 - delta2
    max1 = 2 ** j1 - delta1
    max0 = 2 ** j0 - 1

    for k in range(0, max3 + 1, delta3):
        for l in range(0, max2 + 1, delta2):
            for m in range(0, max1 + 1, delta1):
                for n in range(0, max0 + 1):
                    i0 = n | m | l | k
                    i1 = i0 | i1_plus
                    i2 = i0 | i2_plus
                    i3 = i0 | i3_plus
                    i4 = i0 | i4_plus
                    i5 = i0 | i5_plus
                    i6 = i0 | i6_plus
                    i7 = i0 | i7_plus
                    
                    if len(set([i0, i1, i2, i3, i4, i5, i6, i7])) == 8:  # All indices are different
                        if Gate_type == 'ccx':
                            # CCX (Toffoli) gate: flip the target qubit if both control qubits are |1>
                            psi_real[i7], psi_real[i3] = psi_real[i3].clone(), psi_real[i7].clone()
                            psi_imag[i7], psi_imag[i3] = psi_imag[i3].clone(), psi_imag[i7].clone()
                        elif Gate_type == 'cswap':
                            # CSWAP gate: swap the two target qubits if the control qubit is |1>
                            psi_real[i5], psi_real[i6] = psi_real[i6].clone(), psi_real[i5].clone()
                            psi_imag[i5], psi_imag[i6] = psi_imag[i6].clone(), psi_imag[i5].clone()
                            psi_real[i7], psi_real[i3] = psi_real[i3].clone(), psi_real[i7].clone()
                            psi_imag[i7], psi_imag[i3] = psi_imag[i3].clone(), psi_imag[i7].clone()

    return psi_real + 1j*psi_imag



if __name__ == '__main__':
    psi_real = torch.tensor([1, 0, 0, 0, 0, 0, 0, 0], dtype=torch.float32)
    psi_imag = torch.tensor([0, 0, 0, 0, 0, 0, 0, 0], dtype=torch.float32)
    num_qubits = 3
    circuit = QuantumCircuit(num_qubits)

    circuit.add_triple_gate([0, 1, 2], 'ccx')
    circuit.add_triple_gate([0, 1, 2], 'cswap')
    # print(circuit.gate_list)
    circuit.run_statevector()
    print(circuit.state)
    
    gate_list = [
        ([0, 1, 2], ('ccx',)),  # Toffoli gate
        ([0, 1, 2], ('cswap',))  # Controlled-SWAP gate
    ]
    for ele in gate_list:
        Gate_type = ele[1][0]
        Gate_pos = ele[0]
        Angles = tuple()
        if len(ele[1]) > 1:
            Angles = tuple(ele[1][1:])
        psi_real, psi_imag = ActOn_State(psi_real, psi_imag, num_qubits, Gate_type, Gate_pos, *Angles)
    final_psi = psi_real + 1j * psi_imag
    print("final_psi:", final_psi)