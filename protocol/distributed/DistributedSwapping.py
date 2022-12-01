import netsquid as ns
from netsquid.components import instructions as instr
from netsquid.protocols.nodeprotocols import LocalProtocol, NodeProtocol
from netsquid.protocols.protocol import Signals
from netsquid.components.component import Message, Port
from netsquid.nodes.node import Node
from netsquid.components.qprogram import QuantumProgram
from netsquid.qubits import ketstates as ks
from pydynaa import EventExpression


class DistributedSwapping(NodeProtocol):
    """Entangles two nodes given both are entangled with an intermediary midpoint node.

    Parameters
    ----------
    node : :py:class:`~netsquid.nodes.node.Node`
        Node to run the repeater, localcontroller, centralcontroller or corrector protocol on.
    port : :py:class:`~netsquid.components.component.Port`
        Port to use for classical IO communication between the repeater, localcontroller and corrector node.
    portout : :py:class:`~netsquid.components.component.Port`
        Port to use for classical IO communication in the localcontroller.
    role : "repeater", "localcontroller", or "corrector"
        Whether this protocol should act as repeater, localcontroller, centralcontroller or corrector. All are needed.
    start_expression : :class:`~pydynaa.EventExpression`
        EventExpression node should wait for before starting.
        The EventExpression should have a protocol as source, this protocol should
        signal the quantum memory position of the qubit. In the case of a midpoint
        repeater it requires two such protocols, both signalling a quantum memory
        position
    name : str or None, optional
        Name of protocol. If None a default name is set.
    repeater_mem_posA repeater_mem_posB : int , required for role repeater
        repeater mem to do swapping
    corrector_mem_pos : int, required for role corrector
         corrector mem to do correction


    """
    MSG_HEADER = "repeater:corrections"

    def __init__(self, node, port, role, repeater_mem_posA=None, repeater_mem_posB=None, corrector_mem_pos=None, start_expression=None, name=None):
        if role.lower() not in ["repeater", "corrector"]:
            raise ValueError
        self.role = role.lower()
        name = name if name else "Node({}, {})".format(node.name, role)
        super().__init__(node=node, name=name)
        self.start_expression = start_expression
        self.port = port
        self._repeater_mem_posA = repeater_mem_posA
        self._repeater_mem_posB = repeater_mem_posB
        # Used by corrector:
        self._correction = None
        self._corrector_mem_pos = corrector_mem_pos

    @property
    def start_expression(self):
        return self._start_expression

    @start_expression.setter
    def start_expression(self, value):
        if value:
            if not isinstance(value, EventExpression):
                raise TypeError("Start expression of the corrector role should be an "
                                "event expression")
            elif self.role == "repeater" and value.type != EventExpression.AND:
                raise TypeError("Start expression of the repeater role should be an "
                                "expression that returns two values.")
        self._start_expression = value

    def run(self):
        if self.role == "repeater":
            yield from self._run_repeater()
        elif self.role == "corrector":
            yield from self._run_corrector()

    def _run_repeater(self):
        # Run bell state measurement program
        measure_program = BellMeasurementProgram()
        yield self.node.qmemory.execute_program(measure_program, [self._repeater_mem_posA, self._repeater_mem_posB])
        m, = measure_program.output["BellStateIndex"]
        # Send measurement to corrector
        self.port.tx_output(Message([m], header=self.MSG_HEADER))
        self.send_signal(Signals.SUCCESS)
        print("Node {} exec swapping success".format(self.name))

    def _run_corrector(self):
        # Run loop for endpoint corrector node
        yield self.await_port_input(self.port)
        cmessage = self.port.rx_input(header=self.MSG_HEADER)
        if cmessage:
            self._correction = cmessage.items
        if self._correction is not None:
            yield from self._do_corrections()

    def _do_corrections(self):
        m = self._correction[0]
        if self.node.qmemory.busy:
            yield self.await_program(self.node.qmemory)
        if m == ks.BellIndex.B01 or m == ks.BellIndex.B11:
            self.node.qmemory.execute_instruction(instr.INSTR_X, [self._corrector_mem_pos])
            if self.node.qmemory.busy:
                yield self.await_program(self.node.qmemory)
        if m == ks.BellIndex.B10 or m == ks.BellIndex.B11:
            self.node.qmemory.execute_instruction(instr.INSTR_Z, [self._corrector_mem_pos])
            if self.node.qmemory.busy:
                yield self.await_program(self.node.qmemory)
        self.send_signal(Signals.SUCCESS, self._corrector_mem_pos)
        print("Node {} do correction success".format(self.name))

    @property
    def is_connected(self):
        if not self.check_assigned([self.node], Node):
            return False
        if not self.check_assigned([self.port], Port):
            return False
        if self.role == "repeater" and (self.node.qmemory is None or
                                        self.node.qmemory.num_positions < 2):
            return False
        if self.role == "corrector" and (self.node.qmemory is None or
                                         self.node.qmemory.num_positions < 1):
            return False
        return True

class BellMeasurementProgram(QuantumProgram):
    """Program to perform a Bell measurement on two qubits.

    Measurement results are stored in output key "BellStateIndex""

    """
    default_num_qubits = 2

    def program(self):
        q1, q2 = self.get_qubit_indices(2)
        ### inplace = True means q1,q2 still exist, inplace=False means remove q1,q2 after Bell Measurement###
        self.apply(instr.INSTR_MEASURE_BELL, [q1, q2], inplace=False,
                   output_key="BellStateIndex")
        yield self.run()
