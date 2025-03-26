"""
-*- coding: utf-8 -*-
@Author : Cui Jinghao
@Time : 2024/7/2 14:37
@Function: test
@Contact: cuijinghao@tgqs.net
"""
from circuit.QuantumCircuit import QuantumCircuit
import numpy as np
from sim.QuantumSimulator import QuantumSimulator
from openqasm2.qasmParser import QASMParser
import tgqSim as tgqs
from tgqSim.utils.visualization import to_text_diag

if __name__ == '__main__':
    # use case as below
    nQubits = 3
    qc = QuantumCircuit(0)
    qc.add_qubits(nQubits, name='qft')
    hgatetest = tgqs.h
    hgatetest(1)
    # # hgate = tgqs.h(1)
    # # # print(hgate)
    # qc.append(hgatetest)
    # print(qc.gate_list)

    u3gatetest = tgqs.u3
    u3gatetest(1, 0.1, 0.2, 0.3)
    # qc.append(u3gatetest)
    # print(qc.gate_list)



    ###########
    x0 = tgqs.x(0)
    x1 = tgqs.x(1)
    z0 = tgqs.z(0)
    z1 = tgqs.z(1)
    print(id(z0), id(z1))
    qc.append(z0)
    qc.append(z1)
    print(qc.gate_list)






    xgate = tgqs.x(0)
    # print(xgate)
    # qc.append(xgate)
    # print(qc)
    # qc.with_noise(0,'depolarize', 0.41)

    #

    # qc.append(tgqs.measure([0]))
    # print(qc.noise_circuit)
    # print(qc.displayname_list)
    # print(qc)

    # print(qc.gate_list)
    # rxgate = tgqs.rx(qbit=1, theta=0.707)
    # # print(rxgate)
    # qc.append(rxgate)
    # print(qc.gate_list)
    # rxxgate = tgqs.rxx(0,1,0.707)
    # qc.append(rxxgate)
    # print(qc.gate_list)
    # rxgatetest = tgqs.rx
    # rxgatetest(1, 0.707)
    # qc.append(rxgatetest)
    #
    # ccxgatetest = tgqs.ccx
    # ccxgatetest([0,2], 1)
    #
    # cxgatetest = tgqs.cx
    # cxgatetest()
    # cpgatetest = tgqs.cp
    # cpgatetest()
    #
    # tgqs.rxx()

    # measuregatetest = tgqs.measure

    # tgqs.ccx()
    # tgqs.rzz()


    # qc.append(ccxgatetest)
    # print(qc.gate_list)
    # print(qc)

    # qasm_code = """
    # OPENQASM 2.0;
    # qreg q[5]
    # h q[0];
    # cx q[0], q[1];
    # rz(0.708) q[0];
    # rz(0) q[0];
    # rz(-0.5) q[0];
    # u3(0.708, 0.708, 0.708) q[1];
    #
    # """
    # qc = QASMParser(qasm_code).parse()
    # print(qc)
    # # qc.append(tgqs.measure([2,1,0,3]))
    # print(qc.width)
    # print(qc.gate_list)
    # qc.with_noise(0,'bit_flip', 0.1)
    # print(qc.noise_circuit)
    # print(qc.gate_list)
    # simulator = QuantumSimulator()
    # noise_res = simulator.run_with_noise(qc, shots=1000)
    # print(noise_res)

    # # # get state vector
    # simulated_state = simulator.run_statevector(qc, 'CPU')
    # print(simulated_state)
    # #
    # # # get probability vector
    # result = simulator.execute(qc)
    # print(result)
    # prob = simulator.freq_to_prob(result)
    # print(prob)
    # qc.add_single_gate(hgatetest)
    # qc.append()
    # for i in range(nQubits):
    #     if nQubits - 2 == i:
    #         qc.x(i)
    #     else:
    #         qc.h(i)
    # for i in range(nQubits - 1, -1, -1):
    #     for j in range(i, -1, -1):
    #         if j == i:
    #             qc.h(j)
    #         else:
    #             qc.cp(control_qubit=j, target_qubit=i, theta=np.pi / (2 ** (i - j)))
    # qc.x(0)
    # for i in range(0, nQubits // 2):
    #     qc.swap(qubit_1=i, qubit_2=nQubits - 1 - i)
    #
    # simulator = QuantumSimulator()
    # simulator.
    # qc.run_statevector()
    # print(qc.state)
    # print(len(qc.state))
    # measure_pos = sorted([1, 0], reverse=True)
    # print(qc.execute(measure_bits_list=measure_pos))
    # qc.show_quantum_circuit()
