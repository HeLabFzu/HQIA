import sys
sys.path.append("..")

import netsquid as ns
import pandas
import pydynaa
from util.RoutingComparison import run_centralized_routing_test, run_QCast_routing_test,run_SLMP_routing_test,run_greedy_routing_test
"""
This program is for researching the performance of CER with integrated environmental parameters.
This program data is for matlab 3d_heat_map.
"""
if __name__ == '__main__':
    fidelity_data = pandas.DataFrame()
    centralized_routing_throughputs = []
    round = 300
    depolar_rates = [0.004,0.005,0.001,0.002,0.009,0.008,0.009,0.003,0.001,0.008,0.006,0.001,0.008,0.006,0.003,0.003,0.002,0.004,0.005,0.006,0.003,0.002,0.005,0.009,0.006,0.001,0.002,0.004,0.006]

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
    for qchannel_loss_init in [qchannel_loss_init_group_5, qchannel_loss_init_group_4, qchannel_loss_init_group_3, qchannel_loss_init_group_2, qchannel_loss_init_group_1]:
        ### Because the data can only be grouped by one dimension, manually combine qchannel_loss_noisy and dephase_rates, and run the experiment 25 times to get data ###
        qchannel_loss_noisy = qchannel_loss_noisy_group_1
       # qchannel_loss_noisy = qchannel_loss_noisy_group_2
       # qchannel_loss_noisy = qchannel_loss_noisy_group_3
       # qchannel_loss_noisy = qchannel_loss_noisy_group_4
       # qchannel_loss_noisy = qchannel_loss_noisy_group_5
        dephase_rates = dephase_rates_group_1
       # dephase_rates = dephase_rates_group_2
       # dephase_rates = dephase_rates_group_3
       # dephase_rates = dephase_rates_group_4
       # dephase_rates = dephase_rates_group_5
        fidelity_data_temp,centralized_routing_throughput,_ = run_centralized_routing_test(depolar_rates,dephase_rates,qchannel_loss_init,qchannel_loss_noisy,round)
        fidelity_data = fidelity_data.append(fidelity_data_temp)
        centralized_routing_throughputs.append(centralized_routing_throughput)

    fidelity_cr = fidelity_data[fidelity_data['routing_algorithm']=="Centralized_Routing"].groupby("standard_deviation_of_qchannel_loss_init")['fidelity'].agg(fidelity='mean', sem='sem').reset_index()

    print("std_loss_noisy is 0.0031")
   # print("std_loss_noisy is 0.0034")
   # print("std_loss_noisy is 0.0038")
   # print("std_loss_noisy is 0.0044")
   # print("std_loss_noisy is 0.0051")

    print("std_dephase is 0.096")
   # print("std_dephase is 0.144")
   # print("std_dephase is 0.192")
   # print("std_dephase is 0.241")
   # print("std_dephase is 0.290")
    print("Centralized_Routing data")
    print(fidelity_cr)
    print(centralized_routing_throughputs[4],centralized_routing_throughputs[3],centralized_routing_throughputs[2],centralized_routing_throughputs[1],centralized_routing_throughputs[0])
