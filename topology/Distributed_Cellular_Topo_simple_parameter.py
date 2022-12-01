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


def Distributed_Cellular_Network_setup(prep_delay=0, num_mem_positions=6, node_distance=100,depolar_rate=0,dephase_rate=0,
                         qchannel_loss_init=0, qchannel_loss_noisy=0):
    """
    Create an example network for use with the entangling nodes protocol.

    Parameters
    ----------
    prep_delay : float, optional
        Delay used in the source in this network. Default is 5 [ns].
    num_mem_positions : int
        Number of memory positions on both nodes in the network. Default is 3.
    depolar_rate : float
        Depolarization rate of qubits in memory. probability
    dephase_rate : float
        Dephasing rate of physical measurement instruction. probability
    qchannel_loss_init : float
         Initial probability of losing a photon once it enters a channel
    qchannel_loss_noisy : float
         Photon survival probability per channel length [dB/km].
    Returns
    -------
    :class:`~netsquid.components.component.Component`
        A network component with nodes and channels as subcomponents.

    Notes
    -----
        This network is also used by the matching integration test.

    """
    # Setup Physical Noisy
    ### if time_independent is True then the rate is a probability, if False(default), it is exponential depolarizing rate per unit time [Hz] ###
    measure_noise_model = DephaseNoiseModel(dephase_rate=dephase_rate,time_independent=True)
    physical_instructions = [
        PhysicalInstruction(instr.INSTR_INIT, duration=3, parallel=True),
        PhysicalInstruction(instr.INSTR_H, duration=1, parallel=True),
        PhysicalInstruction(instr.INSTR_X, duration=1, parallel=True, quantum_noise_model=measure_noise_model),
        PhysicalInstruction(instr.INSTR_Z, duration=1, parallel=True, quantum_noise_model=measure_noise_model),
        PhysicalInstruction(instr.INSTR_S, duration=1, parallel=True),
        PhysicalInstruction(instr.INSTR_SWAP, duration=2),
        PhysicalInstruction(instr.INSTR_MEASURE_BELL, duration=2, paraller=False, quantum_noise_model=measure_noise_model )
    ]
    memory_noise_model = DepolarNoiseModel(depolar_rate=depolar_rate, time_independent=True)

    # Setup nodes:
    network = Network("Cellura_Network")

    name = globals()

    ### Replace Controller A~B with Repeater P~X, Define Repeater P~X related_instance array to store device ###
    for i in range(80,89):
        name['Repeater_' + chr(i) + '_related_instance'] = []
        name['Repeater_' + chr(i) + '_related_instance_name'] = []

    ### Define Repeater from Repeater_A ~ Repeater_O###
    for i in range(65,80):
        repeater_name = "Repeater_"+chr(i)
        qmemory_name = repeater_name + "_QMemory"
        name[repeater_name] = network.add_node(repeater_name)
        name[repeater_name].add_subcomponent(QuantumProcessor(
                                             qmemory_name, num_mem_positions, memory_noise_models=[memory_noise_model] * 6,
                                             phys_instructions=physical_instructions,fallback_to_nonphysical=False))
        if chr(i) in ["A", "B", "C"]:
            Repeater_P_related_instance.append(name[repeater_name])
            Repeater_P_related_instance_name.append(repeater_name)
        if chr(i) in ["C", "D", "E"]:
            Repeater_Q_related_instance.append(name[repeater_name])
            Repeater_Q_related_instance_name.append(repeater_name)
        if chr(i) in ["B", "E", "F"]:
            Repeater_R_related_instance.append(name[repeater_name])
            Repeater_R_related_instance_name.append(repeater_name)
        if chr(i) in ["D", "G", "H"]:
            Repeater_S_related_instance.append(name[repeater_name])
            Repeater_S_related_instance_name.append(repeater_name)
        if chr(i) in ["E", "H", "I"]:
            Repeater_T_related_instance.append(name[repeater_name])
            Repeater_T_related_instance_name.append(repeater_name)
        if chr(i) in ["F", "I", "J"]:
            Repeater_U_related_instance.append(name[repeater_name])
            Repeater_U_related_instance_name.append(repeater_name)
        if chr(i) in ["H", "K", "L"]:
            Repeater_V_related_instance.append(name[repeater_name])
            Repeater_V_related_instance_name.append(repeater_name)
        if chr(i) in ["I", "L", "M"]:
            Repeater_W_related_instance.append(name[repeater_name])
            Repeater_W_related_instance_name.append(repeater_name)
        if chr(i) in ["L", "N", "O"]:
            Repeater_X_related_instance.append(name[repeater_name])
            Repeater_X_related_instance_name.append(repeater_name)

    ### Define User ###
    User_A = network.add_node("User_A")
    User_B = network.add_node("User_B")
    User_C = network.add_node("User_C")
    User_D = network.add_node("User_D")
    User_E = network.add_node("User_E")
    User_A.add_subcomponent(QuantumProcessor(
                            "User_A_QMemory", num_mem_positions, memory_noise_models=[memory_noise_model] * 6,
                             phys_instructions=physical_instructions,fallback_to_nonphysical=False))
    User_B.add_subcomponent(QuantumProcessor(
                            "User_B_QMemory", num_mem_positions, memory_noise_models=[memory_noise_model] * 6,
                             phys_instructions=physical_instructions,fallback_to_nonphysical=False))
    User_C.add_subcomponent(QuantumProcessor(
                            "User_C_QMemory", num_mem_positions, memory_noise_models=[memory_noise_model] * 6,
                             phys_instructions=physical_instructions,fallback_to_nonphysical=False))
    User_D.add_subcomponent(QuantumProcessor(
                            "User_D_QMemory", num_mem_positions, memory_noise_models=[memory_noise_model] * 6,
                             phys_instructions=physical_instructions,fallback_to_nonphysical=False))
    User_E.add_subcomponent(QuantumProcessor(
                            "User_E_QMemory", num_mem_positions, memory_noise_models=[memory_noise_model] * 6,
                             phys_instructions=physical_instructions,fallback_to_nonphysical=False))
    Repeater_P_related_instance.append(User_A)
    Repeater_P_related_instance_name.append("User_A")
    Repeater_Q_related_instance.append(User_E)
    Repeater_Q_related_instance_name.append("User_E")
    Repeater_T_related_instance.append(User_D)
    Repeater_T_related_instance_name.append("User_D")
    Repeater_W_related_instance.append(User_C)
    Repeater_W_related_instance_name.append("User_C")
    Repeater_X_related_instance.append(User_B)
    Repeater_X_related_instance_name.append("User_B")
    ### User_C~F need defined where to locate ###

    ### Define Repeater_P~X to replace Controller for traditional topo  ###
    for i in range(80,89):
        repeater_name = "Repeater_"+chr(i)
        qmemory_name = repeater_name + "_QMemory"
        name[repeater_name] = network.add_node(repeater_name)
        name[repeater_name].add_subcomponent(QuantumProcessor(
                                               qmemory_name, num_mem_positions, memory_noise_models=[memory_noise_model] * 6,
                                                phys_instructions=physical_instructions,fallback_to_nonphysical=False))
        ### define topo QSource in all repeater ###
        for j in range(len(name['Repeater_' + chr(i) + '_related_instance_name'])):
            qsource_name_1 = repeater_name + "_" + name['Repeater_' + chr(i) + '_related_instance_name'][j] + "_" + "QSource"
            name[repeater_name].add_subcomponent(QSource(qsource_name_1, state_sampler=StateSampler([ks.b00]),
                                                   num_ports=2, status=SourceStatus.EXTERNAL,
                                                   models={"emission_delay_model": FixedDelayModel(delay=prep_delay)}))
            qsource_name_2 =  name['Repeater_' + chr(i) + '_related_instance_name'][j] + "_" + repeater_name + "_" + "QSource"
            name['Repeater_' + chr(i) + '_related_instance'][j].add_subcomponent(QSource(qsource_name_2, state_sampler=StateSampler([ks.b00]),
                                                   num_ports=2, status=SourceStatus.EXTERNAL,
                                                   models={"emission_delay_model": FixedDelayModel(delay=prep_delay)}))

    
    ### Setup classical connections ###
    for i in range(80,89):
        repeater_name = "Repeater_"+chr(i)
        for j in range(len(name['Repeater_' + chr(i) + '_related_instance_name'])):
            cconnection_name = repeater_name + "_" + name['Repeater_' + chr(i) + '_related_instance_name'][j] + "_CConnection"
            cchannel_in_name = "CChannel_" + name['Repeater_' + chr(i) + '_related_instance_name'][j] + "->" + repeater_name
            cchannel_out_name = "CChannel_" + repeater_name + "->" + name['Repeater_' + chr(i) + '_related_instance_name'][j]
            name[cconnection_name] = DirectConnection( cconnection_name,
                                                  ClassicalChannel(cchannel_in_name, length=node_distance,
                                                                  models={"delay_model": FibreDelayModel(c=200e3)}),
                                                  ClassicalChannel(cchannel_out_name, length=node_distance,
                                                                  models={"delay_model": FibreDelayModel(c=200e3)}))
            network.add_connection(name['Repeater_' + chr(i) + '_related_instance'][j], name[repeater_name], connection=name[cconnection_name])
    ### Create and connect quantum channel, define port name, setup instance quantum port in ###
    ### qin0~3 in instance is for receive qubit. And then it will be swap to mem 4 or mem 5 in TraditionalEntangledDistributionProtocol ###
    for i in range(80,89):
        repeater_name = "Repeater_"+chr(i)
        for j in range(len(name['Repeater_' + chr(i) + '_related_instance_name'])):
            qchannel_name_1 = "QChannel_" + repeater_name + "_" + name['Repeater_' + chr(i) + '_related_instance_name'][j]
            name[qchannel_name_1] = QuantumChannel(qchannel_name_1, length=node_distance, models={"delay_model": FibreDelayModel(c=200e3),
                                  "quantum_loss_model": FibreLossModel(qchannel_loss_init, qchannel_loss_noisy)})
            qchannel_name_2 = "QChannel_" +  name['Repeater_' + chr(i) + '_related_instance_name'][j] + "_" + repeater_name
            name[qchannel_name_2] = QuantumChannel(qchannel_name_2, length=node_distance, models={"delay_model": FibreDelayModel(c=200e3),
                                  "quantum_loss_model": FibreLossModel(qchannel_loss_init, qchannel_loss_noisy)})
            core_repeater_port_name = "port_name_" + repeater_name + "_" + name['Repeater_' + chr(i) + '_related_instance_name'][j]
            instance_port_name = "port_name_" + name['Repeater_' + chr(i) + '_related_instance_name'][j] + "_" + repeater_name
            name[instance_port_name],name[core_repeater_port_name] = network.add_connection(
                                                                   name['Repeater_' + chr(i) + '_related_instance'][j], name[repeater_name],
                                                                   channel_to=name[qchannel_name_2],channel_from=name[qchannel_name_1], label="quantum")
            name['Repeater_' + chr(i) + '_related_instance'][j].ports[name[instance_port_name]].forward_input(
                                                                   name['Repeater_' + chr(i) + '_related_instance'][j].qmemory.ports["qin0"])
            name[repeater_name].ports[name[core_repeater_port_name]].forward_input(
                                                                   name[repeater_name].qmemory.ports["qin0"])
    ### Setup repeater quantum port out ###
    for i in range(80,89):
        repeater_name = "Repeater_"+chr(i)
        for j in range(len(name['Repeater_' + chr(i) + '_related_instance_name'])):
            qsource_name_1 = repeater_name + "_" + name['Repeater_' + chr(i) + '_related_instance_name'][j] + "_" + "QSource"
            qsource_name_2 = name['Repeater_' + chr(i) + '_related_instance_name'][j] + "_" + repeater_name + "_" + "QSource"
            core_repeater_port_name = "port_name_" + repeater_name + "_" + name['Repeater_' + chr(i) + '_related_instance_name'][j]
            instance_port_name = "port_name_" + name['Repeater_' + chr(i) + '_related_instance_name'][j] + "_" + repeater_name
            name[repeater_name].subcomponents[qsource_name_1].ports["qout0"].forward_output(
                     name[repeater_name].ports[name[core_repeater_port_name]])
            name[repeater_name].subcomponents[qsource_name_1].ports["qout1"].connect(
                     name[repeater_name].qmemory.ports["qin" + str(j)])
            name['Repeater_' + chr(i) + '_related_instance'][j].subcomponents[qsource_name_2].ports["qout0"].forward_output(
                     name['Repeater_' + chr(i) + '_related_instance'][j].ports[name[instance_port_name]])
            name['Repeater_' + chr(i) + '_related_instance'][j].subcomponents[qsource_name_2].ports["qout1"].connect(
                     name['Repeater_' + chr(i) + '_related_instance'][j].qmemory.ports["qin" + str(j)])
    ### return network ###
    return network




#network = Distributed_Cellular_Network_setup()
#for conn in network.connections.values():
#    print(conn)
#for node in network.nodes.values():
#    print(node.name, node.qmemory)

### 设置一下三组通信组的位置(保证三组hop数不同)，在传统拓扑中User被直接连接到替代Controller的Repeater上，这样更接近集中式拓扑的设置，对比起来有说服力###
