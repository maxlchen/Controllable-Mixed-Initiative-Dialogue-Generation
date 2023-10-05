import copy


class Agent(object):
    """
    Abstract class for Agent (user or system)
    """

    def __init__(self, domain, complexity):
        self.domain = domain
        self.complexity = complexity

    def step(self, *args, **kwargs):
        """
        Given the new inputs, generate the next response

        :return: reward, terminal, response
        """
        raise NotImplementedError("Implement step function is required")


class Action(dict):
    """
    A generic class that corresponds to a discourse unit. An action is made of an Act and a list of parameters.

    :ivar act: dialog act String
    :ivar parameters: [{slot -> usr_constrain}, {sys_slot -> value}] for INFORM, and [(type, value)...] for other acts.

    """

    def __init__(self, act, parameters=None):
        self.act = act
        if parameters is None:
            self.parameters = None
        elif type(parameters) is not list:
            self.parameters = [parameters]
        else:
            self.parameters = parameters
        super(Action, self).__init__(act=self.act, parameters=self.parameters)

    def add_parameter(self, type, value):
        self.parameters.append((type, value))

    def dump_string(self):
        str_paras = []
        for p in self.parameters:
            if type(p) is not str:
                str_paras.append(str(p))
            else:
                str_paras.append(p)
        str_paras = "-".join(str_paras)
        return "%s:%s" % (self.act, str_paras)


class State(object):
    """
    The base class for a dialog state

    :ivar history: a list of turns
    :cvar USR: user name
    :cvar SYS: system name
    :cvar LISTEN: the agent is waiting for other's input
    :cvar SPEAK: the agent is generating it's output
    :cvar EXT: the agent leaves the session
    """

    USR = "usr"
    SYS = "sys"

    LISTEN = "listen"
    SPEAK = "speak"
    EXIT = "exit"

    def __init__(self):
        self.history = []

    def yield_floor(self, *args, **kwargs):
        """
        Base function that decides if the agent should yield the conversation floor
        """
        raise NotImplementedError("Yield is required")

    def is_terminal(self, *args, **kwargs):
        """
        Base function decides if the agent is left
        """
        raise NotImplementedError("is_terminal is required")

    def last_actions(self, target_speaker):
        """
        Search in the dialog hisotry given a speaker.

        :param target_speaker: the target speaker
        :return: the last turn produced by the given speaker. None if not found.
        """
        for spk, utt in self.history[::-1]:
            if spk == target_speaker:
                return utt
        return None

    def update_history(self, speaker, actions):
        """
        Append the new turn into the history

        :param speaker: SYS or USR
        :param actions: a list of Action
        """
        # make a deep copy of actions
        self.history.append((speaker, copy.deepcopy(actions)))


class SystemAct(object):
    """
    :cvar IMPLICIT_CONFIRM: you said XX
    :cvar EXPLICIT_CONFIRM: do you mean XX
    :cvar INFORM: I think XX is a good fit
    :cvar REQUEST: which location?
    :cvar GREET: hello
    :cvar GOODBYE: goodbye
    :cvar CLARIFY: I think you want either A or B. Which one is right?
    :cvar ASK_REPHRASE: can you please say it in another way?
    :cvar ASK_REPEAT: what did you say?
    """
    """
    GREET = "greet"
    INTRODUCE_CHARITY = "introduce_charity"
    SUGGEST_DONATION = "suggest_donation" # P1 yes
    PROVIDE_FACT = "provide_fact" # L1 yes
    DONATION_IMPACT = "donation_impact" # L3 yes
    # PERSONAL_STORY = "personal_story"
    EMOTION_APPEAL = "emotion_appeal" # E2 yes
    TASK_INFO = "task_info" # TF yes
    INDICATE_SELF_DONATION = "indicate_self_donation" # The persuade often ask whether persuader will donate. In order to persuade the persuadee to donate, most of persuaders will show their approval
    THANK_DONATION = "thank_donation"
    END_CONV = "end_conv" # cannot appear very soon

    OTHER = "other"
    # SIMPLE_RESPONSE = "simple_response"
    # ASK = "ask"
    # PROVIDE_SELF_THOUGHTS = "provide_self_thoughts"
    # AGREE = "agree"
    # DISAGREE = "disagree"
    # OFF_TASK = "off_task"
    # END_CONV = "end_conv  #" the system doesn't terminate the dialog?

    """
    ####################### strategies ########################
    PERSONAL_STORY = "personal_story"
    EMOTION_APPEAL = "emotion_appeal"
    PROPOSE_DONATION = "propose_donation"
    FOOT_IN_THE_DOOR = "foot_in_the_door"
    LOGICAL_APPEAL = "logical_appeal"
    EXAMPLE_DONATION = "example_donation"

    ####################### pairs ########################
    PROVIDE_DONATION_PROCEDURE = "provide_donation_procedure"
    PROVIDE_ORG_FACTS = "provide_org_facts"
    ASK_DONATION_AMOUNT = "ask_donation_amount"
    CONFIRM_DONATION = "confirm_donation"
    HAVE_YOU_HEARD_OF_THE_ORG = "have_you_heard_of_the_org"
    ASK_NOT_DONATE_REASON = "ask_not_donate_reason"
    ASK_DONATE_MORE = "ask_donate_more"

    ############ dialog-act ##############
    TASK_RELATED_INQUIRY = "task_related_inquiry"
    PERSONAL_RELATED_INQUIRY = "personal_related_inquiry"

    POSITIVE_TO_INQUIRY = "positive_to_inquiry"
    NEGATIVE_TO_INQUIRY = "negative_to_inquiry"
    NEUTRAL_TO_INQUIRY = "neutral_to_inquiry"

    COMMENT_PARTNER = 'comment_partner'
    PRAISE_USER = "praise_user"
    THANK = "thank"
    YOU_ARE_WELCOME = "you_are_welcome"

    GREETING = "greeting"
    CLOSING = "closing"
    ACKNOWLEDGEMENT = "acknowledgement"

    #Additions that need to be adjusted for during loss computation
    GENERAL_INQUIRY = "inquiry"
    INQUIRY_RESPONSE = "inquiry_response"
    COMMENTARY = "commentary"

    ############ currently in "other" ##############
    # level 1: other
    OTHER = "other"
    OFF_TASK = "off_task"
    #    # level 2: strategy not annotated
    #    INDICATE_SELF_DONATION = "indicate_self_donation"
    #
    #    # general dialog act
    #    GREET = "greet"
    #    CLOSE = "close"
    #    THANK_DONATION = "thank_donation"
    #    HEARD_OF_CHARITY = "heard_of_charity"


