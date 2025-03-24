import json
from llama_index.core import Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core.node_parser import SentenceSplitter
from .utils import BianxieConfig

def get_llm():
    llm_config = BianxieConfig()

    llm = OpenAI(
        model="gpt-4o",
        api_key=llm_config.api_key,
        api_base=llm_config.api_base,
        temperature=0.1,
    )
    embed_model = OpenAIEmbedding(api_key=llm_config.api_key,
                                api_base = llm_config.api_base)
    Settings.embed_model = embed_model
    Settings.llm = llm
    Settings.text_splitter = SentenceSplitter(chunk_size=4096)
    return llm
    

