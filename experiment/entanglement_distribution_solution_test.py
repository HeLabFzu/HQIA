import sys
sys.path.append("..")

import netsquid as ns
import pandas
import pydynaa
from topology.Distributed_Cellular_Topo_simple_parameter import Distributed_Cellular_Network_setup
from topology.Centralized_Cellular_Topo_simple_parameter import Centralized_Cellular_Network_setup
from protocol.distributed.DistributedEntanglementDistribution import DistributedEntanglementDistribution
from protocol.distributed.DistributedSwapping import DistributedSwapping
from protocol.distributed.DistributedTeleportation import DistributedTeleportation
from protocol.centralized.CentralizedEntanglementDistribution import CentralizedEntanglementDistribution
from protocol.centralized.CentralizedSwapping import CentralizedSwapping
from protocol.centralized.CentralizedTeleportation import CentralizedTeleportation
from util.CheckDistribution import CheckDistribution
from util.NodeStruct import NodeStruct
from util.QubitCreation import CreateQubit
from util.CollectData import collect_distribution_data,collect_fidelity_data
from util.ResourceLockRelease import resource_lock,resource_release
from netsquid.components import instructions as instr
from netsquid.util.datacollector import DataCollector
from netsquid.protocols.protocol import Signals
from matplotlib import pyplot as plt

"""
This program explores the performance of entanglement preparation & distribution solutions(W-state Based CEPD, Double-photon Based CEPD, Traditional DEPD).
The program takes about 3 minutes to complete.
"""

