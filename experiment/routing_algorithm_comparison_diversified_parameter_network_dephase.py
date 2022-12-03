import sys
import gc
sys.path.append("..")

import netsquid as ns
import pandas
import pydynaa
import time
import numpy as np
from util.RoutingComparison import run_centralized_routing_test, run_QCast_routing_test,run_SLMP_routing_test,run_greedy_routing_test
from matplotlib import pyplot as plt

"""
This program explores routing in diversified parameter network (dephasing rate).

Generally speaking, the distributed routing algorithm can only run in distributed topology. However, in order to eliminate the interference of inconsistent topology between centralized_routing and distributed_routing and obtain more accurate experimental results, this experiment runs distributed_routing_algorithm(Q-cast, Greedy, SLMP) in a pseudo_distributed_topo(which is a centralized topo, but we code to hide the controller and the distributed_routing_algorithm will think the topo as a distributed topo).

The program take about 10 minutes to complete.
"""
if __name__ == '__main__':

    ################################
    ####  standard_deviation_of_dephase_rate test ###
    ###############################

    fidelity_data = pandas.DataFrame()
    centralized_routing_throughputs = []
    QCast_throughputs = []
    SLMP_throughputs = []
    greedy_throughputs = []
    centralized_routing_path_selection_time_cost = []
    QCast_path_selection_time_cost = []
    SLMP_path_selection_time_cost = []
    greedy_path_selection_time_cost = []
    depolar_rates = [0.004,0.005,0.001,0.002,0.009,0.008,0.009,0.003,0.001,0.008,0.006,0.001,0.008,0.006,0.003,0.003,0.002,0.004,0.005,0.006,0.003,0.002,0.005,0.009,0.006,0.001,0.002,0.004,0.006]
    qchannel_loss_init = [0.008,0.021,0.002,0.001,0.002,0.002,0.017,0.008,0.015,0.020,0.030,0.002,0.003,0.005,0.002,0.024,0.004,0.006,0.008,0.007,0.002,0.047,0.010,0.053,0.003,0.002,0.008,0.002,0.004,0.034,0.011,0.001]
    qchannel_loss_noisy = [0.0006,0.0004,0.0004,0.0003,0.0002,0.0003,0.0015,0.0005,0.0003,0.0022,0.0033,0.0001,0.0003,0.0003,0.0004,0.0026,0.0003,0.0004,0.0006,0.0004,0.0003,0.0046,0.0012,0.0057,0.0002,0.0001,0.0006,0.0005,0.0003,0.0035,0.0014,0.0001]
    round = 300
   
    ### group_1 std_dephase is 0.096###
    dephase_rates_group_1 = [0.09,0.35,0.03,0.03,0.35,0.35,0.11,0.03,0.03,0.09,0.03,0.03,0.02,0.14,0.07,0.02,0.03,0.04,0.02,0.05,0.06,0.02,0.09,0.04,0.03,0.03,0.05,0.06,0.07]
    ### group_2 std_dephase is 0.144###
    dephase_rates_group_2 = [0.09,0.51,0.025,0.025,0.51,0.51,0.11,0.0025,0.025,0.09,0.03,0.025,0.02,0.14,0.07,0.02,0.03,0.04,0.02,0.05,0.06,0.02,0.09,0.04,0.025,0.025,0.05,0.06,0.07]
    ### group_3 std_dephase is 0.192###
    dephase_rates_group_3 = [0.09,0.67,0.02,0.02,0.67,0.67,0.11,0.02,0.02,0.09,0.03,0.02,0.02,0.14,0.07,0.02,0.03,0.04,0.02,0.05,0.06,0.02,0.09,0.04,0.02,0.02,0.05,0.06,0.07]
    ### group_4 std_dephase is 0.241###
    dephase_rates_group_4 = [0.09,0.83,0.015,0.015,0.83,0.83,0.11,0.015,0.015,0.09,0.03,0.015,0.02,0.14,0.07,0.02,0.03,0.04,0.02,0.05,0.06,0.02,0.09,0.04,0.015,0.015,0.05,0.06,0.07]
    ### group_5 std_dephase is 0.29###
    dephase_rates_group_5 = [0.09,0.99,0.01,0.01,0.99,0.99,0.11,0.01,0.01,0.09,0.03,0.01,0.02,0.14,0.07,0.02,0.03,0.04,0.02,0.05,0.06,0.02,0.09,0.04,0.01,0.01,0.05,0.06,0.07]

    ### run Centralized routing test ###
    for dephase_rates in [dephase_rates_group_5, dephase_rates_group_4, dephase_rates_group_3, dephase_rates_group_2, dephase_rates_group_1]: 
        fidelity_data_temp,centralized_routing_throughput, centralized_routing_time_cost = run_centralized_routing_test(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy,round)
        fidelity_data = fidelity_data.append(fidelity_data_temp)
        centralized_routing_throughputs.append(centralized_routing_throughput)
        centralized_routing_path_selection_time_cost.append(centralized_routing_time_cost)

    ### run Q-Cast routing test ###
    for dephase_rates in [dephase_rates_group_1, dephase_rates_group_2, dephase_rates_group_3, dephase_rates_group_4, dephase_rates_group_5]:
        fidelity_data_temp,QCast_throughput, QCast_time_cost = run_QCast_routing_test(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy,round)
        fidelity_data = fidelity_data.append(fidelity_data_temp)
        QCast_throughputs.append(QCast_throughput)
        QCast_path_selection_time_cost.append(QCast_time_cost)

    ### run Greedy routing test ###
    for dephase_rates in [dephase_rates_group_1, dephase_rates_group_2, dephase_rates_group_3, dephase_rates_group_4, dephase_rates_group_5]:
        fidelity_data_temp,greedy_throughput, greedy_time_cost = run_greedy_routing_test(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy,round)
        fidelity_data = fidelity_data.append(fidelity_data_temp)
        greedy_throughputs.append(greedy_throughput)
        greedy_path_selection_time_cost.append(greedy_time_cost)

    ### run SLMP routing test ###
    for dephase_rates in [dephase_rates_group_1, dephase_rates_group_2, dephase_rates_group_3, dephase_rates_group_4, dephase_rates_group_5]:
        fidelity_data_temp,SLMP_throughput, SLMP_time_cost = run_SLMP_routing_test(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy,round)
        fidelity_data = fidelity_data.append(fidelity_data_temp)
        SLMP_throughputs.append(SLMP_throughput)
        SLMP_path_selection_time_cost.append(SLMP_time_cost)

    
    fidelity_cr_deph = fidelity_data[fidelity_data['routing_algorithm']=="Centralized_Routing"].groupby("standard_deviation_of_dephase_rate")['fidelity'].agg(fidelity='mean', sem='sem').reset_index()
    fidelity_qc_deph = fidelity_data[fidelity_data['routing_algorithm']=="Q-Cast"].groupby("standard_deviation_of_dephase_rate")['fidelity'].agg(fidelity='mean', sem='sem').reset_index()
    fidelity_slmp_deph = fidelity_data[fidelity_data['routing_algorithm']=="SLMP"].groupby("standard_deviation_of_dephase_rate")['fidelity'].agg(fidelity='mean', sem='sem').reset_index()
    fidelity_greedy_deph = fidelity_data[fidelity_data['routing_algorithm']=="Greedy"].groupby("standard_deviation_of_dephase_rate")['fidelity'].agg(fidelity='mean', sem='sem').reset_index()
    entanglement_pair_consumption_cr_deph = fidelity_data[fidelity_data['routing_algorithm']=="Centralized_Routing"].groupby("standard_deviation_of_dephase_rate")['entanglement_pair_consumption'].agg(entanglement_pair_consumption='mean').reset_index()
    entanglement_pair_consumption_qc_deph = fidelity_data[fidelity_data['routing_algorithm']=="Q-Cast"].groupby("standard_deviation_of_dephase_rate")['entanglement_pair_consumption'].agg(entanglement_pair_consumption='mean').reset_index()
    entanglement_pair_consumption_slmp_deph = fidelity_data[fidelity_data['routing_algorithm']=="SLMP"].groupby("standard_deviation_of_dephase_rate")['entanglement_pair_consumption'].agg(entanglement_pair_consumption='mean').reset_index()
    entanglement_pair_consumption_greedy_deph = fidelity_data[fidelity_data['routing_algorithm']=="Greedy"].groupby("standard_deviation_of_dephase_rate")['entanglement_pair_consumption'].agg(entanglement_pair_consumption='mean').reset_index()
    throughput_cr_deph = pandas.DataFrame([[0.096,centralized_routing_throughputs[4]],
                                           [0.144,centralized_routing_throughputs[3]],
                                           [0.192,centralized_routing_throughputs[2]],
                                           [0.241,centralized_routing_throughputs[1]],
                                           [0.290,centralized_routing_throughputs[0]]],
                                           columns=['standard_deviation_of_dephase_rate', 'throughput'])
    throughput_qc_deph = pandas.DataFrame([[0.096,QCast_throughputs[0]],
                                           [0.144,QCast_throughputs[1]],
                                           [0.192,QCast_throughputs[2]],
                                           [0.241,QCast_throughputs[3]],
                                           [0.290,QCast_throughputs[4]]],
                                           columns=['standard_deviation_of_dephase_rate', 'throughput'])
    throughput_slmp_deph = pandas.DataFrame([[0.096,SLMP_throughputs[0]],
                                           [0.144,SLMP_throughputs[1]],
                                           [0.192,SLMP_throughputs[2]],
                                           [0.241,SLMP_throughputs[3]],
                                           [0.290,SLMP_throughputs[4]]],
                                           columns=['standard_deviation_of_dephase_rate', 'throughput'])
    throughput_greedy_deph = pandas.DataFrame([[0.096,greedy_throughputs[0]],
                                           [0.144,greedy_throughputs[1]],
                                           [0.192,greedy_throughputs[2]],
                                           [0.241,greedy_throughputs[3]],
                                           [0.290,greedy_throughputs[4]]],
                                           columns=['standard_deviation_of_dephase_rate', 'throughput'])


    fig,ax = plt.subplots(1,2,figsize=(25,10))
    plot_style = {'kind': 'line', 'grid': True,
      'title': "Routing Algorithm Comparison in Diversified Parameter Network"}
    ax[0].set_ylabel('fidelity')
    ax[1].set_ylabel('throughput(qps)')
    ax[1].set_xticks([0.096,0.144,0.192,0.241,0.290])

    fidelity_cr_deph.plot(x='standard_deviation_of_dephase_rate', y='fidelity', yerr='sem', ax=ax[0],label="Centralized_Routing", **plot_style)
    fidelity_qc_deph.plot(x='standard_deviation_of_dephase_rate', y='fidelity',yerr='sem',ax=ax[0],label="Q-Cast", **plot_style)
    fidelity_slmp_deph.plot(x='standard_deviation_of_dephase_rate', y='fidelity',yerr='sem',ax=ax[0],label="SLMP", **plot_style)
    fidelity_greedy_deph.plot(x='standard_deviation_of_dephase_rate', y='fidelity',yerr='sem',ax=ax[0],label="Greedy", **plot_style)
    throughput_cr_deph.plot(x='standard_deviation_of_dephase_rate', y='throughput', ax=ax[1],label="Centralized_Routing", **plot_style)
    throughput_qc_deph.plot(x='standard_deviation_of_dephase_rate', y='throughput', ax=ax[1],label="Q-Cast", **plot_style)
    throughput_slmp_deph.plot(x='standard_deviation_of_dephase_rate', y='throughput', ax=ax[1],label="SLMP", **plot_style)
    throughput_greedy_deph.plot(x='standard_deviation_of_dephase_rate', y='throughput', ax=ax[1],label="Greedy", **plot_style)
    

    print(fidelity_cr_deph)
    print(fidelity_qc_deph)
    print(fidelity_slmp_deph)
    print(fidelity_greedy_deph)
    print(entanglement_pair_consumption_cr_deph)
    print(entanglement_pair_consumption_qc_deph)
    print(entanglement_pair_consumption_slmp_deph)
    print(entanglement_pair_consumption_greedy_deph)
    print(throughput_cr_deph)
    print(throughput_qc_deph)
    print(throughput_slmp_deph)
    print(throughput_greedy_deph)
    print("Centralized_Routing Time Cost: ")
    print(np.mean(centralized_routing_path_selection_time_cost))
    print("Q-Cast Time Cost: ")
    print(np.mean(QCast_path_selection_time_cost))
    print("SLMP Time Cost: ")
    print(np.mean(SLMP_path_selection_time_cost))
    print("Greedy Time Cost: ")
    print(np.mean(greedy_path_selection_time_cost))
    plt.show()

