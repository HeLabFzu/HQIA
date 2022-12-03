import sys
sys.path.append("..")

import netsquid as ns
import pandas
import pydynaa
from topology.Centralized_Chain_Topo import Centralized_Chain_Network_setup
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
This program explores the reasons for fidelity decline caused by the hop increase in the centralized quantum internet.
The program takes about 3 minutes to complete.
"""
def define_network_and_protocol(depolar_rate,dephase_rate,qchannel_loss_init,qchannel_loss_noisy):
    network = Centralized_Chain_Network_setup(node_distance=100,depolar_rate=depolar_rate,dephase_rate=dephase_rate,
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
    Controller_J = network.subcomponents["Controller_J"]
    Controller_K = network.subcomponents["Controller_K"]
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
    User_A = network.subcomponents["User_A"]
    User_B = network.subcomponents["User_B"]
    User_C = network.subcomponents["User_C"]
    User_D = network.subcomponents["User_D"]

    path_2_hops = []
    path_2_hops.append(NodeStruct(node=User_A,entangle_distribution_role="user",
                          store_mem_pos_1=1))
    path_2_hops.append(NodeStruct(node=Controller_A,entangle_distribution_role="controller",
                          qsource_name="Controller_A_Repeater_A_User_A_QSource"))
    path_2_hops.append(NodeStruct(node=Repeater_A,entangle_distribution_role="repeater",
                          store_mem_pos_1=1,store_mem_pos_2=2))
    path_2_hops.append(NodeStruct(node=Controller_B,entangle_distribution_role="controller",
                          qsource_name="Controller_B_Repeater_A_Repeater_B_QSource"))
    path_2_hops.append(NodeStruct(node=Repeater_B,entangle_distribution_role="repeater",
                          store_mem_pos_1=1,store_mem_pos_2=2))
    path_2_hops.append(NodeStruct(node=Controller_C,entangle_distribution_role="controller",
                          qsource_name="Controller_C_Repeater_B_User_B_QSource"))
    path_2_hops.append(NodeStruct(node=User_B,entangle_distribution_role="user",
                          store_mem_pos_1=1))

    path_6_hops = []
    path_6_hops.append(NodeStruct(node=User_A,entangle_distribution_role="user",
                          store_mem_pos_1=1))
    path_6_hops.append(NodeStruct(node=Controller_A,entangle_distribution_role="controller",
                          qsource_name="Controller_A_Repeater_A_User_A_QSource"))
    path_6_hops.append(NodeStruct(node=Repeater_A,entangle_distribution_role="repeater",
                          store_mem_pos_1=1,store_mem_pos_2=2))
    path_6_hops.append(NodeStruct(node=Controller_B,entangle_distribution_role="controller",
                          qsource_name="Controller_B_Repeater_A_Repeater_B_QSource"))
    path_6_hops.append(NodeStruct(node=Repeater_B,entangle_distribution_role="repeater",
                          store_mem_pos_1=1,store_mem_pos_2=2))
    path_6_hops.append(NodeStruct(node=Controller_C,entangle_distribution_role="controller",
                          qsource_name="Controller_C_Repeater_B_Repeater_C_QSource"))
    path_6_hops.append(NodeStruct(node=Repeater_C,entangle_distribution_role="repeater",
                          store_mem_pos_1=1,store_mem_pos_2=2))
    path_6_hops.append(NodeStruct(node=Controller_D,entangle_distribution_role="controller",
                          qsource_name="Controller_D_Repeater_C_Repeater_D_QSource"))
    path_6_hops.append(NodeStruct(node=Repeater_D,entangle_distribution_role="repeater",
                          store_mem_pos_1=1,store_mem_pos_2=2))
    path_6_hops.append(NodeStruct(node=Controller_E,entangle_distribution_role="controller",
                          qsource_name="Controller_E_Repeater_D_Repeater_E_QSource"))
    path_6_hops.append(NodeStruct(node=Repeater_E,entangle_distribution_role="repeater",
                          store_mem_pos_1=1,store_mem_pos_2=2))
    path_6_hops.append(NodeStruct(node=Controller_F,entangle_distribution_role="controller",
                          qsource_name="Controller_F_Repeater_E_Repeater_F_QSource"))
    path_6_hops.append(NodeStruct(node=Repeater_F,entangle_distribution_role="repeater",
                          store_mem_pos_1=1,store_mem_pos_2=2))
    path_6_hops.append(NodeStruct(node=Controller_G,entangle_distribution_role="controller",
                          qsource_name="Controller_G_Repeater_F_User_C_QSource"))
    path_6_hops.append(NodeStruct(node=User_C,entangle_distribution_role="user",
                          store_mem_pos_1=1))

    path_10_hops = []
    path_10_hops.append(NodeStruct(node=User_A,entangle_distribution_role="user",
                          store_mem_pos_1=1))
    path_10_hops.append(NodeStruct(node=Controller_A,entangle_distribution_role="controller",
                          qsource_name="Controller_A_Repeater_A_User_A_QSource"))
    path_10_hops.append(NodeStruct(node=Repeater_A,entangle_distribution_role="repeater",
                          store_mem_pos_1=1,store_mem_pos_2=2))
    path_10_hops.append(NodeStruct(node=Controller_B,entangle_distribution_role="controller",
                          qsource_name="Controller_B_Repeater_A_Repeater_B_QSource"))
    path_10_hops.append(NodeStruct(node=Repeater_B,entangle_distribution_role="repeater",
                          store_mem_pos_1=1,store_mem_pos_2=2))
    path_10_hops.append(NodeStruct(node=Controller_C,entangle_distribution_role="controller",
                          qsource_name="Controller_C_Repeater_B_Repeater_C_QSource"))
    path_10_hops.append(NodeStruct(node=Repeater_C,entangle_distribution_role="repeater",
                          store_mem_pos_1=1,store_mem_pos_2=2))
    path_10_hops.append(NodeStruct(node=Controller_D,entangle_distribution_role="controller",
                          qsource_name="Controller_D_Repeater_C_Repeater_D_QSource"))
    path_10_hops.append(NodeStruct(node=Repeater_D,entangle_distribution_role="repeater",
                          store_mem_pos_1=1,store_mem_pos_2=2))
    path_10_hops.append(NodeStruct(node=Controller_E,entangle_distribution_role="controller",
                          qsource_name="Controller_E_Repeater_D_Repeater_E_QSource"))
    path_10_hops.append(NodeStruct(node=Repeater_E,entangle_distribution_role="repeater",
                          store_mem_pos_1=1,store_mem_pos_2=2))
    path_10_hops.append(NodeStruct(node=Controller_F,entangle_distribution_role="controller",
                          qsource_name="Controller_F_Repeater_E_Repeater_F_QSource"))
    path_10_hops.append(NodeStruct(node=Repeater_F,entangle_distribution_role="repeater",
                          store_mem_pos_1=1,store_mem_pos_2=2))
    path_10_hops.append(NodeStruct(node=Controller_G,entangle_distribution_role="controller",
                          qsource_name="Controller_G_Repeater_F_Repeater_G_QSource"))
    path_10_hops.append(NodeStruct(node=Repeater_G,entangle_distribution_role="repeater",
                          store_mem_pos_1=1,store_mem_pos_2=2))
    path_10_hops.append(NodeStruct(node=Controller_H,entangle_distribution_role="controller",
                          qsource_name="Controller_H_Repeater_G_Repeater_H_QSource"))
    path_10_hops.append(NodeStruct(node=Repeater_H,entangle_distribution_role="repeater",
                          store_mem_pos_1=1,store_mem_pos_2=2))
    path_10_hops.append(NodeStruct(node=Controller_I,entangle_distribution_role="controller",
                          qsource_name="Controller_I_Repeater_H_Repeater_I_QSource"))
    path_10_hops.append(NodeStruct(node=Repeater_I,entangle_distribution_role="repeater",
                          store_mem_pos_1=1,store_mem_pos_2=2))
    path_10_hops.append(NodeStruct(node=Controller_J,entangle_distribution_role="controller",
                          qsource_name="Controller_J_Repeater_I_Repeater_J_QSource"))
    path_10_hops.append(NodeStruct(node=Repeater_J,entangle_distribution_role="repeater",
                          store_mem_pos_1=1,store_mem_pos_2=2))
    path_10_hops.append(NodeStruct(node=Controller_K,entangle_distribution_role="controller",
                          qsource_name="Controller_K_Repeater_J_User_D_QSource"))
    path_10_hops.append(NodeStruct(node=User_D,entangle_distribution_role="user",
                          store_mem_pos_1=1))

    ### define entanglement_distribution_protocol ###
    entangle_distribution_2_hops_protocol = []
    entangle_distribution_2_hops_protocol_temp = []
    for node_number in range(len(path_2_hops)):
        if path_2_hops[node_number].entangle_distribution_role == "user":
            entangle_distribution_2_hops_protocol_temp.append(CentralizedEntanglementDistribution(node=path_2_hops[node_number].node,
                                                                               role="user",
                                                                               store_mem_pos=path_2_hops[node_number].store_mem_pos_1))
            if len(entangle_distribution_2_hops_protocol_temp) == 3:
                entangle_distribution_2_hops_protocol.append(entangle_distribution_2_hops_protocol_temp)
                entangle_distribution_2_hops_protocol_temp=[]
        if path_2_hops[node_number].entangle_distribution_role == "controller":
            entangle_distribution_2_hops_protocol_temp.append(CentralizedEntanglementDistribution(node=path_2_hops[node_number].node,
                                                                               role="controller",
                                                                               qsource_name=path_2_hops[node_number].qsource_name))
        if path_2_hops[node_number].entangle_distribution_role == "repeater":
            entangle_distribution_2_hops_protocol_temp.append(CentralizedEntanglementDistribution(node=path_2_hops[node_number].node,
                                                                               role="repeater",
                                                                               store_mem_pos=path_2_hops[node_number].store_mem_pos_1))
            if len(entangle_distribution_2_hops_protocol_temp) == 3:
                entangle_distribution_2_hops_protocol.append(entangle_distribution_2_hops_protocol_temp)
                entangle_distribution_2_hops_protocol_temp=[]
            entangle_distribution_2_hops_protocol_temp.append(CentralizedEntanglementDistribution(node=path_2_hops[node_number].node,
                                                                               role="repeater",
                                                                               store_mem_pos=path_2_hops[node_number].store_mem_pos_2))

    entangle_distribution_6_hops_protocol = []
    entangle_distribution_6_hops_protocol_temp = []
    for node_number in range(len(path_6_hops)):
        if path_6_hops[node_number].entangle_distribution_role == "user":
            entangle_distribution_6_hops_protocol_temp.append(CentralizedEntanglementDistribution(node=path_6_hops[node_number].node,
                                                                               role="user",
                                                                               store_mem_pos=path_6_hops[node_number].store_mem_pos_1))
            if len(entangle_distribution_6_hops_protocol_temp) == 3:
                entangle_distribution_6_hops_protocol.append(entangle_distribution_6_hops_protocol_temp)
                entangle_distribution_6_hops_protocol_temp=[]
        if path_6_hops[node_number].entangle_distribution_role == "controller":
            entangle_distribution_6_hops_protocol_temp.append(CentralizedEntanglementDistribution(node=path_6_hops[node_number].node,
                                                                               role="controller",
                                                                               qsource_name=path_6_hops[node_number].qsource_name))
        if path_6_hops[node_number].entangle_distribution_role == "repeater":
            entangle_distribution_6_hops_protocol_temp.append(CentralizedEntanglementDistribution(node=path_6_hops[node_number].node,
                                                                               role="repeater",
                                                                               store_mem_pos=path_6_hops[node_number].store_mem_pos_1))
            if len(entangle_distribution_6_hops_protocol_temp) == 3:
                entangle_distribution_6_hops_protocol.append(entangle_distribution_6_hops_protocol_temp)
                entangle_distribution_6_hops_protocol_temp=[]
            entangle_distribution_6_hops_protocol_temp.append(CentralizedEntanglementDistribution(node=path_6_hops[node_number].node,
                                                                               role="repeater",
                                                                               store_mem_pos=path_6_hops[node_number].store_mem_pos_2))

    entangle_distribution_10_hops_protocol = []
    entangle_distribution_10_hops_protocol_temp = []
    for node_number in range(len(path_10_hops)):
        if path_10_hops[node_number].entangle_distribution_role == "user":
            entangle_distribution_10_hops_protocol_temp.append(CentralizedEntanglementDistribution(node=path_10_hops[node_number].node,
                                                                               role="user",
                                                                               store_mem_pos=path_10_hops[node_number].store_mem_pos_1))
            if len(entangle_distribution_10_hops_protocol_temp) == 3:
                entangle_distribution_10_hops_protocol.append(entangle_distribution_10_hops_protocol_temp)
                entangle_distribution_10_hops_protocol_temp=[]
        if path_10_hops[node_number].entangle_distribution_role == "controller":
            entangle_distribution_10_hops_protocol_temp.append(CentralizedEntanglementDistribution(node=path_10_hops[node_number].node,
                                                                               role="controller",
                                                                               qsource_name=path_10_hops[node_number].qsource_name))
        if path_10_hops[node_number].entangle_distribution_role == "repeater":
            entangle_distribution_10_hops_protocol_temp.append(CentralizedEntanglementDistribution(node=path_10_hops[node_number].node,
                                                                               role="repeater",
                                                                               store_mem_pos=path_10_hops[node_number].store_mem_pos_1))
            if len(entangle_distribution_10_hops_protocol_temp) == 3:
                entangle_distribution_10_hops_protocol.append(entangle_distribution_10_hops_protocol_temp)
                entangle_distribution_10_hops_protocol_temp=[]
            entangle_distribution_10_hops_protocol_temp.append(CentralizedEntanglementDistribution(node=path_10_hops[node_number].node,
                                                                               role="repeater",
                                                                               store_mem_pos=path_10_hops[node_number].store_mem_pos_2))



    ### define swapping protocol ###
    swapping_2_hops_protocol= []
    swapping_2_hops_protocol_temp = []
    for node_number in range(len(path_2_hops)):
        if path_2_hops[node_number].entangle_distribution_role == "user" and node_number != 0:
            swapping_2_hops_protocol_temp.append(CentralizedSwapping(node=path_2_hops[node_number].node,
                                                  port=path_2_hops[node_number].node.get_conn_port(path_2_hops[node_number-1].node.ID),
                                                  role="corrector",corrector_mem_pos=path_2_hops[node_number].store_mem_pos_1))
            if len(swapping_2_hops_protocol_temp) == 3:
                swapping_2_hops_protocol.append(swapping_2_hops_protocol_temp)
                swapping_2_hops_protocol_temp = []
        if path_2_hops[node_number].entangle_distribution_role == "controller" and node_number != 1:
            swapping_2_hops_protocol_temp.append(CentralizedSwapping(node=path_2_hops[node_number].node,
                                                  port=path_2_hops[node_number].node.get_conn_port(path_2_hops[node_number-1].node.ID),
                                                  portout=path_2_hops[node_number].node.get_conn_port(path_2_hops[node_number+1].node.ID),
                                                  role="localcontroller"))
        if path_2_hops[node_number].entangle_distribution_role == "repeater":
            if node_number != 2:
                swapping_2_hops_protocol_temp.append(CentralizedSwapping(node=path_2_hops[node_number].node,
                                                  port=path_2_hops[node_number].node.get_conn_port(path_2_hops[node_number-1].node.ID),
                                                  role="corrector", corrector_mem_pos=path_2_hops[node_number].store_mem_pos_1))
                if len(swapping_2_hops_protocol_temp) == 3:
                    swapping_2_hops_protocol.append(swapping_2_hops_protocol_temp)
                    swapping_2_hops_protocol_temp = []
            swapping_2_hops_protocol_temp.append(CentralizedSwapping(node=path_2_hops[node_number].node,
                                                  port=path_2_hops[node_number].node.get_conn_port(path_2_hops[node_number+1].node.ID),
                                                  role="repeater", repeater_mem_posA=path_2_hops[node_number].store_mem_pos_1,
                                                  repeater_mem_posB=path_2_hops[node_number].store_mem_pos_2))

    swapping_6_hops_protocol= []
    swapping_6_hops_protocol_temp = []
    for node_number in range(len(path_6_hops)):
        if path_6_hops[node_number].entangle_distribution_role == "user" and node_number != 0:
            swapping_6_hops_protocol_temp.append(CentralizedSwapping(node=path_6_hops[node_number].node,
                                                  port=path_6_hops[node_number].node.get_conn_port(path_6_hops[node_number-1].node.ID),
                                                  role="corrector",corrector_mem_pos=path_6_hops[node_number].store_mem_pos_1))
            if len(swapping_6_hops_protocol_temp) == 3:
                swapping_6_hops_protocol.append(swapping_6_hops_protocol_temp)
                swapping_6_hops_protocol_temp = []
        if path_6_hops[node_number].entangle_distribution_role == "controller" and node_number != 1:
            swapping_6_hops_protocol_temp.append(CentralizedSwapping(node=path_6_hops[node_number].node,
                                                  port=path_6_hops[node_number].node.get_conn_port(path_6_hops[node_number-1].node.ID),
                                                  portout=path_6_hops[node_number].node.get_conn_port(path_6_hops[node_number+1].node.ID),
                                                  role="localcontroller"))
        if path_6_hops[node_number].entangle_distribution_role == "repeater":
            if node_number != 2:
                swapping_6_hops_protocol_temp.append(CentralizedSwapping(node=path_6_hops[node_number].node,
                                                  port=path_6_hops[node_number].node.get_conn_port(path_6_hops[node_number-1].node.ID),
                                                  role="corrector", corrector_mem_pos=path_6_hops[node_number].store_mem_pos_1))
                if len(swapping_6_hops_protocol_temp) == 3:
                    swapping_6_hops_protocol.append(swapping_6_hops_protocol_temp)
                    swapping_6_hops_protocol_temp = []
            swapping_6_hops_protocol_temp.append(CentralizedSwapping(node=path_6_hops[node_number].node,
                                                  port=path_6_hops[node_number].node.get_conn_port(path_6_hops[node_number+1].node.ID),
                                                  role="repeater", repeater_mem_posA=path_6_hops[node_number].store_mem_pos_1,
                                                  repeater_mem_posB=path_6_hops[node_number].store_mem_pos_2))

    swapping_10_hops_protocol= []
    swapping_10_hops_protocol_temp = []
    for node_number in range(len(path_10_hops)):
        if path_10_hops[node_number].entangle_distribution_role == "user" and node_number != 0:
            swapping_10_hops_protocol_temp.append(CentralizedSwapping(node=path_10_hops[node_number].node,
                                                  port=path_10_hops[node_number].node.get_conn_port(path_10_hops[node_number-1].node.ID),
                                                  role="corrector",corrector_mem_pos=path_10_hops[node_number].store_mem_pos_1))
            if len(swapping_10_hops_protocol_temp) == 3:
                swapping_10_hops_protocol.append(swapping_10_hops_protocol_temp)
                swapping_10_hops_protocol_temp = []
        if path_10_hops[node_number].entangle_distribution_role == "controller" and node_number != 1:
            swapping_10_hops_protocol_temp.append(CentralizedSwapping(node=path_10_hops[node_number].node,
                                                  port=path_10_hops[node_number].node.get_conn_port(path_10_hops[node_number-1].node.ID),
                                                  portout=path_10_hops[node_number].node.get_conn_port(path_10_hops[node_number+1].node.ID),
                                                  role="localcontroller"))
        if path_10_hops[node_number].entangle_distribution_role == "repeater":
            if node_number != 2:
                swapping_10_hops_protocol_temp.append(CentralizedSwapping(node=path_10_hops[node_number].node,
                                                  port=path_10_hops[node_number].node.get_conn_port(path_10_hops[node_number-1].node.ID),
                                                  role="corrector", corrector_mem_pos=path_10_hops[node_number].store_mem_pos_1))
                if len(swapping_10_hops_protocol_temp) == 3:
                    swapping_10_hops_protocol.append(swapping_10_hops_protocol_temp)
                    swapping_10_hops_protocol_temp = []
            swapping_10_hops_protocol_temp.append(CentralizedSwapping(node=path_10_hops[node_number].node,
                                                  port=path_10_hops[node_number].node.get_conn_port(path_10_hops[node_number+1].node.ID),
                                                  role="repeater", repeater_mem_posA=path_10_hops[node_number].store_mem_pos_1,
                                                  repeater_mem_posB=path_10_hops[node_number].store_mem_pos_2))

    ### define create target qubit protocol ###
    create_qubit_protocol = CreateQubit(User_A,mem_pos=0)

    ### define teleportation protocol ###
    teleportation_2_hops_protocol = CentralizedTeleportation(User_A, User_B, Controller_A, Controller_C, Central_Controller, 0, 1, 1)
    teleportation_6_hops_protocol = CentralizedTeleportation(User_A, User_C, Controller_A, Controller_G, Central_Controller, 0, 1, 1)
    teleportation_10_hops_protocol = CentralizedTeleportation(User_A, User_D, Controller_A, Controller_K, Central_Controller, 0, 1, 1)

    return path_2_hops,path_6_hops,path_10_hops,entangle_distribution_2_hops_protocol,entangle_distribution_6_hops_protocol,entangle_distribution_10_hops_protocol, \
           swapping_2_hops_protocol,swapping_6_hops_protocol,swapping_10_hops_protocol,create_qubit_protocol,\
           teleportation_2_hops_protocol, teleportation_6_hops_protocol, teleportation_10_hops_protocol

if __name__ == '__main__':
    fidelity_data = pandas.DataFrame()
    ### 2_hops test ###
    n = 4
    while n>0:
        qchannel_loss_init_rate = 0
        depolar_rate = 0
        qchannel_loss_noisy_rate = 0
        dephase_rate = 0
        if n == 1:
            qchannel_loss_init_rate = 0.1
        if n == 2:
            depolar_rate = 0.03
        if n == 3: 
            qchannel_loss_noisy_rate = 0.002
        if n == 4:
            dephase_rate = 0.04
        round = 300
        path_2_hops,path_6_hops,path_10_hops, entangle_distribution_2_hops_protocol,entangle_distribution_6_hops_protocol,entangle_distribution_10_hops_protocol, \
                  swapping_2_hops_protocol,swapping_6_hops_protocol,swapping_10_hops_protocol,create_qubit_protocol,\
                  teleportation_2_hops_protocol, teleportation_6_hops_protocol, teleportation_10_hops_protocol = \
                  define_network_and_protocol(depolar_rate,dephase_rate,qchannel_loss_init_rate,qchannel_loss_noisy_rate)
        while round>0:
            resource_lock(path_2_hops)
            print("#### Start Entanglement Distribution Process ####")
            Entanglement_Distribution_Signal = True
            for i in range(len(entangle_distribution_2_hops_protocol)):
                if Entanglement_Distribution_Signal:
                    for j in range(len(entangle_distribution_2_hops_protocol[i])):
                        entangle_distribution_2_hops_protocol[i][j].start()
                    ns.sim_run()
                    for j in range(len(entangle_distribution_2_hops_protocol[i])):
                        if not entangle_distribution_2_hops_protocol[i][j].check():
                            Entanglement_Distribution_Signal = False
                            for k in range(len(entangle_distribution_2_hops_protocol[i])):
                                entangle_distribution_2_hops_protocol[i][k].stop()
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
                resource_release(path_2_hops)
                df=dc_distribution.dataframe
                df['depolar_rate'] = depolar_rate
                df['qchannel_loss_init_rate'] = qchannel_loss_init_rate
                df['dephase_rate'] = dephase_rate
                df['qchannel_loss_noisy_rate'] = qchannel_loss_noisy_rate
                df['hops'] = 2
                fidelity_data = fidelity_data.append(df)
            else:
                print("#### Start Entanglement Swapping Process ####")
                for i in range(len(swapping_2_hops_protocol)):
                    for j in range(len(swapping_2_hops_protocol[i])):
                        swapping_2_hops_protocol[i][j].start()
                    ns.sim_run()
                print("#### Complete Entanglement Swapping Process ####")
                print("#### Start to Create Target Qubit ####")
                create_qubit_protocol.start()
                ns.sim_run()
                print("#### Complete to Create Target Qubit ####")
                print("#### Start to teleport target qubit")
                dc_fidelity = DataCollector(collect_fidelity_data)
                dc_fidelity.collect_on(pydynaa.EventExpression(source=teleportation_2_hops_protocol,
                                                      event_type=Signals.SUCCESS.value))
                teleportation_2_hops_protocol.start()
                ns.sim_run()
                print("#### Complete to teleport target qubit ####")
                resource_release(path_2_hops)
                df=dc_fidelity.dataframe
                df['depolar_rate'] = depolar_rate
                df['qchannel_loss_init_rate'] = qchannel_loss_init_rate
                df['dephase_rate'] = dephase_rate
                df['qchannel_loss_noisy_rate'] = qchannel_loss_noisy_rate
                df['hops'] = 2
                fidelity_data = fidelity_data.append(df)
            round -= 1
        n -=1
    ### 6_hops test ###
    n = 4
    while n>0:
        qchannel_loss_init_rate = 0
        depolar_rate = 0
        qchannel_loss_noisy_rate = 0
        dephase_rate = 0
        if n == 1:
            qchannel_loss_init_rate = 0.1
        if n == 2:
            depolar_rate = 0.03
        if n == 3:
            qchannel_loss_noisy_rate = 0.002
        if n == 4:
            dephase_rate = 0.04
        round = 300
        path_2_hops,path_6_hops,path_10_hops,entangle_distribution_2_hops_protocol,entangle_distribution_6_hops_protocol,entangle_distribution_10_hops_protocol, \
                  swapping_2_hops_protocol,swapping_6_hops_protocol,swapping_10_hops_protocol,create_qubit_protocol,\
                  teleportation_2_hops_protocol, teleportation_6_hops_protocol, teleportation_10_hops_protocol = \
                  define_network_and_protocol(depolar_rate,dephase_rate,qchannel_loss_init_rate,qchannel_loss_noisy_rate)
        while round>0:
            resource_lock(path_6_hops)
            print("#### Start Entanglement Distribution Process ####")
            Entanglement_Distribution_Signal = True
            for i in range(len(entangle_distribution_6_hops_protocol)):
                if Entanglement_Distribution_Signal:
                    for j in range(len(entangle_distribution_6_hops_protocol[i])):
                        entangle_distribution_6_hops_protocol[i][j].start()
                    ns.sim_run()
                    for j in range(len(entangle_distribution_6_hops_protocol[i])):
                        if not entangle_distribution_6_hops_protocol[i][j].check():
                            Entanglement_Distribution_Signal = False
                            for k in range(len(entangle_distribution_6_hops_protocol[i])):
                                entangle_distribution_6_hops_protocol[i][k].stop()
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
                resource_release(path_6_hops)
                df=dc_distribution.dataframe
                df['depolar_rate'] = depolar_rate
                df['qchannel_loss_init_rate'] = qchannel_loss_init_rate
                df['dephase_rate'] = dephase_rate
                df['qchannel_loss_noisy_rate'] = qchannel_loss_noisy_rate
                df['hops'] = 6
                fidelity_data = fidelity_data.append(df)
            else:
                print("#### Start Entanglement Swapping Process ####")
                for i in range(len(swapping_6_hops_protocol)):
                    for j in range(len(swapping_6_hops_protocol[i])):
                        swapping_6_hops_protocol[i][j].start()
                    ns.sim_run()
                print("#### Complete Entanglement Swapping Process ####")
                print("#### Start to Create Target Qubit ####")
                create_qubit_protocol.start()
                ns.sim_run()
                print("#### Complete to Create Target Qubit ####")
                print("#### Start to teleport target qubit")
                dc_fidelity = DataCollector(collect_fidelity_data)
                dc_fidelity.collect_on(pydynaa.EventExpression(source=teleportation_6_hops_protocol,
                                                      event_type=Signals.SUCCESS.value))
                teleportation_6_hops_protocol.start()
                ns.sim_run()
                print("#### Complete to teleport target qubit ####")
                resource_release(path_6_hops)
                df=dc_fidelity.dataframe
                df['depolar_rate'] = depolar_rate
                df['qchannel_loss_init_rate'] = qchannel_loss_init_rate
                df['dephase_rate'] = dephase_rate
                df['qchannel_loss_noisy_rate'] = qchannel_loss_noisy_rate
                df['hops'] = 6
                fidelity_data = fidelity_data.append(df)
            round -= 1
        n -= 1
    ### 10_hops test ###
    n = 4
    while n>0:
        qchannel_loss_init_rate = 0
        depolar_rate = 0
        qchannel_loss_noisy_rate = 0
        dephase_rate = 0
        if n == 1:
            qchannel_loss_init_rate = 0.1
        if n == 2:
            depolar_rate = 0.03
        if n == 3:
            qchannel_loss_noisy_rate = 0.002
        if n == 4:
            dephase_rate = 0.04
        round = 300
        path_2_hops,path_6_hops,path_10_hops,entangle_distribution_2_hops_protocol,entangle_distribution_6_hops_protocol,entangle_distribution_10_hops_protocol, \
                  swapping_2_hops_protocol,swapping_6_hops_protocol,swapping_10_hops_protocol,create_qubit_protocol,\
                  teleportation_2_hops_protocol, teleportation_6_hops_protocol, teleportation_10_hops_protocol = \
                  define_network_and_protocol(depolar_rate,dephase_rate,qchannel_loss_init_rate,qchannel_loss_noisy_rate)
        while round>0:
            print("#### Start Entanglement Distribution Process ####")
            resource_lock(path_10_hops)
            Entanglement_Distribution_Signal = True
            for i in range(len(entangle_distribution_10_hops_protocol)):
                if Entanglement_Distribution_Signal:
                    for j in range(len(entangle_distribution_10_hops_protocol[i])):
                        entangle_distribution_10_hops_protocol[i][j].start()
                    ns.sim_run()
                    for j in range(len(entangle_distribution_10_hops_protocol[i])):
                        if not entangle_distribution_10_hops_protocol[i][j].check():
                            Entanglement_Distribution_Signal = False
                            for k in range(len(entangle_distribution_10_hops_protocol[i])):
                                entangle_distribution_10_hops_protocol[i][k].stop()
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
                resource_release(path_10_hops)
                df=dc_distribution.dataframe
                df['depolar_rate'] = depolar_rate
                df['qchannel_loss_init_rate'] = qchannel_loss_init_rate
                df['dephase_rate'] = dephase_rate
                df['qchannel_loss_noisy_rate'] = qchannel_loss_noisy_rate
                df['hops'] = 10
                fidelity_data = fidelity_data.append(df)
            else:
                print("#### Start Entanglement Swapping Process ####")
                for i in range(len(swapping_10_hops_protocol)):
                    for j in range(len(swapping_10_hops_protocol[i])):
                        swapping_10_hops_protocol[i][j].start()
                    ns.sim_run()
                print("#### Complete Entanglement Swapping Process ####")
                print("#### Start to Create Target Qubit ####")
                create_qubit_protocol.start()
                ns.sim_run()
                print("#### Complete to Create Target Qubit ####")
                print("#### Start to teleport target qubit")
                dc_fidelity = DataCollector(collect_fidelity_data)
                dc_fidelity.collect_on(pydynaa.EventExpression(source=teleportation_10_hops_protocol,
                                                      event_type=Signals.SUCCESS.value))
                teleportation_10_hops_protocol.start()
                ns.sim_run()
                print("#### Complete to teleport target qubit ####")
                resource_release(path_10_hops)
                df=dc_fidelity.dataframe
                df['depolar_rate'] = depolar_rate
                df['qchannel_loss_init_rate'] = qchannel_loss_init_rate
                df['dephase_rate'] = dephase_rate
                df['qchannel_loss_noisy_rate'] = qchannel_loss_noisy_rate
                df['hops'] = 10
                fidelity_data = fidelity_data.append(df)
            round -= 1
        n -= 1
    plot_style = {'kind': 'line', 'grid': True,
      'title': "Route-Hops Effect on Fidelity with Enviromental-Parameter"}
    fig,ax = plt.subplots()

    ax.set_ylabel('fidelity') 

    data = fidelity_data[fidelity_data['qchannel_loss_init_rate']==0.1].groupby("hops")['fidelity'].agg(
                                                                                              fidelity='mean', sem='sem').reset_index()
    label = "qchannel_loss_init_rate"
    data.plot(x='hops', y='fidelity', yerr='sem',ax=ax,label=label, **plot_style)
    print("qchannel_loss_init_rate(fidelity)")
    print(data)


    data = fidelity_data[fidelity_data['depolar_rate']==0.03].groupby("hops")['fidelity'].agg(
                                                                                              fidelity='mean', sem='sem').reset_index()
    label = "depolar_rate"
    data.plot(x='hops', y='fidelity', yerr='sem',ax=ax,label=label, **plot_style)
    print("depolar_rate(fidelity)")
    print(data)


    data = fidelity_data[fidelity_data['qchannel_loss_noisy_rate']==0.002].groupby("hops")['fidelity'].agg(
                                                                                              fidelity='mean', sem='sem').reset_index()
    label = "qchannel_loss_noisy_rate"
    data.plot(x='hops', y='fidelity', yerr='sem',ax=ax,label=label, **plot_style)
    print("qchannel_loss_noisy_rate(fidelity)")
    print(data)


    data = fidelity_data[fidelity_data['dephase_rate']==0.04].groupby("hops")['fidelity'].agg(
                                                                                              fidelity='mean', sem='sem').reset_index()
    label = "dephase_rate"
    data.plot(x='hops', y='fidelity', yerr='sem',ax=ax,label=label, **plot_style)
    print("dephase_rate(fidelity)")
    print(data)
    
    plt.show()
