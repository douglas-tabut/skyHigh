"""
Contains the function `fetch_python_code_snippets`
that gets python code snippets from popular python GitHub repos.
The fetched snippets are then saved to a cached file.
"""

import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("GITHUB_ACCESS_TOKEN")

# List of popular repos on GitHub with python code
repositories = [
        {'owner': 'psf', 'repo': 'requests'},
        {'owner': 'numpy', 'repo': 'numpy'},
        {'owner': 'django', 'repo': 'django'},
        # {'owner': 'pandas-dev', 'repo': 'pandas'},
        # {'owner': 'scikit-learn', 'repo': 'scikit-learn'},
        # {'owner': 'pallets', 'repo': 'flask'},
        # {'owner': 'psf', 'repo': 'requests-html'},
        # {'owner': 'pytorch', 'repo': 'pytorch'},
        # {'owner': 'celery', 'repo': 'celery'},
        # {'owner': 'matplotlib', 'repo': 'matplotlib'}
]

CACHE_FILE = 'cached_code_snippets.json'
MAX_SNIPPETS_LIMIT = 350

TEST_FILE_TERMS = ['test', 'tests'] # Common terms used in test file names

def is_test_file(file_name):
    """
    Checks if the file is a test file based on the name.
    """
    return any(term in file_name.lower() for term in TEST_FILE_TERMS)


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
            if (content['type'] == 'file' and
                content['name'].endswith('.py') and
                content['name'] != '__init__.py' and
                not is_test_file(content['name'])):

                # Fetch the content of Python files and exclude the __init__.py and test files
                file_url = content['download_url']
                file_content = requests.get(file_url).text
                python_code_snippets.append({
                    'repository': f'{owner}/{repo}',
                    'file_name': content['name'],
                    'content': file_content
                })
                print(f"Fetched snippet: {content['name']} from {owner}/{repo}")

                if len(python_code_snippets) >= MAX_SNIPPETS_LIMIT:
                    break

            elif content['type'] == 'dir':
                # Recursively fetch code snippets from files within folders
                folder_path = f"{path}/{content['name']}"
                snippets = fetch_python_code_snippets(owner, repo, folder_path)
                if snippets:
                    python_code_snippets.extend(snippets)

        return python_code_snippets
    else:
        print(f'Failed to fetch code snippets for {owner}/{repo}. Status code: {response.status_code}')
        return None


if __name__ == '__main__':
    all_snippets = []

    try:
        for repo_info in repositories:
            owner, repo = repo_info['owner'], repo_info['repo']
            snippets = fetch_python_code_snippets(owner, repo)

            if snippets:
                all_snippets.extend(snippets)

            if len(all_snippets) >= MAX_SNIPPETS_LIMIT:
                    break  # Exit the loop when the overall limit is reached

    except KeyboardInterrupt:
        pass  # Catch Ctrl+C and proceed to saving snippets

    # Save code snippets to a JSON array in the cache file
    with open(CACHE_FILE, 'w') as cache_file:
        json.dump(all_snippets, cache_file, indent=4)

    print('Code snippets saved to cached_code_snippets.json')
