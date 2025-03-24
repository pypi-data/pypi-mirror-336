from typing import List, Dict,Optional
from llama_index.core.readers.base import BaseReader
from llama_index.core import Document

import yaml
def get_infos_from_md(text):
    _,infos,content = text.split("---",2)
    data = yaml.safe_load(infos)
    topic = data.get('topic','')
    describe = data.get('describe','')
    creation_date = data.get("creation date",'')
    tags = data.get('tags', [])
    return topic,describe,creation_date,tags,content

class CustObsidianReader(BaseReader):
    def load_data(self, file_path: str,
                        extra_info: Optional[Dict] = None) -> List[Document]:
        # 自定义读取逻辑
        with open(file_path, 'r') as file:
            text = file.read()
            
        topic,describe,creation_date,tags,content = get_infos_from_md(text)
            
        # TODO 这里是可以编辑做策略的

        content_cut = content[:4000]
        if len(content_cut) != len(content):
            print(topic,'is too long ***')
        document = Document(text=f"{topic}, describe: {describe}", 
                            metadata={"content":content_cut,
                                      "title":topic,
                                      "tags":tags,},
                            excluded_embed_metadata_keys=["content","tags"])
        return [document]

