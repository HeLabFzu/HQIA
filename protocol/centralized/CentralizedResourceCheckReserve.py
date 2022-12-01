import sys
sys.path.append("..")

from util.NodeStruct import NodeStruct

def CentralizedResourceCheckReserve(path,src_user_mem,dst_user_mem,central_controller):

### check resource in central_controller ###
    FinalResult = []
    for i in range(len(path)):
        if i == 0:
            FinalResult.append(NodeStruct(node=path[i],entangle_distribution_role="user",
                          store_mem_pos_1=src_user_mem))    
        elif i == len(path)-1:
            FinalResult.append(NodeStruct(node=path[i],entangle_distribution_role="user",
                          store_mem_pos_1=dst_user_mem))
        else:
            if "Controller" in path[i].name:
                LocalControllerMaintain = central_controller.domains[ord(path[i].name.split("_")[1])-65].instances[0].device_state
                if LocalControllerMaintain == "normal":
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
                else:
                    FinalResult = "null"
                    break
            if "Repeater" in path[i].name:
                 RepeaterMaintain = central_controller.domains[ord(path[i-1].name.split("_")[1])-65].getInstancebyName(path[i].name).device_state
                 if RepeaterMaintain == "normal":
                     idle_mem_number = 0
                     repeater_mems = []
                     for mem in central_controller.domains[ord(path[i-1].name.split("_")[1])-65].getInstancebyName(path[i].name).mems:
                          if mem.state == "idle":
                               repeater_mems.append(mem.mem_name)
                               idle_mem_number = idle_mem_number + 1
                          if idle_mem_number == 2:
                               break
                     if idle_mem_number == 2:
                          FinalResult.append(NodeStruct(node=path[i],entangle_distribution_role="repeater",
                          store_mem_pos_1=repeater_mems[0],store_mem_pos_2=repeater_mems[1]))
                     else:
                          FinalResult = "null"
                          break
                 else:
                     FinalResult = "null"
                     break

### Directly double-check mem resource in device, Reserve resource ###
    if FinalResult != "null":
         for instance in FinalResult:
             if "Repeater" in instance.node.name:
                if instance.node.qmemory.mem_positions[instance.store_mem_pos_1].in_use or instance.node.qmemory.mem_positions[instance.store_mem_pos_2].in_use:
                     FinalResult = "null"
                     break
             if "User" in instance.node.name:
                if instance.node.qmemory.mem_positions[instance.store_mem_pos_1].in_use:
                     FinalResult = "null"
                     break
    if FinalResult != "null":
         for instance in FinalResult:
             if "Repeater" in instance.node.name:
                 central_controller.setInstanceMemState(instance.node,[instance.store_mem_pos_1,instance.store_mem_pos_2],"occupy")
             if "User" in instance.node.name:
                 central_controller.setInstanceMemState(instance.node,[instance.store_mem_pos_1],"occupy")
    return FinalResult
             
            
        

    
