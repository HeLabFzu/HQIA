import sys
sys.path.append("..")

from util.NodeStruct import NodeStruct
"""
the principle of SLMP_algorithm is that
a) Entanglement is distributed at all adjacent Repeaters
b) In the nodes with successful entanglement distribution, we need to decide which nodes should do entanglment-swapping, the swapping decision principle is that after swapping the two remote nodes should be closest to SRC and DST, respectively。

thus the entanglement-distribution process should be contained in SLMP.
"""
