import sys
import gc
sys.path.append("..")

import netsquid as ns
import pandas
import pydynaa
import time
import numpy as np

from topology.Centralized_Cellular_Topo import Centralized_Cellular_Network_setup
from protocol.centralized.CentralizedEntanglementDistribution import CentralizedEntanglementDistribution
from protocol.centralized.CentralizedSwapping import CentralizedSwapping
from protocol.centralized.CentralizedTeleportation import CentralizedTeleportation
from protocol.centralized.CentralizedRouting import CentralizedRouting
from protocol.centralized.CentralizedResourceCheckReserve import CentralizedResourceCheckReserve
from protocol.distributed.pseudo_distributed_topo_GreedyRouting import Greedy
from protocol.distributed.pseudo_distributed_topo_SLMPRouting import SLMP
from protocol.distributed.pseudo_distributed_topo_QCastRouting import QCast
from util.CheckDistribution import CheckDistribution
from util.QubitCreation import CreateQubit
from util.ResourceLockRelease import resource_lock,resource_release
from util.CollectData import collect_distribution_data,collect_fidelity_data
from util.CentralController import CentralControllerInfoTable,DomainShortestPathTable,DomainEdgeRepeaterTable
from util.ClearCentralControllerTable import ClearCentralControllerTable
from netsquid.util.datacollector import DataCollector
from netsquid.protocols.protocol import Signals
from matplotlib import pyplot as plt

"""
Generally speaking, the distributed routing algorithm can only run in distributed topology. However, in order to eliminate the interference of inconsistent topology between centralized_routing and distributed_routing and obtain more accurate experimental results, this experiment runs distributed_routing_algorithm(Q-cast, Greedy, SLMP) in a pseudo_distributed_topo(which is a centralized topo, but we code to hide the controller and the distributed_routing_algorithm will think the topo as a distributed topo).

"""

def define_centralized_cellular_network(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy,num_mem_positions):
    network = Centralized_Cellular_Network_setup(depolar_rates=depolar_rates,dephase_rates=dephase_rates,
                                 qchannel_loss_init=qchannel_loss_init, qchannel_loss_noisy=qchannel_loss_noisy,num_mem_positions=num_mem_positions)
    central_controller = CentralControllerInfoTable(network,dephase_rates,qchannel_loss_init,qchannel_loss_noisy)
    return network,central_controller

def centralized_routing(src_host,dst_host,src_user_mem,dst_user_mem,network,central_controller):
    sort_paths = CentralizedRouting(src_host,dst_host,central_controller,rc_number=2)
    while 1:
        FinalResult = CentralizedResourceCheckReserve(sort_paths.pop(0)[0],src_user_mem=1,dst_user_mem=1,central_controller=central_controller)
        if FinalResult != "null":
            break
        elif len(sort_paths) == 0:
            break
    if FinalResult != "null":
        print("#### Centralized path####")
        for node in FinalResult:
            print(node.node)
        return FinalResult
    else :
        print("Announce No Path Found For The Request !")
        return "null"

def greedy_routing(src_host,dst_host,network):
    path = Greedy(network,src_host,dst_host)
    print("####Greedy path######")
    for node in path:
        print(node.node)
    return path

def SLMP_routing(src_host,dst_host,network):
    path = SLMP(network,src_host,dst_host)
    print("####SLMP path######")
    if path != "null":
        for node in path:
            print(node.node)
    return path

def QCast_routing(src_host,dst_host,network):
    paths = QCast(network,src_host,dst_host)
    print("####QCast path######")
    for path in paths:
        print("####")
        for node in path:
            print(node.node)
    return paths
    
def define_protocol(path, network):
    Central_Controller = network.subcomponents["Central_Controller"]
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
   
    return entangle_distribution_protocol,swapping_protocol,create_qubit_protocol,teleportation_protocol

