from agent.core import UserAct, SystemAct

START_HAVE_YOU_HEARD_OF = "start_have_you_heard_of"
START_PROPOSE_DONATION = "start_propose_donation"
START_RELATED_INQUIRY = "start_related_inquiry"


STRATEGY_LIST = [
    # inquiries
    # SystemAct.HAVE_YOU_HEARD_OF_THE_ORG,
    SystemAct.TASK_RELATED_INQUIRY,
    SystemAct.PERSONAL_RELATED_INQUIRY,
    # appeals
    SystemAct.PERSONAL_STORY,
    SystemAct.EMOTION_APPEAL,
    # SystemAct.PROVIDE_DONATION_PROCEDURE,
    # SystemAct.PROPOSE_DONATION,
    SystemAct.FOOT_IN_THE_DOOR,
    SystemAct.LOGICAL_APPEAL,
    SystemAct.EXAMPLE_DONATION,
    SystemAct.PROVIDE_ORG_FACTS,

]

PLACEHOLDER_STRATEGY = "placeholder_strategy"
PRE_STRATEGY_ORDER = [
    SystemAct.GREETING,
    SystemAct.HAVE_YOU_HEARD_OF_THE_ORG,
    SystemAct.TASK_RELATED_INQUIRY,
    SystemAct.PERSONAL_RELATED_INQUIRY,
]
STRATEGY_ORDER = [
    SystemAct.PROVIDE_ORG_FACTS,  # credibility appeal
    SystemAct.EMOTION_APPEAL,  # emotion appeal
    SystemAct.LOGICAL_APPEAL,  # logical appeal
    SystemAct.EXAMPLE_DONATION,  # self-modeling
    SystemAct.FOOT_IN_THE_DOOR,  # foot in the door
    SystemAct.PERSONAL_STORY,  # personal story
    #   PLACEHOLDER_STRATEGY
    # SystemAct.PROVIDE_DONATION_PROCEDURE
]
POST_STRATEGY_ORDER = [
    SystemAct.PROPOSE_DONATION,
    SystemAct.CLOSING,
]

