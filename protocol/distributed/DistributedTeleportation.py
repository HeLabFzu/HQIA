from netsquid.components.qprogram import QuantumProgram
from netsquid.components import instructions as instr
from netsquid.protocols.nodeprotocols import NodeProtocol
from netsquid.components.component import Message, Port
from netsquid.protocols.protocol import Signals
from netsquid.qubits import ketstates as ks
import netsquid as ns



class BellMeasurementProgram(QuantumProgram):
    """Program to perform a Bell measurement on two qubits.

    Measurement results are stored in output keys "BellStateIndex"
    Parameters
    ----------
    target_qubit_mem_pos : :int
        mem_pos which store target_qubit in source User
    entangled_qubit_mem_pos : :int
        mem_pos which store entangled_qubit in source User
    """
    def __init__(self,target_qubit_mem_pos, entangled_qubit_mem_pos):
        self._target_qubit_mem_pos = target_qubit_mem_pos
        self._entangled_qubit_mem_pos = entangled_qubit_mem_pos
        super().__init__()
    def program(self):
        self.apply(instr.INSTR_MEASURE_BELL, [self._target_qubit_mem_pos, self._entangled_qubit_mem_pos], inplace=False,
                   output_key="BellStateIndex")
        yield self.run()

class BellMeasurementProtocol(NodeProtocol):
    """Protocol to perform a Bell measurement in source User.
    Parameters
    ----------
    node : :py:class:`~netsquid.nodes.node.Node`
        Src User Node to run the protocol on.
    target_qubit_mem_pos : :int
        mem_pos which store target_qubit in source User
    entangled_qubit_mem_pos : :int
        mem_pos which store entangled_qubit in source User
    result_trans_port : :py:class:`~netsquid.components.component.Port`
        Port to use for classical IO communication to trans BM result in source User
    """
    def __init__(self,node,target_qubit_mem_pos, entangled_qubit_mem_pos,result_trans_port):
        self._target_qubit_mem_pos = target_qubit_mem_pos
        self._entangled_qubit_mem_pos = entangled_qubit_mem_pos
        self._result_trans_port=result_trans_port
        super().__init__(node=node)
    def run(self):
        print("####### Start Teleportation Process###### ")
        measure_program = BellMeasurementProgram(target_qubit_mem_pos=self._target_qubit_mem_pos,
                                            entangled_qubit_mem_pos=self._entangled_qubit_mem_pos)
        yield self.node.qmemory.execute_program(measure_program)
        m, = measure_program.output["BellStateIndex"]
        self._result_trans_port.tx_output(Message([m]))
        self.send_signal(Signals.SUCCESS)
        print("Node {} Bell Measurement in mem{},mem{} success, already trans the result"
              .format(self.node.name, self._target_qubit_mem_pos,self._entangled_qubit_mem_pos))

class RepeaterTransResult(NodeProtocol):
    """Protocol to trans BM result in Local Controller and Central Controller
    Parameters
    ----------
    node : :py:class:`~netsquid.nodes.node.Node`
        Controller Node to run the protocol on.
    port_in : :py:class:`~netsquid.components.component.Port`
        Port to use for classical IO communication to receive BM result in controller.
    port_out : :py:class:`~netsquid.components.component.Port`
        Port to use for classical IO communication to trans BM result in controller.
    """
    def __init__(self,node,port_in,port_out):
        self._port_in = port_in
        self._port_out = port_out
        super().__init__(node=node)
    def run(self):
        yield self.await_port_input(self._port_in)
        m, = self._port_in.rx_input().items
        self._port_out.tx_output(Message([m]))
        self.send_signal(Signals.SUCCESS)
        print("Node {} trans Bell Measurement result success".format(self.node.name))

