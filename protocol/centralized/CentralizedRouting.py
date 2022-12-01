import sys
sys.path.append("..")

import netsquid as ns
from topology.Centralized_Cellular_Topo import Centralized_Cellular_Network_setup
from util.CentralController import DomainShortestPathTable,DomainEdgeRepeaterTable

def CentralizedRouting(src_host,dst_host,central_controller,rc_number):
    ### rc_number is the Recursion number ###
    ### find host domain  ###
    for i in range(0,9):
         for instance in central_controller.domains[i].instances:
              if instance.node == src_host:
                   src_domain = central_controller.domains[i].domain_name
              if instance.node == dst_host:
                   dst_domain = central_controller.domains[i].domain_name
    dspt = DomainShortestPathTable()
    dert = DomainEdgeRepeaterTable()
    paths = []
    shortest_paths = []
    shortest_domain_paths = dspt.table[ord(dst_domain)-65][ord(src_domain)-65]
    
    ### find shortest path between src/dst ###
    for domain_path in shortest_domain_paths:
        path = []
        path.append(src_host)
        domains_in_path = domain_path.split('-')
        for i in range(len(domains_in_path)-1):
            repeater_name = dert.table[ord(domains_in_path[i])-65][ord(domains_in_path[i+1])-65]
            path.append(central_controller.domains[ord(domains_in_path[i])-65].instances[0].node)
            path.append(central_controller.domains[ord(domains_in_path[i])-65].getInstancebyName(repeater_name).node)
            if i == len(domains_in_path)-2:
                path.append(central_controller.domains[ord(domains_in_path[i+1])-65].instances[0].node)
                path.append(dst_host)
        shortest_paths.append(path)

    paths.extend(shortest_paths)
     
    ### Recursion to expand path ###
    N = 0
    paths_lr = shortest_paths
    paths_cr = []
    while(N<rc_number):
        for path in paths_lr:
            i=2
            while(i<len(path)-2):
               Neighbor_Repeaters = central_controller.getNeighborRepeaters(path[i])
               for instance in path:
                   if instance in Neighbor_Repeaters:
                       Neighbor_Repeaters.remove(instance)
               for j in range(len(Neighbor_Repeaters)):
                   for h in range(j+1,len(Neighbor_Repeaters)):
                       is_replace_nodes = False
                       if central_controller.is2RepeatersinSameDomain(Neighbor_Repeaters[j],Neighbor_Repeaters[h]):
                           replace_repeater_domain_controller = central_controller.getDomainControllerbyRepeaters(Neighbor_Repeaters[j],Neighbor_Repeaters[h])
                           if central_controller.is2RepeatersinSameDomain(path[i-2],Neighbor_Repeaters[j]) and central_controller.is2RepeatersinSameDomain(path[i+2],Neighbor_Repeaters[h]):
                               first_replace_node = Neighbor_Repeaters[j]
                               second_replace_node = Neighbor_Repeaters[h]
                               is_replace_nodes = True
 
                           if central_controller.is2RepeatersinSameDomain(path[i-2],Neighbor_Repeaters[h]) and central_controller.is2RepeatersinSameDomain(path[i+2],Neighbor_Repeaters[j]):
                               first_replace_node = Neighbor_Repeaters[h]
                               second_replace_node = Neighbor_Repeaters[j]
                               is_replace_nodes = True
         
                           if is_replace_nodes:
                               path_temp = []
                               for instance in path:
                                   if instance == path[i]:
                                       path_temp.append(first_replace_node)
                                       path_temp.append(replace_repeater_domain_controller)
                                       path_temp.append(second_replace_node)
                                   else:
                                       path_temp.append(instance)
                               is_valid_path = True
                               k = 0
                               while k <= len(path_temp)-5:
                                   if central_controller.is3RepeatersinSameDomain(path_temp[k],path_temp[k+2],path_temp[k+4]):
                                       is_valid_path=False
                                       break
                                   k = k+2
                               if is_valid_path:
                                   paths_cr.append(path_temp) 
               i=i+2
        if len(paths_cr) == 0:
            print("there is no more path to find in this topo, the current recursion round is {}".format(N))
            break
        paths.extend(paths_cr)
        paths_lr = paths_cr
        paths_cr = []
        N = N+1

    ### score evaluation ###
    paths_score_result = []
    for path in paths:
        temp = []
        score_path = 0
        hops = (len(path)-3)/2
        for i in range(len(path)):
            if "Repeater" in path[i].name:
                swapping_success_rate = central_controller.domains[ord(path[i-1].name.split("_")[1])-65].getInstancebyName(path[i].name).swapping_success_rate
                link_state_1 = central_controller.domains[ord(path[i-1].name.split("_")[1])-65].getInstancebyName(path[i].name).link_state
                link_state_2 = central_controller.domains[ord(path[i+1].name.split("_")[1])-65].getInstancebyName(path[i].name).link_state
                link_state = (link_state_1 + link_state_2)/2
                score_repeater = swapping_success_rate * 0.3 + link_state * 0.7
                score_path = score_path + score_repeater
        score_path = round(score_path / hops, 3)
        temp.append(path)
        temp.append(score_path)
        temp.append(hops)
        paths_score_result.append(temp)

    ### sort paths by socre and hops ###
    sort_paths = []
    while len(paths_score_result) > 0 :
        max_score = -9999
        for i in range(len(paths_score_result)):
            if paths_score_result[i][1] < max_score:
                continue
            elif paths_score_result[i][1] > max_score:
                max_score = paths_score_result[i][1]
                max_score_index = i
            elif paths_score_result[i][1] == max_score:
                if paths_score_result[i][2] < paths_score_result[max_score_index][2]:
                    max_score = paths_score_result[i][1]
                    max_score_index = i
        sort_paths.append(paths_score_result[max_score_index])
        del paths_score_result[max_score_index]
    return sort_paths
