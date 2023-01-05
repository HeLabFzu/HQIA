import sys
import gc
sys.path.append("..")

import netsquid as ns
import pandas
import pydynaa
import time

from util.RoutingComparison import run_centralized_routing_test, run_QCast_routing_test,run_SLMP_routing_test,run_greedy_routing_test
from matplotlib import pyplot as plt
"""
This program explores routing in equivalent parameter network.

The program take about 2 minutes to complete.
"""
if __name__ == '__main__':

    ################################
    ####  avg_loss_noisy test ###
    ###############################
    fidelity_data = pandas.DataFrame()
    centralized_routing_throughputs = []
    QCast_throughputs = []
    SLMP_throughputs = []
    greedy_throughputs = []
    qchannel_loss_noisy = []
    for i in range(32):
        qchannel_loss_noisy.append(0.001)

    depolar_rates = []
    for i in range(29):
        depolar_rates.append(0.1)

    dephase_rates = []
    for i in range(29):
        dephase_rates.append(0.1)

    qchannel_loss_init = []
    for i in range(32):
        qchannel_loss_init.append(0.01)

    ### run Centralized routing test ###
    fidelity_data_temp,centralized_routing_throughput, centralized_routing_time_cost = run_centralized_routing_test(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy,300)
    fidelity_data = fidelity_data.append(fidelity_data_temp)
    centralized_routing_throughputs.append(centralized_routing_throughput)

    ### run Greedy routing test ###
    fidelity_data_temp,greedy_throughput, greedy_time_cost = run_greedy_routing_test(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy,300)
    fidelity_data = fidelity_data.append(fidelity_data_temp)
    greedy_throughputs.append(greedy_throughput)

    ### run Q-Cast routing test ###
    fidelity_data_temp,QCast_throughput, QCast_time_cost = run_QCast_routing_test(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy,300)
    fidelity_data = fidelity_data.append(fidelity_data_temp)
    QCast_throughputs.append(QCast_throughput)
    print(fidelity_data)

    ### run SLMP routing test ###
    fidelity_data_temp,SLMP_throughput, SLMP_time_cost = run_SLMP_routing_test(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy,300)
    fidelity_data = fidelity_data.append(fidelity_data_temp)
    SLMP_throughputs.append(SLMP_throughput)


   
    fidelity_data_bar = fidelity_data.groupby("routing_algorithm")['fidelity'].agg(fidelity='mean', sem='sem').reset_index() 
    entanglement_pair_consumption_data = fidelity_data.groupby("routing_algorithm")['entanglement_pair_consumption'].agg(entanglement_pair_consumption='mean').reset_index()
    throughput_data_bar = pandas.DataFrame([["Centralized_Routing",centralized_routing_throughputs[0]],
                                            ["Greedy",greedy_throughputs[0]],
                                           ["Q-Cast",QCast_throughputs[0]],
                                           ["SLMP",SLMP_throughputs[0]]],
                                           columns=['routing_algorithm', 'throughput'])
    
    fig,ax = plt.subplots(1,2,figsize=(25,10))
    plot_style = {'kind': 'bar', 'grid': True,
      'title': "Routing Algorithm Comparison in Equivalent Parameter Network"}
    ax[0].set_ylabel('fidelity')
    ax[1].set_ylabel('throughput(qps)')

    fidelity_data_bar.plot(x='routing_algorithm', y='fidelity',yerr='sem', ax=ax[0], **plot_style)
    ax[0].tick_params(axis='x', labelrotation=0)
    throughput_data_bar.plot(x='routing_algorithm', y='throughput', ax=ax[1], **plot_style)
    ax[1].tick_params(axis='x', labelrotation=0)

    print(fidelity_data_bar)
    print(entanglement_pair_consumption_data)
    print(throughput_data_bar)
    plt.show()

