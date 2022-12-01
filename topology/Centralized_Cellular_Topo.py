import netsquid as ns
from netsquid.nodes import Node
from netsquid.components import  QuantumMemory, QuantumProcessor
from netsquid.nodes import Network
from netsquid.components.qsource import QSource, SourceStatus
from netsquid.components.qprocessor import QuantumProcessor, PhysicalInstruction
from netsquid.qubits import ketstates as ks
from netsquid.qubits.state_sampler import StateSampler
from netsquid.components.models.delaymodels import FixedDelayModel, FibreDelayModel
from netsquid.components import ClassicalChannel,QuantumChannel
from netsquid.nodes.connections import DirectConnection
from netsquid.components.models.qerrormodels import DepolarNoiseModel, DephaseNoiseModel,FibreLossModel
from netsquid.components import instructions as instr


def Centralized_Cellular_Network_setup(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy,prep_delay=0,num_mem_positions=3,node_distance=100):
    """
    Create an example network for use with the entangling nodes protocol.

    Parameters
    ----------
    prep_delay : float, optional
        Delay used in the source in this network. Default is 5 [ns].
    num_mem_positions : int
        Number of memory positions on both nodes in the network. Default is 3.
    depolar_rates : float
        An Array with 29 items (Repeater_A~Repeater_O, Controller_A~Controller_I, User_A~User_E),Depolarization rate of qubits in memory. probability
    dephase_rates : float
        An Array with 29 items (Repeater_A~Repeater_O, Controller_A~Controller_I, User_A,User_E),Dephasing rate of physical measurement instruction. probability
    qchannel_loss_init : float
        An Array with 32 items (Domain_A~Domian_I quantum channel,e.g 0~3 items means Controller_A->RepeaterA,B,C,UserA), Initial probability of losing a photon once it enters a quantum channel
    qchannel_loss_noisy : float
        An Array with 32 items (Domain_A~Domian_I quantum channel,e.g 0~3 items means Controller_A->RepeaterA,B,C,UserA), Photon survival probability per channel length [dB/km].
    Returns
    -------
    :class:`~netsquid.components.component.Component`
        A network component with nodes and channels as subcomponents.

    Notes
    -----
        This network is also used by the matching integration test.

    """
    ### globals may be effect other document to quote "Repeater_X","Controller_X", be notice ####
    name = globals()
    # Setup Physical Noisy
    ### if time_independent is True then the rate is a probability, if False(default), it is exponential depolarizing rate per unit time [Hz] ###
    for num in range(0,15):
        measure_noise_model = DephaseNoiseModel(dephase_rate=dephase_rates[num],time_independent=True)
        name['repeater_' + chr(num+65) + '_physical_instructions'] = [
            PhysicalInstruction(instr.INSTR_INIT, duration=3, parallel=True),
            PhysicalInstruction(instr.INSTR_H, duration=1, parallel=True),
            PhysicalInstruction(instr.INSTR_X, duration=1, parallel=True, quantum_noise_model=measure_noise_model),
            PhysicalInstruction(instr.INSTR_Z, duration=1, parallel=True, quantum_noise_model=measure_noise_model),
            PhysicalInstruction(instr.INSTR_S, duration=1, parallel=True),
            PhysicalInstruction(instr.INSTR_SWAP, duration=2),
            PhysicalInstruction(instr.INSTR_MEASURE_BELL, duration=2, paraller=False, quantum_noise_model=measure_noise_model )
        ]
        name['repeater_' + chr(num+65)+ '_memory_noise_model'] = DepolarNoiseModel(depolar_rate=depolar_rates[num], time_independent=True)
    for num in range(15,24):
        measure_noise_model = DephaseNoiseModel(dephase_rate=dephase_rates[num],time_independent=True)
        name['controller_' + chr(num+50) + '_physical_instructions'] = [
            PhysicalInstruction(instr.INSTR_INIT, duration=3, parallel=True),
            PhysicalInstruction(instr.INSTR_H, duration=1, parallel=True),
            PhysicalInstruction(instr.INSTR_X, duration=1, parallel=True, quantum_noise_model=measure_noise_model),
            PhysicalInstruction(instr.INSTR_Z, duration=1, parallel=True, quantum_noise_model=measure_noise_model),
            PhysicalInstruction(instr.INSTR_S, duration=1, parallel=True),
            PhysicalInstruction(instr.INSTR_SWAP, duration=2),
            PhysicalInstruction(instr.INSTR_MEASURE_BELL, duration=2, paraller=False, quantum_noise_model=measure_noise_model )
        ]
        name['controller_' + chr(num+50)+ '_memory_noise_model'] = DepolarNoiseModel(depolar_rate=depolar_rates[num], time_independent=True)
    for num in range(24,29):
        measure_noise_model = DephaseNoiseModel(dephase_rate=dephase_rates[num],time_independent=True)
        name['user_' + chr(num+41) + '_physical_instructions'] = [
            PhysicalInstruction(instr.INSTR_INIT, duration=3, parallel=True),
            PhysicalInstruction(instr.INSTR_H, duration=1, parallel=True),
            PhysicalInstruction(instr.INSTR_X, duration=1, parallel=True, quantum_noise_model=measure_noise_model),
            PhysicalInstruction(instr.INSTR_Z, duration=1, parallel=True, quantum_noise_model=measure_noise_model),
            PhysicalInstruction(instr.INSTR_S, duration=1, parallel=True),
            PhysicalInstruction(instr.INSTR_SWAP, duration=2),
            PhysicalInstruction(instr.INSTR_MEASURE_BELL, duration=2, paraller=False, quantum_noise_model=measure_noise_model )
        ]
        name['user_' + chr(num+41)+ '_memory_noise_model'] = DepolarNoiseModel(depolar_rate=depolar_rates[num], time_independent=True)

    # Setup nodes:
    network = Network("Cellura_Network")

    ### Define Domian_X to store device in Domain ###
    for i in range(65,74):
        name['Domain_' + chr(i) + '_instance'] = []
        name['Domain_' + chr(i) + '_instance_name'] = []

    ### Define Repeater from Repeater_A ~ Repeater_O###
    for i in range(65,80):
        repeater_name = "Repeater_"+chr(i)
        qmemory_name = repeater_name + "_QMemory"
        name[repeater_name] = network.add_node(repeater_name)
        name[repeater_name].add_subcomponent(QuantumProcessor(
                                             qmemory_name, num_mem_positions, memory_noise_models=[name['repeater_' + chr(i) + '_memory_noise_model']] * num_mem_positions,
                                             phys_instructions=name['repeater_' + chr(i) + '_physical_instructions'],fallback_to_nonphysical=False))
        if chr(i) in ["A", "B", "C"]:
            Domain_A_instance.append(name[repeater_name])
            Domain_A_instance_name.append(repeater_name)
        if chr(i) in ["C", "D", "E"]:
            Domain_B_instance.append(name[repeater_name])
            Domain_B_instance_name.append(repeater_name)
        if chr(i) in ["B", "E", "F"]:
            Domain_C_instance.append(name[repeater_name])
            Domain_C_instance_name.append(repeater_name)
        if chr(i) in ["D", "G", "H"]:
            Domain_D_instance.append(name[repeater_name])
            Domain_D_instance_name.append(repeater_name)
        if chr(i) in ["E", "H", "I"]:
            Domain_E_instance.append(name[repeater_name])
            Domain_E_instance_name.append(repeater_name)
        if chr(i) in ["F", "I", "J"]:
            Domain_F_instance.append(name[repeater_name])
            Domain_F_instance_name.append(repeater_name)
        if chr(i) in ["H", "K", "L"]:
            Domain_G_instance.append(name[repeater_name])
            Domain_G_instance_name.append(repeater_name)
        if chr(i) in ["I", "L", "M"]:
            Domain_H_instance.append(name[repeater_name])
            Domain_H_instance_name.append(repeater_name)
        if chr(i) in ["L", "N", "O"]:
            Domain_I_instance.append(name[repeater_name])
            Domain_I_instance_name.append(repeater_name)
    ### Define Cetral_Controller ###
    Central_Controller = network.add_node("Central_Controller")

    ### Define User ###
    User_A = network.add_node("User_A")
    User_B = network.add_node("User_B")
    User_C = network.add_node("User_C")
    User_D = network.add_node("User_D")
    User_E = network.add_node("User_E")
    User_A.add_subcomponent(QuantumProcessor(
                            "User_A_QMemory", num_mem_positions, memory_noise_models=[user_A_memory_noise_model] * num_mem_positions,
                             phys_instructions=user_A_physical_instructions,fallback_to_nonphysical=False))
    User_B.add_subcomponent(QuantumProcessor(
                            "User_B_QMemory", num_mem_positions, memory_noise_models=[user_B_memory_noise_model] * num_mem_positions,
                             phys_instructions=user_B_physical_instructions,fallback_to_nonphysical=False))
    User_C.add_subcomponent(QuantumProcessor(
                            "User_C_QMemory", num_mem_positions, memory_noise_models=[user_C_memory_noise_model] * num_mem_positions,
                             phys_instructions=user_C_physical_instructions,fallback_to_nonphysical=False))
    User_D.add_subcomponent(QuantumProcessor(
                            "User_D_QMemory", num_mem_positions, memory_noise_models=[user_D_memory_noise_model] * num_mem_positions,
                             phys_instructions=user_D_physical_instructions,fallback_to_nonphysical=False))
    User_E.add_subcomponent(QuantumProcessor(
                            "User_E_QMemory", num_mem_positions, memory_noise_models=[user_E_memory_noise_model] * num_mem_positions,
                             phys_instructions=user_E_physical_instructions,fallback_to_nonphysical=False))
    Domain_A_instance.append(User_A)
    Domain_A_instance_name.append("User_A")
    Domain_B_instance.append(User_E)
    Domain_B_instance_name.append("User_E")
    Domain_E_instance.append(User_D)
    Domain_E_instance_name.append("User_D")
    Domain_H_instance.append(User_C)
    Domain_H_instance_name.append("User_C")
    Domain_I_instance.append(User_B)
    Domain_I_instance_name.append("User_B")

    ### Define Controller from Controller_A ~ Controller_I ###
    for i in range(65,74):
        controller_name = "Controller_"+chr(i)
        qmemory_name = controller_name + "_QMemory"
        name[controller_name] = network.add_node(controller_name)
        name[controller_name].add_subcomponent(QuantumProcessor(
                                               qmemory_name, num_mem_positions, memory_noise_models=[name['controller_' + chr(i) + '_memory_noise_model']] * num_mem_positions,
                                                phys_instructions=name['controller_' + chr(i) + '_physical_instructions'],fallback_to_nonphysical=False))
        for j in range(len(name['Domain_' + chr(i) + '_instance_name'])):
            for h in range(j+1, len(name['Domain_' + chr(i) + '_instance_name'])):
                qsource_name = controller_name + "_" + name['Domain_' + chr(i) + '_instance_name'][j] \
                                + "_" + name['Domain_' + chr(i) + '_instance_name'][h] + "_" + "QSource"
                name[controller_name].add_subcomponent(QSource(qsource_name, state_sampler=StateSampler([ks.b00]),
                                                       num_ports=2, status=SourceStatus.EXTERNAL,
                                                       models={"emission_delay_model": FixedDelayModel(delay=prep_delay)}))


    ### Setup classical connections ###
    for i in range(65,74):
        controller_name = "Controller_"+chr(i)
        cconnection_name = "CetralController_" + controller_name + "_CConnection"
        cchannel_in_name = "CChannel_" + "CetralController" + "->" + controller_name
        cchannel_out_name = "CChannel" + controller_name + "->" + "CetralController"
        name[cconnection_name] = DirectConnection( cconnection_name,
                                                  ClassicalChannel(cchannel_in_name, length=node_distance,
                                                                  models={"delay_model": FibreDelayModel(c=200e3)}),
                                                  ClassicalChannel(cchannel_out_name, length=node_distance,
                                                                  models={"delay_model": FibreDelayModel(c=200e3)}))
        network.add_connection(Central_Controller, name[controller_name], connection=name[cconnection_name])
        for j in range(len(name['Domain_' + chr(i) + '_instance_name'])):
            cconnection_name = controller_name + "_" + name['Domain_' + chr(i) + '_instance_name'][j] + "_CConnection"
            cchannel_in_name = "CChannel_" + name['Domain_' + chr(i) + '_instance_name'][j] + "->" + controller_name
            cchannel_out_name = "CChannel_" + controller_name + "->" + name['Domain_' + chr(i) + '_instance_name'][j]
            name[cconnection_name] = DirectConnection( cconnection_name,
                                                  ClassicalChannel(cchannel_in_name, length=node_distance,
                                                                  models={"delay_model": FibreDelayModel(c=200e3)}),
                                                  ClassicalChannel(cchannel_out_name, length=node_distance,
                                                                  models={"delay_model": FibreDelayModel(c=200e3)}))
            network.add_connection(name['Domain_' + chr(i) + '_instance'][j], name[controller_name], connection=name[cconnection_name])
    ### Create and connect quantum channel, define port name, setup instance quantum port in ###
    ### one-way connection！！！ channel_to means RA->CA, channel_from means RA<-CA  ######
    ### qin0 in Instance is for receive qubit. And then it will be swap to mem 1 or mem 2 in EntangledDistributionProtocol ###
    num = 0
    for i in range(65,74):
        controller_name = "Controller_"+chr(i)
        for j in range(len(name['Domain_' + chr(i) + '_instance_name'])):
            qchannel_name = "QChannel_" + controller_name + "_" + name['Domain_' + chr(i) + '_instance_name'][j]
            name[qchannel_name] = QuantumChannel(qchannel_name, length=node_distance, models={"delay_model": FibreDelayModel(c=200e3),
                                  "quantum_loss_model": FibreLossModel(qchannel_loss_init[num], qchannel_loss_noisy[num])})
            controller_port_name = "port_name_" + controller_name + "_" + name['Domain_' + chr(i) + '_instance_name'][j]
            instance_port_name = "port_name_" + name['Domain_' + chr(i) + '_instance_name'][j] + "_" + controller_name
            name[instance_port_name],name[controller_port_name] = network.add_connection(
                                                                   name['Domain_' + chr(i) + '_instance'][j], name[controller_name],
                                                                   channel_from=name[qchannel_name], label="quantum")
            name['Domain_' + chr(i) + '_instance'][j].ports[name[instance_port_name]].forward_input(
                                                                   name['Domain_' + chr(i) + '_instance'][j].qmemory.ports["qin0"])
            num += 1
    ### Setup Controller quantum port out ###
    for i in range(65,74):
        controller_name = "Controller_"+chr(i)
        for j in range(len(name['Domain_' + chr(i) + '_instance_name'])):
            for h in range(j+1, len(name['Domain_' + chr(i) + '_instance_name'])):
                qsource_name = controller_name + "_" + name['Domain_' + chr(i) + '_instance_name'][j] \
                                + "_" + name['Domain_' + chr(i) + '_instance_name'][h] + "_" + "QSource"
                controller_port_name_1 = "port_name_" + controller_name + "_" + name['Domain_' + chr(i) + '_instance_name'][j]
                controller_port_name_2 = "port_name_" + controller_name + "_" + name['Domain_' + chr(i) + '_instance_name'][h]
                name[controller_name].subcomponents[qsource_name].ports["qout0"].forward_output(
                         name[controller_name].ports[name[controller_port_name_1]])
                name[controller_name].subcomponents[qsource_name].ports["qout1"].forward_output(
                         name[controller_name].ports[name[controller_port_name_2]])
    ### return network ###
    return network


#depolar_rates = [0,0.05,0.04,0.005,0.04,0.05,0,0.005,0.04,0,0,0.04,0,0,0,0,0,0,0,0,0,0,0,0,0.04,0.04,0.04,0.04,0.04]
#dephase_rates = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#qchannel_loss_init = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#qchannel_loss_noisy = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#network = Centralized_Cellular_Network_setup(depolar_rates=depolar_rates,dephase_rates=dephase_rates,qchannel_loss_init=qchannel_loss_init,qchannel_loss_noisy=qchannel_loss_noisy)
#for conn in network.connections.values():
#    print(conn)
#for node in network.nodes.values():
#    print(node.name, node.qmemory)