def run_centralized_routing_test(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy,round):
    fidelity_data_temp = pandas.DataFrame()
    avg_depolar_rate = np.mean(depolar_rates)
    avg_dephase_rate = np.mean(dephase_rates)
    avg_loss_init = np.mean(qchannel_loss_init)
    avg_loss_noisy = np.mean(qchannel_loss_noisy)
    std_depolar_rate = np.std(depolar_rates)
    std_dephase_rate = np.std(dephase_rates)
    std_loss_init = np.std(qchannel_loss_init)
    std_loss_noisy = np.std(qchannel_loss_noisy)
    time_cost = 0
    time_cost_of_path_selection = 0
    success_communication_num = 0
    network,central_controller = define_centralized_cellular_network(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy,num_mem_positions=3)
    src_host = network.subcomponents["User_A"]
    dst_host = network.subcomponents["User_B"]
    ### user_mems are invoved in end-end-request-protocol messages, can be known in the begining ###
    src_user_mem = 1
    dst_user_mem = 1
    time_start_of_path_selection = time.time()
    path = centralized_routing(src_host,dst_host,src_user_mem,dst_user_mem,network,central_controller)
    time_end_of_path_selection = time.time()
    time_cost_of_path_selection = time_end_of_path_selection - time_start_of_path_selection
    entangle_distribution_protocol,swapping_protocol,create_qubit_protocol,teleportation_protocol = define_protocol(path,network)
    while round > 0:
        resource_lock(path)
        time_start=time.time()
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
                        entangle_distribution_protocol[i][0].stop()
                        entangle_distribution_protocol[i][1].stop()
                        entangle_distribution_protocol[i][2].stop()
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
            df['routing_algorithm'] = "Centralized_Routing"
            df['entanglement_pair_consumption'] = (len(path)-1)/2
            df['avg_depolar_rate'] = format(avg_depolar_rate,'.3f')
            df['avg_dephase_rate'] = format(avg_dephase_rate,'.3f')
            df['avg_qchannel_loss_init'] = format(avg_loss_init,'.3f')
            df['avg_qchannel_loss_noisy'] = format(avg_loss_noisy,'.3f')
            df['standard_deviation_of_depolar_rate'] = format(std_depolar_rate,'.3f')
            df['standard_deviation_of_dephase_rate'] = format(std_dephase_rate,'.3f')
            df['standard_deviation_of_qchannel_loss_init'] = format(std_loss_init,'.3f')
            df['standard_deviation_of_qchannel_loss_noisy'] = format(std_loss_noisy,'.4f')
            fidelity_data_temp = fidelity_data_temp.append(df)
            time_end=time.time()
            time_cost = time_cost + (time_end - time_start)
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
            ClearCentralControllerTable(path,central_controller)
            df=dc_fidelity.dataframe
            df['routing_algorithm'] = "Centralized_Routing"
            df['entanglement_pair_consumption'] = (len(path)-1)/2
            df['avg_depolar_rate'] = format(avg_depolar_rate,'.3f')
            df['avg_dephase_rate'] = format(avg_dephase_rate,'.3f')
            df['avg_qchannel_loss_init'] = format(avg_loss_init,'.3f')
            df['avg_qchannel_loss_noisy'] = format(avg_loss_noisy,'.3f')
            df['standard_deviation_of_depolar_rate'] = format(std_depolar_rate,'.3f')
            df['standard_deviation_of_dephase_rate'] = format(std_dephase_rate,'.3f')
            df['standard_deviation_of_qchannel_loss_init'] = format(std_loss_init,'.3f')
            df['standard_deviation_of_qchannel_loss_noisy'] = format(std_loss_noisy,'.4f')
            fidelity_data_temp = fidelity_data_temp.append(df)
            if df['fidelity'][0] == 1:
                success_communication_num = success_communication_num + 1
            time_end=time.time()
            time_cost = time_cost + (time_end - time_start)
        round -= 1
    throughput = success_communication_num / time_cost
    return fidelity_data_temp, throughput, time_cost_of_path_selection