class CorrectionProtocol(NodeProtocol):
    """Protocol to trans BM result in Local Controller and Central Controller
    Parameters
    ----------
    node : :py:class:`~netsquid.nodes.node.Node`
        Dst User Node to run the protocol on.
    entangled_qubit_mem_pos : :int
        mem_pos which store entangled_qubit in dst User
    result_receive_port : :py:class:`~netsquid.components.component.Port`
        Port to use for classical IO communication to receive BM result in dst User.
    """
    def __init__(self,node,entangled_qubit_mem_pos,result_receive_port):
        self._entangled_qubit_mem_pos = entangled_qubit_mem_pos
        self._result_receive_port = result_receive_port
        super().__init__(node=node)
    def run(self):
        yield self.await_port_input(self._result_receive_port)
        m, = self._result_receive_port.rx_input().items
        # Do corrections (blocking)
        if self.node.qmemory.busy:
            yield self.await_program(self.node.qmemory)
        if m == ks.BellIndex.B01 or m == ks.BellIndex.B11:
            self.node.qmemory.execute_instruction(instr.INSTR_X, [self._entangled_qubit_mem_pos])
            if self.node.qmemory.busy:
                yield self.await_program(self.node.qmemory)
        if m == ks.BellIndex.B10 or m == ks.BellIndex.B11:
            self.node.qmemory.execute_instruction(instr.INSTR_Z, [self._entangled_qubit_mem_pos])
            if self.node.qmemory.busy:
                yield self.await_program(self.node.qmemory)
        self.send_signal(Signals.SUCCESS,self._entangled_qubit_mem_pos)
        print("Node {} Correction Done".format(self.node.name))
        print("####### Complete Teleportation Process###### ")

class DistributedTeleportation(NodeProtocol):
    """Protocol to trans BM result in Local Controller and Central Controller
    Parameters
    ----------
    src_user_node : :py:class:`~netsquid.nodes.node.Node`
        src User Node to run teleportation.
    dst_user_node : :py:class:`~netsquid.nodes.node.Node`
        dst User Node to run teleportation.
    src_user_controller : :py:class:`~netsquid.nodes.node.Node`
        the Local Controller Node which belong to src User Node to trans BM result.
    dst_user_controller : :py:class:`~netsquid.nodes.node.Node`
        the Local Controller Node which belong to dst User Node to trans BM result.
    central_controller : :py:class:`~netsquid.nodes.node.Node`
        Central Controller to trans BM result.
    src_target_qubit_mem_pos : :int
        mem_pos which store target_qubit in src User
    src_entangled_qubit_mem_pos : :int
        mem_pos which store entangled_qubit in src User
    dst_entangled_qubit_mem_pos : :int
        mem_pos which store entangled_qubit in dst User
    """
    def __init__(self, path, src_target_qubit_mem_pos):
        self.path = path
        self._src_user_node = path[0].node
        self._dst_user_node = path[len(path)-1].node
        self._src_target_qubit_mem_pos = src_target_qubit_mem_pos
        self._src_entangled_qubit_mem_pos = path[0].store_mem_pos_1
        self._dst_entangled_qubit_mem_pos = path[len(path)-1].store_mem_pos_1
        super().__init__()
    def run(self):
        repeater_classical_protocols = []
        for node_number in range(len(self.path)):
            if node_number == 0:
                result_trans_port =  self._src_user_node.get_conn_port(self.path[1].node.ID)
                src_node_bm_protocol = BellMeasurementProtocol(self._src_user_node, self._src_target_qubit_mem_pos,
                                              self._src_entangled_qubit_mem_pos,result_trans_port)
            if node_number == len(self.path)-1:
                result_receive_port = self._dst_user_node.get_conn_port(self.path[node_number-1].node.ID)
                dst_node_correct_protocol = CorrectionProtocol(self._dst_user_node,self._dst_entangled_qubit_mem_pos, result_receive_port)
            if node_number != 0 and node_number != len(self.path)-1 and self.path[node_number].entangle_distribution_role == "receiver" :
                result_receive_port = self.path[node_number].node.get_conn_port(self.path[node_number-1].node.ID)
                result_trans_port = self.path[node_number].node.get_conn_port(self.path[node_number+2].node.ID)
                repeater_classical_protocol = RepeaterTransResult(self.path[node_number].node, result_receive_port, result_trans_port)
                repeater_classical_protocols.append(repeater_classical_protocol)

        src_node_bm_protocol.start()
        dst_node_correct_protocol.start()
        for repeater_classical_protocol in repeater_classical_protocols:
            repeater_classical_protocol.start()
               
        yield self.await_signal(src_node_bm_protocol,Signals.SUCCESS)
        for repeater_classical_protocol in repeater_classical_protocols:
            yield self.await_signal(repeater_classical_protocol, Signals.SUCCESS) 
        yield self.await_signal(dst_node_correct_protocol,Signals.SUCCESS)
        self.send_signal(Signals.SUCCESS,self._dst_entangled_qubit_mem_pos)
    def get_dst_user_node(self):
        return self._dst_user_node

    @property
    def is_connected(self):
        return True
