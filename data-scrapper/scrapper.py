"""
Contains the function `fetch_python_code_snippets`
that gets python code snippets from popular python GitHub repos.
The fetched snippets are then saved to a cached file.
"""

import requests
import json


# get GitHub personal access token saved as an environment variable
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("GITHUB_ACCESS_TOKEN")

# List of popular repos on GitHub with python code
repositories = [
        {'owner': 'psf', 'repo': 'requests'},
        {'owner': 'numpy', 'repo': 'numpy'},
        {'owner': 'django', 'repo': 'django'},
        {'owner': 'pandas-dev', 'repo': 'pandas'},
        {'owner': 'scikit-learn', 'repo': 'scikit-learn'},
        {'owner': 'pallets', 'repo': 'flask'},
        {'owner': 'psf', 'repo': 'requests-html'},
        {'owner': 'pytorch', 'repo': 'pytorch'},
        {'owner': 'celery', 'repo': 'celery'},
        {'owner': 'matplotlib', 'repo': 'matplotlib'}
]

CACHE_FILE = 'cached_code_snippets.json'

def fetch_python_code_snippets(owner, repo, path=''):
    """
    Function to fetch python code snippets from popular repos
    on GitHub using the GitHub API
    """
    headers = {'Authorization': f'token {token}'}
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        contents = response.json()
        python_code_snippets = []

        # To-Do: Implement parallelizarion instead of caching using concurrent.futures.ThreadPoolExecutir()
        for content in contents:
            if content['type'] == 'file' and content['name'].endswith('.py'):
                # Fetch the content of Python files
                file_url = content['download_url']
                file_content = requests.get(file_url).text
                python_code_snippets.append({
                    'repository': f'{owner}/{repo}',
                    'file_name': content['name'],
                    'content': file_content
                })
                print(f"Fetched snippet: {content['name']} from {owner}/{repo}")

            elif content['type'] == 'dir':
                # Recursively fetch code snippets from files within folders
                folder_path = f"{path}/{content['name']}"
                snippets = fetch_python_code_snippets(owner, repo, folder_path)
                if snippets:
                    python_code_snippets.extend(snippets)

        # Save the fetched code snippets to a caech file
        with open(CACHE_FILE, 'a') as cache_file:
            for snippet in python_code_snippets:
                json.dump(snippet, cache_file)
                cache_file.write('\n')

        return python_code_snippets
    else:
        print(f'Failed to fetch code snippets for {owner}/{repo}. Status code: {response.status_code}')
        return None


if __name__ == '__main__':
    # Check if cache file exists otherwise create it
    if not os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'w') as cache_file:
            cache_file.write('[') # initialize the JSON array

    all_snippets = []

    for repo_info in repositories:
        owner, repo = repo_info['owner'], repo_info['repo']
        snippets = fetch_python_code_snippets(owner, repo)

        if snippets:
            all_snippets.extend(snippets)

    # Save code snippets to a JSON array in the cache file
    with open(CACHE_FILE, 'a') as cache_file:
        cache_file.write(']')

    print('Code snippets saved to cached_code_snippets.json')
