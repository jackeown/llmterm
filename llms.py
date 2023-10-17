from llama_cpp import Llama


def strip(command):
    command = command.strip()
    if command.startswith("'") or command.startswith('"'):
        command = command[1:]
    if command.endswith("'") or command.endswith('"'):
        command = command[:-1]
    return command


def translateLlama(description, previous=[]):
    llm = Llama(model_path="./.models/llama-2-7b.Q5_K_S.gguf", verbose=False)
    output = llm(f"Q: What is '{description}' as a bash oneliner? A:", max_tokens=32, stop=["Q:", "\n"], echo=False)
    return strip(output['choices'][0]['text'])

