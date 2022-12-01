class CentralControllerInfoTable():
    def __init__(self,network,dephase_rates,qchannel_loss_init,qchannel_loss_noisy):
        self.network = network
        self.request_time_limit = 1
        self.distribution_time_limit = 1
        self.swapping_teleportation_time_limit = 1
        Central_Controller = network.subcomponents["Central_Controller"]
        Controller_A = network.subcomponents["Controller_A"]
        Controller_B = network.subcomponents["Controller_B"]
        Controller_C = network.subcomponents["Controller_C"]
        Controller_D = network.subcomponents["Controller_D"]
        Controller_E = network.subcomponents["Controller_E"]
        Controller_F = network.subcomponents["Controller_F"]
        Controller_G = network.subcomponents["Controller_G"]
        Controller_H = network.subcomponents["Controller_H"]
        Controller_I = network.subcomponents["Controller_I"]
        Repeater_A = network.subcomponents["Repeater_A"]
        Repeater_B = network.subcomponents["Repeater_B"]
        Repeater_C = network.subcomponents["Repeater_C"]
        Repeater_D = network.subcomponents["Repeater_D"]
        Repeater_E = network.subcomponents["Repeater_E"]
        Repeater_F = network.subcomponents["Repeater_F"]
        Repeater_G = network.subcomponents["Repeater_G"]
        Repeater_H = network.subcomponents["Repeater_H"]
        Repeater_I = network.subcomponents["Repeater_I"]
        Repeater_J = network.subcomponents["Repeater_J"]
        Repeater_K = network.subcomponents["Repeater_K"]
        Repeater_L = network.subcomponents["Repeater_L"]
        Repeater_M = network.subcomponents["Repeater_M"]
        Repeater_N = network.subcomponents["Repeater_N"]
        Repeater_O = network.subcomponents["Repeater_O"]
        User_A = network.subcomponents["User_A"]
        User_B = network.subcomponents["User_B"]
        User_C = network.subcomponents["User_C"]
        User_D = network.subcomponents["User_D"]
        User_E = network.subcomponents["User_E"]

        self.central_controller = Central_Controller
        ### Conversion swapping success rate from dephase rate ###
        RA_ssr = 1-dephase_rates[0]
        RB_ssr = 1-dephase_rates[1]
        RC_ssr = 1-dephase_rates[2]
        RD_ssr = 1-dephase_rates[3]
        RE_ssr = 1-dephase_rates[4]
        RF_ssr = 1-dephase_rates[5]
        RG_ssr = 1-dephase_rates[6]
        RH_ssr = 1-dephase_rates[7]
        RI_ssr = 1-dephase_rates[8]
        RJ_ssr = 1-dephase_rates[9]
        RK_ssr = 1-dephase_rates[10]
        RL_ssr = 1-dephase_rates[11]
        RM_ssr = 1-dephase_rates[12]
        RN_ssr = 1-dephase_rates[13]
        RO_ssr = 1-dephase_rates[14]
        ###  Conversion link_state from qchannel_loss_init and qchannel_loss_noisy ###
        ### noisy limitation for 100km (dB/km) which is the result of noisy_limitation_test.py ###
        noisy_limitation = 0.2
        CA_RA_ls = 1-((qchannel_loss_init[0]+qchannel_loss_noisy[0]/noisy_limitation)/2)
        CA_RB_ls = 1-((qchannel_loss_init[1]+qchannel_loss_noisy[1]/noisy_limitation)/2)
        CA_RC_ls = 1-((qchannel_loss_init[2]+qchannel_loss_noisy[2]/noisy_limitation)/2)
        CA_UA_ls = 1-((qchannel_loss_init[3]+qchannel_loss_noisy[3]/noisy_limitation)/2)
        CB_RC_ls = 1-((qchannel_loss_init[4]+qchannel_loss_noisy[4]/noisy_limitation)/2)
        CB_RD_ls = 1-((qchannel_loss_init[5]+qchannel_loss_noisy[5]/noisy_limitation)/2)
        CB_RE_ls = 1-((qchannel_loss_init[6]+qchannel_loss_noisy[6]/noisy_limitation)/2)
        CB_UE_ls = 1-((qchannel_loss_init[7]+qchannel_loss_noisy[7]/noisy_limitation)/2)
        CC_RB_ls = 1-((qchannel_loss_init[8]+qchannel_loss_noisy[8]/noisy_limitation)/2)
        CC_RE_ls = 1-((qchannel_loss_init[9]+qchannel_loss_noisy[9]/noisy_limitation)/2)
        CC_RF_ls = 1-((qchannel_loss_init[10]+qchannel_loss_noisy[10]/noisy_limitation)/2)
        CD_RD_ls = 1-((qchannel_loss_init[11]+qchannel_loss_noisy[11]/noisy_limitation)/2)
        CD_RG_ls = 1-((qchannel_loss_init[12]+qchannel_loss_noisy[12]/noisy_limitation)/2)
        CD_RH_ls = 1-((qchannel_loss_init[13]+qchannel_loss_noisy[13]/noisy_limitation)/2)
        CE_RE_ls = 1-((qchannel_loss_init[14]+qchannel_loss_noisy[14]/noisy_limitation)/2)
        CE_RH_ls = 1-((qchannel_loss_init[15]+qchannel_loss_noisy[15]/noisy_limitation)/2)
        CE_RI_ls = 1-((qchannel_loss_init[16]+qchannel_loss_noisy[16]/noisy_limitation)/2)
        CE_UD_ls = 1-((qchannel_loss_init[17]+qchannel_loss_noisy[17]/noisy_limitation)/2)
        CF_RF_ls = 1-((qchannel_loss_init[18]+qchannel_loss_noisy[18]/noisy_limitation)/2)
        CF_RI_ls = 1-((qchannel_loss_init[19]+qchannel_loss_noisy[19]/noisy_limitation)/2)
        CF_RJ_ls = 1-((qchannel_loss_init[20]+qchannel_loss_noisy[20]/noisy_limitation)/2)
        CG_RH_ls = 1-((qchannel_loss_init[21]+qchannel_loss_noisy[21]/noisy_limitation)/2)
        CG_RK_ls = 1-((qchannel_loss_init[22]+qchannel_loss_noisy[22]/noisy_limitation)/2)
        CG_RL_ls = 1-((qchannel_loss_init[23]+qchannel_loss_noisy[23]/noisy_limitation)/2)
        CH_RI_ls = 1-((qchannel_loss_init[24]+qchannel_loss_noisy[24]/noisy_limitation)/2)
        CH_RL_ls = 1-((qchannel_loss_init[25]+qchannel_loss_noisy[25]/noisy_limitation)/2)
        CH_RM_ls = 1-((qchannel_loss_init[26]+qchannel_loss_noisy[26]/noisy_limitation)/2)
        CH_UC_ls = 1-((qchannel_loss_init[27]+qchannel_loss_noisy[27]/noisy_limitation)/2)
        CI_RL_ls = 1-((qchannel_loss_init[28]+qchannel_loss_noisy[28]/noisy_limitation)/2)
        CI_RN_ls = 1-((qchannel_loss_init[29]+qchannel_loss_noisy[29]/noisy_limitation)/2)
        CI_RO_ls = 1-((qchannel_loss_init[30]+qchannel_loss_noisy[30]/noisy_limitation)/2)
        CI_UB_ls = 1-((qchannel_loss_init[31]+qchannel_loss_noisy[31]/noisy_limitation)/2)
        
        
        self.domains = []
        self.domains.append(Domain("A",Controller_A,Repeater_A,CA_RA_ls,RA_ssr,Repeater_B,CA_RB_ls,RB_ssr,Repeater_C,CA_RC_ls,RC_ssr,User_A,CA_UA_ls))
        self.domains.append(Domain("B",Controller_B,Repeater_C,CB_RC_ls,RC_ssr,Repeater_D,CB_RD_ls,RD_ssr,Repeater_E,CB_RE_ls,RE_ssr,User_E,CB_UE_ls))
        self.domains.append(Domain("C",Controller_C,Repeater_B,CC_RB_ls,RB_ssr,Repeater_E,CC_RE_ls,RE_ssr,Repeater_F,CC_RF_ls,RF_ssr))
        self.domains.append(Domain("D",Controller_D,Repeater_D,CD_RD_ls,RD_ssr,Repeater_G,CD_RG_ls,RG_ssr,Repeater_H,CD_RH_ls,RH_ssr))
        self.domains.append(Domain("E",Controller_E,Repeater_E,CE_RE_ls,RE_ssr,Repeater_H,CE_RH_ls,RH_ssr,Repeater_I,CE_RI_ls,RI_ssr,User_D,CE_UD_ls))
        self.domains.append(Domain("F",Controller_F,Repeater_F,CF_RF_ls,RF_ssr,Repeater_I,CF_RI_ls,RI_ssr,Repeater_J,CF_RJ_ls,RJ_ssr))
        self.domains.append(Domain("G",Controller_G,Repeater_H,CG_RH_ls,RH_ssr,Repeater_K,CG_RK_ls,RK_ssr,Repeater_L,CG_RL_ls,RL_ssr))
        self.domains.append(Domain("H",Controller_H,Repeater_I,CH_RI_ls,RI_ssr,Repeater_L,CH_RL_ls,RL_ssr,Repeater_M,CH_RM_ls,RM_ssr,User_C,CH_UC_ls))
        self.domains.append(Domain("I",Controller_I,Repeater_L,CI_RL_ls,RL_ssr,Repeater_N,CI_RN_ls,RN_ssr,Repeater_O,CI_RO_ls,RO_ssr,User_B,CI_UB_ls))        

    def getNeighborRepeaters(self,repeater):
        Neighbor_Repeaters = []
        for domain in self.domains:
            for instance in domain.instances:
                if repeater == instance.node:
                    for i in range(1,len(domain.instances)):
                        if domain.instances[i].node != repeater and i != 4:
                            Neighbor_Repeaters.append(domain.instances[i].node)
        return Neighbor_Repeaters
    
    def getDomainControllerbyRepeaters(self,repeater_1,repeater_2):
        count = 0
        for domain in self.domains:
            for instance in domain.instances:
               if repeater_1 == instance.node or repeater_2 == instance.node:
                   count = count +1
            if count == 1:
                count = 0
            if count == 2:
                return domain.instances[0].node
        return "None"

    def is2RepeatersinSameDomain(self,repeater_1,repeater_2):
        count = 0
        for domain in self.domains:
            for instance in domain.instances:
               if repeater_1 == instance.node or repeater_2 == instance.node:
                   count = count +1
            if count == 1:
                count = 0
            if count == 2:
                return True
        return False

    def is3RepeatersinSameDomain(self,repeater_1,repeater_2,repeater_3):
        count = 0
        for domain in self.domains:
            for instance in domain.instances:
                if repeater_1 == instance.node or repeater_2 == instance.node or repeater_3 == instance.node:
                    count = count +1
            if count == 1 or count == 2:
                count = 0
            if count == 3:
                return True
        return False

    def setInstanceMemState(self,aim_instance,mems,mem_state):
        for domain in self.domains:
            for instance in domain.instances:
                if aim_instance == instance.node:
                    for aim_mem in mems:
                        for target_mem in instance.mems:
                            if aim_mem == target_mem.mem_name:
                                target_mem.state = mem_state

    def getUserLocalController(self,user):
        for domain in self.domains:
            for instance in domain.instances:
                if user == instance.node:
                    return domain.instances[0].node

    def setInstanceMem_aimpair_aimcommuni_distristate(self,aim_instance,mems,aim_pairs,aim_communication,distribution_state):
        for domain in self.domains:
            for instance in domain.instances:
                if aim_instance == instance.node:
                    for index in range(len(mems)):
                        for target_mem in instance.mems:
                            if mems[index] == target_mem.mem_name:
                                target_mem.aim_pair = aim_pairs[index]
                                target_mem.aim_communication = aim_communication
                                target_mem.distribution_state = distribution_state

    def setInstanceMemTeleporationState(self,aim_instance,mem,teleportation_state):
        for domain in self.domains:
            for instance in domain.instances:
                if aim_instance == instance.node:
                    for target_mem in instance.mems:
                        if mem == target_mem.mem_name:
                            target_mem.teleportation_state = teleportation_state
 
    def setInstanceMemSwappingState(self,aim_instance,mems,swapping_state):
        for domain in self.domains:
            for instance in domain.instances:
                if aim_instance == instance.node:
                    for aim_mem in mems:
                        for target_mem in instance.mems:
                            if aim_mem == target_mem.mem_name:
                                target_mem.swapping_state = swapping_state

    def setInstanceStateSingle(self,aim_instance,controller,device_state):
        self.domains[ord(controller.name.split("_")[1])-65].getInstancebyName(aim_instance.name).device_state = device_state

    def setInstanceState(self,aim_instance,device_state):
        for domain in self.domains:
            for instance in domain.instances:
                if aim_instance == instance.node:
                    instance.device_state = device_state

    def clear(self,aim_instance,mems): 
        for domain in self.domains:
            for instance in domain.instances:
                if aim_instance == instance.node:
                    for mem in mems:
                        for target_mem in instance.mems:
                            if mem == target_mem.mem_name:
                                target_mem.aim_pair = None
                                target_mem.aim_communication = None
                                target_mem.distribution_state = None
                                target_mem.teleportation_state = None
                                target_mem.swapping_state = None
                                target_mem.state = "idle"
                
               


