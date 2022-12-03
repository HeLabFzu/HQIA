import sys
sys.path.append("..")

import netsquid as ns
import time
from topology.Centralized_Cellular_Topo import Centralized_Cellular_Network_setup
from protocol.centralized.CentralizedRouting import CentralizedRouting
from protocol.centralized.CentralizedResourceCheckReserve import CentralizedResourceCheckReserve
from protocol.centralized.CentralizedEntanglementDistribution import CentralizedEntanglementDistribution
from protocol.centralized.CentralizedSwapping import CentralizedSwapping
from protocol.centralized.CentralizedTeleportation import CentralizedTeleportation
from protocol.centralized.End2EndRequestProtocol import EndRequestProtocol
from util.CheckDistribution import CheckDistribution
from util.QubitCreation import CreateQubit
from util.NodeStruct import NodeStruct
from util.ResourceLockRelease import resource_lock,resource_release
from util.ClearCentralControllerTable import ClearCentralControllerTable
from util.CentralController import CentralControllerInfoTable,DomainShortestPathTable,DomainEdgeRepeaterTable
from netsquid.protocols.protocol import Signals

"""
This is a integrated example of centralized quantum internet communication.
This example contains all protocols which is designed in paper.
"""

def define_centralized_cellular_network(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy):
    network = Centralized_Cellular_Network_setup(depolar_rates=depolar_rates,dephase_rates=dephase_rates,
                                 qchannel_loss_init=qchannel_loss_init, qchannel_loss_noisy=qchannel_loss_noisy)
    central_controller = CentralControllerInfoTable(network,dephase_rates,qchannel_loss_init,qchannel_loss_noisy)
    return network,central_controller

