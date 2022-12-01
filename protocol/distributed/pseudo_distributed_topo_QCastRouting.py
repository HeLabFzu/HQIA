from util.NodeStruct import NodeStruct

"""
the principle of Q-cast is that 
firstly, Dijkstra algorithm or Greedy is used for path selection, and the path with the maximum theoretical throughput is taken as the main path.
secondly, limit the hop number "l" and select recovery Path as the alternative path. 
finally, When the primary path entanglement distribution fails, enable the alternative path until the path is successfully established, then do entanglement swapping.

In our topology, there is only one pair memory for adjacent node, so for every path the theoretical throughput for one time-slot is 1. 
Therefore, the first step for Q-cast in our experiment is that using Greedy to select shortest path.
Then, we defined the hop number "l" 2, and find the alternative path.
"""
class NodeRoutingTable:
    def __init__(self,node, neighbor_nodes, shortest_hops):
         self.node = node
         self.neighbor_nodes = neighbor_nodes
         self.shortest_hops = shortest_hops

class NetworkRoutingTable:
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

        self.network_routing_table = []
        self.network_routing_table.append(NodeRoutingTable(User_A, [Repeater_A,Repeater_B,Repeater_C], [5,4,4]))
        self.network_routing_table.append(NodeRoutingTable(Repeater_A, [User_A,Repeater_B,Repeater_C], [5,4,4]))
        self.network_routing_table.append(NodeRoutingTable(Repeater_B, [User_A,Repeater_A,Repeater_C,Repeater_F,Repeater_E], [5,5,4,3,3]))
        self.network_routing_table.append(NodeRoutingTable(Repeater_C, [User_A,Repeater_A,Repeater_B,Repeater_D,Repeater_E], [5,5,4,3,3]))
        self.network_routing_table.append(NodeRoutingTable(Repeater_D, [Repeater_C,Repeater_E,Repeater_G,Repeater_H], [4,3,3,2]))
        self.network_routing_table.append(NodeRoutingTable(Repeater_E, [Repeater_B,Repeater_C,Repeater_D,Repeater_F,Repeater_H,Repeater_I], [4,4,3,3,2,2]))
        self.network_routing_table.append(NodeRoutingTable(Repeater_F, [Repeater_B,Repeater_E,Repeater_I,Repeater_J], [4,3,2,3]))
        self.network_routing_table.append(NodeRoutingTable(Repeater_G, [Repeater_D,Repeater_H], [3,2]))
        self.network_routing_table.append(NodeRoutingTable(Repeater_H, [Repeater_D,Repeater_E,Repeater_G,Repeater_I,Repeater_K,Repeater_L], [3,3,3,2,2,1]))
        self.network_routing_table.append(NodeRoutingTable(Repeater_I, [Repeater_E,Repeater_F,Repeater_H,Repeater_J,Repeater_L,Repeater_M], [3,3,2,3,1,2]))
        self.network_routing_table.append(NodeRoutingTable(Repeater_J, [Repeater_F,Repeater_I], [3,2]))
        self.network_routing_table.append(NodeRoutingTable(Repeater_K, [Repeater_H,Repeater_L], [2,1]))
        self.network_routing_table.append(NodeRoutingTable(Repeater_L, [User_B,Repeater_H,Repeater_I,Repeater_K,Repeater_M,Repeater_N,Repeater_O], [0,2,2,2,2,1,1]))
        self.network_routing_table.append(NodeRoutingTable(Repeater_M, [Repeater_I,Repeater_L], [2,1]))
        self.network_routing_table.append(NodeRoutingTable(Repeater_N, [User_B,Repeater_L,Repeater_O], [0,1,1]))
        self.network_routing_table.append(NodeRoutingTable(Repeater_O, [User_B,Repeater_L,Repeater_N], [0,1,1]))
        self.network_routing_table.append(NodeRoutingTable(User_B, [Repeater_L,Repeater_N,Repeater_O], [1,1,1]))
    def findroutingtable(self,node):
        for routingtable in self.network_routing_table:
            if node == routingtable.node:
                return routingtable

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
        self.domain_table = []
        self.domain_table.append([Controller_A,"User_A","Repeater_A","Repeater_B","Repeater_C"])
        self.domain_table.append([Controller_B,"Repeater_C","Repeater_D","Repeater_E"])
        self.domain_table.append([Controller_C,"Repeater_B","Repeater_E","Repeater_F"])
        self.domain_table.append([Controller_D,"Repeater_D","Repeater_G","Repeater_H"])
        self.domain_table.append([Controller_E,"Repeater_E","Repeater_H","Repeater_I"])
        self.domain_table.append([Controller_F,"Repeater_F","Repeater_I","Repeater_J"])
        self.domain_table.append([Controller_G,"Repeater_H","Repeater_K","Repeater_L"])
        self.domain_table.append([Controller_H,"Repeater_I","Repeater_L","Repeater_M"])
        self.domain_table.append([Controller_I,"User_B","Repeater_L","Repeater_N","Repeater_O"])

    def findcontroller(self,node_name_1,node_name_2):
        for domain in self.domain_table:
            if node_name_1 in domain and node_name_2 in domain:
                controller = domain[0]
                return controller
    def isInSameDomain(self,node_name_1,node_name_2):
        result = False
        for domain in self.domain_table:
            if node_name_1 in domain and node_name_2 in domain:
                 result = True
        return result
    def isInSameDomain_3(self,node_name_1,node_name_2,node_name_3):
        result = False
        for domain in self.domain_table:
            if node_name_1 in domain and node_name_2 in domain and node_name_3 in domain:
                 result = True
        return result



