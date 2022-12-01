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
1,Generally speaking, distributed routing algorithm can only run in distributed topology, but in order to eliminate the interference of inconsistent topology between centralized_routing and distributed_routing, obtain more accurate experimental results,
this experiment run distributed_routing_algorithm(Q-cast, Greedy, SLMP) in a pseudo_distributed_topo(which is a centralized topo, but we code to hide the controller and the distributed_routing_algorithm will think the topo as a distributed topo.)

2,this run Centralized-routing, Q-cast, Greedy, SLMP in a Diversified Parameter Network which is every node in network has the different Environment-Parameter.

"""
if __name__ == '__main__':
  #  RAdepo =0.004
  #  RBdepo =0.005
  #  RCdepo =0.001
  #  RDdepo =0.002
  #  REdepo =0.009
  #  RFdepo =0.008
  #  RGdepo =0.009
  #  RHdepo =0.003
  #  RIdepo =0.001
  #  RJdepo =0.008
  #  RKdepo =0.006
  #  RLdepo =0.001
  #  RMdepo =0.008
  #  RNdepo =0.006
  #  ROdepo =0.003
  #  CAdepo =0.003
  #  CBdepo =0.002
  #  CCdepo =0.004
  #  CDdepo =0.005
  #  CEdepo =0.006
  #  CFdepo =0.003
  #  CGdepo =0.002
  #  CHdepo =0.005
  #  CIdepo =0.009
  #  UAdepo =0.006
  #  UBdepo =0.001
  #  UCdepo =0.002
  #  UDdepo =0.004
  #  UEdepo =0.006

  #  RAdeph =0.09
  #  RBdeph =0.52
  #  RCdeph =0.01
  #  RDdeph =0.01
  #  REdeph =0.61
  #  RFdeph =0.21
  #  RGdeph =0.11
  #  RHdeph =0.01
  #  RIdeph =0.01
  #  RJdeph =0.09
  #  RKdeph =0.03
  #  RLdeph =0.01
  #  RMdeph =0.02
  #  RNdeph =0.14
  #  ROdeph =0.07
  #  CAdeph =0.02
  #  CBdeph =0.03
  #  CCdeph =0.04
  #  CDdeph =0.02
  #  CEdeph =0.05
  #  CFdeph =0.06
  #  CGdeph =0.02
  #  CHdeph =0.09
  #  CIdeph =0.04
  #  UAdeph =0.01
  #  UBdeph =0.01
  #  UCdeph =0.05
  #  UDdeph =0.06
  #  UEdeph =0.07


  #  CARA_li =0.008 
  #  CARB_li =0.14
  #  CARC_li =0.0025
  #  CAUA_li =0.0025
  #  CBRC_li =0.0025 
  #  CBRD_li =0.0025
  #  CBRE_li =0.002
  #  CBUE_li =0.008
  #  CCRB_li =0.14
  #  CCRE_li =0.14
  #  CCRF_li =0.18
  #  CDRD_li =0.002
  #  CDRG_li =0.003
  #  CDRH_li =0.005
  #  CERE_li =0.002
  #  CERH_li =0.0025
  #  CERI_li =0.0025
  #  CEUD_li =0.006
  #  CFRF_li =0.008
  #  CFRI_li =0.007
  #  CFRJ_li =0.002
  #  CGRH_li =0.047
  #  CGRK_li =0.010
  #  CGRL_li =0.053
  #  CHRI_li =0.0025
  #  CHRL_li =0.0025
  #  CHRM_li =0.008
  #  CHUC_li =0.002
  #  CIRL_li =0.0025
  #  CIRN_li =0.004
  #  CIRO_li =0.006
  #  CIUB_li =0.0025

  #  CARA_ln =0.0006
  #  CARB_ln =0.0006
  #  CARC_ln =0.0002
  #  CAUA_ln =0.0001
  #  CBRC_ln =0.0003
  #  CBRD_ln =0.0003
  #  CBRE_ln =0.0001
  #  CBUE_ln =0.0005
  #  CCRB_ln =0.0005
  #  CCRE_ln =0.0006
  #  CCRF_ln =0.0013
  #  CDRD_ln =0.0001
  #  CDRG_ln =0.0003
  #  CDRH_ln =0.0003
  #  CERE_ln =0.0002
  #  CERH_ln =0.0002
  #  CERI_ln =0.0003
  #  CEUD_ln =0.0004
  #  CFRF_ln =0.0006
  #  CFRI_ln =0.0004
  #  CFRJ_ln =0.0003
  #  CGRH_ln =0.0046
  #  CGRK_ln =0.0012
  #  CGRL_ln =0.0057
  #  CHRI_ln =0.0002
  #  CHRL_ln =0.0001
  #  CHRM_ln =0.0006
  #  CHUC_ln =0.0005
  #  CIRL_ln =0.0001
  #  CIRN_ln =0.0035
  #  CIRO_ln =0.0014
  #  CIUB_ln =0.0001



 
   # depolar_rates = [RAdepo,RBdepo,RCdepo,RDdepo,REdepo,RFdepo,RGdepo,RHdepo,RIdepo,RJdepo,RKdepo,RLdepo,RMdepo,RNdepo,ROdepo,CAdepo,CBdepo,CCdepo,CDdepo,CEdepo,CFdepo,CGdepo,CHdepo,CIdepo,UAdepo,UBdepo,UCdepo,UDdepo,UEdepo]
   # dephase_rates = [RAdeph,RBdeph,RCdeph,RDdeph,REdeph,RFdeph,RGdeph,RHdeph,RIdeph,RJdeph,RKdeph,RLdeph,RMdeph,RNdeph,ROdeph,CAdeph,CBdeph,CCdeph,CDdeph,CEdeph,CFdeph,CGdeph,CHdeph,CIdeph,UAdeph,UBdeph,UCdeph,UDdeph,UEdeph]
   # qchannel_loss_init = [CARA_li,CARB_li,CARC_li,CAUA_li,CBRC_li,CBRD_li,CBRE_li,CBUE_li,CCRB_li,CCRE_li,CCRF_li,CDRD_li,CDRG_li,CDRH_li,CERE_li,CERH_li,CERI_li,CEUD_li,CFRF_li,CFRI_li,CFRJ_li,CGRH_li,CGRK_li,CGRL_li,CHRI_li,CHRL_li,CHRM_li,CHUC_li,CIRL_li,CIRN_li,CIRO_li,CIUB_li]
   # qchannel_loss_noisy = [CARA_ln,CARB_ln,CARC_ln,CAUA_ln,CBRC_ln,CBRD_ln,CBRE_ln,CBUE_ln,CCRB_ln,CCRE_ln,CCRF_ln,CDRD_ln,CDRG_ln,CDRH_ln,CERE_ln,CERH_ln,CERI_ln,CEUD_ln,CFRF_ln,CFRI_ln,CFRJ_ln,CGRH_ln,CGRK_ln,CGRL_ln,CHRI_ln,CHRL_ln,CHRM_ln,CHUC_ln,CIRL_ln,CIRN_ln,CIRO_ln,CIUB_ln]



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

