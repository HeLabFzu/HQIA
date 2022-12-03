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
This program explores the impact of environmental interference.

The program takes about 5 minutes to complete.
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
    User_C = network.subcomponents["User_C"]
    
    path = []
    path.append(NodeStruct(node=User_A,entangle_distribution_role="user",
                          store_mem_pos_1=1))
    path.append(NodeStruct(node=Controller_A,entangle_distribution_role="controller",
                          qsource_name="Controller_A_Repeater_A_User_A_QSource"))
    path.append(NodeStruct(node=Repeater_A,entangle_distribution_role="repeater",
                          store_mem_pos_1=1,store_mem_pos_2=2))
    path.append(NodeStruct(node=Controller_B,entangle_distribution_role="controller",
                          qsource_name="Controller_B_Repeater_A_Repeater_B_QSource"))
    path.append(NodeStruct(node=Repeater_B,entangle_distribution_role="repeater",
                          store_mem_pos_1=1,store_mem_pos_2=2))
    path.append(NodeStruct(node=Controller_C,entangle_distribution_role="controller",
                          qsource_name="Controller_C_Repeater_B_Repeater_C_QSource"))
    path.append(NodeStruct(node=Repeater_C,entangle_distribution_role="repeater",
                          store_mem_pos_1=1,store_mem_pos_2=2))
    path.append(NodeStruct(node=Controller_D,entangle_distribution_role="controller",
                          qsource_name="Controller_D_Repeater_C_Repeater_D_QSource"))
    path.append(NodeStruct(node=Repeater_D,entangle_distribution_role="repeater",
                          store_mem_pos_1=1,store_mem_pos_2=2))
    path.append(NodeStruct(node=Controller_E,entangle_distribution_role="controller",
                          qsource_name="Controller_E_Repeater_D_Repeater_E_QSource"))
    path.append(NodeStruct(node=Repeater_E,entangle_distribution_role="repeater",
                          store_mem_pos_1=1,store_mem_pos_2=2))
    path.append(NodeStruct(node=Controller_F,entangle_distribution_role="controller",
                          qsource_name="Controller_F_Repeater_E_Repeater_F_QSource"))
    path.append(NodeStruct(node=Repeater_F,entangle_distribution_role="repeater",
                          store_mem_pos_1=1,store_mem_pos_2=2))
    path.append(NodeStruct(node=Controller_G,entangle_distribution_role="controller",
                          qsource_name="Controller_G_Repeater_F_User_C_QSource"))
    path.append(NodeStruct(node=User_C,entangle_distribution_role="user",
                          store_mem_pos_1=1))
    ### lock resource after path defined ###
    resource_lock(path)

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

    ### define create target qubit protocol ###
    create_qubit_protocol = CreateQubit(User_A,mem_pos=0)

    ### define teleportation protocol ###
    teleportation_protocol = CentralizedTeleportation(User_A, User_C, Controller_A, Controller_G, Central_Controller, 0, 1, 1)

    return path,entangle_distribution_protocol,swapping_protocol,create_qubit_protocol,teleportation_protocol

def run_protocol(depolar_rate,dephase_rate,qchannel_loss_init_rate,qchannel_loss_noisy_rate):
    fidelity_data_temp = pandas.DataFrame()
    round = 300
    path, entangle_distribution_protocol,swapping_protocol,create_qubit_protocol,teleportation_protocol = define_network_and_protocol(depolar_rate,dephase_rate,qchannel_loss_init_rate,qchannel_loss_noisy_rate)
    while round>0:
        print("#### Start Entanglement Distribution Process ####")
        Entanglement_Distribution_Signal = True
        for i in range(len(entangle_distribution_protocol)):
            if Entanglement_Distribution_Signal:
                for j in range(len(entangle_distribution_protocol[i])):
                    entangle_distribution_protocol[i][j].start()
                ns.sim_run()
                for j in range(len(entangle_distribution_protocol[i])):
                    if not entangle_distribution_protocol[i][j].check():
                        for k in range(len(entangle_distribution_protocol[i])):
                            entangle_distribution_protocol[i][k].stop()
                        Entanglement_Distribution_Signal = False
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

            ### release resource after transportation failed ###
            resource_release(path)

            df=dc_distribution.dataframe
            df['depolar_rate'] = depolar_rate
            df['dephase_rate'] = dephase_rate
            df['qchannel_loss_init_rate'] = qchannel_loss_init_rate
            df['qchannel_loss_noisy_rate'] = qchannel_loss_noisy_rate
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

            ### release resource after teleport complete ###
            resource_release(path)

            df=dc_fidelity.dataframe
            df['depolar_rate'] = depolar_rate
            df['dephase_rate'] = dephase_rate
            df['qchannel_loss_init_rate'] = qchannel_loss_init_rate
            df['qchannel_loss_noisy_rate'] = qchannel_loss_noisy_rate
            fidelity_data_temp = fidelity_data_temp.append(df)
        round -= 1
    return fidelity_data_temp

