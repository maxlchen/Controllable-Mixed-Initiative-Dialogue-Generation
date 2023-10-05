import re

def reconstruct_history(history):
    """
    history: a DialogHistory object
    """
    context = []
    assert history.sys_first
    for i, utt in enumerate(history.all_utt):
        if history.sys_first:
            if i % 2 == 0:
                context.append(("A", utt))
            else:
                context.append(("B", utt))
        else:
            if i % 2 == 0:
                context.append(("B", utt))
            else:
                context.append(("A", utt))
    return context

question_regex = {
    "ask_back": "|".join([
        r"^(have you)$",
        r"^(what about you)$",
        r"^(how about you)$",
        r"^((what|who)('s| is) yours)$",
        r"^((what|who)('s| is) your favorite one)$",
        r"^(what do you think)$"
    ]),

    "ask_yesno": r"can you|may you|^are you|^do you|^have you|^would you want|(?<!how) do you$|^did you|^you wanna|^do you wanna|^does|^may i|^would you (?!like)|can you$",

    "ask_preference": r"^do you like|what do you want|^do you love|^do you support|^do you hate|what kind of|what type of|would you like|what.* better|which.* better|who.* better",

    "ask_opinion": r"^what do you think|how do you think|what do you like about|what do you love about|what makes you|how do you feel|^how is |^how was|how do you like|why do you like|what kind of| your opinion|your view|your thought|do you know|who do you think|do you believe|what.* best|who.* best|which.* best|which \w+ are you|what.*it like",

    "ask_advice": r"should i |should we |give .* advice|what.* advice|need.* advice|do you know how to|what.* good way to|tips|what.* suggest|how do i|how can i|what.* can i|what .* do i",

    "ask_ability": r"^can you|^could you|will you|teach me|how to|you.* for me|where do you|how do you|are you able to|^how can you",

    "ask_hobby": r"what do you like (?!about)|what do you love (?!about)|what.* your hobby|what.* your favorite",

    "ask_fact": r"what is (?!you)|what are (?!you)|what is (?!my)|what are (?!my)|what's (?!you)|what's (?!my)",

    "ask_info": r"(do you know( anything| something|) about|what do you know about|tell me about \w+)|(^\bbut\b \bwhich\b)",

    "ask_recommend": r"what.* recommend|which.* recommend|do you.* recommend|can you.* recommend|^recommend|give .* recommend|give.* suggestion|have.* suggestion|make.* suggestion|find me",

    "ask_reason": r"^why(?! not)\b|is that why|how (can|could)|^how is that|how do you know|how did you|tell me why|i wonder|what.* reason$",

    "ask_self": r"what.* \bmy\b|about \bme\b|about my",

    "ask_freq": r"how often|how many times",

    "ask_dist": r"how far|what.*distance",

    "ask_loc": r"where|what.* place|what.* address of",

    "ask_count": r"how many (?!times)",

    "ask_degree": r"how much|how long|how old|how tall|how big|how likely|how fast|to what extent",

    "ask_time": r"^when\b|what.* date|release date|what time|what year|how many days.* till|how many days.* until",

    "ask_person": r"^who\b",

    "ask_name": r"what.* name|what.* called|tell.* your name|(what's|whats) your name",

    "ask_user_name": r"(what.* my name)|(know|remember|tell me|repeat|say) my name",

    "ask_leave": r"something else|i don't want to talk about|done|something else|^change|different|this anymore|(do not|don't) care|not interested|boring|leave|i'm good|i'm ok|i'll pass|this sucks|no more|\bexit\b|\bquit\b|enough (news|sports|animals|games|movies|music)",
}

robust_question_regex = {}
for regex in question_regex.keys():
    patterns = question_regex[regex].split('|')
    new_patterns = []
    for pattern in patterns:
        temp = pattern
        new_patterns.append(temp)
        if temp[0] == '^':
            temp = temp[1:]
        temp =  '[^\n]+' + temp 
        new_patterns.append(temp)
    robust_question_regex[regex] = "|".join(new_patterns)

def is_question(utterance):
    utterance = utterance.lstrip().rstrip()
    for regex_type in robust_question_regex.keys():
        match = re.match(robust_question_regex[regex_type], utterance)
        if bool(match):
            return True
    return False

def __check_question_regex_subset(question, regex_type_list):
    question = question.lstrip().rstrip().lower()
    for regex_type in regex_type_list:
        match = re.match(robust_question_regex[regex_type], question)
        if bool(match):
            return True
    return False

def is_factual(question):
    return  __check_question_regex_subset(question, ['ask_fact', 'ask_name', 'ask_info', 'ask_yesno'])

def is_opinion(question):
    return  __check_question_regex_subset(question, ['ask_opinion', 'ask_preference', 'ask_hobby', 'ask_ability', 'ask_reason', 'ask_self'])