class Domain():
    def __init__(self,domain_name,controller,repeater_1,link_state_1,swapping_success_rate_1,repeater_2,link_state_2,swapping_success_rate_2,repeater_3,link_state_3,swapping_success_rate_3,user = None,link_state_4 = None):
         self.domain_name = domain_name
         self.instances = []
         self.instances.append(Instance(controller))
         self.instances.append(Instance(repeater_1,link_state_1,swapping_success_rate_1))
         self.instances.append(Instance(repeater_2,link_state_2,swapping_success_rate_2))
         self.instances.append(Instance(repeater_3,link_state_3,swapping_success_rate_3))
         if user is not None:
             self.instances.append(Instance(user,link_state_4))

    def getInstancebyName(self,instance_name):
         for instance in self.instances:
              if instance.node.name == instance_name:
                  return instance
 



class Instance():
    def __init__(self,node,link_state=None,swapping_success_rate=None,device_state="normal"):
        self.node = node
        self.mems = []
        mem_state_1 = "idle"
        mem_state_2 = "idle"
        if  node.qmemory.mem_positions[1].in_use:
            mem_state_1 = "occupy"
        if  node.qmemory.mem_positions[2].in_use:
            mem_state_2 = "occupy"
        self.mems.append(QuantumMem(1,mem_state_1))
        self.mems.append(QuantumMem(2,mem_state_2))
        self.device_state = device_state
        self.link_state = link_state
        self.swapping_success_rate = swapping_success_rate


