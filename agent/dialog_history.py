
class DialogHistory:
    def __init__(self, sys_first=True) -> None:
        self.sys_first = sys_first
        # system side
        self.sys_utt = []
        self.sys_act = []
        
        # user side
        self.usr_utt = []
        self.usr_act = []

        # overall
        self.all_utt = []
        self.all_act = []

        self.start_of_most_recent_usr_acts = None
        self.start_of_most_recent_sys_acts = None        

        #Strategy planner
        self.next_sys_strategy_index = 0
        self.post_strategies_index = 0
        self.post_strategies = False

    def reload(self, sys_first=True):
        self.sys_first = sys_first
        # system side
        self.sys_utt = []
        self.sys_act = []
        # user side
        self.usr_utt = []
        self.usr_act = []

        # overall
        self.all_utt = []

    def update_usr_history(self, usr_utt=None, usr_act_list=None):
        """
        usr_act_list: list of user-acts
        """
        if usr_act_list:
            assert type(usr_act_list) is list 
        if self.sys_first:
            assert len(self.sys_utt) > len(self.usr_utt)
        else:
            assert len(self.sys_utt) == len(self.usr_utt)
        self.start_of_most_recent_usr_acts = len(self.usr_act)
        self.usr_utt.append(usr_utt)
        if usr_act_list:
            for act in usr_act_list:
                self.usr_act.append(act)
                self.all_act.append(act)
        self.all_utt.append(usr_utt)        

    def update_sys_history(self, sys_utt=None, sys_act_list=None):
        """
        sys_act_list: list of sys-acts
        """
        if sys_act_list:
            assert type(sys_act_list) is list
        if self.sys_first:
            assert len(self.sys_utt) == len(self.usr_utt)
        else:
            assert len(self.sys_utt) < len(self.usr_utt)
        self.start_of_most_recent_sys_acts = len(self.sys_act)
        self.sys_utt.append(sys_utt)
        if sys_act_list:
            for act in sys_act_list:
                self.sys_act.append(act)
                self.all_act.append(act)
        self.all_utt.append(sys_utt)