def end_to_end_request(src_host,dst_host,central_controller_table,central_controller_node):
    src_lc = central_controller_table.getUserLocalController(src_host)
    dst_lc = central_controller_table.getUserLocalController(dst_host)
    
    ### two hosts in the same domain ###
    if src_lc == dst_lc:
        print("this is a local domain communication, need not to run centralized_routing_algorithm.")
        lc = src_lc
        src_request_protocol = EndRequestProtocol(src_host,"src_host",lc)
        src_request_protocol.start()
        EndRequestProtocol(lc,"controller",src_host,dst_host).start()
        EndRequestProtocol(dst_host,"dst_host",lc).start()
        ns.sim_run()
        receive_reply = False
        request_wait_time_start = time.time()
        request_wait_time = 0
        while request_wait_time < central_controller_table.request_time_limit:
            reply = src_request_protocol.get_signal_result(Signals.SUCCESS)
            request_wait_time_stop = time.time()
            request_wait_time = request_wait_time_stop - request_wait_time_start
            if reply != None:
                receive_reply = True
                break
        if receive_reply :
            print("Request Time Cost is {}s".format(request_wait_time))
            if isinstance(reply[0],str):
                return reply[0]
            else:
                print("dst_host accepted the request.")
                path = []
                path.append(NodeStruct(node=src_host,entangle_distribution_role="user",store_mem_pos_1=1))
                path.append(NodeStruct(node=lc,entangle_distribution_role="controller",
                          qsource_name=lc.name + "_" + src_host.name + "_" + dst_host.name + "_QSource"))
                path.append(NodeStruct(node=dst_host,entangle_distribution_role="user",store_mem_pos_1=reply[0]))
                resource_lock(path)
                print("Locked all related resource!")
                distribution_retry = 0
                problem_device = []
                while distribution_retry < 3:
                    print(" ")
                    print("#### Start Entanglement Distribution Process ####")
                    Entanglement_Distribution_Signal = True
                    distribution_time_cost_start = time.time()
                    distri_protocol_src_host = CentralizedEntanglementDistribution(node=path[0].node,role=path[0].entangle_distribution_role,store_mem_pos=path[0].store_mem_pos_1)
                    distri_protocol_lc = CentralizedEntanglementDistribution(node=path[1].node,role=path[1].entangle_distribution_role,qsource_name=path[1].qsource_name)
                    distri_protocol_dst_host = CentralizedEntanglementDistribution(node=path[2].node,role=path[2].entangle_distribution_role,store_mem_pos=path[2].store_mem_pos_1)
                    distri_protocol_src_host.start()
                    distri_protocol_lc.start()
                    distri_protocol_dst_host.start()
                    ns.sim_run()
                    distribution_time_cost_stop = time.time()
                    distribution_time_cost = distribution_time_cost_stop - distribution_time_cost_start
                    if not (distri_protocol_src_host.check() and distri_protocol_dst_host.check() and distribution_time_cost <= central_controller_table.distribution_time_limit):
                        Entanglement_Distribution_Signal = False
                        distri_protocol_src_host.stop()
                        distri_protocol_lc.stop()
                        distri_protocol_dst_host.stop()
                        print("Entanglement Distribution Failed")
                        print("Distribution Time Cost is {}s".format(distribution_time_cost))
                        if distribution_time_cost > central_controller_table.distribution_time_limit:
                            print("Distribution Time Out")
                        if not distri_protocol_src_host.check():
                            print("{} did not receive the entanglement qubit".format(src_host.name))
                            if src_host not in problem_device:
                                problem_device.append(src_host)
                        if not distri_protocol_dst_host.check():
                            print("{} did not received the entanglement qubit".format(dst_host.name))
                            if dst_host not in problem_device:
                                problem_device.append(dst_host)
                        distribution_retry += 1
                    if Entanglement_Distribution_Signal == True:
                        problem_device = []
                        print("#### Complete Entanglement Distribution Process ####")
                        print("Distribution Time Cost is {}s".format(distribution_time_cost))
                        central_controller_table.setInstanceMemState(src_host,[1],"occupy") 
                        central_controller_table.setInstanceMemState(dst_host,[reply[0]],"occupy")
                        central_controller_table.setInstanceMem_aimpair_aimcommuni_distristate(src_host,[1],[dst_host.name + "_mem_" + str(reply[0])], src_host.name + "->" + dst_host.name, "Success" )
                        central_controller_table.setInstanceMem_aimpair_aimcommuni_distristate(dst_host,[reply[0]],[src_host.name + "_mem_" + "1"], src_host.name + "->" + dst_host.name, "Success" )
                        print("Updated Central Controller Table")
                        break
                        
                if Entanglement_Distribution_Signal == False:
                    print("all entanglement distribution retry failed")
                    for device in problem_device:
                        central_controller_table.setInstanceStateSingle(device,lc,"maintain")
                    print("Updated Central Controller Table")
                    resource_release(path)
                    print("Released all related resource!")
                else:
                    print(" ")   
                    print("#### Start to teleport target qubit ####")
                    CreateQubit(src_host,mem_pos=0).start()
                    ns.sim_run()
                    teleportation_time_cost_start = time.time()
                    CentralizedTeleportation(src_host, dst_host, lc, lc, central_controller_node, 0, 1, reply[0]).start()
                    ns.sim_run()
                    teleportation_time_cost_stop = time.time()
                    teleportation_time_cost = teleportation_time_cost_stop - teleportation_time_cost_start
                    if teleportation_time_cost <= central_controller_table.swapping_teleportation_time_limit:
                        print("#### Complete to teleport target qubit ####")
                        print("Teleportation Time Cost is {}s".format(teleportation_time_cost))
                        central_controller_table.setInstanceMemTeleporationState(src_host,1,"Success")
                        central_controller_table.setInstanceMemTeleporationState(dst_host,reply[0],"Success")
                        print("Updated Central Controller Table")
                        target_qubit = dst_host.qmemory.peek(reply[0])
                        fidelity = ns.qubits.fidelity(target_qubit, ns.y0, squared=True)
                        print(" ")
                        print("The fidelity of this quantum communication is {}".format(fidelity))
                    else:
                        print("Teleportation Time Cost is {}s".format(teleportation_time_cost))
                        print("Teleportation Failed, Time Out")
                        central_controller_table.setInstanceMemTeleporationState(src_host,1,"Failed")
                        central_controller_table.setInstanceMemTeleporationState(dst_host,reply[0],"Failed")
                        print("Updated Central Controller Table")

                    central_controller_table.clear(src_host,[1])
                    central_controller_table.clear(dst_host,[reply[0]])
                    print("Cleared The Central Controller Table")               
                    resource_release(path)
                    print("Released all related resource !") 
                return "Local Domain Communication Complete" 
        else :
            print("Request Time Cost is {}s, the request time limit is {}s".format(request_wait_time,central_controller_table.request_time_limit))
            return "request_time_out"

    ### two hosts in different domains ###
    else:
        print("this is a Inter-Domain communication.")
        src_request_protocol = EndRequestProtocol(src_host,"src_host",src_lc)
        src_request_protocol.start()
        EndRequestProtocol(src_lc,"controller",src_host,central_controller_node).start()
        EndRequestProtocol(central_controller_node,"controller",src_lc,dst_lc).start()
        EndRequestProtocol(dst_lc,"controller",central_controller_node,dst_host).start()
        EndRequestProtocol(dst_host,"dst_host",dst_lc).start()
        ns.sim_run()
        receive_reply = False
        request_wait_time_start = time.time()
        request_wait_time = 0
        while request_wait_time < central_controller_table.request_time_limit:
            reply = src_request_protocol.get_signal_result(Signals.SUCCESS)
            request_wait_time_stop = time.time()
            request_wait_time = request_wait_time_stop - request_wait_time_start
            if reply != None:
                receive_reply = True
                break
        if receive_reply :
            return reply[0]
        else :
            print("Request Time Cost is {}s, the request time limit is {}s".format(request_wait_time,central_controller_table.request_time_limit))
            return "request_time_out"
        