class QuantumMem():
    def __init__(self, mem_name, state,aim_pair = None,aim_communication = None,distribution_state = None,swapping_state = None,teleportation_state = None):
        self.mem_name = mem_name
        self.state = state
        self.aim_pair = aim_pair
        self.aim_communication = aim_communication
        self.distribution_state = distribution_state
        self.swapping_state = swapping_state
        self.teleporation_state =teleportation_state
    def add_aim_pair(self,aim_pair):
        self.aim_pair = aim_pair
    def add_aim_communication(self,aim_communication):
        self.aim_communication = aim_communication
    def add_distribution_state(self,distribution_state):
        self.distribution_state = distribution_state
    def add_swapping_state(self,swapping_state):
        self.swapping_state = swapping_state
    def add_teleportation_state(self,teleportation_state):
        self.teleportation_state = teleportation_state


class DomainShortestPathTable():
     def __init__(self):
          ### column_number 0~8 means src_domain A~I, row_number 0~8 means dst_domain A~I ,the values are src->dst shortest paths###
          self.table = [[0 for i in range(9)] for j in range(9)]
          self.table[1][0] = ["A-B"]
          self.table[2][0] = ["A-C"]
          self.table[3][0] = ["A-B-D"]
          self.table[4][0] = ["A-B-E","A-C-E"]
          self.table[5][0] = ["A-C-F"]
          self.table[6][0] = ["A-B-D-G","A-B-E-G","A-C-E-G"]
          self.table[7][0] = ["A-C-F-H","A-C-E-H","A-B-E-H"]
          self.table[8][0] = ["A-B-D-G-I","A-B-E-G-I","A-B-E-H-I","A-C-E-H-I","A-C-F-H-I","A-C-E-G-I"]
          self.table[0][1] = ["B-A"]
          self.table[2][1] = ["B-C"]
          self.table[3][1] = ["B-D"]
          self.table[4][1] = ["B-E"]
          self.table[5][1] = ["B-E-F","B-C-F"]
          self.table[6][1] = ["B-E-G","B-D-G"]
          self.table[7][1] = ["B-E-H"]
          self.table[8][1] = ["B-D-G-I","B-E-G-I","B-E-H-I"]
          self.table[0][2] = ["C-A"]
          self.table[1][2] = ["C-B"]
          self.table[3][2] = ["C-B-D","C-E-D"]
          self.table[4][2] = ["C-E"]
          self.table[5][2] = ["C-F"]
          self.table[6][2] = ["C-E-G"]
          self.table[7][2] = ["C-E-H","C-F-H"]
          self.table[8][2] = ["C-E-H-I","C-F-H-I","C-E-G-I"]
          self.table[0][3] = ["D-B-A"]
          self.table[1][3] = ["D-B"]
          self.table[2][3] = ["D-B-C","D-E-C"]
          self.table[4][3] = ["D-E"]
          self.table[5][3] = ["D-E-F"]
          self.table[6][3] = ["D-G"]
          self.table[7][3] = ["D-G-H","D-E-H"]
          self.table[8][3] = ["D-G-I"]
          self.table[0][4] = ["E-B-A","E-C-A"]
          self.table[1][4] = ["E-B"]
          self.table[2][4] = ["E-C"]
          self.table[3][4] = ["E-D"]
          self.table[5][4] = ["E-F"]
          self.table[6][4] = ["E-G"]
          self.table[7][4] = ["E-H"]
          self.table[8][4] = ["E-G-I","E-H-I"]
          self.table[0][5] = ["F-C-A"]
          self.table[1][5] = ["F-E-B","F-C-B"]
          self.table[2][5] = ["F-C"]
          self.table[3][5] = ["F-E-D"]
          self.table[4][5] = ["F-E"]
          self.table[6][5] = ["F-E-G","F-H-G"]
          self.table[7][5] = ["F-H"]
          self.table[8][5] = ["F-H-I"]
          self.table[0][6] = ["G-D-B-A","G-E-B-A","G-E-C-A"]
          self.table[1][6] = ["G-E-B","G-D-B"]
          self.table[2][6] = ["G-E-C"]
          self.table[3][6] = ["G-D"]
          self.table[4][6] = ["G-E"]
          self.table[5][6] = ["G-E-F","G-H-F"]
          self.table[7][6] = ["G-H"]
          self.table[8][6] = ["G-I"]
          self.table[0][7] = ["H-F-C-A","H-E-C-A","H-E-B-A"]
          self.table[1][7] = ["H-E-B"]
          self.table[2][7] = ["H-E-C","H-F-C"]
          self.table[3][7] = ["H-G-D","H-E-D"]
          self.table[4][7] = ["H-E"]
          self.table[5][7] = ["H-F"]
          self.table[6][7] = ["H-G"]
          self.table[8][7] = ["H-I"]
          self.table[0][8] = ["I-G-D-B-A","I-G-E-B-A","I-H-E-B-A","I-H-E-C-A","I-H-F-C-A","I-G-E-C-A"]
          self.table[1][8] = ["I-G-D-B","I-G-E-B","I-H-E-B"]
          self.table[2][8] = ["I-H-E-C","I-H-F-C","I-G-E-C"]
          self.table[3][8] = ["I-G-D"]
          self.table[4][8] = ["I-G-E","I-H-E"]
          self.table[5][8] = ["I-H-F"]
          self.table[6][8] = ["I-G"]
          self.table[7][8] = ["I-H"]


