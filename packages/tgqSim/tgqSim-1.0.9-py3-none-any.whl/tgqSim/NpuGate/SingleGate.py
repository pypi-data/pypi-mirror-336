import torch
import torch_npu
import math
# from tgqSim import QuantumCircuit
# Define complex multiplication function
def complex_mul(a_real, a_imag, b_real, b_imag):
    return [a_real * b_real - a_imag * b_imag, a_real * b_imag + a_imag * b_real]

# Define complex exponential function
def complex_exp(real, imag):
    exp_real = torch.exp(real)
    return [exp_real * torch.cos(imag), exp_real * torch.sin(imag)]

# Function to apply a gate on a quantum state
def ActOn_State(psi, num_qubits, Gate_type, Gate_pos: int, *Angles):
    psi_real = torch.tensor(psi, dtype=torch.float32)
    psi_imag = torch.tensor([0]*len(psi), dtype=torch.float32)
    if torch.npu.is_available():
        device = torch.device("npu")
    else:
        device = torch.device("cpu")
    psi_real = psi_real.to(device)
    psi_imag = psi_imag.to(device)

    # Calculate position indices
    delta = 2 ** (Gate_pos + 1)
    max_delta = 2 ** num_qubits - delta
    i = 1 << Gate_pos

    # Iterate over state vector
    for k in range(0, max_delta + 1, delta):
        for l in range(0, i):
            i0 = l | k
            i1 = i0 | i
            
            # Handle different gate types
            if Gate_type == 'x':
                # Pauli-X (NOT) gate
                psi_real[i0], psi_real[i1] = psi_real[i1].clone(), psi_real[i0].clone()
                psi_imag[i0], psi_imag[i1] = psi_imag[i1].clone(), psi_imag[i0].clone()
            elif Gate_type == 'y':
                # Pauli-Y gate
                psi_real[i0], psi_imag[i0], psi_real[i1], psi_imag[i1] = -psi_imag[i1].clone(), psi_real[i1].clone(), psi_imag[i0].clone(), -psi_real[i0].clone()
            elif Gate_type == 'z':
                # Pauli-Z gate
                psi_real[i1], psi_imag[i1] = -psi_real[i1].clone(), -psi_imag[i1].clone()
            elif Gate_type == 'h':
                # Hadamard gate
                inv_sqrt2 = 1 / math.sqrt(2)
                temp_real_i0 = (psi_real[i0] + psi_real[i1]) * inv_sqrt2
                temp_imag_i0 = (psi_imag[i0] + psi_imag[i1]) * inv_sqrt2
                temp_real_i1 = (psi_real[i0] - psi_real[i1]) * inv_sqrt2
                temp_imag_i1 = (psi_imag[i0] - psi_imag[i1]) * inv_sqrt2
                psi_real[i0], psi_imag[i0], psi_real[i1], psi_imag[i1] = temp_real_i0, temp_imag_i0, temp_real_i1, temp_imag_i1
            elif Gate_type == 'rx':
                # RX gate
                angle = torch.tensor(Angles[0])
                cos_val = torch.cos(angle / 2)
                sin_val = torch.sin(angle / 2)
                temp_real_i0 = cos_val * psi_real[i0] + sin_val * psi_imag[i1]
                temp_imag_i0 = cos_val * psi_imag[i0] - sin_val * psi_real[i1]
                temp_real_i1 = cos_val * psi_real[i1] + sin_val * psi_imag[i0]
                temp_imag_i1 = cos_val * psi_imag[i1] - sin_val * psi_real[i0]
                psi_real[i0], psi_imag[i0], psi_real[i1], psi_imag[i1] = temp_real_i0, temp_imag_i0, temp_real_i1, temp_imag_i1
            elif Gate_type == 'ry':
                # RY gate
                angle = torch.tensor(Angles[0])
                cos_val = torch.cos(angle / 2)
                sin_val = torch.sin(angle / 2)
                temp_real_i0 = cos_val * psi_real[i0] - sin_val * psi_real[i1]
                temp_imag_i0 = cos_val * psi_imag[i0] - sin_val * psi_imag[i1]
                temp_real_i1 = cos_val * psi_real[i1] + sin_val * psi_real[i0]
                temp_imag_i1 = cos_val * psi_imag[i1] + sin_val * psi_imag[i0]
                psi_real[i0], psi_imag[i0], psi_real[i1], psi_imag[i1] = temp_real_i0, temp_imag_i0, temp_real_i1, temp_imag_i1
            elif Gate_type == 'rz':
                # RZ gate
                angle = torch.tensor(Angles[0])
                exp_i1 = complex_exp(torch.tensor(0.), angle / 2)
                exp_i0 = complex_exp(torch.tensor(0.), -angle / 2)
                psi_real[i0], psi_imag[i0] = complex_mul(psi_real[i0], psi_imag[i0], exp_i0[0], exp_i0[1])
                psi_real[i1], psi_imag[i1] = complex_mul(psi_real[i1], psi_imag[i1], exp_i1[0], exp_i1[1])

            elif Gate_type == 'u3':

                theta, phi, lamb = Angles[0], Angles[1], Angles[2]
                theta = torch.tensor(theta, dtype=torch.float32)
                phi = torch.tensor(phi, dtype=torch.float32)
                lamb = torch.tensor(lamb, dtype=torch.float32)

                c = torch.cos(theta / 2)
                s = torch.sin(theta / 2)
                psi_real_i0 = c * psi_real[i0] - s * torch.cos(lamb) * psi_real[i1] + s * torch.sin(lamb) * psi_imag[i1]
                psi_imag_i0 = c * psi_imag[i0] - s * torch.cos(lamb) * psi_imag[i1] - s * torch.sin(lamb) * psi_real[i1]
                psi_real_i1 = s * torch.cos(phi) * psi_real[i0] - s * torch.sin(phi) * psi_imag[i0] + \
                    c * torch.cos(phi + lamb) * psi_real[i1] - c * torch.sin(phi + lamb) * psi_imag[i1]
                psi_imag_i1 = s * torch.cos(phi) * psi_imag[i0] + s * torch.sin(phi) * psi_real[i0] + \
                    c * torch.cos(phi + lamb) * psi_imag[i1] + c * torch.sin(phi + lamb) * psi_real[i1]
                psi_real[i0], psi_imag[i0], psi_real[i1], psi_imag[i1] = psi_real_i0, psi_imag_i0, psi_real_i1, psi_imag_i1
            elif Gate_type == 's':
                psi_real[i1], psi_imag[i1] = -1.0 * psi_imag[i1].clone(), psi_real[i1].clone()
            elif Gate_type == 'sdg':
                psi_imag[i1], psi_real[i1] = -1.0 * psi_real[i1].clone(), psi_imag[i1].clone()
            elif Gate_type == 't':
                angle = torch.tensor(math.pi / 4)
                c = torch.cos(angle)
                s = torch.sin(angle)
                psi_real_i1 = c * psi_real[i1] - s * psi_imag[i1]
                psi_imag_i1 = s * psi_real[i1] + c * psi_imag[i1]
                psi_real[i1], psi_imag[i1] = psi_real_i1, psi_imag_i1
            elif Gate_type == 'tdg':
                angle = torch.tensor(-math.pi / 4)
                c = torch.cos(angle)
                s = torch.sin(angle)
                psi_real_i1 = c * psi_real[i1] - s * psi_imag[i1]
                psi_imag_i1 = s * psi_real[i1] + c * psi_imag[i1]
                psi_real[i1], psi_imag[i1] = psi_real_i1, psi_imag_i1

    return psi_real + 1j*psi_imag

