# Data-Scrapper

This repository contains all the necesseray files for scrapping the python code from popular GitHub python repos, normalising the code and tokenizing it.

## How It Works

- Python code snippets are scrapped from popular GitHub repositories using the `scrapper.py` module. The code snippets are saved in a JSON file --> `cached_code_snippets.json`.
- The snippets are then normalized by removing extra white spaces, comments and tab spaces using the `normalizer.py` and the results are saved in --> `cleaned_code_snippets.json`.
- Using `tokenizer.py` the cleaned and normalised snippets are then transformed into tokens and subtoken. The results are saved in --> `tokenized_code_snippets.json`.
- `unique_snippets.json` contains unique subtokens.
- The module `compressor.py` can be utilised to compress and decompress json files to gz files.
