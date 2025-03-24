import re

def extract_python_code(text):
    pattern = r'```python([\s\S]*?)```'
    matches = re.findall(pattern, text)
    return matches

def extract_json_code(text):
    pattern = r'```json([\s\S]*?)```'
    matches = re.findall(pattern, text)
    return matches

