import sys
sys.path.insert(1, '../')
sys.path.insert(1, 'agent/')
import os
from persuasion_config import SYS_TEMPLATE_ACT_DIC, STRATEGY_TO_ACT_DICT, ACT_TO_STRATEGY_DICT
from sentence_transformers import SentenceTransformer
import pickle
from scipy.spatial.distance import cosine
import openai
import nltk
import json
import random
import time
import re
openai.api_key = os.getenv("OPENAI_API_KEY")

class Generator(object):
    # base generator
    def __init__(self):
        pass

    def generate(dialog_act):
        raise NotImplementedError

class TemplateBasedGenerator(Generator):
    def __init__(self):
        super().__init__()
        self.method = "template-based"

    def generate(self, history, dialog_act_list):
        utts = [random.choice(SYS_TEMPLATE_ACT_DIC[dialog_act])
                for dialog_act in dialog_act_list]
        return " ".join(utts)

class GPT3Generator(Generator):
    def __init__(self):#, model_path, device):
        super().__init__()
        self.method = "prompt"
        self.prompt_header = """The following is background information about Save the Children. Save the Children is headquartered in London, and they work to help fight poverty around the world. Children need help in developing countries and war zones. Small donations like $1 or $2 go a long way to help. 
The following is a conversation between a Persuader and a Persuadee about a charity called Save the Children. The Persuader is trying to persuade the Persuadee to donate to Save the Children."""
        self.appeal_mapping = {
            "personal-story":"The Persuader tells a personal story.",
            "credibility-appeal":"The Persuader uses a credibility appeal.",
            "provide-org-facts":"The Persuader uses a credibility appeal.",
            "emotion-appeal":"The Persuader uses an emotion appeal.",
            "proposition-of-donation":"The Persuader asks if the Persuadee would like to make a small donation.",
            "propose-donation":"The Persuader asks if the Persuadee would like to make a small donation.",
            'foot-in-the-door': "The Persuader tells the Persuadee about how useful even small donations are.",
            'logical-appeal': "The Persuader uses a logical appeal.",
            'self-modeling': "The Persuader talks about how often they donate to charities.",
            'example-donation': "The Persuader talks about how often they donate to charities.",
            'task-related-inquiry': "The Persuader asks the Persuadee if they have donated to any charities before.",
            "source-related-inquiry":"The Persuader asks the Persuadee if they have heard of Save the Children before.",
            "have-you-heard-of-the-org":"The Persuader asks the Persuadee if they have heard of Save the Children before.",
            "personal-related-inquiry":"The Persuader asks the Persuadee if they have kids."
        }
        self.sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')

    def call_gpt3(self, prompt):
        try:
            return openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                temperature=0.7,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0.75,
                presence_penalty=0
            )
        except (openai.error.RateLimitError, openai.error.ServiceUnavailableError) as e:
            print("Caught", e)
            print("Retrying API call")
            return self.call_gpt3(prompt)
    def generate(self, dialog_act_list, history):
        print(dialog_act_list)
        return self.prompt_generate(dialog_act_list, history)
    
        
    def prepare_prompt(self, dialog_act_condition, history):
        history.sys_act = [act for act in history.sys_act if act != "DBCALL"]
        model_input = '\n' + '\n'.join(history.all_utt)
        model_input = model_input.replace("A:", "Persuader:")
        model_input = model_input.replace("B:", "Persuadee:")
        persuader_count = 0
        prompt = ""
        for line in model_input.split("\n"):
            if line.startswith("Persuader:"):
                dialog_act = history.sys_act[persuader_count]
                if type(dialog_act) is tuple or type(dialog_act) is list:
                    dialog_act = dialog_act[1]
                print("HERE", dialog_act)
                if dialog_act.replace("_","-") in self.appeal_mapping.keys():
                    prompt += self.appeal_mapping[dialog_act.replace("_","-")] + "\n"
                persuader_count += 1
            prompt += line + "\n"
        model_input = self.prompt_header + prompt.rstrip()
        
        #TODO:Add prompts into model history.
        model_input = model_input + "\nThe Persuader acknowledges the Persuadee's response and " + self.appeal_mapping[dialog_act_condition.replace("_","-")]
        model_input += "\nPersuader:"
        return model_input
    def prompt_generate(self, dialog_act_list, history):
        dialog_act_condition = dialog_act_list[0]
        if dialog_act_list[0] == "greeting":
            return "Hi, how are you doing?"
        elif dialog_act_list[0] == "closing":
            return "Sorry, I have to go now. It was great chatting with you!"
        else:
            model_input = self.prepare_prompt(dialog_act_condition, history)
            response = self.call_gpt3(model_input)
            print(response)
            response = response['choices'][0]['text'].lstrip()
            response = response.split("\n")[0]
            response = self.guardrails(dialog_act_list[0], response)
            return response
        # return outputs
        
class DualPromptGenerator(GPT3Generator):
    def __init__(self, qa_path, question_representation_path):
        super().__init__()
        self.qa = self.load_qa(qa_path)
        self.question_representation = self.load_qa_representation(question_representation_path)
        self.method = "dual-prompt"

    def load_qa(self, path):
        with open(path, 'r') as f:
            return json.load(f)
    
    def load_qa_representation(self, path):
        with open(path, 'rb') as f:
            return pickle.load(f)


    def generate(self, dialog_act_list, history):                
        qa_output = ""
        model_input = ""
        for i, dialog_tuple in enumerate(dialog_act_list):
            sentence = dialog_tuple[0]
            dialog_act = dialog_tuple[1]
            # import pdb
            # pdb.set_trace()
            print("Received:", dialog_act)
            if dialog_act == 'DBCALL':
                user_utterance = history.usr_utt[-1]
                rep = self.sentence_transformer.encode(user_utterance)
                CLOSEST_DIST = 10000
                CLOSEST = None
                for q in self.qa.keys():
                    q_rep = self.question_representation[q]
                    dist = cosine(rep, q_rep)
                    CLOSEST_DIST = min(dist, CLOSEST_DIST)
                    CLOSEST = q if CLOSEST_DIST == dist else CLOSEST
                if CLOSEST and CLOSEST_DIST < 0.6:
                    #Possibly explore a minmum jaccard threshold, so AND (CLOSEST_DIST < X OR JACCARD_SIM > Y)
                    print("Most similar question:", CLOSEST)
                    qa_output = random.choice(self.qa[CLOSEST]) #self.punctuator.punctuate(random.choice(self.qa[CLOSEST]))
                    qa_output = qa_output.replace("URL", "savethechildren.org")
                    print("Retrieved:", qa_output)
                else:
                    qa_output = "" 
            elif dialog_act == "greeting" and len(dialog_act_list) == 1:
                return "Hi, how are you doing?"
            elif dialog_act == "closing":
                return "Sorry, I have to go now. It was great chatting with you!"
            else:
                if dialog_act in self.appeal_mapping.keys():
                    model_input = self.prepare_prompt(dialog_act, history)
                # break
        model_input += " " + qa_output
        model_input = model_input.rstrip()  
        print("###INPUT PROMPT###")
        print(model_input)
        response = self.call_gpt3(model_input)
        print("Unparsed output text:", response['choices'][0]['text'])
        response = response['choices'][0]['text'].lstrip()
        response = response.split("\n")[0]
        response = qa_output.rstrip() + " " + response
        # response = self.guardrails(dialog_act_list[0], response)
        return response
        