class DomainEdgeRepeaterTable():
     def __init__(self):
          ### column_number 0~8 means domain A~I, row_number 0~8 means domain A~I ,the values is edge repeater of two domains ###     
          self.table = [[0 for i in range(9)] for j in range(9)]
          self.table[1][0] = "Repeater_C"
          self.table[2][0] = "Repeater_B"
          self.table[0][1] = "Repeater_C"
          self.table[2][1] = "Repeater_E"
          self.table[3][1] = "Repeater_D"
          self.table[4][1] = "Repeater_E"
          self.table[0][2] = "Repeater_B"
          self.table[1][2] = "Repeater_E"
          self.table[4][2] = "Repeater_E"
          self.table[5][2] = "Repeater_F"
          self.table[1][3] = "Repeater_D"
          self.table[4][3] = "Repeater_H"
          self.table[6][3] = "Repeater_H"
          self.table[1][4] = "Repeater_E"
          self.table[2][4] = "Repeater_E"
          self.table[3][4] = "Repeater_H"
          self.table[5][4] = "Repeater_I"
          self.table[6][4] = "Repeater_H"
          self.table[7][4] = "Repeater_I"
          self.table[2][5] = "Repeater_F"
          self.table[4][5] = "Repeater_I"
          self.table[7][5] = "Repeater_I"
          self.table[3][6] = "Repeater_H"
          self.table[4][6] = "Repeater_H"
          self.table[7][6] = "Repeater_L"
          self.table[8][6] = "Repeater_L"
          self.table[4][7] = "Repeater_I"
          self.table[5][7] = "Repeater_I"
          self.table[6][7] = "Repeater_L"
          self.table[8][7] = "Repeater_L"
          self.table[6][8] = "Repeater_L"
          self.table[7][8] = "Repeater_L"
          