def generate_distributed_path(depolar_rate,dephase_rate,qchannel_loss_init,qchannel_loss_noisy):
    network = Distributed_Cellular_Network_setup(node_distance=100,depolar_rate=depolar_rate,dephase_rate=dephase_rate,
                             qchannel_loss_init=qchannel_loss_init, qchannel_loss_noisy=qchannel_loss_noisy)
    Repeater_A = network.subcomponents["Repeater_A"]
    Repeater_B = network.subcomponents["Repeater_B"]
    Repeater_C = network.subcomponents["Repeater_C"]
    Repeater_D = network.subcomponents["Repeater_D"]
    Repeater_E = network.subcomponents["Repeater_E"]
    Repeater_F = network.subcomponents["Repeater_F"]
    Repeater_G = network.subcomponents["Repeater_G"]
    Repeater_H = network.subcomponents["Repeater_H"]
    Repeater_I = network.subcomponents["Repeater_I"]
    Repeater_J = network.subcomponents["Repeater_J"]
    Repeater_K = network.subcomponents["Repeater_K"]
    Repeater_L = network.subcomponents["Repeater_L"]
    Repeater_M = network.subcomponents["Repeater_M"]
    Repeater_N = network.subcomponents["Repeater_N"]
    Repeater_O = network.subcomponents["Repeater_O"]
    Repeater_P = network.subcomponents["Repeater_P"]
    Repeater_Q = network.subcomponents["Repeater_Q"]
    Repeater_R = network.subcomponents["Repeater_R"]
    Repeater_S = network.subcomponents["Repeater_S"]
    Repeater_T = network.subcomponents["Repeater_T"]
    Repeater_U = network.subcomponents["Repeater_U"]
    Repeater_V = network.subcomponents["Repeater_V"]
    Repeater_W = network.subcomponents["Repeater_W"]
    Repeater_X = network.subcomponents["Repeater_X"]
    User_A = network.subcomponents["User_A"]
    User_B = network.subcomponents["User_B"]
    User_C = network.subcomponents["User_C"]
    User_D = network.subcomponents["User_D"]
    User_E = network.subcomponents["User_E"]
    ### path_UA_UB is User_A->Repeater_P->Repeater_C->Repeater_Q->Repeater_E->Repeater_T->Repeater_I->Repeater_W->Repeater_L->Repeater_X->User_B 9_hops_path in distributed network###
    path_UA_UB = []
    path_UA_UB.append(NodeStruct(node=User_A,entangle_distribution_role="generator",qsource_name="User_A_Repeater_P_QSource",store_mem_pos_1=4))
    path_UA_UB.append(NodeStruct(node=Repeater_P,entangle_distribution_role="receiver",store_mem_pos_1=4))
    path_UA_UB.append(NodeStruct(node=Repeater_P,entangle_distribution_role="generator",qsource_name="Repeater_P_Repeater_C_QSource",store_mem_pos_1=5))
    path_UA_UB.append(NodeStruct(node=Repeater_C,entangle_distribution_role="receiver",store_mem_pos_1=4))
    path_UA_UB.append(NodeStruct(node=Repeater_C,entangle_distribution_role="generator",qsource_name="Repeater_C_Repeater_Q_QSource",store_mem_pos_1=5))
    path_UA_UB.append(NodeStruct(node=Repeater_Q,entangle_distribution_role="receiver",store_mem_pos_1=4))
    path_UA_UB.append(NodeStruct(node=Repeater_Q,entangle_distribution_role="generator",qsource_name="Repeater_Q_Repeater_E_QSource",store_mem_pos_1=5))
    path_UA_UB.append(NodeStruct(node=Repeater_E,entangle_distribution_role="receiver",store_mem_pos_1=4))
    path_UA_UB.append(NodeStruct(node=Repeater_E,entangle_distribution_role="generator",qsource_name="Repeater_E_Repeater_T_QSource",store_mem_pos_1=5))
    path_UA_UB.append(NodeStruct(node=Repeater_T,entangle_distribution_role="receiver",store_mem_pos_1=4))
    path_UA_UB.append(NodeStruct(node=Repeater_T,entangle_distribution_role="generator",qsource_name="Repeater_T_Repeater_I_QSource",store_mem_pos_1=5))
    path_UA_UB.append(NodeStruct(node=Repeater_I,entangle_distribution_role="receiver",store_mem_pos_1=4))
    path_UA_UB.append(NodeStruct(node=Repeater_I,entangle_distribution_role="generator",qsource_name="Repeater_I_Repeater_W_QSource",store_mem_pos_1=5))
    path_UA_UB.append(NodeStruct(node=Repeater_W,entangle_distribution_role="receiver",store_mem_pos_1=4))
    path_UA_UB.append(NodeStruct(node=Repeater_W,entangle_distribution_role="generator",qsource_name="Repeater_W_Repeater_L_QSource",store_mem_pos_1=5))
    path_UA_UB.append(NodeStruct(node=Repeater_L,entangle_distribution_role="receiver",store_mem_pos_1=4))
    path_UA_UB.append(NodeStruct(node=Repeater_L,entangle_distribution_role="generator",qsource_name="Repeater_L_Repeater_X_QSource",store_mem_pos_1=5))
    path_UA_UB.append(NodeStruct(node=Repeater_X,entangle_distribution_role="receiver",store_mem_pos_1=4))
    path_UA_UB.append(NodeStruct(node=Repeater_X,entangle_distribution_role="generator",qsource_name="Repeater_X_User_B_QSource",store_mem_pos_1=5))
    path_UA_UB.append(NodeStruct(node=User_B,entangle_distribution_role="receiver",store_mem_pos_1=4))
    resource_lock(path_UA_UB)
    return path_UA_UB

