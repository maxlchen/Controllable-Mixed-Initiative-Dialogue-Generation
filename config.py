"""
Config file for model paths; mostly used for original RAP.
"""

# conditional generator
conditional_generator_model_path = '/local-scratch1/data/maxlchen/generation_model_v2'
conditional_generator_device = "cuda:0"

agenda_generator_model_path = '/local-scratch1/data/maxlchen/persuasion_online/conditional_generation/generation_best_model_bart-largedialog_lr2e-06_wd0.01_utterances10_acts1_unpreprocessed_cond_penalty0.4_sem_threshold0.2_sem_penalty0.4_dont_collapse_inquiries_one_act_during_training_dont_require_no_same_turn_sentences_in_context__combined'
response_generator_path = '/local-scratch1/data/maxlchen/persuasion_online/conditional_generation/dialog_lr2e-06_wd0.01_utterances10_acts1_unpreprocessed_cond_penalty0.4_sem_threshold0.2_sem_penalty0.4_dont_collapse_inquiries_one_act_during_training_dont_require_no_same_turn_sentences_in_context__responses/checkpoint-7628'#'/local-scratch1/data/maxlchen/persuasion_online/conditional_generation/generation_best_model_bart-largedialog_lr2e-06_wd0.01_utterances10_acts1_unpreprocessed_cond_penalty0.4_sem_threshold0.2_sem_penalty0.4_dont_collapse_inquiries_one_act_during_training_dont_require_no_same_turn_sentences_in_context__responses'#'/local-scratch1/data/maxlchen/persuasion_online/conditional_generation/generation_best_model_bart-largedialog_lr2e-06_wd0.01_utterances10_acts1_unpreprocessed_cond_penalty0.4_sem_threshold0.2_sem_penalty0.4_dont_collapse_inquiries_one_act_during_training_dont_require_no_same_turn_sentences_in_context__combined' 
response_generator_path = '/local-scratch1/data/maxlchen/generation_model_v2'

qa_path = '/local-scratch1/data/maxlchen/persuasion_online/conditional_generation/qa_persona.json'
question_representation_path = '/local-scratch1/data/maxlchen/persuasion_online/conditional_generation/qa_question_representations_persona.pickle'

# supervised planner
supervised_planner_model_path = '/data/persuasion_agent/planner_model'
planner_device = "cuda:0"

# imitation learning classifier
il_clf_dir = "/local-scratch1/data/maxlchen/persuasion_online/imitation_learning/data/clf_model.pth"#"~/persuasion/consistency/Checkpoint_act_clf/epoch7_multitask_TF_best_acc_0.7944444444444444_f1_0.7861271676300577_A_acc_0.687741935483871_f1_0.6602596916886914_B_acc_0.6437699680511182_f1_0.6186370327752058.pth"#"Checkpoint_act_clf/multitask_TF_best_acc_0.7777777777777778_f1_0.776536312849162_A_acc_0.6954838709677419_f1_0.6707423935799665_B_acc_0.6166134185303515_f1_0.5898033645875225.pth"
il_clf_device1 = "cuda:0"
il_clf_device2 = "cuda:0"
force_response_to_be_strategy = False # the generated response has to be a strategy, even if it passes the imitation learning classifier, if not a strategy, cannot be selected
max_num_trial = 5

collected_data_path  = "/local-scratch1/data/fy2241/persuasion_online_data/"