def QCast(network,src_host,dst_host):
    nrt = NetworkRoutingTable(network)
    dt = DomainTable(network)
    main_path = [src_host]

    while main_path[len(main_path)-1] != dst_host:
        present_node = main_path[len(main_path)-1]
        rt = nrt.findroutingtable(present_node)
        min_hops = 9999
        for i in range(len(rt.shortest_hops)):
             if rt.shortest_hops[i] < min_hops:
                 min_hops = rt.shortest_hops[i]
                 index = i
        main_path.append(rt.neighbor_nodes[index])
        
    ### find recovery path ###
    recovery_paths = []
    
    ### when hop number "l" is 1 ###
    for i in range(len(main_path)-1):
        recovery_path = []
        rt = nrt.findroutingtable(main_path[i])
        for node in rt.neighbor_nodes:
            if node not in main_path:
                 for j in range(i+1,len(main_path)):
                     if dt.isInSameDomain(node.name,main_path[j].name):
                         if j - i == 1:
                             for k in range(len(main_path)):
                                 recovery_path.append(main_path[k])
                                 if k == i:
                                     recovery_path.append(node)
                         else:
                             flag = False
                             for k in range(len(main_path)):
                                 if k<=i or k>=j:
                                     recovery_path.append(main_path[k])
                                 elif flag == False:
                                     recovery_path.append(node)
                                     flag = True
                     if len(recovery_path) != 0:   
                         ### Excluding loops with three Repeaters in the same domain, this is an invalid redundant path ###
                         judge = True
                         for h in range(len(recovery_path)-2):
                             if dt.isInSameDomain_3(recovery_path[h].name,recovery_path[h+1].name,recovery_path[h+2].name):
                                  judge = False
                                  break
                         if judge :
                             recovery_paths.append(recovery_path)
                         recovery_path = []
                                 
    ### when hop number "l" is 2 ### 
    for i in range(len(main_path)):
        recovery_path = []
        rt_1 = nrt.findroutingtable(main_path[i])
        for node_1 in rt_1.neighbor_nodes:
            if node_1 not in main_path:
                rt_2 = nrt.findroutingtable(node_1)
                for node_2 in rt_2.neighbor_nodes:
                    if node_2 not in main_path:
                        for j in range(i+1,len(main_path)):
                            if dt.isInSameDomain(node_2.name,main_path[j].name):
                                if j - i == 1:
                                    for k in range(len(main_path)):
                                        recovery_path.append(main_path[k])
                                        if k == i:
                                            recovery_path.append(node_1)
                                            recovery_path.append(node_2)
                                else:
                                    flag = False
                                    for k in range(len(main_path)):
                                        if k<=i or k>=j:
                                            recovery_path.append(main_path[k])
                                        elif flag == False:
                                            recovery_path.append(node_1)
                                            recovery_path.append(node_2)
                                            flag = True
                            if len(recovery_path) != 0:
                                ### Excluding loops with three Repeaters in the same domain, this is an invalid redundant path ###
                                judge = True
                                for h in range(len(recovery_path)-2):
                                    if dt.isInSameDomain_3(recovery_path[h].name,recovery_path[h+1].name,recovery_path[h+2].name):
                                         judge = False
                                         break
                                if judge :
                                    recovery_paths.append(recovery_path)
                                recovery_path = []

    
   
    ### find controller and insert to path, only for pseudo_distributed_topo ###
    path = []
    for i in range(len(main_path)-1):
        path.append(main_path[i])
        controller = dt.findcontroller(main_path[i].name,main_path[i+1].name)
        path.append(controller)
        if i == len(main_path)-2:
            path.append(main_path[i+1])
    paths = [path]
    for recovery_path in recovery_paths:
        path = []
        for i in range(len(recovery_path)-1):
            path.append(recovery_path[i])
            controller = dt.findcontroller(recovery_path[i].name,recovery_path[i+1].name)
            path.append(controller)
            if i == len(recovery_path)-2:
                path.append(recovery_path[i+1])
        paths.append(path)
    
    FinalResults = []    
    for path in paths:
        FinalResult = []
        for i in range(len(path)):
            if i == 0:
                FinalResult.append(NodeStruct(node=path[i],entangle_distribution_role="user",
                              store_mem_pos_1=1))
            elif i == len(path)-1:
                FinalResult.append(NodeStruct(node=path[i],entangle_distribution_role="user",
                              store_mem_pos_1=1))
            else:
                if "Controller" in path[i].name:
                    if "User" in path[i-1].name:
                        node_name_1 = path[i+1].name
                        node_name_2 = path[i-1].name
                    elif "User" in path[i+1].name:
                        node_name_1 = path[i-1].name
                        node_name_2 = path[i+1].name
                    elif path[i-1].name.split("_")[1] < path[i+1].name.split("_")[1]:
                        node_name_1 = path[i-1].name
                        node_name_2 = path[i+1].name
                    else:
                        node_name_1 = path[i+1].name
                        node_name_2 = path[i-1].name
                    qsource_name = path[i].name + "_" + node_name_1 + "_" + node_name_2 + "_" + "QSource"
                    FinalResult.append(NodeStruct(node = path[i], entangle_distribution_role="controller",qsource_name=qsource_name))
                if "Repeater" in path[i].name:
                    FinalResult.append(NodeStruct(node=path[i],entangle_distribution_role="repeater",
                              store_mem_pos_1=1,store_mem_pos_2=2))
        FinalResults.append(FinalResult)
    return FinalResults         