def generate_centralized_path(depolar_rate,dephase_rate,qchannel_loss_init,qchannel_loss_noisy):
    network = Centralized_Cellular_Network_setup(node_distance=100,depolar_rate=depolar_rate,dephase_rate=dephase_rate,
                             qchannel_loss_init=qchannel_loss_init, qchannel_loss_noisy=qchannel_loss_noisy)
    Central_Controller = network.subcomponents["Central_Controller"]
    Controller_A = network.subcomponents["Controller_A"]
    Controller_B = network.subcomponents["Controller_B"]
    Controller_C = network.subcomponents["Controller_C"]
    Controller_D = network.subcomponents["Controller_D"]
    Controller_E = network.subcomponents["Controller_E"]
    Controller_F = network.subcomponents["Controller_F"]
    Controller_G = network.subcomponents["Controller_G"]
    Controller_H = network.subcomponents["Controller_H"]
    Controller_I = network.subcomponents["Controller_I"]
    Repeater_A = network.subcomponents["Repeater_A"]
    Repeater_B = network.subcomponents["Repeater_B"]
    Repeater_C = network.subcomponents["Repeater_C"]
    Repeater_D = network.subcomponents["Repeater_D"]
    Repeater_E = network.subcomponents["Repeater_E"]
    Repeater_F = network.subcomponents["Repeater_F"]
    Repeater_G = network.subcomponents["Repeater_G"]
    Repeater_H = network.subcomponents["Repeater_H"]
    Repeater_I = network.subcomponents["Repeater_I"]
    Repeater_J = network.subcomponents["Repeater_J"]
    Repeater_K = network.subcomponents["Repeater_K"]
    Repeater_L = network.subcomponents["Repeater_L"]
    Repeater_M = network.subcomponents["Repeater_M"]
    Repeater_N = network.subcomponents["Repeater_N"]
    Repeater_O = network.subcomponents["Repeater_O"]
    User_A = network.subcomponents["User_A"]
    User_B = network.subcomponents["User_B"]
    User_C = network.subcomponents["User_C"]
    User_D = network.subcomponents["User_D"]
    User_E = network.subcomponents["User_E"]

    ### path_UA_UB is User_A->Repeater_C->Repeater_E->Repeater_I->Repeater_L->User_B 4_hops_path in centralized network ###
    path_UA_UB = []
    path_UA_UB.append(NodeStruct(node=User_A,entangle_distribution_role="user",
                         store_mem_pos_1=1))
    path_UA_UB.append(NodeStruct(node=Controller_A,entangle_distribution_role="controller",
                         qsource_name="Controller_A_Repeater_C_User_A_QSource"))
    path_UA_UB.append(NodeStruct(node=Repeater_C,entangle_distribution_role="repeater",
                         store_mem_pos_1=1,store_mem_pos_2=2))
    path_UA_UB.append(NodeStruct(node=Controller_B,entangle_distribution_role="controller",
                         qsource_name="Controller_B_Repeater_C_Repeater_E_QSource"))
    path_UA_UB.append(NodeStruct(node=Repeater_E,entangle_distribution_role="repeater",
                         store_mem_pos_1=1,store_mem_pos_2=2))
    path_UA_UB.append(NodeStruct(node=Controller_E,entangle_distribution_role="controller",
                         qsource_name="Controller_E_Repeater_E_Repeater_I_QSource"))
    path_UA_UB.append(NodeStruct(node=Repeater_I,entangle_distribution_role="repeater",
                         store_mem_pos_1=1,store_mem_pos_2=2))
    path_UA_UB.append(NodeStruct(node=Controller_H,entangle_distribution_role="controller",
                         qsource_name="Controller_H_Repeater_I_Repeater_L_QSource"))
    path_UA_UB.append(NodeStruct(node=Repeater_L,entangle_distribution_role="repeater",
                         store_mem_pos_1=1,store_mem_pos_2=2))
    path_UA_UB.append(NodeStruct(node=Controller_I,entangle_distribution_role="controller",
                         qsource_name="Controller_I_Repeater_L_User_B_QSource"))
    path_UA_UB.append(NodeStruct(node=User_B,entangle_distribution_role="user",
                          store_mem_pos_1=1))
    resource_lock(path_UA_UB)
    return path_UA_UB,Central_Controller

