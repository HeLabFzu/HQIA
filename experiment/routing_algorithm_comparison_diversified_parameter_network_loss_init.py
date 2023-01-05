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
This program explores routing in diversified parameter network (Q-channel loss init rate).

The program take about 10 minutes to complete.
"""
if __name__ == '__main__':

    ################################
    ####  standard_deviation_of_qchannel_loss_init test ###
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
    dephase_rates = [0.09,0.52,0.01,0.01,0.61,0.21,0.11,0.01,0.01,0.09,0.03,0.01,0.02,0.14,0.07,0.02,0.03,0.04,0.02,0.05,0.06,0.02,0.09,0.04,0.01,0.01,0.05,0.06,0.07]
    qchannel_loss_noisy = [0.0006,0.0006,0.0002,0.0001,0.0003,0.0003,0.0001,0.0005,0.0005,0.0006,0.0013,0.0001,0.0003,0.0003,0.0002,0.0002,0.0003,0.0004,0.0006,0.0004,0.0003,0.0046,0.0012,0.0057,0.0002,0.0001,0.0006,0.0005,0.0001,0.0035,0.0014,0.0001]
    round = 300
   
    ### group_1 std_loss_init is 0.041###
    qchannel_loss_init_group_1 = [0.008,0.1,0.003,0.003,0.003,0.003,0.002,0.008,0.1,0.1,0.18,0.002,0.003,0.005,0.002,0.003,0.003,0.006,0.008,0.007,0.002,0.047,0.010,0.053,0.003,0.003,0.008,0.002,0.003,0.004,0.006,0.003]
    ### group_2 std_loss_init is 0.049###
    qchannel_loss_init_group_2 = [0.008,0.14,0.0025,0.0025,0.0025,0.0025,0.002,0.008,0.14,0.14,0.18,0.002,0.003,0.005,0.002,0.0025,0.0025,0.006,0.008,0.007,0.002,0.047,0.010,0.053,0.0025,0.0025,0.008,0.002,0.0025,0.004,0.006,0.0025]
    ### group_3 std_loss_init is 0.053###
    qchannel_loss_init_group_3 = [0.008,0.16,0.002,0.002,0.002,0.002,0.002,0.008,0.16,0.16,0.18,0.002,0.003,0.005,0.002,0.002,0.002,0.006,0.008,0.007,0.002,0.047,0.010,0.053,0.002,0.002,0.008,0.002,0.002,0.004,0.006,0.002]
    ### group_4 std_loss_init is 0.058###
    qchannel_loss_init_group_4 = [0.008,0.18,0.0015,0.0015,0.0015,0.0015,0.002,0.008,0.18,0.18,0.18,0.002,0.003,0.005,0.002,0.0015,0.0015,0.006,0.008,0.007,0.002,0.047,0.010,0.053,0.0015,0.0015,0.008,0.002,0.0015,0.004,0.006,0.0015]
    ### group_5 std_loss_init is 0.063###
    qchannel_loss_init_group_5 = [0.008,0.2,0.001,0.001,0.001,0.001,0.002,0.008,0.2,0.2,0.18,0.002,0.003,0.005,0.002,0.001,0.001,0.006,0.008,0.007,0.002,0.047,0.010,0.053,0.001,0.001,0.008,0.002,0.001,0.004,0.006,0.001]

    ### run Centralized routing test ###
    for qchannel_loss_init in [qchannel_loss_init_group_5, qchannel_loss_init_group_4, qchannel_loss_init_group_3, qchannel_loss_init_group_2, qchannel_loss_init_group_1]: 
        fidelity_data_temp,centralized_routing_throughput, centralized_routing_time_cost = run_centralized_routing_test(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy,round)
        fidelity_data = fidelity_data.append(fidelity_data_temp)
        centralized_routing_throughputs.append(centralized_routing_throughput)
        centralized_routing_path_selection_time_cost.append(centralized_routing_time_cost)

    ### run Q-Cast routing test ###
    for qchannel_loss_init in [qchannel_loss_init_group_1, qchannel_loss_init_group_2, qchannel_loss_init_group_3, qchannel_loss_init_group_4, qchannel_loss_init_group_5]:
        fidelity_data_temp,QCast_throughput, QCast_time_cost = run_QCast_routing_test(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy,round)
        fidelity_data = fidelity_data.append(fidelity_data_temp)
        QCast_throughputs.append(QCast_throughput)
        QCast_path_selection_time_cost.append(QCast_time_cost)

    ### run Greedy routing test ###
    for qchannel_loss_init in [qchannel_loss_init_group_1, qchannel_loss_init_group_2, qchannel_loss_init_group_3, qchannel_loss_init_group_4, qchannel_loss_init_group_5]:
        fidelity_data_temp,greedy_throughput, greedy_time_cost = run_greedy_routing_test(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy,round)
        fidelity_data = fidelity_data.append(fidelity_data_temp)
        greedy_throughputs.append(greedy_throughput)
        greedy_path_selection_time_cost.append(greedy_time_cost)

    ### run SLMP routing test ###
    for qchannel_loss_init in [qchannel_loss_init_group_1, qchannel_loss_init_group_2, qchannel_loss_init_group_3, qchannel_loss_init_group_4, qchannel_loss_init_group_5]:
        fidelity_data_temp,SLMP_throughput, SLMP_time_cost = run_SLMP_routing_test(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy,round)
        fidelity_data = fidelity_data.append(fidelity_data_temp)
        SLMP_throughputs.append(SLMP_throughput)
        SLMP_path_selection_time_cost.append(SLMP_time_cost)

    
    fidelity_cr_loss_init = fidelity_data[fidelity_data['routing_algorithm']=="Centralized_Routing"].groupby("standard_deviation_of_qchannel_loss_init")['fidelity'].agg(fidelity='mean', sem='sem').reset_index()
    fidelity_qc_loss_init = fidelity_data[fidelity_data['routing_algorithm']=="Q-Cast"].groupby("standard_deviation_of_qchannel_loss_init")['fidelity'].agg(fidelity='mean', sem='sem').reset_index()
    fidelity_slmp_loss_init = fidelity_data[fidelity_data['routing_algorithm']=="SLMP"].groupby("standard_deviation_of_qchannel_loss_init")['fidelity'].agg(fidelity='mean', sem='sem').reset_index()
    fidelity_greedy_loss_init = fidelity_data[fidelity_data['routing_algorithm']=="Greedy"].groupby("standard_deviation_of_qchannel_loss_init")['fidelity'].agg(fidelity='mean', sem='sem').reset_index()
    entanglement_pair_consumption_cr_loss_init = fidelity_data[fidelity_data['routing_algorithm']=="Centralized_Routing"].groupby("standard_deviation_of_qchannel_loss_init")['entanglement_pair_consumption'].agg(entanglement_pair_consumption='mean').reset_index()
    entanglement_pair_consumption_qc_loss_init = fidelity_data[fidelity_data['routing_algorithm']=="Q-Cast"].groupby("standard_deviation_of_qchannel_loss_init")['entanglement_pair_consumption'].agg(entanglement_pair_consumption='mean').reset_index()
    entanglement_pair_consumption_slmp_loss_init = fidelity_data[fidelity_data['routing_algorithm']=="SLMP"].groupby("standard_deviation_of_qchannel_loss_init")['entanglement_pair_consumption'].agg(entanglement_pair_consumption='mean').reset_index()
    entanglement_pair_consumption_greedy_loss_init = fidelity_data[fidelity_data['routing_algorithm']=="Greedy"].groupby("standard_deviation_of_qchannel_loss_init")['entanglement_pair_consumption'].agg(entanglement_pair_consumption='mean').reset_index()
    throughput_cr_loss_init = pandas.DataFrame([[0.041,centralized_routing_throughputs[4]],
                                           [0.049,centralized_routing_throughputs[3]],
                                           [0.053,centralized_routing_throughputs[2]],
                                           [0.058,centralized_routing_throughputs[1]],
                                           [0.063,centralized_routing_throughputs[0]]],
                                           columns=['standard_deviation_of_qchannel_loss_init', 'throughput'])
    throughput_qc_loss_init = pandas.DataFrame([[0.041,QCast_throughputs[0]],
                                           [0.049,QCast_throughputs[1]],
                                           [0.053,QCast_throughputs[2]],
                                           [0.058,QCast_throughputs[3]],
                                           [0.063,QCast_throughputs[4]]],
                                           columns=['standard_deviation_of_qchannel_loss_init', 'throughput'])
    throughput_slmp_loss_init = pandas.DataFrame([[0.041,SLMP_throughputs[0]],
                                           [0.049,SLMP_throughputs[1]],
                                           [0.053,SLMP_throughputs[2]],
                                           [0.058,SLMP_throughputs[3]],
                                           [0.063,SLMP_throughputs[4]]],
                                           columns=['standard_deviation_of_qchannel_loss_init', 'throughput'])
    throughput_greedy_loss_init = pandas.DataFrame([[0.041,greedy_throughputs[0]],
                                           [0.049,greedy_throughputs[1]],
                                           [0.053,greedy_throughputs[2]],
                                           [0.058,greedy_throughputs[3]],
                                           [0.063,greedy_throughputs[4]]],
                                           columns=['standard_deviation_of_qchannel_loss_init', 'throughput'])


    fig,ax = plt.subplots(1,2,figsize=(25,10))
    plot_style = {'kind': 'line', 'grid': True,
      'title': "Routing Algorithm Comparison in Diversified Parameter Network"}
    ax[0].set_ylabel('fidelity')
    ax[1].set_ylabel('throughput(qps)')
    ax[1].set_xticks([0.041,0.049,0.053,0.058,0.063])

    fidelity_cr_loss_init.plot(x='standard_deviation_of_qchannel_loss_init', y='fidelity', yerr='sem', ax=ax[0],label="Centralized_Routing", **plot_style)
    fidelity_qc_loss_init.plot(x='standard_deviation_of_qchannel_loss_init', y='fidelity',yerr='sem',ax=ax[0],label="Q-Cast", **plot_style)
    fidelity_slmp_loss_init.plot(x='standard_deviation_of_qchannel_loss_init', y='fidelity',yerr='sem',ax=ax[0],label="SLMP", **plot_style)
    fidelity_greedy_loss_init.plot(x='standard_deviation_of_qchannel_loss_init', y='fidelity',yerr='sem',ax=ax[0],label="Greedy", **plot_style)
    throughput_cr_loss_init.plot(x='standard_deviation_of_qchannel_loss_init', y='throughput', ax=ax[1],label="Centralized_Routing", **plot_style)
    throughput_qc_loss_init.plot(x='standard_deviation_of_qchannel_loss_init', y='throughput', ax=ax[1],label="Q-Cast", **plot_style)
    throughput_slmp_loss_init.plot(x='standard_deviation_of_qchannel_loss_init', y='throughput', ax=ax[1],label="SLMP", **plot_style)
    throughput_greedy_loss_init.plot(x='standard_deviation_of_qchannel_loss_init', y='throughput', ax=ax[1],label="Greedy", **plot_style)
    

    print(fidelity_cr_loss_init)
    print(fidelity_qc_loss_init)
    print(fidelity_slmp_loss_init)
    print(fidelity_greedy_loss_init)
    print(entanglement_pair_consumption_cr_loss_init)
    print(entanglement_pair_consumption_qc_loss_init)
    print(entanglement_pair_consumption_slmp_loss_init)
    print(entanglement_pair_consumption_greedy_loss_init)
    print(throughput_cr_loss_init)
    print(throughput_qc_loss_init)
    print(throughput_slmp_loss_init)
    print(throughput_greedy_loss_init)
    print("Centralized_Routing Time Cost: ")
    print(np.mean(centralized_routing_path_selection_time_cost))
    print("Q-Cast Time Cost: ")
    print(np.mean(QCast_path_selection_time_cost))
    print("SLMP Time Cost: ")
    print(np.mean(SLMP_path_selection_time_cost))
    print("Greedy Time Cost: ")
    print(np.mean(greedy_path_selection_time_cost))

    plt.show()

