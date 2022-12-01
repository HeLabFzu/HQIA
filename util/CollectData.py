import netsquid as ns
from netsquid.protocols.protocol import Signals

def collect_distribution_data(evexpr):
     protocol = evexpr.triggered_events[-1].source
     fidelity = protocol.getresult()
     return {"fidelity": fidelity}

def collect_fidelity_data(evexpr):
    protocol = evexpr.triggered_events[-1].source
    mem_pos = protocol.get_signal_result(Signals.SUCCESS)
    qubit, = protocol.get_dst_user_node().qmemory.peek(mem_pos)
    fidelity = ns.qubits.fidelity(qubit, ns.y0, squared=True)
    return {"fidelity": fidelity}