def define_distributed_protocol(path):
    ### define entanglement_distribution_protocol ###
    entangle_distribution_protocol = []
    entangle_distribution_protocol_temp = []
    for node_number in range(len(path)):
        if path[node_number].entangle_distribution_role == "generator":
            entangle_distribution_protocol_temp.append(DistributedEntanglementDistribution(node=path[node_number].node,
                                                                               role="generator",qsource_name=path[node_number].qsource_name,
                                                                               store_mem_pos=path[node_number].store_mem_pos_1))
        if path[node_number].entangle_distribution_role == "receiver":
            entangle_distribution_protocol_temp.append(DistributedEntanglementDistribution(node=path[node_number].node,
                                                                               role="receiver",store_mem_pos=path[node_number].store_mem_pos_1))
            if len(entangle_distribution_protocol_temp) == 2:
                entangle_distribution_protocol.append(entangle_distribution_protocol_temp)
                entangle_distribution_protocol_temp=[]

    ### define swapping protocol ###
    swapping_protocol= []
    swapping_protocol_temp = []
    for node_number in range(len(path)):
        if path[node_number].entangle_distribution_role == "generator" and node_number != 0:
            swapping_protocol_temp.append(DistributedSwapping(node=path[node_number].node,
                                                  port=path[node_number].node.get_conn_port(path[node_number+1].node.ID),
                                                  role="repeater",repeater_mem_posA=path[node_number-1].store_mem_pos_1,
                                                  repeater_mem_posB=path[node_number].store_mem_pos_1))
        if path[node_number].entangle_distribution_role == "receiver" and node_number != 1:
            swapping_protocol_temp.append(DistributedSwapping(node=path[node_number].node,
                                                  port=path[node_number].node.get_conn_port(path[node_number-1].node.ID),
                                                  role="corrector", corrector_mem_pos=path[node_number].store_mem_pos_1))
            if len(swapping_protocol_temp) == 2:
                swapping_protocol.append(swapping_protocol_temp)
                swapping_protocol_temp = []

    ### define create target qubit protocol ###
    create_qubit_protocol = CreateQubit(path[0].node,mem_pos=0)

    ### define teleportation protocol ###
    teleportation_protocol = DistributedTeleportation(path, 0)

    return entangle_distribution_protocol,swapping_protocol, create_qubit_protocol, teleportation_protocol

def define_centralized_protocol(path,Central_Controller):
    ### define entanglement_distribution_protocol ###
    entangle_distribution_protocol = []
    entangle_distribution_protocol_temp = []
    for node_number in range(len(path)):
        if path[node_number].entangle_distribution_role == "user":
            entangle_distribution_protocol_temp.append(CentralizedEntanglementDistribution(node=path[node_number].node,
                                                                               role="user",
                                                                               store_mem_pos=path[node_number].store_mem_pos_1))
            if len(entangle_distribution_protocol_temp) == 3:
                entangle_distribution_protocol.append(entangle_distribution_protocol_temp)
                entangle_distribution_protocol_temp=[]
        if path[node_number].entangle_distribution_role == "controller":
            entangle_distribution_protocol_temp.append(CentralizedEntanglementDistribution(node=path[node_number].node,
                                                                               role="controller",
                                                                               qsource_name=path[node_number].qsource_name))
        if path[node_number].entangle_distribution_role == "repeater":
            entangle_distribution_protocol_temp.append(CentralizedEntanglementDistribution(node=path[node_number].node,
                                                                               role="repeater",
                                                                               store_mem_pos=path[node_number].store_mem_pos_1))
            if len(entangle_distribution_protocol_temp) == 3:
                entangle_distribution_protocol.append(entangle_distribution_protocol_temp)
                entangle_distribution_protocol_temp=[]
            entangle_distribution_protocol_temp.append(CentralizedEntanglementDistribution(node=path[node_number].node,
                                                                               role="repeater",
                                                                               store_mem_pos=path[node_number].store_mem_pos_2))
    ### define swapping protocol ###
    swapping_protocol= []
    swapping_protocol_temp = []
    for node_number in range(len(path)):
        if path[node_number].entangle_distribution_role == "user" and node_number != 0:
            swapping_protocol_temp.append(CentralizedSwapping(node=path[node_number].node,
                                                  port=path[node_number].node.get_conn_port(path[node_number-1].node.ID),
                                                  role="corrector",corrector_mem_pos=path[node_number].store_mem_pos_1))
            if len(swapping_protocol_temp) == 3:
                swapping_protocol.append(swapping_protocol_temp)
                swapping_protocol_temp = []
        if path[node_number].entangle_distribution_role == "controller" and node_number != 1:
            swapping_protocol_temp.append(CentralizedSwapping(node=path[node_number].node,
                                                  port=path[node_number].node.get_conn_port(path[node_number-1].node.ID),
                                                  portout=path[node_number].node.get_conn_port(path[node_number+1].node.ID),
                                                  role="localcontroller"))
        if path[node_number].entangle_distribution_role == "repeater":
            if node_number != 2:
                swapping_protocol_temp.append(CentralizedSwapping(node=path[node_number].node,
                                                  port=path[node_number].node.get_conn_port(path[node_number-1].node.ID),
                                                  role="corrector", corrector_mem_pos=path[node_number].store_mem_pos_1))
                if len(swapping_protocol_temp) == 3:
                    swapping_protocol.append(swapping_protocol_temp)
                    swapping_protocol_temp = []
            swapping_protocol_temp.append(CentralizedSwapping(node=path[node_number].node,
                                                  port=path[node_number].node.get_conn_port(path[node_number+1].node.ID),
                                                  role="repeater", repeater_mem_posA=path[node_number].store_mem_pos_1,
                                                  repeater_mem_posB=path[node_number].store_mem_pos_2))

    ### define create target qubit protocol ###
    create_qubit_protocol = CreateQubit(path[0].node,mem_pos=0)

    ### define teleportation protocol ###
    teleportation_protocol = CentralizedTeleportation(path[0].node, path[len(path)-1].node, path[1].node, path[len(path)-2].node, Central_Controller, 0, path[0].store_mem_pos_1, path[len(path)-1].store_mem_pos_1)

    return entangle_distribution_protocol,swapping_protocol, create_qubit_protocol, teleportation_protocol

