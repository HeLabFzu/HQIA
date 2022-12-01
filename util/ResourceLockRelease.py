def resource_lock(path):
    for node_number in range(len(path)):
        if path[node_number].store_mem_pos_1 is not None: 
            path[node_number].node.qmemory.mem_positions[path[node_number].store_mem_pos_1].in_use = True
        if path[node_number].store_mem_pos_2 is not None:
            path[node_number].node.qmemory.mem_positions[path[node_number].store_mem_pos_2].in_use = True

def resource_release(path):
    for node_number in range(len(path)):
        if path[node_number].store_mem_pos_1 is not None:
            path[node_number].node.qmemory.mem_positions[path[node_number].store_mem_pos_1].in_use = False
        if path[node_number].store_mem_pos_2 is not None:
            path[node_number].node.qmemory.mem_positions[path[node_number].store_mem_pos_2].in_use = False


