import netsquid as ns
from netsquid.protocols.nodeprotocols import NodeProtocol
from netsquid.protocols.protocol import Signals
from netsquid.components.component import Message,Port

class EndRequestProtocol(NodeProtocol):
    """End to End Request Protocol.

    Parameters
    ----------
    node : :class:`~netsquid.nodes.node.Node`
        Node to gennerate/transmit/reply request
    node_1 : :class:`~netsquid.nodes.node.Node`
        node_1
    node_2 : :class:`~netsquid.nodes.node.Node`
        node_2
    role : "controller" or "repeater"
        Whether this protocol should act as a controller or a repeater. Both are needed.
    name : str or None, optional
        Name of protocol. If None a default name is set.

    """
    MSG_HEADER_REQ = "user:request"
    MSG_HEADER_REP = "user:reply"
    def __init__(self, node,role, node_1, node_2=None, name=None):
        if role.lower() not in ["src_host", "dst_host","controller"]:
            raise ValueError
        self.role = role
        self.node_1 = node_1
        self.node_2 = node_2
        name = name if name else "({}, {})".format(node.name, role)
        super().__init__(node=node,name=name)

    def start(self):
        # Call parent start method
        super().start()

    def stop(self):
        # Call parent stop method
        super().stop()

    def run(self):
        if self.role == "src_host":
            yield from self._src_host()
        elif self.role == "controller":
            yield from self._controller()
        elif self.role == "dst_host":
            yield from self._dst_host()

    def _src_host(self):
        request_message = self.node.name + " request to build quantum connection"
        port = self.node.get_conn_port(self.node_1.ID)
        port.tx_output(Message(request_message, header=self.MSG_HEADER_REQ))
        print("{} send request success".format(self.node.name))
        yield self.await_port_input(port)
        print("{} received reply".format(self.node.name))
        cmessage = port.rx_input(header=self.MSG_HEADER_REP)
        reply_message = cmessage.items
        self.send_signal(Signals.SUCCESS, reply_message)

    def _controller(self):
        port_in = self.node.get_conn_port(self.node_1.ID)
        port_out = self.node.get_conn_port(self.node_2.ID)
        yield self.await_port_input(port_in)
        print("{} received request".format(self.node.name))
        cmessage = port_in.rx_input(header=self.MSG_HEADER_REQ)
        request_message = cmessage.items
        port_out.tx_output(Message(request_message, header=self.MSG_HEADER_REQ))
        print("{} transmitted request".format(self.node.name))
        yield self.await_port_input(port_out)
        print("{} received reply".format(self.node.name))
        cmessage = port_out.rx_input(header=self.MSG_HEADER_REP)
        reply_message = cmessage.items
        port_in.tx_output(Message(reply_message, header=self.MSG_HEADER_REP))
        print("{} transmitted reply".format(self.node.name))  

    def _dst_host(self):
        port = self.node.get_conn_port(self.node_1.ID)
        yield self.await_port_input(port)
        print("{} received request".format(self.node.name))
        cmessage = port.rx_input(header=self.MSG_HEADER_REQ)
        request_message = cmessage.items
        if request_message != None:
            for mem_position in [1,2]:
                if self.node.qmemory.mem_positions[mem_position].in_use == False:
                    reply_message = mem_position
                    port.tx_output(Message(reply_message, header=self.MSG_HEADER_REP))
                    print("{} send reply success".format(self.node.name))
                    break
                elif mem_position == 2:
                    reply_message = "reject, no enough mem to receive qubit"
                    port.tx_output(Message(reply_message, header=self.MSG_HEADER_REP))
                    print("{} send reply success".format(self.node.name)) 
        else:
            reply_message = "reject, Unknown User"
            port.tx_output(Message(reply_message, header=self.MSG_HEADER_REP))    
            print("{} send reply success".format(self.node.name))
          
    @property
    def is_connected(self):
        return True
