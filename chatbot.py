from agent.planner import RandomPlanner, OptimalPlanner, SupervisedlearningPlanner, RulePlanner, RetrievalPlanner
from agent.generator import TemplateBasedGenerator, ConditionalGenerator, DualConditionalGenerator, PromptGenerator, GPT3Generator, DualPromptGenerator
from agent.core import UserAct, SystemAct

import config as CONFIG
import utils

import imitation_learning.load_model as il
from persuasion_config import STRATEGY_ORDER, STRATEGY_TO_ACT_DICT


class Chatbot:
    def __init__(self, planner_type, generator_type, max_cycle=1, use_imitation_clf=False, force_response_to_be_strategy=False) -> None:
        # config initialization
        self.planner_device = CONFIG.planner_device
        self.generator_device = CONFIG.conditional_generator_device
        self.generator_model_path = CONFIG.conditional_generator_model_path
        self.force_response_to_be_strategy = force_response_to_be_strategy
        self.planner_path = CONFIG.supervised_planner_model_path
        self.response_generator_path = CONFIG.response_generator_path
        self.agenda_generator_path = CONFIG.agenda_generator_model_path

        # load models
        self.planner_type = planner_type
        self.generator_type = generator_type
        self.planner = self.load_planner(planner_type=planner_type, max_cycle=max_cycle)
        self.generator = self.load_generator(generator_type=generator_type)
        self.use_imitation_clf = use_imitation_clf or (planner_type in ['rule', 'retrieval'])
        if self.use_imitation_clf: #use_imitation_clf or planner_type == 'rule': 
            self.il_classifier = self.load_il_classifier()

    def load_planner(self, planner_type, max_cycle=1):
        if planner_type == "random":
            planner = RandomPlanner(max_cycle=max_cycle, device=self.planner_device)
        elif planner_type == "optimal":
            planner = OptimalPlanner(max_cycle=max_cycle, device=self.planner_device)
        elif planner_type == "supervised":
            planner = SupervisedlearningPlanner(self.planner_path, max_cycle=max_cycle, device=self.planner_device)
        elif planner_type == "rule":
            planner = RulePlanner(max_cycle = max_cycle, device = self.planner_device)
        elif planner_type == "retrieval":
            planner = RetrievalPlanner
        return planner

    def load_generator(self, generator_type):
        if generator_type == "template":
            generator = TemplateBasedGenerator()
        elif generator_type == "conditional":
            generator = ConditionalGenerator(
                model_path=self.generator_model_path, device=self.generator_device
            )
        elif generator_type == "dual":
            generator = DualConditionalGenerator(
                strategy_model_path=self.agenda_generator_path,
                device = self.generator_device,
                response_model_path=self.response_generator_path,
                qa_path = CONFIG.qa_path,
                question_representation_path = CONFIG.question_representation_path
            )
        elif generator_type == "prompt":
            generator = GPT3Generator()
        elif generator_type == "dual-prompt":
            generator = DualPromptGenerator(
                qa_path = CONFIG.qa_path,
                question_representation_path = CONFIG.question_representation_path
            )
        return generator

    def load_il_classifier(self):
        """
        the imitation learning classifier to detect if the response is good or not
        """
        loaded_model = il.load_model_clf_for_AMT(
            model_clf_dir=CONFIG.il_clf_dir,
            device1=CONFIG.il_clf_device1,
            device2=CONFIG.il_clf_device2,
        )
        il_classifier = il.ImitationClassifier(loaded_model)
        return il_classifier

    def chat(self, history, user_input=None):
        end_chat = False
        if (
            user_input == "[quit]"
            or user_input == "[accept]"
            or user_input == "quit"
            or user_input == "accept"
        ):
            usr_act = [SystemAct.CLOSING]
            user_input = 'B: ' + user_input
            history.update_usr_history(usr_utt=user_input, usr_act_list=usr_act)
            
            end_chat = True
            next_act_list = None
            next_response = "TASK COMPLETE"
        else:
            # update user-side history
            if user_input is not None:
                usr_act = self.pred_dialog_act(history=history, sent=user_input, role="B")
                user_input='B: ' + user_input                
                history.update_usr_history(usr_utt=user_input, usr_act_list=usr_act)
            
            # plan the next act
            next_act_list = self.planner.plan(history=history)

            #Map each planned act to the dialog act domain used during training            
            #However, can't change next_act_list because necessary for the dialog act order.
            input_dialog_act = []
            for act in next_act_list:
                if type(act) == tuple:
                    if act[1] != 'DBCALL':
                        input_dialog_act.append((act[0], STRATEGY_TO_ACT_DICT[act[1]]))
                    else:
                        input_dialog_act.append(act)
                else:
                    input_dialog_act.append(("", act))
            input_dialog_act = [(act[0], STRATEGY_TO_ACT_DICT[act[1]]) if act[1] != 'DBCALL' else act for act in next_act_list] if self.generator.method == 'dual-conditional-based' or self.generator.method == "dual-prompt" else next_act_list
            
            # generate the response
            next_response = self.generator.generate(history=history, dialog_act_list=input_dialog_act)
            
            # if imitation learning, then make the decision
            if self.use_imitation_clf:
                cnt = 0
                while cnt < CONFIG.max_num_trial and (not self.il_classifier_pred(history, next_response, next_act_list)):
                    cnt += 1
                    print(f"imitation learning says no: {next_response}")
                    next_response = self.generator.generate(history=history, dialog_act_list=input_dialog_act)
            
            # update system-side history 
            next_response = 'A: ' + next_response.replace('<s>', '').replace('</s>', "")
            history.update_sys_history(sys_utt=next_response.replace('\n', ' '), sys_act_list=next_act_list)
            # Account for differences in using rule + dual
            acts=[]
            for a in next_act_list:
                if type(a) == tuple:
                    acts.append(a[1])
                else:
                    acts.append(a)
            if SystemAct.CLOSING in acts:
                end_chat = True
        return history, next_act_list, next_response, end_chat


    def pred_dialog_act(self, history, sent, role):
        if self.use_imitation_clf:
            act = self.il_classifier.predict_dialog_act(context=utils.reconstruct_history(history), sent=sent, role=role)
            return act
        else:
            return None

    def il_classifier_pred(self, history, response_to_detect, acts_of_response):
        """
        imitation learning classifier decides if the response is good or not
        """
        original_selected = self.il_classifier.predict_TF(
            context=utils.reconstruct_history(history),
            next_response_candidate=response_to_detect,
        )
        if original_selected == 0:
            print(f"original imitation learning says no: {response_to_detect}")
        if self.force_response_to_be_strategy:
            if (original_selected == 1) and any([act in STRATEGY_ORDER for act in acts_of_response]):
                # it's selected by the original imitation learning classifier and we are at "during strategy" phase
                acts = self.pred_dialog_act(history=history, sent=response_to_detect, role='A')
                if len(set(acts) & set(STRATEGY_ORDER)) > 0:
                    # is strategy
                    return 1
                else: 
                    return 0
            else:
                return original_selected
        else:
            return original_selected