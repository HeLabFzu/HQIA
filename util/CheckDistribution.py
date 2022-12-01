import netsquid as ns
from netsquid.protocols.nodeprotocols import NodeProtocol
from netsquid.protocols.protocol import Signals

class CheckDistribution(NodeProtocol):
    def __init__(self, distribution_success_signal):
        super().__init__()
        self._distribution_success_signal = distribution_success_signal
        self.result = None
    def run(self):
        if self._distribution_success_signal:
            self.result = 1
        else:
            self.result = 0
        self.send_signal(Signals.SUCCESS)   
    def getresult(self):
        return self.result
    @property
    def is_connected(self):
        return True
