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

1,Generally speaking, distributed routing algorithm can only run in distributed topology, but in order to eliminate the interference of inconsistent topology between centralized_routing and distributed_routing, obtain more accurate experimental results,
this experiment run distributed_routing_algorithm(Q-cast, Greedy, SLMP) in a pseudo_distributed_topo(which is a centralized topo, but we code to hide the controller and the distributed_routing_algorithm will think the topo as a distributed topo.)

2,this run Centralized-routing, Q-cast, Greedy, SLMP in a Equivalent Parameter Network which is every node in network has the same Environment-Parameter.

"""
if __name__ == '__main__':
   # RAdepo =0.01 
   # RBdepo =0.01
   # RCdepo =0.01
   # RDdepo =0.01
   # REdepo =0.01
   # RFdepo =0.01
   # RGdepo =0.01
   # RHdepo =0.01
   # RIdepo =0.01
   # RJdepo =0.01
   # RKdepo =0.01
   # RLdepo =0.01
   # RMdepo =0.01
   # RNdepo =0.01
   # ROdepo =0.01
   # CAdepo =0.01 
   # CBdepo =0.01
   # CCdepo =0.01
   # CDdepo =0.01
   # CEdepo =0.01
   # CFdepo =0.01
   # CGdepo =0.01
   # CHdepo =0.01
   # CIdepo =0.01
   # UAdepo =0.01 
   # UBdepo =0.01
   # UCdepo =0.01
   # UDdepo =0.01
   # UEdepo =0.01

   # RAdeph =0.01
   # RBdeph =0.01
   # RCdeph =0.01
   # RDdeph =0.01
   # REdeph =0.01
   # RFdeph =0.01
   # RGdeph =0.01
   # RHdeph =0.01
   # RIdeph =0.01
   # RJdeph =0.01
   # RKdeph =0.01
   # RLdeph =0.01
   # RMdeph =0.01
   # RNdeph =0.01
   # ROdeph =0.01
   # CAdeph =0.01
   # CBdeph =0.01
   # CCdeph =0.01
   # CDdeph =0.01
   # CEdeph =0.01
   # CFdeph =0.01
   # CGdeph =0.01
   # CHdeph =0.01
   # CIdeph =0.01
   # UAdeph =0.01
   # UBdeph =0.01
   # UCdeph =0.01
   # UDdeph =0.01
   # UEdeph =0.01

   # CARA_li =0.01 
   # CARB_li =0.01 
   # CARC_li =0.01
   # CAUA_li =0.01
   # CBRC_li =0.01  
   # CBRD_li =0.01
   # CBRE_li =0.01
   # CBUE_li =0.01 
   # CCRB_li =0.01
   # CCRE_li =0.01
   # CCRF_li =0.01
   # CDRD_li =0.01
   # CDRG_li =0.01
   # CDRH_li =0.01
   # CERE_li =0.01
   # CERH_li =0.01
   # CERI_li =0.01
   # CEUD_li =0.01
   # CFRF_li =0.01
   # CFRI_li =0.01
   # CFRJ_li =0.01
   # CGRH_li =0.01
   # CGRK_li =0.01
   # CGRL_li =0.01
   # CHRI_li =0.01
   # CHRL_li =0.01
   # CHRM_li =0.01
   # CHUC_li =0.01
   # CIRL_li =0.01
   # CIRN_li =0.01
   # CIRO_li =0.01
   # CIUB_li =0.01

   # CARA_ln =0.0001
   # CARB_ln =0.0001
   # CARC_ln =0.0001
   # CAUA_ln =0.0001
   # CBRC_ln =0.0001
   # CBRD_ln =0.0001
   # CBRE_ln =0.0001
   # CBUE_ln =0.0001
   # CCRB_ln =0.0001
   # CCRE_ln =0.0001
   # CCRF_ln =0.0001
   # CDRD_ln =0.0001
   # CDRG_ln =0.0001
   # CDRH_ln =0.0001
   # CERE_ln =0.0001
   # CERH_ln =0.0001
   # CERI_ln =0.0001
   # CEUD_ln =0.0001
   # CFRF_ln =0.0001
   # CFRI_ln =0.0001
   # CFRJ_ln =0.0001
   # CGRH_ln =0.0001
   # CGRK_ln =0.0001
   # CGRL_ln =0.0001
   # CHRI_ln =0.0001
   # CHRL_ln =0.0001
   # CHRM_ln =0.0001
   # CHUC_ln =0.0001
   # CIRL_ln =0.0001
   # CIRN_ln =0.0001
   # CIRO_ln =0.0001
   # CIUB_ln =0.0001
    
   # depolar_rates = [RAdepo,RBdepo,RCdepo,RDdepo,REdepo,RFdepo,RGdepo,RHdepo,RIdepo,RJdepo,RKdepo,RLdepo,RMdepo,RNdepo,ROdepo,CAdepo,CBdepo,CCdepo,CDdepo,CEdepo,CFdepo,CGdepo,CHdepo,CIdepo,UAdepo,UBdepo,UCdepo,UDdepo,UEdepo]
   # dephase_rates = [RAdeph,RBdeph,RCdeph,RDdeph,REdeph,RFdeph,RGdeph,RHdeph,RIdeph,RJdeph,RKdeph,RLdeph,RMdeph,RNdeph,ROdeph,CAdeph,CBdeph,CCdeph,CDdeph,CEdeph,CFdeph,CGdeph,CHdeph,CIdeph,UAdeph,UBdeph,UCdeph,UDdeph,UEdeph]
   # qchannel_loss_init = [CARA_li,CARB_li,CARC_li,CAUA_li,CBRC_li,CBRD_li,CBRE_li,CBUE_li,CCRB_li,CCRE_li,CCRF_li,CDRD_li,CDRG_li,CDRH_li,CERE_li,CERH_li,CERI_li,CEUD_li,CFRF_li,CFRI_li,CFRJ_li,CGRH_li,CGRK_li,CGRL_li,CHRI_li,CHRL_li,CHRM_li,CHUC_li,CIRL_li,CIRN_li,CIRO_li,CIUB_li]
   # qchannel_loss_noisy = [CARA_ln,CARB_ln,CARC_ln,CAUA_ln,CBRC_ln,CBRD_ln,CBRE_ln,CBUE_ln,CCRB_ln,CCRE_ln,CCRF_ln,CDRD_ln,CDRG_ln,CDRH_ln,CERE_ln,CERH_ln,CERI_ln,CEUD_ln,CFRF_ln,CFRI_ln,CFRJ_ln,CGRH_ln,CGRK_ln,CGRL_ln,CHRI_ln,CHRL_ln,CHRM_ln,CHUC_ln,CIRL_ln,CIRN_ln,CIRO_ln,CIUB_ln]


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

