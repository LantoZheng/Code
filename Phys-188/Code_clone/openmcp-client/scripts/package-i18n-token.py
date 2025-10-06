from typing import List
import sys
import os
sys.path.append(os.path.abspath('.'))

import json
from typing import Any

PACKAGE_FILE = './package.json'

LANG_PACKGE_FILES = {
    'en': './package.nls.json',
    'zh-cn': './package.nls.zh-cn.json',
    'ja': './package.nls.ja.json'
}

def read_json(path: str) -> Any:
    if not os.path.exists(path):
        return {}
    try:
        with open(path, 'r', encoding='utf-8') as fp:
            config = json.load(fp=fp)
            return config
    except Exception as e:
        return {}

def write_json(path: str, obj: object):
    with open(path, 'w', encoding='utf-8') as fp:
        json.dump(obj, fp=fp, indent=4, ensure_ascii=False)

def generate_title_token(command_name: str) -> str:
    names = command_name.split('.')
    prj_name = names[0]
    main_names = names[1:]
    title_token_name = [prj_name] + main_names + ['title']
    return '.'.join(title_token_name)

def merge_tokens(lang_package_path: str, tokens: List[str], token_values: List[str]):
    config = read_json(lang_package_path)
    for token, value in zip(tokens, token_values):
        if token not in config:
            config[token] = value
    
    write_json(lang_package_path, config)

if __name__ == '__main__':
    # adjust main package
    config = read_json(PACKAGE_FILE)
    token_names = []
    token_values = []

    # 获取 properties 中的 title
    for property_name in config.get('contributes', {}).get('configuration', {}).get('properties', {}):
        # property_name: digital-ide.welcome.show
        property_body = config['contributes']['configuration']['properties'][property_name]
        print(property_body)
        token_name = generate_title_token(property_name)
        token_names.append(token_name)
        if 'description' in property_body and not property_body['description'].startswith('%'):
            token_values.append(property_body['description'])
        else:
            token_values.append("")
        property_body['description'] = '%' + token_name + '%'
    
    # 获取 command 中的 title
    for item in config.get('contributes', {}).get('commands', []):
        if 'command' in item:
            token_name = generate_title_token(item['command'])
            token_names.append(token_name)
            token_values.append(item.get('title', ''))
            item['title'] = '%' + token_name + '%'
            
    # 获取 command 中的 title
    for viewName in config.get('contributes', {}).get('views', {}):
        view = config['contributes']['views'][viewName]
        for item in view:
            if 'id' in item:
                token_name = generate_title_token(item['id'] + '.view')
                token_names.append(token_name)
                token_values.append(item.get('name', ''))
                item['name'] = '%' + token_name + '%'

    write_json(PACKAGE_FILE, config)
    
    # cover in lang package
    for name, lang_path in LANG_PACKGE_FILES.items():
        merge_tokens(lang_path, token_names, token_values)