def run_greedy_routing_test(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy,round):
    fidelity_data_temp = pandas.DataFrame()
    avg_depolar_rate = np.mean(depolar_rates)
    avg_dephase_rate = np.mean(dephase_rates)
    avg_loss_init = np.mean(qchannel_loss_init)
    avg_loss_noisy = np.mean(qchannel_loss_noisy)
    std_depolar_rate = np.std(depolar_rates)
    std_dephase_rate = np.std(dephase_rates)
    std_loss_init = np.std(qchannel_loss_init)
    std_loss_noisy = np.std(qchannel_loss_noisy)
    time_cost = 0
    time_cost_of_path_selection = 0
    success_communication_num = 0
    network,_ = define_centralized_cellular_network(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy,num_mem_positions=3)
    src_host = network.subcomponents["User_A"]
    dst_host = network.subcomponents["User_B"]
    time_start_of_path_selection = time.time()
    path = greedy_routing(src_host,dst_host,network)
    time_end_of_path_selection = time.time()
    time_cost_of_path_selection = time_end_of_path_selection - time_start_of_path_selection
    entangle_distribution_protocol,swapping_protocol,create_qubit_protocol,teleportation_protocol = define_protocol(path,network)
    while round > 0:
        time_start=time.time()
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
                        entangle_distribution_protocol[i][0].stop()
                        entangle_distribution_protocol[i][1].stop()
                        entangle_distribution_protocol[i][2].stop()
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
            df=dc_distribution.dataframe
            df['routing_algorithm'] = "Greedy"
            df['entanglement_pair_consumption'] = (len(path)-1)/2
            df['avg_depolar_rate'] = format(avg_depolar_rate,'.3f')
            df['avg_dephase_rate'] = format(avg_dephase_rate,'.3f')
            df['avg_qchannel_loss_init'] = format(avg_loss_init,'.3f')
            df['avg_qchannel_loss_noisy'] = format(avg_loss_noisy,'.3f')
            df['standard_deviation_of_depolar_rate'] = format(std_depolar_rate,'.3f')
            df['standard_deviation_of_dephase_rate'] = format(std_dephase_rate,'.3f')
            df['standard_deviation_of_qchannel_loss_init'] = format(std_loss_init,'.3f')
            df['standard_deviation_of_qchannel_loss_noisy'] = format(std_loss_noisy,'.4f')
            fidelity_data_temp = fidelity_data_temp.append(df)
            time_end=time.time()
            time_cost = time_cost + (time_end - time_start)
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
            df=dc_fidelity.dataframe
            df['routing_algorithm'] = "Greedy"
            df['entanglement_pair_consumption'] = (len(path)-1)/2
            df['avg_depolar_rate'] = format(avg_depolar_rate,'.3f')
            df['avg_dephase_rate'] = format(avg_dephase_rate,'.3f')
            df['avg_qchannel_loss_init'] = format(avg_loss_init,'.3f')
            df['avg_qchannel_loss_noisy'] = format(avg_loss_noisy,'.3f')
            df['standard_deviation_of_depolar_rate'] = format(std_depolar_rate,'.3f')
            df['standard_deviation_of_dephase_rate'] = format(std_dephase_rate,'.3f')
            df['standard_deviation_of_qchannel_loss_init'] = format(std_loss_init,'.3f')
            df['standard_deviation_of_qchannel_loss_noisy'] = format(std_loss_noisy,'.4f')
            fidelity_data_temp = fidelity_data_temp.append(df)
            if df['fidelity'][0] == 1:
                success_communication_num = success_communication_num + 1
            time_end=time.time()
            time_cost = time_cost + (time_end - time_start)
        round -= 1
    throughput = success_communication_num / time_cost
    return fidelity_data_temp,throughput, time_cost_of_path_selection

