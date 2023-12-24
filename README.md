# Repo for Hierarchical Architecture of Quantum Internet
## Abstract
The research of architecture has tremendous significance in realizing quantum Internet. Although there is not yet a standard quantum Internet architecture, the distributed architecture is one of the possible solutions, which utilizes quantum repeaters or dedicated entanglement sources in a flat structure for entanglement preparation & distribution. In this paper, we analyze the distributed architecture in detail and demonstrate that it has three limitations: 1) possible high maintenance overhead, 2) possible low-performance entanglement distribution, and 3) unable to support optimal entanglement routing. We design a hierarchical quantum Internet architecture and a communication model to solve the problems above. We also present a W-state Based Centralized Entanglement Preparation & Distribution (W-state Based CEPD) scheme and a Centralized Entanglement Routing (CER) algorithm within our hierarchical architecture and perform an experimental comparison with other entanglement preparation & distribution schemes and entanglement routing algorithms within the distributed architecture. The evaluation results show that the entanglement distribution efficiency of hierarchical architecture is 11.5% higher than that of distributed architecture on average (minimum 3.3%, maximum 37.3%), and the entanglement routing performance of hierarchical architecture is much better than that of a distributed architecture according to the fidelity and throughput.
## Repository Structure
- `experiment`                   source code of experiment
	+ `integrated_example.py`    a completed use case for hierarchical quantum internet communication.
	+ `environmental_parameter_effect_test.py` impact of environmental interference
	+ `route_hops_effect_test.py`     hops vs. fidelity
	+ `path_with_different_environmental_parameter_effect_test.py` shows the importance of environmental interference in entanglement routing
	+ `entanglement_distribution_solution_test.py` performance of entanglement preparation & distribution solution
	+ `routing_algorithm_comparison_equivalent_parameter_network.py` routing in equivalent parameter network
	+ `routing_algorithm_comparison_diversified_parameter_network_dephase.py` routing in diversified parameter network (dephasing rate)
	+ `routing_algorithm_comparison_diversified_parameter_network_loss_init.py` routing in diversified parameter network (Q-channel loss init rate)
	+ `routing_algorithm_comparison_diversified_parameter_network_loss_noisy.py` routing in diversified parameter network (Q-channel loss noise)
	+ `3d_heat_map_centralized_routing.py` Centralized Entanglement Routing (CER) with integrated environmental parameters
	+ `noisy_limitation_test.py` shows the maximum acceptable noise
of a 100 km quantum channel is 0.2 dB/km
- `protocol`                     protocols for quantum internet
	+ `centralized`                hierarchical quantum internet protocol
		* `CentralizedEntanglementDistribution.py` including entanglement preparation & distribution / Physical & Link Layer
		* `CentralizedResourceCheckReserve.py` resource check & reservation / Link Layer
		* `CentralizedRouting.py` CER / Network Layer
		* `CentralizedSwapping.py` entanglment swapping / Network Layer
		* `CentralizedTeleportation.py` quantum teleportation / Transport Layer
		* `End2EndRequestProtocol.py` end-end communication request / Transport Layer
	+ `distributed`                distributed quantum internet protocol
		* `DistributedEntanglementDistribution.py` including entanglement preparation & distribution / Physical & Link Layer
		* `DistributedSwapping.py` entanglement swapping / Network Layer
		* `GreedyRouting.py` Greedy Routing / Network Layer
		* `QCastRouting.py` Q-Cast Routing / Network Layer
		* `SLMPRouting.py` SLMP Routing / Network Layer
		* `DistributedTeleportation.py` quantum teleportation / Transport Layer
- `topology`                     topologies for quantum internet
	+ `Centralized_Cellular_Topo.py` diversified parameter network of hierarchical cellular topology
	+ `Centralized_Cellular_Topo_simple_parameter.py` equivalent parameter network of hierarchical cellular topology
	+ `Distributed_Cellular_Topo_simple_parameter.py` equivalent parameter network of distributed cellular topology
	+ `Centralized_Chain_Topo.py` hierarchical chain topology
- `util`                         utilities functions
	+ `CentralController.py` include Central State Matrix, Domain Shortest Path Table, Domain Edge Repeater Table
	+ `CheckDistribution.py` check entanglement distribution result
	+ `ClearCentralControllerTable.py` clear information in the central controller
	+ `CollectData.py` experimental data collector
	+ `NodeStruct` struct of quantum devices
	+ `QubitCreation.py` create qubit
	+ `ResourceLockRelease.py` lock and release quantum memory
	+ `RoutingComparison.py` run entanglement routing algorithm
## Run Experiments
```bash
# 1. *This step is platform-specific* 
# install Python >= 3.8.2, NetSquid >= 1.1.5 (prefer to install NetSquid 1.1.5)
# 2. Install NetSquid
# refer to https://docs.netsquid.org/latest-release/INSTALL.html
# NetSquid might require additional python package, please refer to the UserBook of NetSquid
# 3. Download source code
# git clone https://github.com/hebinjie33/CQIA.git
# 4. Run test
# cd experiment/
# python3 xxx.py
```
## Experimental Result
The results may fluctuate slightly due to randomness; our original results are shown in result.pdf.
## Authors
- Binjie He (hebinjie33@gmail.com)
- Dong Zhang (zhangdong@fzu.edu.cn)
- Seng W. Loke (seng.loke@deakin.edu.au)
- Shengrui Lin (xmlsr@foxmail.com)
- Luke Lu (luklu@cisco.com)