import pandasai as pai
from pandasai_openai import OpenAI
from pandasai_local import LocalLLM
# !pip install pandasai-openai
#pip install pandasai-local

class PandasAI():

    def __init__(self):
        pass


    def set_config(self):
        llm = OpenAI(api_token="my-openai-api-key")
        pai.config.set({
        "llm": llm,
        "save_logs": True,
        "verbose": False,
        "max_retries": 3
        })
        # 设置官方的api-key

        pai.api_key.set("PAI-e874a529-0404-4829-ae8c-543b25763088")

    def set_llm(self):
        ollama_llm = LocalLLM(api_base="http://localhost:11434/v1", model="codellama")
        pai.config.set({"llm": ollama_llm})

    def work(self):
        pass

