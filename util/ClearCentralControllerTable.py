def ClearCentralControllerTable(path,central_controller):
    for instance in path:
        if "Repeater" in instance.node.name:
            central_controller.setInstanceMemState(instance.node,[instance.store_mem_pos_1,instance.store_mem_pos_2],"idle")
        if "User" in instance.node.name:
            central_controller.setInstanceMemState(instance.node,[instance.store_mem_pos_1],"idle")