ACT_TO_STRATEGY_DICT = {
    'personal-story': SystemAct.PERSONAL_STORY,
    'emotion-appeal': SystemAct.EMOTION_APPEAL,
    'proposition-of-donation': SystemAct.PROPOSE_DONATION,
    'foot-in-the-door': SystemAct.FOOT_IN_THE_DOOR,
    'logical-appeal': SystemAct.LOGICAL_APPEAL,
    'self-modeling': SystemAct.EXAMPLE_DONATION,

    ####################### pairs ########################
    'donation-information': SystemAct.PROVIDE_DONATION_PROCEDURE,
    'credibility-appeal': SystemAct.PROVIDE_ORG_FACTS,
    'ask-donation-amount': SystemAct.ASK_DONATION_AMOUNT,
    'confirm-donation': SystemAct.CONFIRM_DONATION,
    'source-related-inquiry': SystemAct.HAVE_YOU_HEARD_OF_THE_ORG,
    'ask-not-donate-reason': SystemAct.ASK_NOT_DONATE_REASON,
    'ask-donate-more': SystemAct.ASK_DONATE_MORE,


    ############ dialog-act ##############
    'task-related-inquiry': SystemAct.TASK_RELATED_INQUIRY,
    'personal-related-inquiry': SystemAct.PERSONAL_RELATED_INQUIRY,

    'positive-to-inquiry': SystemAct.POSITIVE_TO_INQUIRY,
    'negative-to-inquiry': SystemAct.NEGATIVE_TO_INQUIRY,
    'neutral-to-inquiry': SystemAct.NEUTRAL_TO_INQUIRY,

    'comment-partner': SystemAct.COMMENT_PARTNER,
    'praise-user': SystemAct.PRAISE_USER,
    'thank': SystemAct.THANK,
    'you-are-welcome': SystemAct.YOU_ARE_WELCOME,

    'greeting': SystemAct.GREETING,
    'closing': SystemAct.CLOSING,
    'acknowledgement': SystemAct.ACKNOWLEDGEMENT,

    'other': SystemAct.OTHER,


    ################### USER ######################

    ################### pair ######################
    'ask-org-info': UserAct.ASK_ORG_INFO,
    'ask-donation-procedure': UserAct.ASK_DONATION_PROCEDURE,

    'agree-donation': UserAct.AGREE_DONATION,
    'disagree-donation': UserAct.DISAGREE_DONATION,
    'disagree-donation-more': UserAct.DISAGREE_DONATION_MORE,
    'provide-donation-amount': UserAct.PROVIDE_DONATION_AMOUNT,
    'confirm-donation': UserAct.CONFIRM_DONATION,

    'positive-to-inquiry': UserAct.POSITIVE_TO_INQUIRY,
    'negative-to-inquiry': UserAct.NEGATIVE_TO_INQUIRY,
    'neutral-to-inquiry': UserAct.NEUTRAL_TO_INQUIRY,


    ################# reaction #####################
    'positive-reaction-to-donation': UserAct.POSITIVE_REACTION_TO_DONATION,
    'negative-reaction-to-donation': UserAct.NEGATIVE_REACTION_TO_DONATION,
    'neutral-reaction-to-donation': UserAct.NEUTRAL_REACTION_TO_DONATION,

    'ask-persuader-donation-intention': UserAct.ASK_PERSUADER_DONATION_INTENTION,

    ################ dialog act ####################
    'task-related-inquiry': UserAct.TASK_RELATED_INQUIRY,
    'personal-related-inquiry': UserAct.PERSONAL_RELATED_INQUIRY,

    'thank': UserAct.THANK,
    'you-are-welcome': UserAct.YOU_ARE_WELCOME,

    'greeting': UserAct.GREETING,
    'closing': UserAct.CLOSING,
    'acknowledgement': UserAct.ACKNOWLEDGEMENT,

    ############### Shared Dialog Act ###############
    'greeting-inquiry': UserAct.GREETING,
    'kids-related-inquiry': UserAct.PERSONAL_RELATED_INQUIRY,
    "donation-related-inquiry": UserAct.TASK_RELATED_INQUIRY,
    "other-inquiry": UserAct.TASK_RELATED_INQUIRY,
    "greeting-answer": UserAct.GREETING,
    "off-task": SystemAct.OTHER,
    "organization-info-inquiry": UserAct.ASK_ORG_INFO,
    "donation-procedure-inquiry": UserAct.ASK_DONATION_PROCEDURE,
    "persuader-intention-inquiry": UserAct.ASK_PERSUADER_DONATION_INTENTION,
    "inquiry": SystemAct.GENERAL_INQUIRY,
    "organization-related-inquiry":SystemAct.HAVE_YOU_HEARD_OF_THE_ORG,
    'have-you-heard-of-the-org':SystemAct.HAVE_YOU_HEARD_OF_THE_ORG,
    "propose-donation-inquiry":SystemAct.PROPOSE_DONATION,
    'provide_donation_procedure':SystemAct.PROVIDE_DONATION_PROCEDURE,
    'example-donation':SystemAct.EXAMPLE_DONATION,
    'provide-org-facts': SystemAct.PROVIDE_ORG_FACTS,
    "propose-donation":SystemAct.PROPOSE_DONATION,
    "inquiry-response" : SystemAct.INQUIRY_RESPONSE,
    "commentary" : SystemAct.COMMENTARY

}

# Invert ACT_TO_STRATEGY_DICT so that the string can be used for the generation model
STRATEGY_TO_ACT_DICT = {}
for key in ACT_TO_STRATEGY_DICT.keys():
    # Ignore the ones that already exist so we don't overwrite the general dialog acts with the more obscure duplicates
    if ACT_TO_STRATEGY_DICT[key] not in STRATEGY_TO_ACT_DICT.keys():
        STRATEGY_TO_ACT_DICT.update({ACT_TO_STRATEGY_DICT[key]: key})


