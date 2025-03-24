"""
配置环境变量
bianxie_api_key
bianxie_api_base
"""

from abc import ABC

class LLMConfig(ABC):
    api_key = None
    api_base = None


class BianxieConfig(LLMConfig):
    model="gpt-4o"
    api_key = 'sk-tQ17YaQSAvb6REf474A112Eb57064c5d9f6a9599F96a35A6'
    api_base = 'https://api.bianxieai.com/v1'
    