def centralized_routing(src_host,dst_host,src_user_mem,dst_user_mem,network,central_controller):
    sort_paths = CentralizedRouting(src_host,dst_host,central_controller,rc_number=2)
    while 1:
        FinalResult = CentralizedResourceCheckReserve(sort_paths.pop(0)[0],src_user_mem=src_user_mem,dst_user_mem=dst_user_mem,central_controller=central_controller)
        if FinalResult != "null":
            break
        elif len(sort_paths) == 0:
            break
    if FinalResult != "null":
        print("#### Centralized path result ####")
        for i in range(len(FinalResult)):
            if i == 0 or i == len(FinalResult)-1:
               print("Node {},mem {}".format(FinalResult[i].node.name,FinalResult[i].store_mem_pos_1))
            elif i%2 == 0:
                print("Node {} , mem {},{}".format(FinalResult[i].node.name,FinalResult[i].store_mem_pos_1,FinalResult[i].store_mem_pos_2))
            else:
                print("Local Controller {} (Distribute Entanglement Pair only)".format(FinalResult[i].node.name))
        return FinalResult
    else :
        print("Announce No Path Found For The Request !")
        return "null"

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

def run_entangle_distribution_protocol():
    distribution_retry = 0
    distribution_problem_device = []
    while distribution_retry < 3:
        print(" ")
        if distribution_retry == 0:
            print("#### Start Entanglement Distribution Process ####")
        if distribution_retry > 0:
            print("#### Retry Entanglement Distribution Process ####")
        Entanglement_Distribution_Signal = True
        distribution_time_cost_start = time.time()
        for i in range(len(entangle_distribution_protocol)):
            if Entanglement_Distribution_Signal:
                for j in range(len(entangle_distribution_protocol[i])):
                    entangle_distribution_protocol[i][j].start()
                ns.sim_run()
                for j in range(len(entangle_distribution_protocol[i])):
                    if not entangle_distribution_protocol[i][j].check():
                        Entanglement_Distribution_Signal = False
                        if not entangle_distribution_protocol[i][0].check():
                            print("{} did not receive the entanglement qubit from {}".format(path_result[2*i].node.name,path_result[2*i+1].node.name))
                            problem_device = [path_result[2*i].node, path_result[2*i+1].node]
                            if problem_device not in distribution_problem_device:
                                distribution_problem_device.append(problem_device)
                        if not entangle_distribution_protocol[i][2].check():
                            print("{} did not receive the entanglement qubit from {}".format(path_result[2*i+2].node.name,path_result[2*i+1].node.name))
                            problem_device = [path_result[2*i+2].node, path_result[2*i+1].node]
                            if problem_device not in distribution_problem_device:
                                distribution_problem_device.append(problem_device)
                        entangle_distribution_protocol[i][0].stop()
                        entangle_distribution_protocol[i][1].stop()
                        entangle_distribution_protocol[i][2].stop()
                        print("Entanglement Distribution Failed")
                        distribution_retry += 1
                        break
            else:
                break
        distribution_time_cost_stop = time.time()
        distribution_time_cost = distribution_time_cost_stop - distribution_time_cost_start
        print("Distribution Time Cost is {}s".format(distribution_time_cost))
        if Entanglement_Distribution_Signal == True and distribution_time_cost > central_controller_table.distribution_time_limit:
            print("Distribution Time Out")
            Entanglement_Distribution_Signal = False
            distribution_retry += 1
        elif Entanglement_Distribution_Signal == True:
            distribution_problem_device = []
            print("#### Complete Entanglement Distribution Process ####")
            for index in range(len(path_result)):
                if src_host == path_result[index].node:
                    central_controller_table.setInstanceMem_aimpair_aimcommuni_distristate(src_host,[1],[path_result[index+2].node.name + "_mem_" + str(path_result[index+2].store_mem_pos_1)], src_host.name + "->" + dst_host.name, "Success" )
                elif dst_host == path_result[index].node:
                    central_controller_table.setInstanceMem_aimpair_aimcommuni_distristate(dst_host,[reply_result],[path_result[index-2].node.name + "_mem_" + str(path_result[index-2].store_mem_pos_2)], src_host.name + "->" + dst_host.name, "Success" )
                elif index == 2:
                    central_controller_table.setInstanceMem_aimpair_aimcommuni_distristate(path_result[index].node,[path_result[index].store_mem_pos_1,path_result[index].store_mem_pos_2],[src_host.name + "_mem_1", path_result[index+2].node.name + "_mem_" + str(path_result[index+2].store_mem_pos_1)], src_host.name + "->" + dst_host.name, "Success" )
                elif "Repeater" in path_result[index].node.name:
                    central_controller_table.setInstanceMem_aimpair_aimcommuni_distristate(path_result[index].node,[path_result[index].store_mem_pos_1,path_result[index].store_mem_pos_2],[path_result[index-2].node.name + "_mem_" + str(path_result[index-2].store_mem_pos_2),path_result[index+2].node.name + "_mem_" + str(path_result[index+2].store_mem_pos_1)], src_host.name + "->" + dst_host.name, "Success" )
            print("Updated Central Controller Table")
            break
    if Entanglement_Distribution_Signal == False:
        print(" ")
        print("#### All Entanglement Distribution Retry Failed ####")
        for device in distribution_problem_device:
            central_controller_table.setInstanceStateSingle(device[0],device[1],"maintain")
        for nodestruct in path_result:
            if "User" in nodestruct.node.name:
                central_controller_table.clear(nodestruct.node,[nodestruct.store_mem_pos_1])
            elif "Repeater" in nodestruct.node.name:
                central_controller_table.clear(nodestruct.node,[nodestruct.store_mem_pos_1,nodestruct.store_mem_pos_2])
        print("Updated Central Controller Table")
        resource_release(path_result)
        print(" ")
        print("#### Released all related resource and restart to select alternative path ####")
        return False
    else:
        return True