PROPOSE_INTERLEAVE = 5  # propose_donation every 5 turns

NO_INQUIRY = 1
PERSONAL_INQUIRY_ONLY = 2
NON_PERSONAL_INQUIRY_ONLY = 3
BOTH_INQUIRIES = 4

NLG_RETRIEVAL_THRESHOLD = 0.45  # right inclusive


SUB_STRATEGY_L = [
    SystemAct.PERSONAL_STORY,
    SystemAct.EMOTION_APPEAL,
    # SystemAct.PROPOSE_DONATION,
    SystemAct.FOOT_IN_THE_DOOR,
    SystemAct.LOGICAL_APPEAL,
    SystemAct.PROVIDE_ORG_FACTS,
    SystemAct.PROVIDE_DONATION_PROCEDURE
]

STRATEGY_LIST_FOR_REGRESSION = [
    SystemAct.PERSONAL_STORY,
    SystemAct.EMOTION_APPEAL,
    SystemAct.PROVIDE_DONATION_PROCEDURE,
    SystemAct.PROVIDE_ORG_FACTS,
    # SystemAct.PROPOSE_DONATION,
    SystemAct.FOOT_IN_THE_DOOR,
    SystemAct.LOGICAL_APPEAL,
    SystemAct.EXAMPLE_DONATION,
    SystemAct.HAVE_YOU_HEARD_OF_THE_ORG,
    SystemAct.TASK_RELATED_INQUIRY,
    SystemAct.PERSONAL_RELATED_INQUIRY,
]

SMALL_TALK_1 = "small_talk_1"

SMALL_TALK_2 = "small_talk_2"

SMALL_TALK_3 = "small_talk_3"

# LAST_PROPOSE = "last_propose"

SYS_TEMPLATE_ACT_DIC = {
    ####### persuasive inquiry #######
    SystemAct.HAVE_YOU_HEARD_OF_THE_ORG: ["Have you heard of the organization \"Save the Children\"?",
                                          "Are you aware of the organization \"Save the Children\"?"],
    SystemAct.TASK_RELATED_INQUIRY: ["Have you donated to a charity before?"],
    SystemAct.PERSONAL_RELATED_INQUIRY: ["Are you aware of the dangerous situations children face in conflicted areas?",
                                         "Do you have kids yourself?"],
    ####### persuasive appeal #######
    SystemAct.EXAMPLE_DONATION: ['I\'ll match your donation. And together we can double the amount.',
                                 'I think I\'ll donate all my task payment to Save the Children. $2.'],
    SystemAct.PERSONAL_STORY: ['Someone told me that he and his brother replaced birthday gifts with charity donations a few years ago, and it was a really rewarding experience for them.'],
    # credibility appeal
    SystemAct.PROVIDE_ORG_FACTS: ["Save The Children is an international non-governmental organization that promotes children's rights, provides relief and helps support children in developing countries."],
    # emotion appeal
    SystemAct.EMOTION_APPEAL: ["It makes me feel sad to see that so many children are suffering from poverty and hunger."],
    SystemAct.LOGICAL_APPEAL: ["Donations are extremely important in order for children to have their rights to healthcare, education, safety, etc. If you were to donate you would be making a huge impact for these children and on the world."],  # logical appeal
    # foot in the door
    SystemAct.FOOT_IN_THE_DOOR: ["Every little bit helps. Even a small amount!"],
    ######## donation-related dialog act #######
    SystemAct.PROPOSE_DONATION: ["Would you like to make a donation to \"Save the Children\"?",
                                 "Do you want to make a donation to \"Save the Children\"?"],
    # ["Your donation will be directly deducted from your task payment, and you can choose any amount from $0 to all your payment ($2). The research team will collect all donations and send it to \"Save the Children\"."], # It\'s as simple as that."],
    SystemAct.PROVIDE_DONATION_PROCEDURE: ["You can choose any amount from $0 to all your task payment ($2) to donate, which will be directly deducted from your payment. After task completion, the research team will send the donations to \"Save the Children\"."],
    SystemAct.ASK_DONATION_AMOUNT: ["How much would you like to donate?"],
    SystemAct.CONFIRM_DONATION: ["Just to confirm, how much would you like to donate?"],
    # are you sure you want to make a donation?"],
    SystemAct.ASK_DONATE_MORE: ["Any chance you would consider making a greater donation?"],
    SystemAct.ASK_NOT_DONATE_REASON: ["May I ask why you don't want to donate?"],
    ######## traditional dialog act #######
    SystemAct.THANK: ["Thank you so much!",
                      "Thank you a lot!",
                      "Thanks so much!"],
    SystemAct.YOU_ARE_WELCOME: ["You are welcome."],
    SystemAct.GREETING: ["Hello there! How are you doing?",
                         "I am doing good!"],
    SystemAct.CLOSING: ["Thank you. It\'s been lovely talking to you. Enjoy your day and bye!"],
    ######## small talk #######
    SMALL_TALK_1: ["Well, are you doing anything fun after this?"],
    SMALL_TALK_2: ["Well, I plan to relax a bit, what do you usually do to relax?"],
    SMALL_TALK_3: ["Alright, it’s been a long day. Thanks for sharing."]
    # LAST_PROPOSE: ["Do you still not consider making a donation?"]
}


