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
This program explores routing in diversified parameter network (Q-channel loss noise).

The program take about 10 minutes to complete.
"""
if __name__ == '__main__':
    ################################
    ####  standard_deviation_of_qchannel_loss_noisy test ###
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
    qchannel_loss_init = [0.006,0.001,0.002,0.001,0.003,0.003,0.001,0.005,0.002,0.001,0.013,0.001,0.003,0.003,0.002,0.002,0.003,0.004,0.006,0.004,0.003,0.046,0.012,0.057,0.002,0.001,0.006,0.005,0.001,0.035,0.014,0.001]
    round = 300
   
    ### group_1 std_loss_noisy is 0.0031###
    qchannel_loss_noisy_group_1 = [0.0008,0.00300,0.00030,0.00030,0.00030,0.00030,0.0002,0.0008,0.00300,0.00300,0.018,0.0002,0.0003,0.0005,0.0002,0.00030,0.00030,0.0006,0.0008,0.0007,0.0002,0.0027,0.0010,0.0023,0.00030,0.00030,0.0008,0.00030,0.00030,0.0004,0.0006,0.00030]
    ### group_2 std_loss_noisy is 0.0034###
    qchannel_loss_noisy_group_2 = [0.0008,0.00600,0.00025,0.00025,0.00025,0.00025,0.0002,0.0008,0.00600,0.00600,0.018,0.0002,0.0003,0.0005,0.0002,0.00025,0.00025,0.0006,0.0008,0.0007,0.0002,0.0027,0.0010,0.0023,0.00025,0.00025,0.0008,0.00025,0.00025,0.0004,0.0006,0.00025]
    ### group_3 std_loss_noisy is 0.0038###
    qchannel_loss_noisy_group_3 = [0.0008,0.00900,0.00020,0.00020,0.00020,0.00020,0.0002,0.0008,0.00900,0.00900,0.018,0.0002,0.0003,0.0005,0.0002,0.00020,0.00020,0.0006,0.0008,0.0007,0.0002,0.0027,0.0010,0.0023,0.00020,0.00020,0.0008,0.00020,0.00020,0.0004,0.0006,0.00020]
    ### group_4 std_loss_noisy is 0.0044###
    qchannel_loss_noisy_group_4 = [0.0008,0.01200,0.00015,0.00015,0.00015,0.00015,0.0002,0.0008,0.01200,0.01200,0.018,0.0002,0.0003,0.0005,0.0002,0.00015,0.00015,0.0006,0.0008,0.0007,0.0002,0.0027,0.0010,0.0023,0.00015,0.00015,0.0008,0.00015,0.00015,0.0004,0.0006,0.00015]
    ### group_5 std_loss_noisy is 0.0051###
    qchannel_loss_noisy_group_5 = [0.0008,0.01500,0.00010,0.00010,0.00010,0.00010,0.0002,0.0008,0.01500,0.01500,0.018,0.0002,0.0003,0.0005,0.0002,0.00010,0.00010,0.0006,0.0008,0.0007,0.0002,0.0027,0.0010,0.0023,0.00010,0.00010,0.0008,0.00010,0.00010,0.0004,0.0006,0.00010]

    ### run Centralized routing test ###
    for qchannel_loss_noisy in [qchannel_loss_noisy_group_5, qchannel_loss_noisy_group_4, qchannel_loss_noisy_group_3, qchannel_loss_noisy_group_2, qchannel_loss_noisy_group_1]: 
        fidelity_data_temp,centralized_routing_throughput, centralized_routing_time_cost = run_centralized_routing_test(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy,round)
        fidelity_data = fidelity_data.append(fidelity_data_temp)
        centralized_routing_throughputs.append(centralized_routing_throughput)
        centralized_routing_path_selection_time_cost.append(centralized_routing_time_cost)

    ### run Q-Cast routing test ###
    for qchannel_loss_noisy in [qchannel_loss_noisy_group_1, qchannel_loss_noisy_group_2, qchannel_loss_noisy_group_3, qchannel_loss_noisy_group_4, qchannel_loss_noisy_group_5]:
        fidelity_data_temp,QCast_throughput, QCast_time_cost = run_QCast_routing_test(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy,round)
        fidelity_data = fidelity_data.append(fidelity_data_temp)
        QCast_throughputs.append(QCast_throughput)
        QCast_path_selection_time_cost.append(QCast_time_cost)

    ### run Greedy routing test ###
    for qchannel_loss_noisy in [qchannel_loss_noisy_group_1, qchannel_loss_noisy_group_2, qchannel_loss_noisy_group_3, qchannel_loss_noisy_group_4, qchannel_loss_noisy_group_5]:
        fidelity_data_temp,greedy_throughput, greedy_time_cost = run_greedy_routing_test(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy,round)
        fidelity_data = fidelity_data.append(fidelity_data_temp)
        greedy_throughputs.append(greedy_throughput)
        greedy_path_selection_time_cost.append(greedy_time_cost)

    ### run SLMP routing test ###
    for qchannel_loss_noisy in [qchannel_loss_noisy_group_1, qchannel_loss_noisy_group_2, qchannel_loss_noisy_group_3, qchannel_loss_noisy_group_4, qchannel_loss_noisy_group_5]:
        fidelity_data_temp,SLMP_throughput, SLMP_time_cost = run_SLMP_routing_test(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy,round)
        fidelity_data = fidelity_data.append(fidelity_data_temp)
        SLMP_throughputs.append(SLMP_throughput)
        SLMP_path_selection_time_cost.append(SLMP_time_cost)

    
    fidelity_cr_loss_noisy = fidelity_data[fidelity_data['routing_algorithm']=="Centralized_Routing"].groupby("standard_deviation_of_qchannel_loss_noisy")['fidelity'].agg(fidelity='mean', sem='sem').reset_index()
    fidelity_qc_loss_noisy = fidelity_data[fidelity_data['routing_algorithm']=="Q-Cast"].groupby("standard_deviation_of_qchannel_loss_noisy")['fidelity'].agg(fidelity='mean', sem='sem').reset_index()
    fidelity_slmp_loss_noisy = fidelity_data[fidelity_data['routing_algorithm']=="SLMP"].groupby("standard_deviation_of_qchannel_loss_noisy")['fidelity'].agg(fidelity='mean', sem='sem').reset_index()
    fidelity_greedy_loss_noisy = fidelity_data[fidelity_data['routing_algorithm']=="Greedy"].groupby("standard_deviation_of_qchannel_loss_noisy")['fidelity'].agg(fidelity='mean', sem='sem').reset_index()
    entanglement_pair_consumption_cr_loss_noisy = fidelity_data[fidelity_data['routing_algorithm']=="Centralized_Routing"].groupby("standard_deviation_of_qchannel_loss_noisy")['entanglement_pair_consumption'].agg(entanglement_pair_consumption='mean').reset_index()
    entanglement_pair_consumption_qc_loss_noisy = fidelity_data[fidelity_data['routing_algorithm']=="Q-Cast"].groupby("standard_deviation_of_qchannel_loss_noisy")['entanglement_pair_consumption'].agg(entanglement_pair_consumption='mean').reset_index()
    entanglement_pair_consumption_slmp_loss_noisy = fidelity_data[fidelity_data['routing_algorithm']=="SLMP"].groupby("standard_deviation_of_qchannel_loss_noisy")['entanglement_pair_consumption'].agg(entanglement_pair_consumption='mean').reset_index()
    entanglement_pair_consumption_greedy_loss_noisy = fidelity_data[fidelity_data['routing_algorithm']=="Greedy"].groupby("standard_deviation_of_qchannel_loss_noisy")['entanglement_pair_consumption'].agg(entanglement_pair_consumption='mean').reset_index()
    throughput_cr_loss_noisy = pandas.DataFrame([[0.0031,centralized_routing_throughputs[4]],
                                           [0.0034,centralized_routing_throughputs[3]],
                                           [0.0038,centralized_routing_throughputs[2]],
                                           [0.0044,centralized_routing_throughputs[1]],
                                           [0.0051,centralized_routing_throughputs[0]]],
                                           columns=['standard_deviation_of_qchannel_loss_noisy', 'throughput'])
    throughput_qc_loss_noisy = pandas.DataFrame([[0.0031,QCast_throughputs[0]],
                                           [0.0034,QCast_throughputs[1]],
                                           [0.0038,QCast_throughputs[2]],
                                           [0.0044,QCast_throughputs[3]],
                                           [0.0051,QCast_throughputs[4]]],
                                           columns=['standard_deviation_of_qchannel_loss_noisy', 'throughput'])
    throughput_slmp_loss_noisy = pandas.DataFrame([[0.0031,SLMP_throughputs[0]],
                                           [0.0034,SLMP_throughputs[1]],
                                           [0.0038,SLMP_throughputs[2]],
                                           [0.0044,SLMP_throughputs[3]],
                                           [0.0051,SLMP_throughputs[4]]],
                                           columns=['standard_deviation_of_qchannel_loss_noisy', 'throughput'])
    throughput_greedy_loss_noisy = pandas.DataFrame([[0.0031,greedy_throughputs[0]],
                                           [0.0034,greedy_throughputs[1]],
                                           [0.0038,greedy_throughputs[2]],
                                           [0.0044,greedy_throughputs[3]],
                                           [0.0051,greedy_throughputs[4]]],
                                           columns=['standard_deviation_of_qchannel_loss_noisy', 'throughput'])


    fig,ax = plt.subplots(1,2,figsize=(25,10))
    plot_style = {'kind': 'line', 'grid': True,
      'title': "Routing Algorithm Comparison in Diversified Parameter Network"}
    ax[0].set_ylabel('fidelity')
    ax[1].set_ylabel('throughput(qps)')
    ax[1].set_xticks([0.0031,0.0034,0.0038,0.0044,0.0051])

    fidelity_cr_loss_noisy.plot(x='standard_deviation_of_qchannel_loss_noisy', y='fidelity', yerr='sem', ax=ax[0],label="Centralized_Routing", **plot_style)
    fidelity_qc_loss_noisy.plot(x='standard_deviation_of_qchannel_loss_noisy', y='fidelity',yerr='sem',ax=ax[0],label="Q-Cast", **plot_style)
    fidelity_slmp_loss_noisy.plot(x='standard_deviation_of_qchannel_loss_noisy', y='fidelity',yerr='sem',ax=ax[0],label="SLMP", **plot_style)
    fidelity_greedy_loss_noisy.plot(x='standard_deviation_of_qchannel_loss_noisy', y='fidelity',yerr='sem',ax=ax[0],label="Greedy", **plot_style)
    throughput_cr_loss_noisy.plot(x='standard_deviation_of_qchannel_loss_noisy', y='throughput', ax=ax[1],label="Centralized_Routing", **plot_style)
    throughput_qc_loss_noisy.plot(x='standard_deviation_of_qchannel_loss_noisy', y='throughput', ax=ax[1],label="Q-Cast", **plot_style)
    throughput_slmp_loss_noisy.plot(x='standard_deviation_of_qchannel_loss_noisy', y='throughput', ax=ax[1],label="SLMP", **plot_style)
    throughput_greedy_loss_noisy.plot(x='standard_deviation_of_qchannel_loss_noisy', y='throughput', ax=ax[1],label="Greedy", **plot_style)
    

    print(fidelity_cr_loss_noisy)
    print(fidelity_qc_loss_noisy)
    print(fidelity_slmp_loss_noisy)
    print(fidelity_greedy_loss_noisy)
    print(entanglement_pair_consumption_cr_loss_noisy)
    print(entanglement_pair_consumption_qc_loss_noisy)
    print(entanglement_pair_consumption_slmp_loss_noisy)
    print(entanglement_pair_consumption_greedy_loss_noisy)
    print(throughput_cr_loss_noisy)
    print(throughput_qc_loss_noisy)
    print(throughput_slmp_loss_noisy)
    print(throughput_greedy_loss_noisy)
    print("Centralized_Routing Time Cost: ")
    print(np.mean(centralized_routing_path_selection_time_cost))
    print("Q-Cast Time Cost: ")
    print(np.mean(QCast_path_selection_time_cost))
    print("SLMP Time Cost: ")
    print(np.mean(SLMP_path_selection_time_cost))
    print("Greedy Time Cost: ")
    print(np.mean(greedy_path_selection_time_cost))

    plt.show()

