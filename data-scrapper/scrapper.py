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

def fetch_python_code_snippets(owner, repo):
    """Function to fetch python code snippets from popular repos
    on GitHub using the GitHub API
    """
    headers = {'Authorization': f'token {token}'}
    url = f'https://api.github.com/repos/{owner}/{repo}/contents'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        contents = response.json()
        python_code_snippets = []

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
        return python_code_snippets
    else:
        print(f'Failed to fetch code snippets for {owner}/{repo}. Status code: {response.status_code}')
        return None


if __name__ == '__main__':
    all_snippets = []

    for repo_info in repositories:
        owner, repo = repo_info['owner'], repo_info['repo']
        snippets = fetch_python_code_snippets(owner, repo)

        if snippets:
            all_snippets.extend(snippets)

    # Save code snippets to a JSON file
    with open('python_code_snippets.json', 'w') as json_file:
        json.dump(all_snippets, json_file, indent=4)

    print('Code snippets saved to python_code_snippets.json')
