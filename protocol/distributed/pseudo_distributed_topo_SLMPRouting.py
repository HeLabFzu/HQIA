import netsquid as ns
from protocol.centralized.CentralizedEntanglementDistribution import CentralizedEntanglementDistribution
from util.NodeStruct import NodeStruct

"""
the principle of SLMP_algorithm is that 
a) Entanglement is distributed at all adjacent Repeaters
b) In the nodes with successful entanglement distribution, we need to decide which nodes should do entanglment-swapping, the swapping decision principle is that after swapping the two remote nodes should be closest to SRC and DST, respectively。

thus the entanglement-distribution process should be contained in SLMP.
"""

class AdjacentTable:
    def __init__(self,network):
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
  
        self.adjacent_table = []
        self.adjacent_table.append([User_A, [Repeater_A,Repeater_B,Repeater_C]])
        self.adjacent_table.append([Repeater_A, [User_A,Repeater_B,Repeater_C]])
        self.adjacent_table.append([Repeater_B, [User_A,Repeater_A,Repeater_C,Repeater_E,Repeater_F]])
        self.adjacent_table.append([Repeater_C, [User_A,Repeater_A,Repeater_B,Repeater_D,Repeater_E]])
        self.adjacent_table.append([Repeater_D, [Repeater_C,Repeater_E,Repeater_G,Repeater_H]])
        self.adjacent_table.append([Repeater_E, [Repeater_B,Repeater_C,Repeater_D,Repeater_F,Repeater_H,Repeater_I]])
        self.adjacent_table.append([Repeater_F, [Repeater_B,Repeater_E,Repeater_I,Repeater_J]])
        self.adjacent_table.append([Repeater_G, [Repeater_D,Repeater_H]])
        self.adjacent_table.append([Repeater_H, [Repeater_D,Repeater_E,Repeater_G,Repeater_I,Repeater_K,Repeater_L]])
        self.adjacent_table.append([Repeater_I, [Repeater_E,Repeater_F,Repeater_H,Repeater_J,Repeater_L,Repeater_M]])
        self.adjacent_table.append([Repeater_J, [Repeater_F,Repeater_I]])
        self.adjacent_table.append([Repeater_K, [Repeater_H,Repeater_L]])
        self.adjacent_table.append([Repeater_L, [User_B,Repeater_H,Repeater_I,Repeater_K,Repeater_M,Repeater_N,Repeater_O]])
        self.adjacent_table.append([Repeater_M, [Repeater_I,Repeater_L]])
        self.adjacent_table.append([Repeater_N, [User_B,Repeater_L,Repeater_O]])
        self.adjacent_table.append([Repeater_O, [User_B,Repeater_L,Repeater_N]])
        self.adjacent_table.append([User_B, [Repeater_L,Repeater_N,Repeater_O]])

        ### hops_record first element is node, second is hops-to-src-host, third is hops-to-dst-host
        self.hops_record = []
        self.hops_record.append([User_A, 0, 5])
        self.hops_record.append([Repeater_A, 1, 5])
        self.hops_record.append([Repeater_B, 1, 4])
        self.hops_record.append([Repeater_C, 1, 4])
        self.hops_record.append([Repeater_D, 2, 3])
        self.hops_record.append([Repeater_E, 2, 3])
        self.hops_record.append([Repeater_F, 2, 3])
        self.hops_record.append([Repeater_G, 3, 3])
        self.hops_record.append([Repeater_H, 3, 2])
        self.hops_record.append([Repeater_I, 3, 2])
        self.hops_record.append([Repeater_J, 3, 3])
        self.hops_record.append([Repeater_K, 4, 2])
        self.hops_record.append([Repeater_L, 4, 1])
        self.hops_record.append([Repeater_M, 4, 2])
        self.hops_record.append([Repeater_N, 5, 1])
        self.hops_record.append([Repeater_O, 5, 1])
        self.hops_record.append([User_B, 5, 0])
    
    def findmempos(self,node_1,node_2):
        for item in self.adjacent_table:
            if node_1 == item[0]:
                for i in range(len(item[1])):
                    if node_2 == item[1][i]:
                        return i+1
    def find_hops_to_dst(self,node):
        for item in self.hops_record:
            if node == item[0]:
                return item[2]

### DomainTable only for pseudo_distributed_topo ###
class DomainTable:
    def __init__(self,network):
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
        self.domain_table = []
        self.domain_table.append([Controller_A,User_A,Repeater_A,Repeater_B,Repeater_C])
        self.domain_table.append([Controller_B,Repeater_C,Repeater_D,Repeater_E])
        self.domain_table.append([Controller_C,Repeater_B,Repeater_E,Repeater_F])
        self.domain_table.append([Controller_D,Repeater_D,Repeater_G,Repeater_H])
        self.domain_table.append([Controller_E,Repeater_E,Repeater_H,Repeater_I])
        self.domain_table.append([Controller_F,Repeater_F,Repeater_I,Repeater_J])
        self.domain_table.append([Controller_G,Repeater_H,Repeater_K,Repeater_L])
        self.domain_table.append([Controller_H,Repeater_I,Repeater_L,Repeater_M])
        self.domain_table.append([Controller_I,User_B,Repeater_L,Repeater_N,Repeater_O])
    def findcontroller(self,node_name_1,node_name_2):
        for domain in self.domain_table:
            if node_name_1 in domain and node_name_2 in domain:
                controller = domain[0]
                return controller

