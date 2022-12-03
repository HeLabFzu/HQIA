import sys
sys.path.append("..")

import netsquid as ns
import pandas
import pydynaa
from topology.Centralized_Cellular_Topo import Centralized_Cellular_Network_setup
from protocol.centralized.CentralizedEntanglementDistribution import CentralizedEntanglementDistribution
from protocol.centralized.CentralizedSwapping import CentralizedSwapping
from protocol.centralized.CentralizedTeleportation import CentralizedTeleportation
from util.CheckDistribution import CheckDistribution
from util.QubitCreation import CreateQubit
from util.NodeStruct import NodeStruct
from util.CollectData import collect_distribution_data,collect_fidelity_data
from util.ResourceLockRelease import resource_lock,resource_release
from netsquid.components import instructions as instr
from netsquid.util.datacollector import DataCollector
from netsquid.protocols.protocol import Signals
from matplotlib import pyplot as plt
"""
This program explores the communication fidelity under integrated conditions.

The program takes about 2 minutes to complete.
"""
def generate_path(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy):
    network = Centralized_Cellular_Network_setup(depolar_rates=depolar_rates,dephase_rates=dephase_rates,
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

    ### path_A is User_A->Repeater_C->Repeater_E->Repeater_I->Repeater_L->User_B ###
    path_A = []
    path_A.append(NodeStruct(node=User_A,entangle_distribution_role="user",
                          store_mem_pos_1=1))
    path_A.append(NodeStruct(node=Controller_A,entangle_distribution_role="controller",
                          qsource_name="Controller_A_Repeater_C_User_A_QSource"))
    path_A.append(NodeStruct(node=Repeater_C,entangle_distribution_role="repeater",
                          store_mem_pos_1=1,store_mem_pos_2=2))
    path_A.append(NodeStruct(node=Controller_B,entangle_distribution_role="controller",
                          qsource_name="Controller_B_Repeater_C_Repeater_E_QSource"))
    path_A.append(NodeStruct(node=Repeater_E,entangle_distribution_role="repeater",
                          store_mem_pos_1=1,store_mem_pos_2=2))
    path_A.append(NodeStruct(node=Controller_E,entangle_distribution_role="controller",
                          qsource_name="Controller_E_Repeater_E_Repeater_I_QSource"))
    path_A.append(NodeStruct(node=Repeater_I,entangle_distribution_role="repeater",
                          store_mem_pos_1=1,store_mem_pos_2=2))
    path_A.append(NodeStruct(node=Controller_H,entangle_distribution_role="controller",
                          qsource_name="Controller_H_Repeater_I_Repeater_L_QSource"))
    path_A.append(NodeStruct(node=Repeater_L,entangle_distribution_role="repeater",
                          store_mem_pos_1=1,store_mem_pos_2=2))
    path_A.append(NodeStruct(node=Controller_I,entangle_distribution_role="controller",
                          qsource_name="Controller_I_Repeater_L_User_B_QSource"))
    path_A.append(NodeStruct(node=User_B,entangle_distribution_role="user",
                          store_mem_pos_1=1))

    ### path_B is User_A->Repeater_C->Repeater_D->Repeater_H->Repeater_I->Repeater_L->User_B ###
    path_B = []
    path_B.append(NodeStruct(node=User_A,entangle_distribution_role="user",
                          store_mem_pos_1=1))
    path_B.append(NodeStruct(node=Controller_A,entangle_distribution_role="controller",
                          qsource_name="Controller_A_Repeater_C_User_A_QSource"))
    path_B.append(NodeStruct(node=Repeater_C,entangle_distribution_role="repeater",
                          store_mem_pos_1=1,store_mem_pos_2=2))
    path_B.append(NodeStruct(node=Controller_B,entangle_distribution_role="controller",
                          qsource_name="Controller_B_Repeater_C_Repeater_D_QSource"))
    path_B.append(NodeStruct(node=Repeater_D,entangle_distribution_role="repeater",
                          store_mem_pos_1=1,store_mem_pos_2=2))
    path_B.append(NodeStruct(node=Controller_D,entangle_distribution_role="controller",
                          qsource_name="Controller_D_Repeater_D_Repeater_H_QSource"))
    path_B.append(NodeStruct(node=Repeater_H,entangle_distribution_role="repeater",
                          store_mem_pos_1=1,store_mem_pos_2=2))
    path_B.append(NodeStruct(node=Controller_E,entangle_distribution_role="controller",
                          qsource_name="Controller_E_Repeater_H_Repeater_I_QSource"))
    path_B.append(NodeStruct(node=Repeater_I,entangle_distribution_role="repeater",
                          store_mem_pos_1=1,store_mem_pos_2=2))
    path_B.append(NodeStruct(node=Controller_H,entangle_distribution_role="controller",
                          qsource_name="Controller_H_Repeater_I_Repeater_L_QSource"))
    path_B.append(NodeStruct(node=Repeater_L,entangle_distribution_role="repeater",
                          store_mem_pos_1=1,store_mem_pos_2=2))
    path_B.append(NodeStruct(node=Controller_I,entangle_distribution_role="controller",
                          qsource_name="Controller_I_Repeater_L_User_B_QSource"))
    path_B.append(NodeStruct(node=User_B,entangle_distribution_role="user",
                          store_mem_pos_1=1))

    ### path_C is User_A->Repeater_B->Repeater_F->Repeater_I->Repeater_L->User_B ###
    path_C = []
    path_C.append(NodeStruct(node=User_A,entangle_distribution_role="user",
                          store_mem_pos_1=1))
    path_C.append(NodeStruct(node=Controller_A,entangle_distribution_role="controller",
                          qsource_name="Controller_A_Repeater_B_User_A_QSource"))
    path_C.append(NodeStruct(node=Repeater_B,entangle_distribution_role="repeater",
                          store_mem_pos_1=1,store_mem_pos_2=2))
    path_C.append(NodeStruct(node=Controller_C,entangle_distribution_role="controller",
                          qsource_name="Controller_C_Repeater_B_Repeater_F_QSource"))
    path_C.append(NodeStruct(node=Repeater_F,entangle_distribution_role="repeater",
                          store_mem_pos_1=1,store_mem_pos_2=2))
    path_C.append(NodeStruct(node=Controller_F,entangle_distribution_role="controller",
                          qsource_name="Controller_F_Repeater_F_Repeater_I_QSource"))
    path_C.append(NodeStruct(node=Repeater_I,entangle_distribution_role="repeater",
                          store_mem_pos_1=1,store_mem_pos_2=2))
    path_C.append(NodeStruct(node=Controller_H,entangle_distribution_role="controller",
                          qsource_name="Controller_H_Repeater_I_Repeater_L_QSource"))
    path_C.append(NodeStruct(node=Repeater_L,entangle_distribution_role="repeater",
                          store_mem_pos_1=1,store_mem_pos_2=2))
    path_C.append(NodeStruct(node=Controller_I,entangle_distribution_role="controller",
                          qsource_name="Controller_I_Repeater_L_User_B_QSource"))
    path_C.append(NodeStruct(node=User_B,entangle_distribution_role="user",
                          store_mem_pos_1=1))
    return path_A,path_B,path_C,User_A,User_B,Controller_A,Controller_I,Central_Controller

def define_protocol(path,User_A,User_B,Controller_A,Controller_I,Central_Controller):


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
    create_qubit_protocol = CreateQubit(User_A,mem_pos=0)

    ### define teleportation protocol ###
    teleportation_protocol = CentralizedTeleportation(User_A, User_B, Controller_A, Controller_I, Central_Controller, 0, 1, 1)


    return entangle_distribution_protocol,swapping_protocol,create_qubit_protocol,teleportation_protocol
def run_protocol(depolar_rates,dephase_rates,qchannel_loss_init_rates,qchannel_loss_noisy_rates,group_name,path_name):
    fidelity_data_temp = pandas.DataFrame()
    round = 300
    path_A,path_B,path_C,User_A,User_B,Controller_A,Controller_I,Central_Controller = generate_path(depolar_rates,dephase_rates,qchannel_loss_init_rates,qchannel_loss_noisy_rates)
    if path_name == "path_A":
        path = path_A
    if path_name == "path_B":
        path = path_B
    if path_name == "path_C":
        path = path_C
    entangle_distribution_protocol,swapping_protocol,create_qubit_protocol,teleportation_protocol = define_protocol(path,User_A,User_B,Controller_A,Controller_I,Central_Controller)
    while round > 0:
        resource_lock(path)
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
            resource_release(path)
            df=dc_distribution.dataframe
            df['group_name'] = group_name
            df['path_name'] = path_name
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
            resource_release(path)
            df=dc_fidelity.dataframe
            df['group_name'] = group_name
            df['path_name'] = path_name
            fidelity_data_temp = fidelity_data_temp.append(df)
        round -= 1
    return fidelity_data_temp

if __name__ == '__main__':
    fidelity_data = pandas.DataFrame()
    """
    depolar_rates : float
        An Array with 29 items (Repeater_A~Repeater_O, Controller_A~Controller_I, User_A~User_E),Depolarization rate of qubits in memory. probability
    dephase_rates : float
        An Array with 29 items (Repeater_A~Repeater_O, Controller_A~Controller_I, User_A,User_E),Dephasing rate of physical measurement instruction. probability
    qchannel_loss_init : float
        An Array with 32 items (Domain_A~Domian_I quantum channel,e.g 0~3 items means Controller_A->RepeaterA,B,C,UserA), Initial probability of losing a photon once it enters a quantum channel
    qchannel_loss_noisy : float
        An Array with 32 items (Domain_A~Domian_I quantum channel,e.g 0~3 items means Controller_A->RepeaterA,B,C,UserA), Photon survival probability per channel length [dB/km].
    """

    """
    Group_1 
    Path A 
    avg depolar: 0.025
    avg dephase: 0.025
    avg init: 0.011
    avg noisy*100km: 0.11 dB
    
    Path B 
    avg depolar: 0.012        Difference : vs Path A 0.013  vs Path C 0.028
    avg dephase: 0.012        Difference : vs Path A 0.013  vs Path C 0.028
    avg init: 0.007           Difference : vs Path A 0.004  vs Path C 0.019
    avg noisy*100km: 0.07dB   Difference : vs Path A 0.04dB  vs Path C 0.19dB
    
    Path C 
    avg depolar: 0.040
    avg dephase: 0.040
    avg init: 0.026 
    avg noisy*100km: 0.26dB 
    """

    depolar_rates_group_1 = [0,0.1,0.01,0.02,0.1,0.1,0,0.02,0.01,0,0,0.01,0,0,0,0,0,0,0,0,0,0,0,0,0.01,0.01,0,0,0]
    dephase_rates_group_1 = [0,0.1,0.01,0.02,0.1,0.1,0,0.02,0.01,0,0,0.01,0,0,0,0,0,0,0,0,0,0,0,0,0.01,0.01,0,0,0]
    qchannel_loss_init_rates_group_1 = [0,0.05,0.001,0.001,0.001,0.02,0.05,0,0.05,0,0.05,0.02,0,0.02,0.05,0.02,0.001,0,0.05,0.05,0,0,0,0,0.001,0.001,0,0,0.001,0,0,0.001]
    qchannel_loss_noisy_rates_group_1 = [0,0.005,0.0001,0.0001,0.0001,0.002,0.005,0,0.005,0,0.005,0.002,0,0.002,0.005,0.002,0.0001,0,0.005,0.005,0,0,0,0,0.0001,0.0001,0,0,0.0001,0,0,0.0001]

    fidelity_data_temp = run_protocol(depolar_rates_group_1,dephase_rates_group_1,qchannel_loss_init_rates_group_1,qchannel_loss_noisy_rates_group_1,"Group_1","path_A")
    fidelity_data = fidelity_data.append(fidelity_data_temp)

    fidelity_data_temp = run_protocol(depolar_rates_group_1,dephase_rates_group_1,qchannel_loss_init_rates_group_1,qchannel_loss_noisy_rates_group_1,"Group_1","path_B")
    fidelity_data = fidelity_data.append(fidelity_data_temp)

    fidelity_data_temp = run_protocol(depolar_rates_group_1,dephase_rates_group_1,qchannel_loss_init_rates_group_1,qchannel_loss_noisy_rates_group_1,"Group_1","path_C")
    fidelity_data = fidelity_data.append(fidelity_data_temp)
    
    """
    Group_2 
    Path A 
    avg depolar: 0.042
    avg dephase: 0.042
    avg init: 0.016
    avg noisy*100km: 0.16dB
    
    Path B 
    avg depolar: 0.010           Difference :  vs Path A 0.032   vs Path C 0.060
    avg dephase: 0.010           Difference :  vs Path A 0.032   vs Path C 0.060
    avg init: 0.004              Difference : vs Path A 0.012  vs Path C 0.034
    avg noisy*100km: 0.04dB      Difference : vs Path A 0.12dB  vs Path C 0.34dB
    
    Path C 
    avg depolar: 0.070
    avg dephase: 0.070
    avg init: 0.038 
    avg noisy*100km: 0.38dB 
    """

    depolar_rates_group_2 = [0,0.2,0.01,0.01,0.2,0.2,0,0.01,0.01,0,0,0.01,0,0,0,0,0,0,0,0,0,0,0,0,0.01,0.01,0,0,0]
    dephase_rates_group_2 = [0,0.2,0.01,0.01,0.2,0.2,0,0.01,0.01,0,0,0.01,0,0,0,0,0,0,0,0,0,0,0,0,0.01,0.01,0,0,0]
    qchannel_loss_init_rates_group_2 = [0,0.075,0.001,0.001,0.001,0.01,0.075,0,0.075,0,0.075,0.01,0,0.01,0.075,0.01,0.001,0,0.075,0.075,0,0,0,0,0.001,0.001,0,0,0.001,0,0,0.001]
    qchannel_loss_noisy_rates_group_2 = [0,0.0075,0.0001,0.0001,0.0001,0.001,0.0075,0,0.0075,0,0.0075,0.001,0,0.001,0.0075,0.001,0.0001,0,0.0075,0.0075,0,0,0,0,0.0001,0.0001,0,0,0.0001,0,0,0.0001]

    fidelity_data_temp = run_protocol(depolar_rates_group_2,dephase_rates_group_2,qchannel_loss_init_rates_group_2,qchannel_loss_noisy_rates_group_2,"Group_2","path_A")
    fidelity_data = fidelity_data.append(fidelity_data_temp)

    fidelity_data_temp = run_protocol(depolar_rates_group_2,dephase_rates_group_2,qchannel_loss_init_rates_group_2,qchannel_loss_noisy_rates_group_2,"Group_2","path_B")
    fidelity_data = fidelity_data.append(fidelity_data_temp)

    fidelity_data_temp = run_protocol(depolar_rates_group_2,dephase_rates_group_2,qchannel_loss_init_rates_group_2,qchannel_loss_noisy_rates_group_2,"Group_2","path_C")
    fidelity_data = fidelity_data.append(fidelity_data_temp)

    """
    Group_3 
    Path A 
    avg depolar: 0.092
    avg dephase: 0.092
    avg init: 0.028
    avg noisy*100km: 0.28dB
    
    Path B 
    avg depolar: 0.009        Difference : vs Path A 0.083   vs Path C 0.164
    avg dephase: 0.009        Difference : vs Path A 0.083   vs Path C 0.164
    avg init: 0.001           Difference : vs Path A 0.027  vs Path C 0.054
    avg noisy*100km: 0.01dB   Difference : vs Path A 0.27dB    vs Path C 0.54dB
    
    Path C 
    avg depolar: 0.173
    avg dephase: 0.173
    avg init: 0.055 
    avg noisy*100km: 0.55dB
    """

    depolar_rates_group_3 = [0,0.5,0.01,0.005,0.5,0.5,0,0.005,0.01,0,0,0.01,0,0,0,0,0,0,0,0,0,0,0,0,0.01,0.01,0,0,0]
    dephase_rates_group_3 = [0,0.5,0.01,0.005,0.5,0.5,0,0.005,0.01,0,0,0.01,0,0,0,0,0,0,0,0,0,0,0,0,0.01,0.01,0,0,0]
    qchannel_loss_init_rates_group_3 = [0,0.1,0.001,0.001,0.001,0.001,0.1,0,0.1,0,0.1,0.001,0,0.001,0.1,0.001,0.001,0,0.1,0.1,0,0,0,0,0.001,0.001,0,0,0.001,0,0,0.001]
    qchannel_loss_noisy_rates_group_3 = [0,0.01,0.0001,0.0001,0.0001,0.0001,0.01,0,0.01,0,0.01,0.0001,0,0.0001,0.01,0.0001,0.0001,0,0.01,0.01,0,0,0,0,0.0001,0.0001,0,0,0.0001,0,0,0.0001]

    fidelity_data_temp = run_protocol(depolar_rates_group_3,dephase_rates_group_3,qchannel_loss_init_rates_group_3,qchannel_loss_noisy_rates_group_3,"Group_3","path_A")
    fidelity_data = fidelity_data.append(fidelity_data_temp)

    fidelity_data_temp = run_protocol(depolar_rates_group_3,dephase_rates_group_3,qchannel_loss_init_rates_group_3,qchannel_loss_noisy_rates_group_3,"Group_3","path_B")
    fidelity_data = fidelity_data.append(fidelity_data_temp)

    fidelity_data_temp = run_protocol(depolar_rates_group_3,dephase_rates_group_3,qchannel_loss_init_rates_group_3,qchannel_loss_noisy_rates_group_3,"Group_3","path_C")
    fidelity_data = fidelity_data.append(fidelity_data_temp)

    group_1 = fidelity_data[fidelity_data['group_name']=="Group_1"].groupby("path_name")['fidelity'].agg(
                                                                                              fidelity='mean', sem='sem').reset_index()
    group_2 = fidelity_data[fidelity_data['group_name']=="Group_2"].groupby("path_name")['fidelity'].agg(
                                                                                              fidelity='mean', sem='sem').reset_index()
    group_3 = fidelity_data[fidelity_data['group_name']=="Group_3"].groupby("path_name")['fidelity'].agg(
                                                                                              fidelity='mean', sem='sem').reset_index()
    ### Draw Diagrams ###
    fig,ax = plt.subplots(1,2,figsize=(25,5))
    ax[0].set_title('Fidelity of Paths with Different Environmental-Parameter')
    ax[0].set_ylabel('fidelity')
    ax[0].set_xlabel('group name')
    ax[1].set_title('The Degree of Change in Fidelity Difference')
    ax[1].set_ylabel('fidelity difference')
    ax[1].set_xlabel('group name')
    
    ### bar chart ###
    data_bar = pandas.crosstab(fidelity_data.group_name,fidelity_data.path_name,fidelity_data.fidelity,aggfunc='mean')
    data_bar.plot(kind='bar', ax=ax[0])
    ax[0].tick_params(axis='x', labelrotation=0)
    print("fidelity data")
    print(data_bar)
    print(" ")
    print("group_1_sem,path_A,path_B,path_C")
    print(group_1['sem'])
    print(" ")
    print("group_2_sem,path_A,path_B,path_C")
    print(group_2['sem'])
    print(" ")
    print("group_3_sem,path_A,path_B,path_C")
    print(group_3['sem'])
    print(" ")

    ### line chart ###
    path_B_vs_path_A_fidelity_difference_group_1 = data_bar.iloc[0,1]-data_bar.iloc[0,0]
    path_B_vs_path_C_fidelity_difference_group_1 = data_bar.iloc[0,1]-data_bar.iloc[0,2]
    path_B_vs_path_A_fidelity_difference_group_2 = data_bar.iloc[1,1]-data_bar.iloc[1,0]
    path_B_vs_path_C_fidelity_difference_group_2 = data_bar.iloc[1,1]-data_bar.iloc[1,2]
    path_B_vs_path_A_fidelity_difference_group_3 = data_bar.iloc[2,1]-data_bar.iloc[2,0]
    path_B_vs_path_C_fidelity_difference_group_3 = data_bar.iloc[2,1]-data_bar.iloc[2,2]
    fidelity_difference_data_path_B_vs_path_A = pandas.DataFrame([['Group_1',path_B_vs_path_A_fidelity_difference_group_1],
                                                                  ['Group_2',path_B_vs_path_A_fidelity_difference_group_2],
                                                                  ['Group_3',path_B_vs_path_A_fidelity_difference_group_3]],
                                                                   columns=['group_name', 'fidelity_difference'])
    fidelity_difference_data_path_B_vs_path_A.plot(kind='line', grid=True, x='group_name', y='fidelity_difference',ax=ax[1],label="path_B vs path_A fidelity difference")
    print("fidelity_difference_data_path_B_vs_path_A")
    print(fidelity_difference_data_path_B_vs_path_A)
    print(" ")
    fidelity_difference_data_path_B_vs_path_C = pandas.DataFrame([['Group_1',path_B_vs_path_C_fidelity_difference_group_1],
                                                                  ['Group_2',path_B_vs_path_C_fidelity_difference_group_2],
                                                                  ['Group_3',path_B_vs_path_C_fidelity_difference_group_3]],
                                                                   columns=['group_name', 'fidelity_difference'])
    fidelity_difference_data_path_B_vs_path_C.plot(kind='line', grid=True, x='group_name', y='fidelity_difference',ax=ax[1],label="path_B vs path_C fidelity difference")
    print("fidelity_difference_data_path_B_vs_path_C")
    print(fidelity_difference_data_path_B_vs_path_C)

    plt.show()
