from llama_cpp import Llama




def translateLlama(description, previous=[]):
    llm = Llama(model_path="./.models/llama-2-7b.Q5_K_S.gguf", verbose=False)
    output = llm(f"Q: What is '{description}' as a bash oneliner? A: The exact command is '", max_tokens=64, stop=["Q:", "\n"], echo=False)
    command = output['choices'][0]['text']
    command = command[:-1]
    return command
    

def translateGPT4(description, previous=[]):
    return ""