def run_SLMP_routing_test(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy,round):
    fidelity_data_temp = pandas.DataFrame()
    count_for_path_selection = round
    avg_depolar_rate = np.mean(depolar_rates)
    avg_dephase_rate = np.mean(dephase_rates)
    avg_loss_init = np.mean(qchannel_loss_init)
    avg_loss_noisy = np.mean(qchannel_loss_noisy)
    std_depolar_rate = np.std(depolar_rates)
    std_dephase_rate = np.std(dephase_rates)
    std_loss_init = np.std(qchannel_loss_init)
    std_loss_noisy = np.std(qchannel_loss_noisy)
    time_cost = 0
    time_cost_of_path_selection = 0
    success_communication_num = 0
    network,_ = define_centralized_cellular_network(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy,num_mem_positions=8)
    src_host = network.subcomponents["User_A"]
    dst_host = network.subcomponents["User_B"]
    while round > 0:
        time_start=time.time()
        time_start_of_path_selection = time.time()
        path = SLMP_routing(src_host,dst_host,network)
        time_end_of_path_selection = time.time()
        time_cost_of_path_selection = time_cost_of_path_selection + (time_end_of_path_selection - time_start_of_path_selection)
        if path != "null":
            _,swapping_protocol,create_qubit_protocol,teleportation_protocol = define_protocol(path,network)
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
            df=dc_fidelity.dataframe
            df['routing_algorithm'] = "SLMP"
            df['entanglement_pair_consumption'] = 33
            df['avg_depolar_rate'] = format(avg_depolar_rate,'.3f')
            df['avg_dephase_rate'] = format(avg_dephase_rate,'.3f')
            df['avg_qchannel_loss_init'] = format(avg_loss_init,'.3f')
            df['avg_qchannel_loss_noisy'] = format(avg_loss_noisy,'.3f')
            df['standard_deviation_of_depolar_rate'] = format(std_depolar_rate,'.3f')
            df['standard_deviation_of_dephase_rate'] = format(std_dephase_rate,'.3f')
            df['standard_deviation_of_qchannel_loss_init'] = format(std_loss_init,'.3f')
            df['standard_deviation_of_qchannel_loss_noisy'] = format(std_loss_noisy,'.4f')
            fidelity_data_temp = fidelity_data_temp.append(df)
            if df['fidelity'][0] == 1:
                success_communication_num = success_communication_num + 1
            time_end=time.time()
            time_cost = time_cost + (time_end - time_start)
        else:
            print("no path found")
            Entanglement_Distribution_Signal = False
            check_distribution=CheckDistribution(Entanglement_Distribution_Signal)
            dc_distribution = DataCollector(collect_distribution_data)
            dc_distribution.collect_on(pydynaa.EventExpression(source=check_distribution,
                                              event_type=Signals.SUCCESS.value))
            check_distribution.start()
            ns.sim_run()
            if check_distribution.getresult() == 0:
                df=dc_distribution.dataframe
                df['routing_algorithm'] = "SLMP"
                df['entanglement_pair_consumption'] = 33
                df['avg_depolar_rate'] = format(avg_depolar_rate,'.3f')
                df['avg_dephase_rate'] = format(avg_dephase_rate,'.3f')
                df['avg_qchannel_loss_init'] = format(avg_loss_init,'.3f')
                df['avg_qchannel_loss_noisy'] = format(avg_loss_noisy,'.3f')
                df['standard_deviation_of_depolar_rate'] = format(std_depolar_rate,'.3f')
                df['standard_deviation_of_dephase_rate'] = format(std_dephase_rate,'.3f')
                df['standard_deviation_of_qchannel_loss_init'] = format(std_loss_init,'.3f')
                df['standard_deviation_of_qchannel_loss_noisy'] = format(std_loss_noisy,'.4f')
                fidelity_data_temp = fidelity_data_temp.append(df)
                time_end=time.time()
                time_cost = time_cost + (time_end - time_start)
        round -= 1
    throughput = success_communication_num / time_cost
    time_cost_of_path_selection = time_cost_of_path_selection / count_for_path_selection
    return fidelity_data_temp,throughput, time_cost_of_path_selection