class UserAct(object):
    """
    :cvar PROVIDE_PRIOR_EXPERIENCE: yes
    :cvar DISCONFIRM: no
    :cvar YN_QUESTION: Is it going to rain?
    :cvar INFORM: I like Chinese food.
    :cvar REQUEST: find me a place to eat.
    :cvar GREET: hello
    :cvar NEW_SEARCH: I have a new request.
    :cvar GOODBYE: goodbye
    :cvar CHAT: how is your day
    """
    ################### pair ######################
    ASK_ORG_INFO = "ask_org_info"
    ASK_DONATION_PROCEDURE = "ask_donation_procedure"

    AGREE_DONATION = "agree_donation"
    DISAGREE_DONATION = "disagree_donation"
    DISAGREE_DONATION_MORE = "disagree_donation_more"
    PROVIDE_DONATION_AMOUNT = "provide_donation_amount"
    CONFIRM_DONATION = "confirm_donation"

    POSITIVE_TO_INQUIRY = "positive_to_inquiry"
    NEGATIVE_TO_INQUIRY = "negative_to_inquiry"
    NEUTRAL_TO_INQUIRY = "neutral_to_inquiry"

    ################# reaction #####################
    POSITIVE_REACTION_TO_DONATION = "positive_reaction_to_donation"
    NEGATIVE_REACTION_TO_DONATION = "negative_reaction_to_donation"
    NEUTRAL_REACTION_TO_DONATION = "neutral_reaction_to_donation"

    ASK_PERSUADER_DONATION_INTENTION = "ask_persuader_donation_intention"

    ################ dialog act ####################
    TASK_RELATED_INQUIRY = "task_related_inquiry"
    PERSONAL_RELATED_INQUIRY = "personal_related_inquiry"

    THANK = "thank"
    YOU_ARE_WELCOME = "you_are_welcome"

    GREETING = "greeting"
    CLOSING = "closing"
    ACKNOWLEDGEMENT = "acknowledgement"

    ############ currently in "other" ##############
    # level 1: other
    OTHER = "other"
    OFF_TASK = "off_task"


class ConvAct(object):
    START_CONV = "start_conv"
    END_CONV = "end_conv"


class BaseSysSlot(object):
    """
    :cvar DEFAULT: the db entry
    :cvar PURPOSE: what's the purpose of the system
    """

    PURPOSE = "#purpose"
    DEFAULT = "#default"


class BaseUsrSlot(object):
    """
    :cvar NEED: what user want
    :cvar HAPPY: if user is satisfied about system's results
    :cvar AGAIN: the user rephrase the same sentence.
    :cvar SELF_CORRECT: the user correct itself.
    """
    NEED = "#need"
    HAPPY = "#happy"
    AGAIN = "#again"
    SELF_CORRECT = "#self_correct"