if __name__ == '__main__':
    fidelity_data_depolar_rate = pandas.DataFrame()
    fidelity_data_dephase_rate = pandas.DataFrame()
    fidelity_data_qchannel_loss_init_rate = pandas.DataFrame()
    fidelity_data_qchannel_loss_noisy_rate = pandas.DataFrame()

    qchannel_loss_init_rates = [0,0.05,0.1,0.15,0.2]
    depolar_rates = [0,0.005,0.01,0.015,0.02]
    qchannel_loss_noisy_rates = [0,0.005,0.01,0.015,0.02]
    dephase_rates = [0,0.05,0.1,0.15,0.2]
    for depolar_rate in depolar_rates:
        fidelity_data_temp = run_protocol(depolar_rate,0,0,0)
        fidelity_data_depolar_rate = fidelity_data_depolar_rate.append(fidelity_data_temp)
    for dephase_rate in dephase_rates:
        fidelity_data_temp = run_protocol(0,dephase_rate,0,0)
        fidelity_data_dephase_rate = fidelity_data_dephase_rate.append(fidelity_data_temp)
    for qchannel_loss_init_rate in qchannel_loss_init_rates:
        fidelity_data_temp = run_protocol(0,0,qchannel_loss_init_rate,0)
        fidelity_data_qchannel_loss_init_rate = fidelity_data_qchannel_loss_init_rate.append(fidelity_data_temp)
    for qchannel_loss_noisy_rate in qchannel_loss_noisy_rates:
        fidelity_data_temp = run_protocol(0,0,0,qchannel_loss_noisy_rate)
        fidelity_data_qchannel_loss_noisy_rate = fidelity_data_qchannel_loss_noisy_rate.append(fidelity_data_temp)
    fig,ax = plt.subplots(2,2,figsize=(25,10))
    ax[0][0].set_ylabel('fidelity')
    ax[0][1].set_ylabel('fidelity')
    ax[1][0].set_ylabel('fidelity')
    ax[1][1].set_ylabel('fidelity')
    plot_style = {'kind': 'line', 'grid': True}
    depolar_data = fidelity_data_depolar_rate.groupby("depolar_rate")['fidelity'].agg(
                                                              fidelity='mean', sem='sem').reset_index()
    dephase_data = fidelity_data_dephase_rate.groupby("dephase_rate")['fidelity'].agg(
                                                              fidelity='mean', sem='sem').reset_index()
    qchannel_loss_init_data = fidelity_data_qchannel_loss_init_rate.groupby("qchannel_loss_init_rate")['fidelity'].agg(
                                                              fidelity='mean', sem='sem').reset_index()
    qchannel_loss_noisy_data = fidelity_data_qchannel_loss_noisy_rate.groupby("qchannel_loss_noisy_rate")['fidelity'].agg(
                                                              fidelity='mean', sem='sem').reset_index()
    depolar_data.plot(x='depolar_rate', y='fidelity', yerr='sem',ax=ax[0][0], title='Depolar Rate Effect on Fidelity', **plot_style)
    dephase_data.plot(x='dephase_rate', y='fidelity', yerr='sem', ax=ax[0][1], title='Dephase Rate Effect on Fidelity', **plot_style)
    qchannel_loss_init_data.plot(x='qchannel_loss_init_rate', y='fidelity', yerr='sem', ax=ax[1][0], title='Qchannel Loss Init Rate Effect on Fidelity', **plot_style)
    qchannel_loss_noisy_data.plot(x='qchannel_loss_noisy_rate', y='fidelity', yerr='sem', ax=ax[1][1], title='Qchannel Loss Noisy Rate Effect on Fidelity', **plot_style)
    
    print("depolar_rate fidelity")
    print(depolar_data)
    print("dephase_rate fidelity")
    print(dephase_data)
    print("qchannel_loss_init_rate fidelity")
    print(qchannel_loss_init_data)
    print("qchannel_loss_noisy_rate fidelity")
    print(qchannel_loss_noisy_data)
    plt.show()