def run_swapping_protocol():
    print(" ")
    print("#### Start Entanglement Swapping Process ####")
    Swapping_Signal = True
    for i in range(len(swapping_protocol)):
        for j in range(len(swapping_protocol[i])):
            swapping_protocol[i][j].start()
        ns.sim_run()
        q1, = src_host.qmemory.peek(1)
        q2, = path_result[2*i+4].node.qmemory.peek(path_result[2*i+4].store_mem_pos_1)
        if ns.qubits.fidelity([q1, q2], ns.b00) == 0:
            Swapping_Signal = False
            print("node {} swapping failed".format(path_result[2*i+2].node.name))
            break
    if Swapping_Signal == True:
        print("#### Complete Entanglement Swapping Process ####")
        for nodestruct in path_result:
            if "Repeater" in nodestruct.node.name:
                central_controller_table.setInstanceMemSwappingState(nodestruct.node,[nodestruct.store_mem_pos_1,nodestruct.store_mem_pos_2],"Success")
        print("Updated Central Controller Table")
        return True
    else:
        return path_result[2*i+2].node

def run_teleportation_protocol():
    print(" ")
    print("#### Start to teleport target qubit ####")
    CreateQubit(src_host,mem_pos=0).start()
    ns.sim_run()
    teleportation_time_cost_start = time.time()
    CentralizedTeleportation(src_host, dst_host, path_result[1].node, path_result[len(path_result)-2].node, central_controller_node, 0, 1, reply_result).start()
    ns.sim_run()
    teleportation_time_cost_stop = time.time()
    swapping_teleportation_time_cost = teleportation_time_cost_stop - teleportation_time_cost_start + swapping_time_cost
    if swapping_teleportation_time_cost <= central_controller_table.swapping_teleportation_time_limit:
        print("#### Complete to teleport target qubit ####")
        print("Swapping and Teleportation Time Cost is {}s".format(swapping_teleportation_time_cost))
        central_controller_table.setInstanceMemTeleporationState(src_host,1,"Success")
        central_controller_table.setInstanceMemTeleporationState(dst_host,reply_result,"Success")
        print("Updated Central Controller Table")
        target_qubit = dst_host.qmemory.peek(reply_result)
        fidelity = ns.qubits.fidelity(target_qubit, ns.y0, squared=True)
        print(" ")
        print("The fidelity of this quantum communication is {}".format(fidelity))
    else:
        print("Swapping_Teleportation Time Cost is {}s".format(swapping_teleportation_time_cost))
        print("Teleportation Failed, Time Out")
        central_controller_table.setInstanceMemTeleporationState(src_host,1,"Failed")
        central_controller_table.setInstanceMemTeleporationState(dst_host,reply_result,"Failed")
        print("Updated Central Controller Table")

    for nodestruct in path_result:
        if "User" in nodestruct.node.name:
            central_controller_table.clear(nodestruct.node,[nodestruct.store_mem_pos_1])
        elif "Repeater" in nodestruct.node.name:
            central_controller_table.clear(nodestruct.node,[nodestruct.store_mem_pos_1,nodestruct.store_mem_pos_2])
    print("Cleared The Central Controller Table")
    resource_release(path_result)
    print("Released all related resource!")

