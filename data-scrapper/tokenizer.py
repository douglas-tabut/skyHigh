"""
This module contains the `tokenize_code` function that turns
python code snippets into subtokens using the `tokenize` module.
"""

import json
import io
import tokenize


def tokenize_code(code):
    """ Function to tokenize code snippets into subtokens """
    subtokens = []
    try:
        with io.BytesIO(code.encode('utf-8')) as code_stream:
            tokens = tokenize.tokenize(code_stream.readline)
            for tok in tokens:
                if tok.type == tokenize.NAME:
                    subtokens.append(tok.string)
    except tokenize.TokenError:
        pass
    return subtokens

input_file = 'cleaned_code_snippets.json'

with open(input_file, 'r', encoding='utf-8') as json_file:
    cleaned_code_snippets = json.load(json_file)

# Tokenize the code into subtokens
tokenized_code_snippets = []
for snippet in cleaned_code_snippets:
    subtokens = tokenize_code(snippet['content'])
    tokenized_code_snippets.append({
        'repository': snippet['repository'],
        'file_name': snippet['file_name'],
        'subtokens': subtokens
        })

output_file = 'tokenized_code_snippets.json'
with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump(tokenized_code_snippets, json_file, indent=4)

print(f'Tokenized code snippets saved to {output_file}')
