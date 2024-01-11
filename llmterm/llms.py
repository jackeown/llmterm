import os
from llama_cpp import Llama
from langchain.llms.openai import OpenAI, AzureOpenAI

from rich.prompt import Prompt
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


def getEnvOrPrompt(var, prompt):
    if os.environ.get(var) is None:
        ans = Prompt.ask(prompt)
        os.environ[var] = ans
        return ans
    else:
        return os.environ.get(var)


def getOpenAIInfo():
    return getEnvOrPrompt("OPENAI_API_KEY", "OpenAI API Key")
    

def getAzureOpenAIInfo():
    return {
        "deployment_name" : getEnvOrPrompt("AZURE_OPENAI_DEPLOYMENT", "Azure OpenAI Deployment"),
        "openai_api_key" : getEnvOrPrompt("AZURE_OPENAI_API_KEY", "Azure OpenAI API Key"),
        "openai_api_base" : getEnvOrPrompt("AZURE_OPENAI_API_BASE", "Azure OpenAI API Base"),
        "openai_api_type" : 'azure',
        "openai_api_version": getEnvOrPrompt("AZURE_OPENAI_API_VERSION", "Azure OpenAI API Version"),
    }



def translateLlama(description, previous=[]):
    llm = Llama(model_path="./.models/llama-2-7b.Q5_K_S.gguf", verbose=False)
    output = llm(f"Q: What is '{description}' as a bash oneliner? A: The exact command is '", max_tokens=64, stop=["Q:", "\n"], echo=False)
    command = output['choices'][0]['text']
    command = command[:-1]
    return command
    

def translateGPT4(description, previous=[]):
    getOpenAIInfo()
    llm = OpenAI(model_name="gpt-3.5-turbo", verbose=False)

    template = """Rewrite '{description}' as a bash oneliner.
Only include the exact command(s) in your output without quotes or backticks.
"""

    prompt = PromptTemplate(template=template, input_variables=["description"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    command = llm_chain.run(description)

    return command




def translateAzure(description, previous=[]):
    info = getAzureOpenAIInfo()
    llm = AzureOpenAI(**info, verbose=False)

    template = """Rewrite '{description}' as a bash oneliner.
Only include the exact command(s) in your output without quotes or backticks.
"""

    prompt = PromptTemplate(template=template, input_variables=["description"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    command = llm_chain.run(description)

    return command