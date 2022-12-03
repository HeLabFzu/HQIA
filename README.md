# Repo for Centralized Architecture of Quantum Internet
## Abstract
The quantum internet is an advanced network that connects quantum systems. The research of architecture has tremendous significance in realizing quantum internet. Currently, studies focus on the distributed architecture, which relies on quantum repeaters to perform entanglement preparation & distribution, caused the critical problems: 1) vast costs of maintaining the entanglement preparing environment, 2) inefficient entanglement preparation & distribution, 3) non-optimal entanglement routing without considering the global network state, 4) lack of ability to perform time synchronization of quantum operations and action control of quantum devices. We propose a three-layer centralized quantum internet architecture to solve the problems above. At the top layer, we deploy the central controller to collect the global network state for optimal entanglement routing. Also, we can perform network management with the powerful ability of the central controller. At the middle layer, we design the local domain controller for entanglement preparation & distribution, reducing maintenance overhead and improving efficiency. At the bottom layer, quantum devices are responsible for executing quantum operations. In the experimental part, we evaluate the performance of centralized quantum internet architecture by using the discrete-event simulator for quantum networks.
## Repository Structure
- `experiment`                   source code of experiment
	+ `integrated_example.py`    a completed use case for centralized quantum internet communication.
	+ `environmental_parameter_effect_test.py` impact of environmental interference
	+ `route_hops_effect_test.py`     hops vs. fidelity
	+ `path_with_different_environmental_parameter_effect_test.py` communication fidelity under integrated conditions
	+ `entanglement_distribution_solution_test.py` performance of entanglement preparation & distribution solution
	+ `routing_algorithm_comparison_equivalent_parameter_network.py` routing in equivalent parameter network
	+ `routing_algorithm_comparison_diversified_parameter_network_dephase.py` routing in diversified parameter network (dephasing rate)
	+ `routing_algorithm_comparison_diversified_parameter_network_loss_init.py` routing in diversified parameter network (Q-channel loss init rate)
	+ `routing_algorithm_comparison_diversified_parameter_network_loss_noisy.py` routing in diversified parameter network (Q-channel loss noise)
	+ `3d_heat_map_centralized_routing.py` Centralized Entanglement Routing (CER) with integrated environmental parameters
	+ `noisy_limitation_test.py` shows the maximum acceptable noise
of a 100 km quantum channel is 0.2 dB/km
- `protocol`                     protocols for quantum internet
	+ `centralized`                centralized quantum internet protocol
		* `CentralizedEntanglementDistribution.py` including entanglement preparation & distribution / Physical & Link Layer
		* `CentralizedResourceCheckReserve.py` resource check & reservation / Link Layer
		* `CentralizedRouting.py` CER / Network Layer
		* `CentralizedSwapping.py` entanglment swapping / Network Layer
		* `CentralizedTeleportation.py` quantum teleportation / Transport Layer
		* `End2EndRequestProtocol.py` end-end communication request / Transport Layer
	+ `distributed`                distributed quantum internet protocol
		* `DistributedEntanglementDistribution.py` including entanglement preparation & distribution / Physical & Link Layer
		* `DistributedSwapping.py` entanglement swapping / Network Layer
		* `pseudo_distributed_topo_GreedyRouting.py` Greedy Routing / Network Layer
		* `pseudo_distributed_topo_QCastRouting.py` Q-Cast Routing / Network Layer
		* `pseudo_distributed_topo_SLMPRouting.py` SLMP Routing / Network Layer
		* `DistributedTeleportation.py` quantum teleportation / Transport Layer
- `topology`                     topologies for quantum internet
	+ `Centralized_Cellular_Topo.py` diversified parameter network of centralized cellular topology
	+ `Centralized_Cellular_Topo_simple_parameter.py` equivalent parameter network of centralized cellular topology
	+ `Distributed_Cellular_Topo_simple_parameter.py` equivalent parameter network of distributed cellular topology
	+ `Centralized_Chain_Topo.py` centralized chain topology
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
- Binjie He (275640880@qq.com)
