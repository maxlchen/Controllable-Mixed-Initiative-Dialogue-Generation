"""
Strategy Planner
"""
import sys
sys.path.insert(1, '../')
import torch
from persuasion_config import PRE_STRATEGY_ORDER, STRATEGY_ORDER, POST_STRATEGY_ORDER, ACT_TO_STRATEGY_DICT
import random
import copy
import pickle as pkl
import numpy as np
import utils
import nltk
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

def load_pkl(dir):
    with open(dir, "rb") as fh:
        obj = pkl.load(fh)
    return obj

class StrategyPlanner(object):
    # base generator
    def __init__(self, max_cycle=1):
        self.pre_strategy_dialogact_order = PRE_STRATEGY_ORDER
        self.post_strategy_dialogact_order = POST_STRATEGY_ORDER
        self.strategy_order = copy.deepcopy(STRATEGY_ORDER)
        self.max_cycle = max_cycle
        #TODO 
        assert max_cycle == 1, f"max_cycle only support 1 for now"

    def is_pre_strategy(self, history):
        return len(history.sys_act) < len(self.pre_strategy_dialogact_order)

    def start_post_strategy(self, history):
        """
        condition to stop the persuasion, and start the post strategy process
        """
        if len(history.sys_act) < (len(self.pre_strategy_dialogact_order) + self.max_cycle * len(self.strategy_order)):
            # pre-strategy finished, and max cycle of strategies
            return False
        else:
            return True

    def pre_strategy_plan(self, history):
        return [self.pre_strategy_dialogact_order[len(history.sys_act)]]
    
    def post_strategy_plan(self, history):
        left_acts = [act for act in history.sys_act if (act not in self.pre_strategy_dialogact_order) and (act not in self.strategy_order) and (act != ACT_TO_STRATEGY_DICT['other'])]
        return [self.post_strategy_dialogact_order[len(left_acts)]]

    def during_strategy_plan(self, history):
        raise NotImplementedError

    def plan(self, history):
        if self.is_pre_strategy(history):
            # pre-strategy
            return self.pre_strategy_plan(history)
        elif self.start_post_strategy(history):
            # post strategy
            return self.post_strategy_plan(history)
        else:
            return self.during_strategy_plan(history)

class RandomPlanner(StrategyPlanner):
    """
    random strategy baseline
    """
    def __init__(self, max_cycle=1, device="cuda:0"):
        super().__init__(max_cycle=max_cycle)

    def during_strategy_plan(self, history):
        # during strategy
        left_strategy = [strategy for strategy in self.strategy_order if strategy not in history.sys_act]
        strategy_this_turn = random.choice(left_strategy)
        return [strategy_this_turn]


class OptimalPlanner(StrategyPlanner):
    """
    optimal order based on previous study
    """
    def __init__(self, max_cycle=1, device="cuda:0"):
        super().__init__(max_cycle=max_cycle)
        

    def during_strategy_plan(self, history):
        # during strategy
        last_strategy = history.sys_act[-1]
        if last_strategy in self.strategy_order:
            next_strategy_id = self.strategy_order.index(last_strategy) + 1
        else:
            next_strategy_id = 0
        strategy_this_turn = self.strategy_order[next_strategy_id]
        return [strategy_this_turn]

