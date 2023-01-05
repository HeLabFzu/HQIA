import sys
sys.path.append("..")

import netsquid as ns
import pydynaa
import pandas

from protocol.centralized.CentralizedEntanglementDistribution import CentralizedEntanglementDistribution
from util.CollectData import collect_distribution_data
from util.CheckDistribution import CheckDistribution
from netsquid.util.datacollector import DataCollector
from netsquid.nodes import Node
from netsquid.components import  QuantumMemory, QuantumProcessor
from netsquid.nodes import Network
from netsquid.components.qsource import QSource, SourceStatus
from netsquid.components.qprocessor import QuantumProcessor, PhysicalInstruction
from netsquid.qubits import ketstates as ks
from netsquid.qubits.state_sampler import StateSampler
from netsquid.components.models.delaymodels import FixedDelayModel, FibreDelayModel
from netsquid.components import ClassicalChannel,QuantumChannel
from netsquid.components.models.qerrormodels import DepolarNoiseModel, DephaseNoiseModel,FibreLossModel
from netsquid.components import instructions as instr
from netsquid.protocols.protocol import Signals


"""
we design a two-node with 100km-qchannel distribution test to explore the channel noise limitation according the distribution success rate.
"""

def create_topo(qchannel_loss_noisy):
    network = Network("Simple_topo")
    node_a, node_b = network.add_nodes(["node_a", "node_b"])
    node_a.add_subcomponent(QuantumProcessor(
        "quantum_processor_a", num_positions=2, fallback_to_nonphysical=True,
        memory_noise_models=DepolarNoiseModel(0)))
    node_b.add_subcomponent(QuantumProcessor(
        "quantum_processor_b", num_positions=2, fallback_to_nonphysical=True,
        memory_noise_models=DepolarNoiseModel(0)))
    node_a.add_subcomponent(QSource("node_a_qsource", state_sampler=StateSampler([ks.b00]),
                                                       num_ports=2, status=SourceStatus.EXTERNAL,
                                                       models={"emission_delay_model": FixedDelayModel(delay=0)}))
    a_b_qchannel = QuantumChannel("node_a_to_node_B", length=100, models={"delay_model": FibreDelayModel(c=200e3),
                                  "quantum_loss_model": FibreLossModel(0, qchannel_loss_noisy)})
    node_b_port, node_a_port = network.add_connection(node_b, node_a, channel_from=a_b_qchannel, label="quantum")
    node_a.subcomponents["node_a_qsource"].ports["qout0"].forward_output(
        node_a.ports[node_a_port])
    node_a.subcomponents["node_a_qsource"].ports["qout1"].connect(
        node_a.qmemory.ports["qin0"])
    node_b.ports[node_b_port].forward_input(node_b.qmemory.ports["qin0"])
    return network

def define_network_and_protocol(qchannel_loss_noisy):
    network = create_topo(qchannel_loss_noisy)
    node_a = network.subcomponents["node_a"]
    node_b = network.subcomponents["node_b"]
    protocol_a = CentralizedEntanglementDistribution(node=node_a,role="controller",qsource_name="node_a_qsource")
    protocol_b = CentralizedEntanglementDistribution(node=node_b,role="user",store_mem_pos=1)

    return protocol_a,protocol_b

if __name__ == '__main__':
    fidelity_data = pandas.DataFrame()
    for qchannel_loss_noisy in [0,0.05,0.1,0.15,0.2,0.25,0.3]:
        n = 0
        while(n<100):
            Entanglement_Distribution_Signal = True
            protocol_a,protocol_b = define_network_and_protocol(qchannel_loss_noisy)
            protocol_a.start()
            protocol_b.start()
            ns.sim_run()
            if not protocol_b.check():
                Entanglement_Distribution_Signal = False
            check_distribution=CheckDistribution(Entanglement_Distribution_Signal)
            dc_distribution = DataCollector(collect_distribution_data)
            dc_distribution.collect_on(pydynaa.EventExpression(source=check_distribution,
                                                          event_type=Signals.SUCCESS.value))
            check_distribution.start()
            ns.sim_run()
            df=dc_distribution.dataframe
            df['qchannel_loss_noisy'] = qchannel_loss_noisy
            df['group'] = 1
            fidelity_data = fidelity_data.append(df)
            n = n+1
    data = pandas.crosstab(fidelity_data.group,fidelity_data.qchannel_loss_noisy,fidelity_data.fidelity,aggfunc='mean')
    print(data)