def run_QCast_routing_test(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy,round):
    fidelity_data_temp = pandas.DataFrame()
    avg_depolar_rate = np.mean(depolar_rates)
    avg_dephase_rate = np.mean(dephase_rates)
    avg_loss_init = np.mean(qchannel_loss_init)
    avg_loss_noisy = np.mean(qchannel_loss_noisy)
    std_depolar_rate = np.std(depolar_rates)
    std_dephase_rate = np.std(dephase_rates)
    std_loss_init = np.std(qchannel_loss_init)
    std_loss_noisy = np.std(qchannel_loss_noisy)
    time_cost = 0
    time_cost_of_path_selection = 0
    success_communication_num = 0
    network,_ = define_centralized_cellular_network(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy,num_mem_positions=3)
    src_host = network.subcomponents["User_A"]
    dst_host = network.subcomponents["User_B"]
    time_start_of_path_selection = time.time()
    paths = QCast_routing(src_host,dst_host,network)
    time_end_of_path_selection = time.time()
    time_cost_of_path_selection = time_end_of_path_selection - time_start_of_path_selection
    while round > 0:
        for index in range(len(paths)):
            entangle_distribution_protocol,swapping_protocol,create_qubit_protocol,teleportation_protocol = define_protocol(paths[index],network)
            time_start=time.time()
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
                            entangle_distribution_protocol[i][0].stop()
                            entangle_distribution_protocol[i][1].stop()
                            entangle_distribution_protocol[i][2].stop()
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
                df=dc_distribution.dataframe
                df['routing_algorithm'] = "Q-Cast"
                df['entanglement_pair_consumption'] = (len(paths[index])-1)/2
                df['avg_depolar_rate'] = format(avg_depolar_rate,'.3f')
                df['avg_dephase_rate'] = format(avg_dephase_rate,'.3f')
                df['avg_qchannel_loss_init'] = format(avg_loss_init,'.3f')
                df['avg_qchannel_loss_noisy'] = format(avg_loss_noisy,'.3f')
                df['standard_deviation_of_depolar_rate'] = format(std_depolar_rate,'.3f')
                df['standard_deviation_of_dephase_rate'] = format(std_dephase_rate,'.3f')
                df['standard_deviation_of_qchannel_loss_init'] = format(std_loss_init,'.3f')
                df['standard_deviation_of_qchannel_loss_noisy'] = format(std_loss_noisy,'.4f')
                fidelity_data_temp = fidelity_data_temp.append(df)
                time_end=time.time()
                time_cost = time_cost + (time_end - time_start)
                round -= 1
                if round > 0:
                    continue
                else:
                    break
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
                df=dc_fidelity.dataframe
                df['routing_algorithm'] = "Q-Cast"
                df['entanglement_pair_consumption'] = (len(paths[index])-1)/2
                df['avg_depolar_rate'] = format(avg_depolar_rate,'.3f')
                df['avg_dephase_rate'] = format(avg_dephase_rate,'.3f')
                df['avg_qchannel_loss_init'] = format(avg_loss_init,'.3f')
                df['avg_qchannel_loss_noisy'] = format(avg_loss_noisy,'.3f')
                df['standard_deviation_of_depolar_rate'] = format(std_depolar_rate,'.3f')
                df['standard_deviation_of_dephase_rate'] = format(std_dephase_rate,'.3f')
                df['standard_deviation_of_qchannel_loss_init'] = format(std_loss_init,'.3f')
                df['standard_deviation_of_qchannel_loss_noisy'] = format(std_loss_noisy,'.4f')
                fidelity_data_temp = fidelity_data_temp.append(df)
                if df['fidelity'][0] == 1:
                    success_communication_num = success_communication_num + 1
                time_end=time.time()
                time_cost = time_cost + (time_end - time_start)
                round -= 1
                break
        
    throughput = success_communication_num / time_cost
    return fidelity_data_temp,throughput, time_cost_of_path_selection
