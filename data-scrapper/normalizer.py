"""
This module contains the function `normalize_code` that
normalizes the python code snippets that were saved in the zipped file.
"""

import re
import json
import gzip


def normalize_code(code):
    """
    This function removes comments, non-ASCII chars, extra white spaces
    line continuation chars.
    """
    # Remove single and multi-line comments
    code = re.sub(r'#.*', '', code) # singleline
    code = re.sub(r'\'\'\'(.*?)\'\'\'', '', code, flags=re.DOTALL) # mulltiline with single quote '
    code = re.sub(r'\"\"\"(.*?)\"\"\"', '', code, flags=re.DOTALL) # multitline with double qoutes "

    # Replace tabs with spaces = 4
    code = re.sub(r'\t', '    ', code)

    # Remove special chatacters and formatiing
    code = re.sub(r'[^\x00-\x7F]+', '', code) # remove non-ASCII chars
    code = re.sub(r'\\\n', '', code) # remove line continuation chars
    code = re.sub(r' +', ' ', code) # Remove extra white spaces

    # strip leading and trailing whitespace
    code = code.strip()

    return code

input_file = 'cached_code_snippets.json.gz'
output_file = 'cleaned_code_snippets.json'

# Decompress the gzipped file
with gzip.open(input_file, 'rt', encoding='utf-8') as gz_file:
    code_snippets = json.load(gz_file)

cleaned_code_snippets = []
for snippet in code_snippets:
    cleaned_code = normalize_code(snippet['content'])
    cleaned_code_snippets.append({
        'repository': snippet['repository'],
        'file_name': snippet['file_name'],
        'content': cleaned_code
        })

with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump(cleaned_code_snippets, json_file, indent=4)

print(f'Cleaned and normalized code saved to {output_file}')