if __name__ == '__main__':
    depolar_rates = []
    dephase_rates = []
    qchannel_loss_init = []
    qchannel_loss_noisy = []


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
    ### you can change the parameter here to obeserve the teleport result,depolar_rate(0~1),dephase_rate(0~1),qchannel_loss_init(0~1),qchannel_loss_noisy(0~n(No more than 0.2（noisy_limitation in this topo）is recommended),dB/km) ###
    ### notice: this code set all devices parameter with same value, if you want different values in different devices ,you can define the arrays by yourself. ###
    """
    there are some recommand values to check this programe:
    #### if you want to see a success quantum communication example , please use the parameters:
    for i in range(29):
        depolar_rates.append(0)
    for i in range(29):
        dephase_rates.append(0)
    for i in range(32):
        qchannel_loss_init.append(0)
    for i in range(32):
        qchannel_loss_noisy.append(0)

    #### if you want to see a how the distribution failed due to the bad link_state , please use the parameters:
    for i in range(29):
        depolar_rates.append(0)
    for i in range(29):
        dephase_rates.append(0)
    for i in range(32):
        qchannel_loss_init.append(1)
    for i in range(32):
        qchannel_loss_noisy.append(0.2)

    #### if you want to see a how the swapping failed due to bad device parameter , please use the parameters:
    for i in range(29):
        depolar_rates.append(1)
    for i in range(29):
        dephase_rates.append(1)
    for i in range(32):
        qchannel_loss_init.append(0)
    for i in range(32):
        qchannel_loss_noisy.append(0)

    #### if you want to see a relative random result , please use the parameters:
    for i in range(29):
        depolar_rates.append(0.01)
    for i in range(29):
        dephase_rates.append(0.01)
    for i in range(32):
        qchannel_loss_init.append(0.01)
    for i in range(32):
        qchannel_loss_noisy.append(0.001)

    #### if you want to check how the routing algorithm(score evaluation) select the optimal path(not have to be shortest path) due to the parameter, please define the arrays with different values by yourself:
    such as :
    depolar_rates = [0.004,0.005,0.001,0.002,0.009,0.008,0.009,0.003,0.001,0.008,0.006,0.001,0.008,0.006,0.003,0.003,0.002,0.004,0.005,0.006,0.003,0.002,0.005,0.009,0.006,0.001,0.002,0.004,0.006]
    dephase_rates = [0.09,0.35,0.03,0.03,0.35,0.35,0.11,0.03,0.03,0.09,0.03,0.03,0.02,0.14,0.07,0.02,0.03,0.04,0.02,0.05,0.06,0.02,0.09,0.04,0.03,0.03,0.05,0.06,0.07]
    qchannel_loss_init = [0.008,0.021,0.002,0.001,0.002,0.002,0.017,0.008,0.015,0.020,0.030,0.002,0.003,0.005,0.002,0.024,0.004,0.006,0.008,0.007,0.002,0.047,0.010,0.053,0.003,0.002,0.008,0.002,0.004,0.034,0.011,0.001]
    qchannel_loss_noisy = [0.0006,0.0004,0.0004,0.0003,0.0002,0.0003,0.0015,0.0005,0.0003,0.0022,0.0033,0.0001,0.0003,0.0003,0.0004,0.0026,0.0003,0.0004,0.0006,0.0004,0.0003,0.0046,0.0012,0.0057,0.0002,0.0001,0.0006,0.0005,0.0003,0.0035,0.0014,0.0001]
    """


    for i in range(29):
        depolar_rates.append(0)
    for i in range(29):
        dephase_rates.append(0)
    for i in range(32):
        qchannel_loss_init.append(0)
    for i in range(32):
        qchannel_loss_noisy.append(0)

    network,central_controller_table = define_centralized_cellular_network(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy)

    ### User_C,User_D,User_E are also available, they are in different domains ###
    src_host = network.subcomponents["User_A"]
    dst_host = network.subcomponents["User_B"]
    central_controller_node = network.subcomponents["Central_Controller"]
    print("#### Start to End-End Request Process ####")
    reply_result = end_to_end_request(src_host,dst_host,central_controller_table,central_controller_node)
    if reply_result == "Local Domain Communication Complete":
        print("Local Domain Quantum Communication Complete!")
    elif isinstance(reply_result,str):
        print(reply_result)
    else:
        print("dst_host already accept the request!")
        while 1:
            print(" ")
            print("### Start Routing Process ###")
            path_result = centralized_routing(src_host,dst_host,1,reply_result,network,central_controller_table)
            if path_result == "null":
                print("Quantum Communication Failed !")
                break
            else:
                print("Locked all related resource!")
                resource_lock(path_result)
                entangle_distribution_protocol,swapping_protocol,create_qubit_protocol,teleportation_protocol = define_protocol(path_result,network)

                swap_retry = 0
                swap_problem_node = []
                teleportation_Signal = False

                while swap_retry < 3:
                    distribution_result = run_entangle_distribution_protocol()
                    if distribution_result == True:
                        swapping_time_cost_start = time.time()
                        swapping_result = run_swapping_protocol()
                        swapping_time_cost_stop = time.time()
                        swapping_time_cost = swapping_time_cost_stop - swapping_time_cost_start
                        if swapping_result == True and swapping_time_cost <= central_controller_table.swapping_teleportation_time_limit:
                            swap_problem_node = []
                            run_teleportation_protocol()
                            teleportation_Signal = True
                            break
                        elif not isinstance(swapping_result, bool):
                            print("Swapping time cost is {}".format(swapping_time_cost))
                            if swap_retry < 2:
                                print(" ")
                                print("#### Recall to Entanglement Distribution and Retry Swapping ####")
                            else:
                                print(" ")
                                print("#### All Entanglement Swapping Retry Failed! ####")
                            if swapping_result not in swap_problem_node:
                                swap_problem_node.append(swapping_result)
                            swap_retry += 1
                        elif swapping_time_cost > central_controller_table.swapping_teleportation_time_limit:
                            print("Swapping time cost is {}".format(swapping_time_cost))
                            print("entanglement swapping time out!")
                            if swap_retry < 2:
                                print(" ")
                                print("#### Recall to Entanglement Distribution and Retry Swapping ####")
                            else:
                                print(" ")
                                print("#### All Entanglement Swapping Retry Failed! ####")
                            swap_retry += 1
                    else:
                        break

                if teleportation_Signal == True:
                    print("Inter-Domain Quantum Communication Complete!")
                    break
                elif swap_retry == 3:
                    for node in swap_problem_node:
                        central_controller_table.setInstanceState(node,"maintain")
                    for nodestruct in path_result:
                        if "User" in nodestruct.node.name:
                            central_controller_table.clear(nodestruct.node,[nodestruct.store_mem_pos_1])
                        elif "Repeater" in nodestruct.node.name:
                            central_controller_table.clear(nodestruct.node,[nodestruct.store_mem_pos_1,nodestruct.store_mem_pos_2])
                    print("Updated Central Controller Table")
                    resource_release(path_result)
                    print(" ")
                    print("#### Released all related resource and restart to select alternative path ####")