class RulePlanner(StrategyPlanner):
    """
    optimal order based on previous study
    """    
    def __init__(self, max_cycle=1, device="cuda:0"):        
        super().__init__(max_cycle=max_cycle)
        self.next_sys_strategy_index = 0
        self.post_strategies_index = 0
        self.post_strategies = False
    
    def reset_counters(self):
        self.next_sys_strategy_index = 0
        self.post_strategies_index = 0
        self.post_strategies = False

    def map_strategies(self, history):
        usr_acts = [ACT_TO_STRATEGY_DICT[x.replace('_', '-')].replace('_', '-') for x in history.usr_act[history.start_of_most_recent_usr_acts:]]
        planned_acts = []
        if history.usr_utt:
            sentences = nltk.sent_tokenize(history.usr_utt[-1])
        for i in range(len(usr_acts)):
            act = usr_acts[i]
            sent = sentences[i]
            if act == 'acknowledgement':
                continue
            elif act not in ['personal-related-inquiry', 'greeting', 'ask-org-info', 'task-related-inquiry', 'positive-to-inquiry', 'neutral-to-inquiry', 'negative-to-inquiry', 'positive-reaction-to-donation', 'agree-donation',  'thank', 'negative-reaction-to-donation', 'disagree-donation', 'disagree-donation-more', 'neutral-to-donation', 'provide-donation-amount', 'ask-donation-procedure']:
                continue
            else:
                # if act in ['personal-related-inquiry']:#, 'task-related-inquiry']:
                    # planned_acts.append(ACT_TO_STRATEGY_DICT['inquiry-response'])
                if act in ['task-related-inquiry', 'personal-related-inquiry'] or utils.is_factual(sent) or utils.is_opinion(sent):
                    planned_acts.append((sent, 'DBCALL'))                
                    #pos to inquiry, neg to inquiry, neu to inquiry, personal stoery, logical appeal
                elif act in ['ask-org-info']:
                    planned_acts.append((sent, ACT_TO_STRATEGY_DICT['credibility-appeal']))
                elif act in ['greeting']:
                    planned_acts.append((sent, ACT_TO_STRATEGY_DICT['greeting']))
                elif act in ['positive-reaction-to-donation', 'positive-to-inquiry', 'neutral-to-inquiry',  'negative-to-inquiry']:
                    planned_acts.append((sent, ACT_TO_STRATEGY_DICT['comment-partner']))
                    # continue
                elif act in ['agree-donation']:
                    planned_acts.append((sent, ACT_TO_STRATEGY_DICT['thank']))
                elif act in ['thank']:
                    planned_acts.append((sent, ACT_TO_STRATEGY_DICT['you-are-welcome']))
                elif act in ['negative-reaction-to-donation', 'disagree-donation', 'disagree-donation-more']:
                    planned_acts.append((sent, ACT_TO_STRATEGY_DICT['ask-not-donate-reason']))
                elif act in ['neutral-to-donation']:
                    planned_acts.append((sent, ACT_TO_STRATEGY_DICT['comment-partner']))
                elif act in ['provide-donation-amount']:
                    planned_acts.append((sent, ACT_TO_STRATEGY_DICT['praise-user']))
                elif act in ['ask-donation-procedure']:
                    planned_acts.append((sent, ACT_TO_STRATEGY_DICT['donation-information']))
                else:
                    continue                
        return planned_acts
    def start_post_strategy(self, history):
        """
        condition to stop the persuasion, and start the post strategy process
        """
        return history.post_strategies
        # if len(history.sys_act) - self.inserted_strategy_offset + self.skipped_strategies < (len(self.pre_strategy_dialogact_order) + self.max_cycle * len(self.strategy_order)):
        #     # pre-strategy finished, and max cycle of strategies
        #     return False
        # else:
        #     return True
    def pre_strategy_plan(self, history):
        planned_acts = self.map_strategies(history)
        pre_strategy_act = self.pre_strategy_dialogact_order[len(history.sys_act)]
        acts = [x[1] for x in planned_acts]
        if pre_strategy_act not in acts:
            if history.usr_utt:
                planned_acts.append((history.usr_utt[-1], pre_strategy_act))
            else:
                planned_acts.append(('', pre_strategy_act))        
        return planned_acts
    
    def post_strategy_plan(self, history):
        planned_acts = self.map_strategies(history)
        # left_acts = [act for act in history.sys_act if (act not in self.pre_strategy_dialogact_order) and (act not in self.strategy_order) and (act != ACT_TO_STRATEGY_DICT['other'])]
        if history.post_strategies_index < len(self.post_strategy_dialogact_order):
            post_strategy_act = self.post_strategy_dialogact_order[history.post_strategies_index]
            history.post_strategies_index  += 1
            acts = [x[1] for x in planned_acts]
            if post_strategy_act not in acts:
                if history.usr_utt:
                    planned_acts.append((history.usr_utt[-1], post_strategy_act))
                else:
                    planned_acts.append(('', post_strategy_act))            
        else:
            planned_acts.append(("", POST_STRATEGY_ORDER[-1]))
            self.reset_counters()
        return planned_acts

    def during_strategy_plan(self, history):
        # during strategy
        planned_acts = self.map_strategies(history)

        #Substitute optimal order for supervised planner here, maybe?
        # last_strategy = history.sys_act[-1]
        last_strategy = history.next_sys_strategy_index        
        # if last_strategy in self.strategy_order:
        #     next_strategy_id = self.strategy_order.index(last_strategy) + 1
        # else:
        #     next_strategy_id = 0
        strategy_this_turn = self.strategy_order[last_strategy]
        acts = [x[1] for x in planned_acts]
        if strategy_this_turn not in acts:
            if history.usr_utt:
                planned_acts.append((history.usr_utt[-1], strategy_this_turn))
            else:
                planned_acts.append(('', strategy_this_turn))
        history.next_sys_strategy_index += 1
        if history.next_sys_strategy_index == len(self.strategy_order):
            history.post_strategies =  True    
        return planned_acts