def run_protocol(depolar_rate,dephase_rate,qchannel_loss_init_rate,qchannel_loss_noisy_rate,multiple,solution_name):
    fidelity_data_temp = pandas.DataFrame()
    round = 300
    if solution_name == "distributed":
        path_UA_UB = generate_distributed_path(depolar_rate,dephase_rate,qchannel_loss_init_rate,qchannel_loss_noisy_rate)
        entangle_distribution_protocol, swapping_protocol, create_qubit_protocol, teleportation_protocol= define_distributed_protocol(path_UA_UB)
    if solution_name == "centralized_optical_quantum_memory":
        path_UA_UB, Central_Controller = generate_centralized_path(depolar_rate,dephase_rate,qchannel_loss_init_rate,qchannel_loss_noisy_rate)
        entangle_distribution_protocol, swapping_protocol, create_qubit_protocol, teleportation_protocol= define_centralized_protocol(path_UA_UB,Central_Controller)
    if solution_name == "centralized_w_state":
        path_UA_UB, Central_Controller = generate_centralized_path(depolar_rate,dephase_rate,qchannel_loss_init_rate,qchannel_loss_noisy_rate)
        entangle_distribution_protocol, swapping_protocol, create_qubit_protocol, teleportation_protocol= define_centralized_protocol(path_UA_UB,Central_Controller)
    while round > 0:
        print("#### Start Entanglement Distribution Process ####")
        Entanglement_Distribution_Signal = True
        for i in range(len(entangle_distribution_protocol)):
            if Entanglement_Distribution_Signal:
                for j in range(len(entangle_distribution_protocol[i])):
                    entangle_distribution_protocol[i][j].start()
                ns.sim_run()
                for j in range(len(entangle_distribution_protocol[i])):
                    if not entangle_distribution_protocol[i][j].check():
                        Entanglement_Distribution_Signal = False
                        for k in range(len(entangle_distribution_protocol[i])):
                            entangle_distribution_protocol[i][k].stop()
                        print("Entanglement Distribution Failed")
                        break
            else:
                break
        check_distribution=CheckDistribution(Entanglement_Distribution_Signal)
        dc_distribution = DataCollector(collect_distribution_data)
        dc_distribution.collect_on(pydynaa.EventExpression(source=check_distribution,
                                              event_type=Signals.SUCCESS.value))
        check_distribution.start()
        ns.sim_run()
        print("#### Complete Entanglement Distribution Process ####")
        if check_distribution.getresult() == 0:
            resource_release(path_UA_UB)
            if solution_name == "distributed" or solution_name == "centralized_optical_quantum_memory":
                for num in [2,5,10,20,50]:
                    df=dc_distribution.dataframe
                    df['multiple_of_storage_efficiency_for_atom_mem_vs_optical_mem'] = num
                    df['solution_name'] = solution_name
                    fidelity_data_temp = fidelity_data_temp.append(df)
            else:
                df=dc_distribution.dataframe
                df['multiple_of_storage_efficiency_for_atom_mem_vs_optical_mem'] = multiple
                df['solution_name'] = solution_name
                fidelity_data_temp = fidelity_data_temp.append(df)
        else:
            print("#### Start Entanglement Swapping Process ####")
            for i in range(len(swapping_protocol)):
                for j in range(len(swapping_protocol[i])):
                    swapping_protocol[i][j].start()
                ns.sim_run()
            print("#### Complete Entanglement Swapping Process ####")
            print("#### Start to Create Target Qubit ####")
            create_qubit_protocol.start()
            ns.sim_run()
            print("#### Complete to Create Target Qubit ####")
            print("#### Start to teleport target qubit")
            dc_fidelity = DataCollector(collect_fidelity_data)
            dc_fidelity.collect_on(pydynaa.EventExpression(source=teleportation_protocol,
                                                  event_type=Signals.SUCCESS.value))
            teleportation_protocol.start()
            ns.sim_run()
            print("#### Complete to teleport target qubit ####")
            resource_release(path_UA_UB)
            if solution_name == "distributed" or solution_name == "centralized_optical_quantum_memory":
                for num in [2,5,10,20,50]:
                    df=dc_fidelity.dataframe
                    df['multiple_of_storage_efficiency_for_atom_mem_vs_optical_mem'] = num
                    df['solution_name'] = solution_name
                    fidelity_data_temp = fidelity_data_temp.append(df)
            else:
                df=dc_fidelity.dataframe
                df['multiple_of_storage_efficiency_for_atom_mem_vs_optical_mem'] = multiple
                df['solution_name'] = solution_name
                fidelity_data_temp = fidelity_data_temp.append(df)
        round -= 1
    return fidelity_data_temp
