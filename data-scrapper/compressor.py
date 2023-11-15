import json
import gzip
import os

CACHE_FILE = 'cached_code_snippets.json'
COMPRESSED_CACHE_FILE = 'cached_code_snippets.json.gz'

# Load the existing cache file
with open(CACHE_FILE, 'r') as file:
    content = file.read()

# Compress the content and save it to a new file
with gzip.open(COMPRESSED_CACHE_FILE, 'wb') as compressed_file:
    compressed_file.write(content.encode('utf-8'))

print(f'Original file size: {os.path.getsize(CACHE_FILE)} bytes')
print(f'Compressed file size: {os.path.getsize(COMPRESSED_CACHE_FILE)} bytes')

