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

class ControllerTransResult(NodeProtocol):
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

class CentralizedTeleportation(NodeProtocol):
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
    def __init__(self, src_user_node, dst_user_node, src_user_controller, dst_user_controller,
                  central_controller,src_target_qubit_mem_pos, src_entangled_qubit_mem_pos, dst_entangled_qubit_mem_pos):
        self._src_user_node = src_user_node
        self._dst_user_node = dst_user_node
        self._src_user_controller = src_user_controller
        self._dst_user_controller = dst_user_controller
        self._central_controller = central_controller
        self._src_target_qubit_mem_pos = src_target_qubit_mem_pos
        self._src_entangled_qubit_mem_pos = src_entangled_qubit_mem_pos
        self._dst_entangled_qubit_mem_pos = dst_entangled_qubit_mem_pos
        super().__init__()
    def run(self):
        result_trans_port = self._src_user_node.get_conn_port(self._src_user_controller.ID)
        src_controller_port_in = self._src_user_controller.get_conn_port(self._src_user_node.ID)
        src_controller_port_out = self._src_user_controller.get_conn_port(self._central_controller.ID)
        central_controller_port_in = self._central_controller.get_conn_port(self._src_user_controller.ID)
        central_controller_port_out = self._central_controller.get_conn_port(self._dst_user_controller.ID)
        dst_controller_port_in = self._dst_user_controller.get_conn_port(self._central_controller.ID)
        dst_controller_port_out = self._dst_user_controller.get_conn_port(self._dst_user_node.ID)
        result_receive_port = self._dst_user_node.get_conn_port(self._dst_user_controller.ID)
        src_node_bm_protocol = BellMeasurementProtocol(self._src_user_node, self._src_target_qubit_mem_pos,
                                              self._src_entangled_qubit_mem_pos,result_trans_port)
        src_controller_trans = ControllerTransResult(self._src_user_controller, src_controller_port_in, src_controller_port_out)
        central_controller_trans = ControllerTransResult(self._central_controller, central_controller_port_in, 
                                              central_controller_port_out)
        dst_controller_trans = ControllerTransResult(self._dst_user_controller, dst_controller_port_in, dst_controller_port_out)
        dst_node_correct_protocol = CorrectionProtocol(self._dst_user_node,self._dst_entangled_qubit_mem_pos, result_receive_port)
        src_node_bm_protocol.start()
        src_controller_trans.start()
        central_controller_trans.start()
        dst_controller_trans.start()
        dst_node_correct_protocol.start()
        yield self.await_signal(src_node_bm_protocol,Signals.SUCCESS)
        yield self.await_signal(src_controller_trans,Signals.SUCCESS)
        yield self.await_signal(central_controller_trans,Signals.SUCCESS)
        yield self.await_signal(dst_controller_trans,Signals.SUCCESS)
        yield self.await_signal(dst_node_correct_protocol,Signals.SUCCESS)
        self.send_signal(Signals.SUCCESS,self._dst_entangled_qubit_mem_pos)
    def get_dst_user_node(self):
        return self._dst_user_node
          
    @property
    def is_connected(self): 
        return True
                
        

        
        





