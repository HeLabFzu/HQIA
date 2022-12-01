import netsquid as ns
from netsquid.protocols.nodeprotocols import NodeProtocol
from netsquid.protocols.protocol import Signals
from netsquid.components.instructions import INSTR_SWAP
from netsquid.components.qsource import QSource, SourceStatus
from netsquid.components.qprocessor import QuantumProcessor
from netsquid.qubits import ketstates as ks
from netsquid.qubits.state_sampler import StateSampler
from netsquid.components.models.delaymodels import FixedDelayModel
from netsquid.components.qchannel import QuantumChannel
from netsquid.nodes.network import Network
from pydynaa import EventExpression

class CentralizedEntanglementDistribution(NodeProtocol):
    """Controller start to prepare entangment and distribute entanglement.

    Parameters
    ----------
    node : :class:`~netsquid.nodes.node.Node`
        Node to gennerate&distribute or receive Entanglement Pair
    role : "controller" or "repeater"
        Whether this protocol should act as a controller or a repeater. Both are needed.
    start_expression : :class:`~pydynaa.core.EventExpression` or None, optional
        Event Expression to wait for before starting entanglement round.
    input_mem_pos : int, optional
        Index of quantum memory position to expect incoming qubits on. Default is 0.
    store_mem_pos : int required
        Index of quantum memory position to store incoming qubits. Default is 0.
    num_pairs : int, optional
        Number of entanglement pairs to create per round. only 1 is allowed
        will be stored on available memory positions.
    name : str or None, optional
        Name of protocol. If None a default name is set.

    """

    def __init__(self, node, role, store_mem_pos=None, qsource_name=None, start_expression=None, input_mem_pos=0, num_pairs=1, name=None):
        if role.lower() not in ["controller", "repeater", "user"]:
            raise ValueError
        self._is_controller = role.lower() == "controller"
        name = name if name else "({}, {})".format(node.name, role)
        super().__init__(node=node,name=name)
        if start_expression is not None and not isinstance(start_expression, EventExpression):
            raise TypeError("Start expression should be a {}, not a {}".format(EventExpression, type(start_expression)))
        self.start_expression = start_expression
        self._store_mem_pos = store_mem_pos
        self._qsource_name = qsource_name
        self._num_pairs = num_pairs
        # Claim input memory position:
        if not self._is_controller:
            if self.node.qmemory is None:
                 raise ValueError("Node {} does not have a quantum memory assigned.".format(self.node))
            self._input_mem_pos = input_mem_pos
            self._qmem_input_port = self.node.qmemory.ports["qin{}".format(self._input_mem_pos)]
            self.node.qmemory.mem_positions[self._input_mem_pos].in_use = True

    def start(self):
        self.entangled_pairs = 0  # counter
        # Call parent start method
        super().start()

    def stop(self):
        # Unclaim used memory positions:
        if not self._is_controller:
            self.node.qmemory.mem_positions[self._input_mem_pos].in_use = False
        # Call parent stop method
        super().stop()

    def run(self):
        if self.start_expression is not None:
            yield self.start_expression
        if self._is_controller:
            self.node.subcomponents[self._qsource_name].trigger()
            self.entangled_pairs += 1
            print("Node {} distribute entanglement pair complete".format(self.name))
           
        else:
            yield self.await_port_input(self._qmem_input_port)
            self.node.qmemory.execute_instruction(
                INSTR_SWAP, [self._input_mem_pos, self._store_mem_pos])
            if self.node.qmemory.busy:
                yield self.await_program(self.node.qmemory)
            self.entangled_pairs += 1
            self.send_signal(Signals.SUCCESS, self._store_mem_pos)
            print("Node {} mem {} received qubit".format(self.name, self._store_mem_pos))
    def check(self):
        if not self._is_controller and self.get_signal_result(Signals.SUCCESS) is None:
            return False
        else:
            return True

    @property
    def is_connected(self):
        if not self._is_controller:
            if not super().is_connected:
                return False
            if self.node.qmemory is None:
                return False
            if self._store_mem_pos is None:
                return False
        if self._is_controller:
            if self._qsource_name is None:
                return False
        return True