if __name__ == '__main__':
    # Initial state vector |000>
    psi_real = torch.tensor([1, 0, 0, 0, 0, 0, 0, 0], dtype=torch.float32)
    psi_imag = torch.tensor([0, 0, 0, 0, 0, 0, 0, 0], dtype=torch.float32)
    num_qubits = 3  # Number of qubits in the system

    circuit = QuantumCircuit(num_qubits)
    # 制备初态
    circuit.add_single_gate(0, 'x')
    circuit.add_single_gate(1, 'x')
    circuit.add_single_gate(2, 'x')
    circuit.add_single_gate(1, 'h')
    circuit.add_single_gate(0, 'rx', math.pi/4)
    circuit.add_single_gate(1, 'ry', math.pi/3)
    circuit.add_single_gate(2, 'rz', math.pi/2)
    circuit.add_single_gate(0, 'u3', math.pi/4, math.pi/3, math.pi/2)
    circuit.add_single_gate(1, 's')
    circuit.add_single_gate(2, 'sdg')
    circuit.add_single_gate(1, 't')
    circuit.add_single_gate(2, 'tdg')
    circuit.run_statevector()
    print(circuit.state)

    gate_list = [
        ([0], 'x'),
        ([1], 'x'),
        ([2], ('x',)),
        ([1], ('h',)),  
        ([0], ('rx', math.pi/4)),  
        ([1], ('ry', math.pi/3)),  
        ([2], ('rz', math.pi/2)),  
        ([0], ('u3', math.pi/4, math.pi/3, math.pi/2)),
        ([1], ('s',)),
        ([2], ('sdg',)),
        ([1], ('t',)),
        ([2], ('tdg',))  
    ]

    # Apply each gate in the list to the state vector
    for ele in gate_list:
        Gate_pos = ele[0]
        Gate_type = ele[1][0]
        Angles = tuple()
        if len(ele[1]) > 1:
            Angles = tuple(ele[1][1:])
        psi_real, psi_imag = ActOn_State(psi_real, psi_imag, num_qubits, Gate_type, Gate_pos, *Angles)

    # Combine the real and imaginary parts to form the complex state vector
    final_psi = psi_real + 1j * psi_imag
    print("final_psi:", final_psi)
