from netsquid.components.qprogram import QuantumProgram
from netsquid.components import instructions as instr
from netsquid.protocols.nodeprotocols import NodeProtocol
class InitStateProgram(QuantumProgram):
    """Program to create a qubit and transform it to the y0 state.

    Parameters
    ----------
    mem_pos : :int
        mem_pos to store created qubit
    """
    def __init__(self,mem_pos):
        self._mem_pos = mem_pos
        super().__init__()
    def program(self):
        q1 = self._mem_pos
        self.apply(instr.INSTR_INIT, q1)
        self.apply(instr.INSTR_H, q1)
        self.apply(instr.INSTR_S, q1)
        yield self.run()

class CreateQubit(NodeProtocol):
    """Protocol to create a qubit and transform it to the y0 state.

    Parameters
    ----------
    node : :class:`~netsquid.nodes.node.Node`
        Node to create target qubit
    mem_pos : :int
        mem_pos to store target qubit
    """
    def __init__(self,node,mem_pos):
        self._mem_pos = mem_pos
        super().__init__(node=node)
    def run(self):
        qubit_init_program = InitStateProgram(mem_pos=self._mem_pos)
        yield self.node.qmemory.execute_program(qubit_init_program)
        print("Node {} create qubit with state y0 success, store in mem[0]".format(self.node.name))

