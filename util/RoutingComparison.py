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

Generally speaking, distributed routing algorithm can only run in distributed topology, but in order to eliminate the interference of inconsistent topology between centralized_routing and distributed_routing, obtain more accurate experimental comparison results,
these experiments run distributed_routing_algorithm(Q-cast, Greedy, SLMP) in a pseudo_distributed_topo(which is a centralized topo, but we use code to hide the controller and the distributed_routing_algorithm will think the topo as a distributed topo.)

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

#if __name__ == '__main__':
#   # RAdepo =0.01 
#   # RBdepo =0.01
#   # RCdepo =0.01
#   # RDdepo =0.01
#   # REdepo =0.01
#   # RFdepo =0.01
#   # RGdepo =0.01
#   # RHdepo =0.01
#   # RIdepo =0.01
#   # RJdepo =0.01
#   # RKdepo =0.01
#   # RLdepo =0.01
#   # RMdepo =0.01
#   # RNdepo =0.01
#   # ROdepo =0.01
#   # CAdepo =0.01 
#   # CBdepo =0.01
#   # CCdepo =0.01
#   # CDdepo =0.01
#   # CEdepo =0.01
#   # CFdepo =0.01
#   # CGdepo =0.01
#   # CHdepo =0.01
#   # CIdepo =0.01
#   # UAdepo =0.01 
#   # UBdepo =0.01
#   # UCdepo =0.01
#   # UDdepo =0.01
#   # UEdepo =0.01
#
#   # RAdeph =0.01
#   # RBdeph =0.01
#   # RCdeph =0.01
#   # RDdeph =0.01
#   # REdeph =0.01
#   # RFdeph =0.01
#   # RGdeph =0.01
#   # RHdeph =0.01
#   # RIdeph =0.01
#   # RJdeph =0.01
#   # RKdeph =0.01
#   # RLdeph =0.01
#   # RMdeph =0.01
#   # RNdeph =0.01
#   # ROdeph =0.01
#   # CAdeph =0.01
#   # CBdeph =0.01
#   # CCdeph =0.01
#   # CDdeph =0.01
#   # CEdeph =0.01
#   # CFdeph =0.01
#   # CGdeph =0.01
#   # CHdeph =0.01
#   # CIdeph =0.01
#   # UAdeph =0.01
#   # UBdeph =0.01
#   # UCdeph =0.01
#   # UDdeph =0.01
#   # UEdeph =0.01
#
#   # CARA_li =0.01 
#   # CARB_li =0.01 
#   # CARC_li =0.01
#   # CAUA_li =0.01
#   # CBRC_li =0.01  
#   # CBRD_li =0.01
#   # CBRE_li =0.01
#   # CBUE_li =0.01 
#   # CCRB_li =0.01
#   # CCRE_li =0.01
#   # CCRF_li =0.01
#   # CDRD_li =0.01
#   # CDRG_li =0.01
#   # CDRH_li =0.01
#   # CERE_li =0.01
#   # CERH_li =0.01
#   # CERI_li =0.01
#   # CEUD_li =0.01
#   # CFRF_li =0.01
#   # CFRI_li =0.01
#   # CFRJ_li =0.01
#   # CGRH_li =0.01
#   # CGRK_li =0.01
#   # CGRL_li =0.01
#   # CHRI_li =0.01
#   # CHRL_li =0.01
#   # CHRM_li =0.01
#   # CHUC_li =0.01
#   # CIRL_li =0.01
#   # CIRN_li =0.01
#   # CIRO_li =0.01
#   # CIUB_li =0.01
#
#   # CARA_ln =0.0001
#   # CARB_ln =0.0001
#   # CARC_ln =0.0001
#   # CAUA_ln =0.0001
#   # CBRC_ln =0.0001
#   # CBRD_ln =0.0001
#   # CBRE_ln =0.0001
#   # CBUE_ln =0.0001
#   # CCRB_ln =0.0001
#   # CCRE_ln =0.0001
#   # CCRF_ln =0.0001
#   # CDRD_ln =0.0001
#   # CDRG_ln =0.0001
#   # CDRH_ln =0.0001
#   # CERE_ln =0.0001
#   # CERH_ln =0.0001
#   # CERI_ln =0.0001
#   # CEUD_ln =0.0001
#   # CFRF_ln =0.0001
#   # CFRI_ln =0.0001
#   # CFRJ_ln =0.0001
#   # CGRH_ln =0.0001
#   # CGRK_ln =0.0001
#   # CGRL_ln =0.0001
#   # CHRI_ln =0.0001
#   # CHRL_ln =0.0001
#   # CHRM_ln =0.0001
#   # CHUC_ln =0.0001
#   # CIRL_ln =0.0001
#   # CIRN_ln =0.0001
#   # CIRO_ln =0.0001
#   # CIUB_ln =0.0001
#    
#   # depolar_rates = [RAdepo,RBdepo,RCdepo,RDdepo,REdepo,RFdepo,RGdepo,RHdepo,RIdepo,RJdepo,RKdepo,RLdepo,RMdepo,RNdepo,ROdepo,CAdepo,CBdepo,CCdepo,CDdepo,CEdepo,CFdepo,CGdepo,CHdepo,CIdepo,UAdepo,UBdepo,UCdepo,UDdepo,UEdepo]
#   # dephase_rates = [RAdeph,RBdeph,RCdeph,RDdeph,REdeph,RFdeph,RGdeph,RHdeph,RIdeph,RJdeph,RKdeph,RLdeph,RMdeph,RNdeph,ROdeph,CAdeph,CBdeph,CCdeph,CDdeph,CEdeph,CFdeph,CGdeph,CHdeph,CIdeph,UAdeph,UBdeph,UCdeph,UDdeph,UEdeph]
#   # qchannel_loss_init = [CARA_li,CARB_li,CARC_li,CAUA_li,CBRC_li,CBRD_li,CBRE_li,CBUE_li,CCRB_li,CCRE_li,CCRF_li,CDRD_li,CDRG_li,CDRH_li,CERE_li,CERH_li,CERI_li,CEUD_li,CFRF_li,CFRI_li,CFRJ_li,CGRH_li,CGRK_li,CGRL_li,CHRI_li,CHRL_li,CHRM_li,CHUC_li,CIRL_li,CIRN_li,CIRO_li,CIUB_li]
#   # qchannel_loss_noisy = [CARA_ln,CARB_ln,CARC_ln,CAUA_ln,CBRC_ln,CBRD_ln,CBRE_ln,CBUE_ln,CCRB_ln,CCRE_ln,CCRF_ln,CDRD_ln,CDRG_ln,CDRH_ln,CERE_ln,CERH_ln,CERI_ln,CEUD_ln,CFRF_ln,CFRI_ln,CFRJ_ln,CGRH_ln,CGRK_ln,CGRL_ln,CHRI_ln,CHRL_ln,CHRM_ln,CHUC_ln,CIRL_ln,CIRN_ln,CIRO_ln,CIUB_ln]
#
#    ################################
#    ####  avg_dephase_rate test ###
#    ###############################
#    fidelity_data = pandas.DataFrame()
#    centralized_routing_throughputs = []
#    QCast_throughputs = []
#    SLMP_throughputs = []
#    greedy_throughputs = []
#    for avg_dephase_rate in [0.01,0.05,0.1,0.15,0.2]:
#         dephase_rates = []
#         for i in range(29):  
#             dephase_rates.append(avg_dephase_rate)
#
#         depolar_rates = []
#         for i in range(29):
#             depolar_rates.append(0.01)
#
#         qchannel_loss_init = []
#         for i in range(32):
#             qchannel_loss_init.append(0.01)
#
#         qchannel_loss_noisy = []
#         for i in range(32):
#             qchannel_loss_noisy.append(0.001)         
#
#         ### run Centralized routing test ###
#         fidelity_data_temp,centralized_routing_throughput, centralized_routing_time_cost = run_centralized_routing_test(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy)
#         fidelity_data = fidelity_data.append(fidelity_data_temp)
#         centralized_routing_throughputs.append(centralized_routing_throughput)
#
#         ### run Q-Cast routing test ###
#         fidelity_data_temp,QCast_throughput, QCast_time_cost = run_QCast_routing_test(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy)
#         fidelity_data = fidelity_data.append(fidelity_data_temp)
#         QCast_throughputs.append(QCast_throughput)
#
#         ### run SLMP routing test ###
#         fidelity_data_temp,SLMP_throughput, SLMP_time_cost = run_SLMP_routing_test(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy)
#         fidelity_data = fidelity_data.append(fidelity_data_temp)
#         SLMP_throughputs.append(SLMP_throughput)
#
#         ### run Greedy routing test ###
#         fidelity_data_temp,greedy_throughput, greedy_time_cost = run_greedy_routing_test(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy)
#         fidelity_data = fidelity_data.append(fidelity_data_temp)
#         greedy_throughputs.append(greedy_throughput)
#
#    fidelity_cr_deph = fidelity_data[fidelity_data['routing_algorithm']=="Centralized_Routing"].groupby("avg_dephase_rate")['fidelity'].agg(fidelity='mean', sem='sem').reset_index()
#    fidelity_qc_deph = fidelity_data[fidelity_data['routing_algorithm']=="Q-Cast"].groupby("avg_dephase_rate")['fidelity'].agg(fidelity='mean', sem='sem').reset_index()
#    fidelity_slmp_deph = fidelity_data[fidelity_data['routing_algorithm']=="SLMP"].groupby("avg_dephase_rate")['fidelity'].agg(fidelity='mean', sem='sem').reset_index()
#    fidelity_greedy_deph = fidelity_data[fidelity_data['routing_algorithm']=="Greedy"].groupby("avg_dephase_rate")['fidelity'].agg(fidelity='mean', sem='sem').reset_index()
#    entanglement_pair_consumption_cr_deph = fidelity_data[fidelity_data['routing_algorithm']=="Centralized_Routing"].groupby("avg_dephase_rate")['entanglement_pair_consumption'].agg(entanglement_pair_consumption='mean').reset_index()
#    entanglement_pair_consumption_qc_deph = fidelity_data[fidelity_data['routing_algorithm']=="Q-Cast"].groupby("avg_dephase_rate")['entanglement_pair_consumption'].agg(entanglement_pair_consumption='mean').reset_index()
#    entanglement_pair_consumption_slmp_deph = fidelity_data[fidelity_data['routing_algorithm']=="SLMP"].groupby("avg_dephase_rate")['entanglement_pair_consumption'].agg(entanglement_pair_consumption='mean').reset_index()
#    entanglement_pair_consumption_greedy_deph = fidelity_data[fidelity_data['routing_algorithm']=="Greedy"].groupby("avg_dephase_rate")['entanglement_pair_consumption'].agg(entanglement_pair_consumption='mean').reset_index()
#    throughput_cr_deph = pandas.DataFrame([[0.01,centralized_routing_throughputs[0]],
#                                           [0.05,centralized_routing_throughputs[1]],
#                                           [0.1,centralized_routing_throughputs[2]],
#                                           [0.15,centralized_routing_throughputs[3]],
#                                           [0.2,centralized_routing_throughputs[4]]],
#                                           columns=['avg_dephase_rate', 'throughput'])
#    throughput_qc_deph = pandas.DataFrame([[0.01,QCast_throughputs[0]],
#                                           [0.05,QCast_throughputs[1]],
#                                           [0.1,QCast_throughputs[2]],
#                                           [0.15,QCast_throughputs[3]],
#                                           [0.2,QCast_throughputs[4]]],
#                                           columns=['avg_dephase_rate', 'throughput'])
#    throughput_slmp_deph = pandas.DataFrame([[0.01,SLMP_throughputs[0]],
#                                           [0.05,SLMP_throughputs[1]],
#                                           [0.1,SLMP_throughputs[2]],
#                                           [0.15,SLMP_throughputs[3]],
#                                           [0.2,SLMP_throughputs[4]]],
#                                           columns=['avg_dephase_rate', 'throughput'])
#    throughput_greedy_deph = pandas.DataFrame([[0.01,greedy_throughputs[0]],
#                                           [0.05,greedy_throughputs[1]],
#                                           [0.1,greedy_throughputs[2]],
#                                           [0.15,greedy_throughputs[3]],
#                                           [0.2,greedy_throughputs[4]]],
#                                           columns=['avg_dephase_rate', 'throughput'])
#
#    ################################
#    ####  avg_loss_init test ###
#    ###############################
#    fidelity_data = pandas.DataFrame()
#    centralized_routing_throughputs = []
#    QCast_throughputs = []
#    SLMP_throughputs = []
#    greedy_throughputs = []
#    for avg_loss_init in [0.01,0.05,0.1,0.15,0.2]:
#         qchannel_loss_init = []
#         for i in range(32):
#             qchannel_loss_init.append(avg_loss_init)
#
#         depolar_rates = []
#         for i in range(29):
#             depolar_rates.append(0.01)
#
#         dephase_rates = []
#         for i in range(29):
#             dephase_rates.append(0.01)
#
#         qchannel_loss_noisy = []
#         for i in range(32):
#             qchannel_loss_noisy.append(0.001)
#
#         ### run Centralized routing test ###
#         fidelity_data_temp,centralized_routing_throughput, centralized_routing_time_cost = run_centralized_routing_test(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy)
#         fidelity_data = fidelity_data.append(fidelity_data_temp)
#         centralized_routing_throughputs.append(centralized_routing_throughput)
#
#         ### run Q-Cast routing test ###
#         fidelity_data_temp,QCast_throughput, QCast_time_cost = run_QCast_routing_test(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy)
#         fidelity_data = fidelity_data.append(fidelity_data_temp)
#         QCast_throughputs.append(QCast_throughput)
#
#         ### run SLMP routing test ###
#         fidelity_data_temp,SLMP_throughput, SLMP_time_cost = run_SLMP_routing_test(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy)
#         fidelity_data = fidelity_data.append(fidelity_data_temp)
#         SLMP_throughputs.append(SLMP_throughput)
#
#         ### run Greedy routing test ###
#         fidelity_data_temp,greedy_throughput, greedy_time_cost = run_greedy_routing_test(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy)
#         fidelity_data = fidelity_data.append(fidelity_data_temp)
#         greedy_throughputs.append(greedy_throughput)
#
#    fidelity_cr_init = fidelity_data[fidelity_data['routing_algorithm']=="Centralized_Routing"].groupby("avg_qchannel_loss_init")['fidelity'].agg(fidelity='mean', sem='sem').reset_index()
#    fidelity_qc_init = fidelity_data[fidelity_data['routing_algorithm']=="Q-Cast"].groupby("avg_qchannel_loss_init")['fidelity'].agg(fidelity='mean', sem='sem').reset_index()
#    fidelity_slmp_init = fidelity_data[fidelity_data['routing_algorithm']=="SLMP"].groupby("avg_qchannel_loss_init")['fidelity'].agg(fidelity='mean', sem='sem').reset_index()
#    fidelity_greedy_init = fidelity_data[fidelity_data['routing_algorithm']=="Greedy"].groupby("avg_qchannel_loss_init")['fidelity'].agg(fidelity='mean', sem='sem').reset_index()
#    entanglement_pair_consumption_cr_init = fidelity_data[fidelity_data['routing_algorithm']=="Centralized_Routing"].groupby("avg_qchannel_loss_init")['entanglement_pair_consumption'].agg(entanglement_pair_consumption='mean').reset_index()
#    entanglement_pair_consumption_qc_init = fidelity_data[fidelity_data['routing_algorithm']=="Q-Cast"].groupby("avg_qchannel_loss_init")['entanglement_pair_consumption'].agg(entanglement_pair_consumption='mean').reset_index()
#    entanglement_pair_consumption_slmp_init = fidelity_data[fidelity_data['routing_algorithm']=="SLMP"].groupby("avg_qchannel_loss_init")['entanglement_pair_consumption'].agg(entanglement_pair_consumption='mean').reset_index()
#    entanglement_pair_consumption_greedy_init = fidelity_data[fidelity_data['routing_algorithm']=="Greedy"].groupby("avg_qchannel_loss_init")['entanglement_pair_consumption'].agg(entanglement_pair_consumption='mean').reset_index()
#    throughput_cr_init = pandas.DataFrame([[0.01,centralized_routing_throughputs[0]],
#                                           [0.05,centralized_routing_throughputs[1]],
#                                           [0.1,centralized_routing_throughputs[2]],
#                                           [0.15,centralized_routing_throughputs[3]],
#                                           [0.2,centralized_routing_throughputs[4]]],
#                                           columns=['avg_qchannel_loss_init', 'throughput'])
#    throughput_qc_init = pandas.DataFrame([[0.01,QCast_throughputs[0]],
#                                           [0.05,QCast_throughputs[1]],
#                                           [0.1,QCast_throughputs[2]],
#                                           [0.15,QCast_throughputs[3]],
#                                           [0.2,QCast_throughputs[4]]],
#                                           columns=['avg_qchannel_loss_init', 'throughput'])
#    throughput_slmp_init = pandas.DataFrame([[0.01,SLMP_throughputs[0]],
#                                           [0.05,SLMP_throughputs[1]],
#                                           [0.1,SLMP_throughputs[2]],
#                                           [0.15,SLMP_throughputs[3]],
#                                           [0.2,SLMP_throughputs[4]]],
#                                           columns=['avg_qchannel_loss_init', 'throughput'])
#    throughput_greedy_init = pandas.DataFrame([[0.01,greedy_throughputs[0]],
#                                           [0.05,greedy_throughputs[1]],
#                                           [0.1,greedy_throughputs[2]],
#                                           [0.15,greedy_throughputs[3]],
#                                           [0.2,greedy_throughputs[4]]],
#                                           columns=['avg_qchannel_loss_init', 'throughput'])
#
#    ################################
#    ####  avg_loss_noisy test ###
#    ###############################
#    fidelity_data = pandas.DataFrame()
#    centralized_routing_throughputs = []
#    QCast_throughputs = []
#    SLMP_throughputs = []
#    greedy_throughputs = []
#    for avg_loss_noisy in [0.001,0.005,0.01,0.015,0.02]:
#         qchannel_loss_noisy = []
#         for i in range(32):
#             qchannel_loss_noisy.append(avg_loss_noisy)
#
#         depolar_rates = []
#         for i in range(29):
#             depolar_rates.append(0.01)
#
#         dephase_rates = []
#         for i in range(29):
#             dephase_rates.append(0.01)
#
#         qchannel_loss_init = []
#         for i in range(32):
#             qchannel_loss_init.append(0.01)
#
#         ### run Centralized routing test ###
#         fidelity_data_temp,centralized_routing_throughput, centralized_routing_time_cost = run_centralized_routing_test(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy)
#         fidelity_data = fidelity_data.append(fidelity_data_temp)
#         centralized_routing_throughputs.append(centralized_routing_throughput)
#
#         ### run Q-Cast routing test ###
#         fidelity_data_temp,QCast_throughput, QCast_time_cost = run_QCast_routing_test(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy)
#         fidelity_data = fidelity_data.append(fidelity_data_temp)
#         QCast_throughputs.append(QCast_throughput)
#
#         ### run SLMP routing test ###
#         fidelity_data_temp,SLMP_throughput, SLMP_time_cost = run_SLMP_routing_test(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy)
#         fidelity_data = fidelity_data.append(fidelity_data_temp)
#         SLMP_throughputs.append(SLMP_throughput)
#
#         ### run Greedy routing test ###
#         fidelity_data_temp,greedy_throughput, greedy_time_cost = run_greedy_routing_test(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy)
#         fidelity_data = fidelity_data.append(fidelity_data_temp)
#         greedy_throughputs.append(greedy_throughput)
#
#    fidelity_cr_noisy = fidelity_data[fidelity_data['routing_algorithm']=="Centralized_Routing"].groupby("avg_qchannel_loss_noisy")['fidelity'].agg(fidelity='mean', sem='sem').reset_index()
#    fidelity_qc_noisy = fidelity_data[fidelity_data['routing_algorithm']=="Q-Cast"].groupby("avg_qchannel_loss_noisy")['fidelity'].agg(fidelity='mean', sem='sem').reset_index()
#    fidelity_slmp_noisy = fidelity_data[fidelity_data['routing_algorithm']=="SLMP"].groupby("avg_qchannel_loss_noisy")['fidelity'].agg(fidelity='mean', sem='sem').reset_index()
#    fidelity_greedy_noisy = fidelity_data[fidelity_data['routing_algorithm']=="Greedy"].groupby("avg_qchannel_loss_noisy")['fidelity'].agg(fidelity='mean', sem='sem').reset_index()
#    entanglement_pair_consumption_cr_noisy = fidelity_data[fidelity_data['routing_algorithm']=="Centralized_Routing"].groupby("avg_qchannel_loss_noisy")['entanglement_pair_consumption'].agg(entanglement_pair_consumption='mean').reset_index()
#    entanglement_pair_consumption_qc_noisy = fidelity_data[fidelity_data['routing_algorithm']=="Q-Cast"].groupby("avg_qchannel_loss_noisy")['entanglement_pair_consumption'].agg(entanglement_pair_consumption='mean').reset_index()
#    entanglement_pair_consumption_slmp_noisy = fidelity_data[fidelity_data['routing_algorithm']=="SLMP"].groupby("avg_qchannel_loss_noisy")['entanglement_pair_consumption'].agg(entanglement_pair_consumption='mean').reset_index()
#    entanglement_pair_consumption_greedy_noisy = fidelity_data[fidelity_data['routing_algorithm']=="Greedy"].groupby("avg_qchannel_loss_noisy")['entanglement_pair_consumption'].agg(entanglement_pair_consumption='mean').reset_index()
#    throughput_cr_noisy = pandas.DataFrame([[0.01,centralized_routing_throughputs[0]],
#                                           [0.05,centralized_routing_throughputs[1]],
#                                           [0.1,centralized_routing_throughputs[2]],
#                                           [0.15,centralized_routing_throughputs[3]],
#                                           [0.2,centralized_routing_throughputs[4]]],
#                                           columns=['avg_qchannel_loss_noisy', 'throughput'])
#    throughput_qc_noisy = pandas.DataFrame([[0.01,QCast_throughputs[0]],
#                                           [0.05,QCast_throughputs[1]],
#                                           [0.1,QCast_throughputs[2]],
#                                           [0.15,QCast_throughputs[3]],
#                                           [0.2,QCast_throughputs[4]]],
#                                           columns=['avg_qchannel_loss_noisy', 'throughput'])
#    throughput_slmp_noisy = pandas.DataFrame([[0.01,SLMP_throughputs[0]],
#                                           [0.05,SLMP_throughputs[1]],
#                                           [0.1,SLMP_throughputs[2]],
#                                           [0.15,SLMP_throughputs[3]],
#                                           [0.2,SLMP_throughputs[4]]],
#                                           columns=['avg_qchannel_loss_noisy', 'throughput'])
#    throughput_greedy_noisy = pandas.DataFrame([[0.01,greedy_throughputs[0]],
#                                           [0.05,greedy_throughputs[1]],
#                                           [0.1,greedy_throughputs[2]],
#                                           [0.15,greedy_throughputs[3]],
#                                           [0.2,greedy_throughputs[4]]],
#                                           columns=['avg_qchannel_loss_noisy', 'throughput'])
#
#    fig,ax = plt.subplots(2,3,figsize=(25,10))
#    plot_style = {'kind': 'line', 'grid': True,
#      'title': "Routing Algorithm Comparison"}
#    ax[0][0].set_ylabel('fidelity')
#    ax[0][1].set_ylabel('fidelity')
#    ax[0][2].set_ylabel('fidelity')
#    ax[1][0].set_ylabel('throughput(qps)')
#    ax[1][1].set_ylabel('throughput(qps)')
#    ax[1][2].set_ylabel('throughput(qps)')
#
#    fidelity_cr_deph.plot(x='avg_dephase_rate', y='fidelity',ax=ax[0][0],label="Centralized_Routing", **plot_style)
#    fidelity_qc_deph.plot(x='avg_dephase_rate', y='fidelity',ax=ax[0][0],label="Q-Cast", **plot_style)
#    fidelity_slmp_deph.plot(x='avg_dephase_rate', y='fidelity',ax=ax[0][0],label="SLMP", **plot_style)
#    fidelity_greedy_deph.plot(x='avg_dephase_rate', y='fidelity',ax=ax[0][0],label="Greedy", **plot_style)
#    throughput_cr_deph.plot(x='avg_dephase_rate', y='throughput', ax=ax[1][0],label="Centralized_Routing", **plot_style)
#    throughput_qc_deph.plot(x='avg_dephase_rate', y='throughput', ax=ax[1][0],label="Q-Cast", **plot_style)
#    throughput_slmp_deph.plot(x='avg_dephase_rate', y='throughput', ax=ax[1][0],label="SLMP", **plot_style)
#    throughput_greedy_deph.plot(x='avg_dephase_rate', y='throughput', ax=ax[1][0],label="Greedy", **plot_style)
#
#    fidelity_cr_init.plot(x='avg_qchannel_loss_init', y='fidelity',ax=ax[0][1],label="Centralized_Routing", **plot_style)
#    fidelity_qc_init.plot(x='avg_qchannel_loss_init', y='fidelity',ax=ax[0][1],label="Q-Cast", **plot_style)
#    fidelity_slmp_init.plot(x='avg_qchannel_loss_init', y='fidelity',ax=ax[0][1],label="SLMP", **plot_style)
#    fidelity_greedy_init.plot(x='avg_qchannel_loss_init', y='fidelity',ax=ax[0][1],label="Greedy", **plot_style)
#    throughput_cr_init.plot(x='avg_qchannel_loss_init', y='throughput', ax=ax[1][1],label="Centralized_Routing", **plot_style)
#    throughput_qc_init.plot(x='avg_qchannel_loss_init', y='throughput', ax=ax[1][1],label="Q-Cast", **plot_style)
#    throughput_slmp_init.plot(x='avg_qchannel_loss_init', y='throughput', ax=ax[1][1],label="SLMP", **plot_style)
#    throughput_greedy_init.plot(x='avg_qchannel_loss_init', y='throughput', ax=ax[1][1],label="Greedy", **plot_style)
#   
#
#    fidelity_cr_noisy.plot(x='avg_qchannel_loss_noisy', y='fidelity',ax=ax[0][2],label="Centralized_Routing", **plot_style)
#    fidelity_qc_noisy.plot(x='avg_qchannel_loss_noisy', y='fidelity',ax=ax[0][2],label="Q-Cast", **plot_style)
#    fidelity_slmp_noisy.plot(x='avg_qchannel_loss_noisy', y='fidelity',ax=ax[0][2],label="SLMP", **plot_style)
#    fidelity_greedy_noisy.plot(x='avg_qchannel_loss_noisy', y='fidelity',ax=ax[0][2],label="Greedy", **plot_style)
#    throughput_cr_noisy.plot(x='avg_qchannel_loss_noisy', y='throughput', ax=ax[1][2],label="Centralized_Routing", **plot_style)
#    throughput_qc_noisy.plot(x='avg_qchannel_loss_noisy', y='throughput', ax=ax[1][2],label="Q-Cast", **plot_style)
#    throughput_slmp_noisy.plot(x='avg_qchannel_loss_noisy', y='throughput', ax=ax[1][2],label="SLMP", **plot_style)
#    throughput_greedy_noisy.plot(x='avg_qchannel_loss_noisy', y='throughput', ax=ax[1][2],label="Greedy", **plot_style)
#
#   # print(fidelity_cr_deph)
#   # print(fidelity_qc_deph)
#   # print(fidelity_slmp_deph)
#   # print(fidelity_greedy_deph)
#   # print(entanglement_pair_consumption_cr_deph)
#   # print(entanglement_pair_consumption_qc_deph)
#   # print(entanglement_pair_consumption_slmp_deph)
#   # print(entanglement_pair_consumption_greedy_deph)
#   # print(centralized_routing_throughputs)
#   # print(QCast_throughputs)
#   # print(SLMP_throughputs)
#   # print(greedy_throughputs)
#    plt.show()