if __name__ == '__main__':
    fidelity_data = pandas.DataFrame()
    depolar_rate = 0.1
    dephase_rate = 0.01 
    qchannel_loss_init_rate = 0.0001
    qchannel_loss_noisy_rate = 0.00001

    fidelity_data_temp = run_protocol(depolar_rate,dephase_rate,qchannel_loss_init_rate,qchannel_loss_noisy_rate,1,"distributed")
    fidelity_data = fidelity_data.append(fidelity_data_temp)

    fidelity_data_temp = run_protocol(depolar_rate,dephase_rate,qchannel_loss_init_rate,qchannel_loss_noisy_rate,1,"centralized_optical_quantum_memory")
    fidelity_data = fidelity_data.append(fidelity_data_temp)

    for multiple in [2,5,10,20,50]:
        w_state_depolar_rate = depolar_rate/multiple
        w_state_dephase_rate = 1-pow(1-dephase_rate,8)
        w_state_qchannel_loss_init_rate = 1-pow(1-qchannel_loss_init_rate,2)
        w_state_qchannel_loss_noisy_rate = qchannel_loss_noisy_rate * 2
        fidelity_data_temp = run_protocol(w_state_depolar_rate,w_state_dephase_rate,w_state_qchannel_loss_init_rate,w_state_qchannel_loss_noisy_rate,multiple,"centralized_w_state")
        fidelity_data = fidelity_data.append(fidelity_data_temp)

    plot_style = {'kind': 'line', 'grid': True,
      'title': "Fidelity in Different Entanglement Distribution Solutions"}
    fig,ax = plt.subplots()
    ax.set_ylabel('fidelity')
    for solution_name in ["distributed", "centralized_optical_quantum_memory", "centralized_w_state"]:
        data = fidelity_data[fidelity_data['solution_name']==solution_name].groupby("multiple_of_storage_efficiency_for_atom_mem_vs_optical_mem")['fidelity'].agg(
                                                                                              fidelity='mean', sem='sem').reset_index()
        data.plot(x='multiple_of_storage_efficiency_for_atom_mem_vs_optical_mem', y='fidelity', yerr='sem',ax=ax,label=solution_name, **plot_style)
        print(data)
    plt.show()