# system special action for personal-inqury or task-inqury
System_Answer_to_Inquiry = "system_answer_to_inquiry"
User_Answer_to_Inquiry = "user_answer_to_inquiry"

USR_REACTION_LIST = [
    UserAct.POSITIVE_REACTION_TO_DONATION,
    UserAct.NEGATIVE_REACTION_TO_DONATION,
    UserAct.NEUTRAL_REACTION_TO_DONATION,

    UserAct.ASK_PERSUADER_DONATION_INTENTION,

    ################ dialog act ####################
    UserAct.TASK_RELATED_INQUIRY,
    UserAct.PERSONAL_RELATED_INQUIRY,
    UserAct.ASK_ORG_INFO,
    UserAct.ASK_DONATION_PROCEDURE,

]

USER_DONATION_BEHAVIOR = [
    UserAct.DISAGREE_DONATION,
    UserAct.AGREE_DONATION,
    UserAct.DISAGREE_DONATION_MORE,
    UserAct.PROVIDE_DONATION_AMOUNT,
]

HAVE_TO_PROPOSE_DONATION_TURN = 8

#################### donation amount ###################
MAX_DONATION = 2
MORE_DONATION = 0.1
MAX_DIALOG_LENGTH = 10
MAX_DIALOG_LENGTH_AMT = 10  # 7

# dialog status
NO_OUTCOME_YET = 0
DIALOG_DONE = 1


FAILURE_REWARD = -1

################ training mode ################
RL_TRAINING = 1
RANDOM_ACT = 2
RL_WARM_START = 3
INTERACTIVE = 4

################ reward #######################
PER_TURN_REWARD = 0
AGREE_DONATION_REWARD = 0.1
FAILURE_REWARD = -2
SUCCESS_REWARD = 2
DISAGREE_REWARD = -0.5
SAME_PENALTY = -2

DONATION_BEHAVIOR_REWARD = 0.1

################ cardinality ##################
SYS_ACTION_CARDINALITY = 27
USER_ACT_CARDINALITY = 23


################ probability ##################
AGREE_DONT_CHANGE_MIND_PROB = 0.99
DELTA_PROB = 0.1
STRATEGY_EFFECT = 0.15


################ nlg retrieval policy ###########
TRADITIONAL = "traditional"
TRADITIONAL_SCORE_RANK = "tranditional_score_rank"
SCORE_RANK = "score_rank"
SCORE_RANK_ALLOW_3 = "score_rank_allow_3"
