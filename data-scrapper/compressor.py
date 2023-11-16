"""
This module contains functions for compressing a json file to a .gz
file and decompressing from .gz to a json file.
"""

import json
import gzip
import os


def compress_json_to_gzip(input_file, output_file):
    """Compresses a JSON file to a gzip file."""
    with open(input_file, 'r', encoding='utf-8') as json_file:
        content = json_file.read()

    with gzip.open(output_file, 'wb') as compressed_file:
        compressed_file.write(content.encode('utf-8'))

def decompress_gzip_to_json(input_file, output_file):
    """Decompresses a gzip file to a JSON file."""
    with gzip.open(input_file, 'rt', encoding='utf-8') as compressed_file:
        content = compressed_file.read()

    with open(output_file, 'w', encoding='utf-8') as json_file:
        json_file.write(content)

CACHE_FILE = 'cached_code_snippets.json'
COMPRESSED_CACHE_FILE = 'cached_code_snippets.json.gz'

"""
Comment this code out in case you want to compress and comment the decompressor
# Compress JSON to Gzip
compress_json_to_gzip(CACHE_FILE, COMPRESSED_CACHE_FILE)

print(f'Original file size: {os.path.getsize(CACHE_FILE)} bytes')
print(f'Compressed file size: {os.path.getsize(COMPRESSED_CACHE_FILE)} bytes')
"""
# Decompress Gzip to JSON
DECOMPRESSED_CACHE_FILE = 'decompressed_code_snippets.json'
decompress_gzip_to_json(COMPRESSED_CACHE_FILE, DECOMPRESSED_CACHE_FILE)