def SLMP(network,src_host,dst_host):
    at = AdjacentTable(network)
    dt = DomainTable(network) 
    entanglement_pairs = []
    for item in dt.domain_table:
        for i in range(1,len(item)):
            for j in range(i+1,len(item)):
                if "User" in item[i].name:
                    role = "user"
                    protocol_1 = CentralizedEntanglementDistribution(node=item[0], role="controller", qsource_name=item[0].name + "_" + item[j].name + "_" + item[i].name + "_QSource")
                elif "Repeater" in item[i].name:
                    role = "repeater"
                    protocol_1 = CentralizedEntanglementDistribution(node=item[0], role="controller", qsource_name=item[0].name + "_" + item[i].name + "_" + item[j].name + "_QSource")
                protocol_2 = CentralizedEntanglementDistribution(node=item[i], role=role, store_mem_pos=at.findmempos(item[i],item[j]))
                protocol_3 = CentralizedEntanglementDistribution(node=item[j], role="repeater", store_mem_pos=at.findmempos(item[j],item[i]))
                protocol_2.start()
                protocol_3.start()
                protocol_1.start()
                ns.sim_run()
                if protocol_2.check() == False or protocol_3.check() == False:
                    protocol_2.stop()
                    protocol_3.stop()
                else:
                    entanglement_pairs.append([item[i],item[j],at.findmempos(item[i],item[j]),at.findmempos(item[j],item[i])])
    path = []
    flag = True
    while len(path) == 0 and flag == True:
        flag = False
        present_node = network.subcomponents["User_A"]
        temp_path = []
        temp_path.append(present_node)
        min_hops = 9999
        while present_node.name != "User_B":
            for entanglement_pair in entanglement_pairs:
                if present_node.name in entanglement_pair[0].name:
                    if at.find_hops_to_dst(entanglement_pair[1]) < min_hops and entanglement_pair[1] not in temp_path:
                        min_hops = at.find_hops_to_dst(entanglement_pair[1])
                        pre_hop_node_mem = at.findmempos(entanglement_pair[0],entanglement_pair[1])
                        next_hop_node_mem = at.findmempos(entanglement_pair[1],entanglement_pair[0])
                        next_hop_node = entanglement_pair[1]
                elif present_node.name in entanglement_pair[1].name and entanglement_pair[0] not in temp_path:
                    if at.find_hops_to_dst(entanglement_pair[0]) < min_hops:
                        min_hops = at.find_hops_to_dst(entanglement_pair[0])
                        pre_hop_node_mem = at.findmempos(entanglement_pair[1],entanglement_pair[0])
                        next_hop_node_mem = at.findmempos(entanglement_pair[0],entanglement_pair[1])
                        next_hop_node = entanglement_pair[0]
            if min_hops != 9999:
                temp_path.append(pre_hop_node_mem)
                temp_path.append(next_hop_node_mem)
                temp_path.append(next_hop_node)
                present_node = next_hop_node
                min_hops = 9999
            else:
                for entanglement_pair in entanglement_pairs:
                    if entanglement_pair[1] == temp_path[len(temp_path)-1] or entanglement_pair[0] == temp_path[len(temp_path)-1]:
                         entanglement_pairs.remove(entanglement_pair)
                break
        for entanglement_pair in entanglement_pairs:
            if "User_A" in entanglement_pair[0].name or "User_A" in entanglement_pair[1].name:
                 flag = True
                 break
        if temp_path[len(temp_path)-1].name == "User_B":
            path = temp_path   
    FinalResult = []
    if len(path) == 0:
        return "null"
    else:
        i = 0
        while i in range(len(path)):
            if i == 0:
                FinalResult.append(NodeStruct(node=path[0],entangle_distribution_role="user",store_mem_pos_1=path[1]))
                FinalResult.append(NodeStruct(node=dt.findcontroller(path[0],path[3]),entangle_distribution_role="controller"))
            elif i == len(path)-1:
                FinalResult.append(NodeStruct(node=path[i],entangle_distribution_role="user",store_mem_pos_1=path[i-1]))
            else:
                FinalResult.append(NodeStruct(node=path[i],entangle_distribution_role="repeater",store_mem_pos_1=path[i-1],store_mem_pos_2=path[i+1]))
                FinalResult.append(NodeStruct(node=dt.findcontroller(path[i],path[i+3]),entangle_distribution_role="controller"))
            i = i+3
        return FinalResult
                
         
     
                     
                

          
