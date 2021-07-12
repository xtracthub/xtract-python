import urllib.parse
import pycurl
import json
import io
import re
import os

OWNER = 'edeng23'
REPO = 'binance-trade-bot'
DIRECTORY = 'test_files/binance-trade-bot/'
TOKEN = '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'
EXTENSIONS = ['.py', '.py3']

def curl_wrapper(url, query=None):
    """
    curl_wrapper

    """
    buffer = io.BytesIO()
    c = pycurl.Curl()
    if not query:
        c.setopt(c.URL, url)
    else:
        c.setopt(c.URL, url + '?' + urllib.parse.urlencode(query))
    c.setopt(c.HTTPHEADER, ['Accept: application/vnd.github.v3+json', f'Authorization: token {TOKEN}'])
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    buffer_contents = buffer.getvalue()
    return buffer_contents.decode('iso-8859-1')

def get_last_commit_sha(owner, repo):
    """
    get_last_commit_sha

    """
    url = f'https://api.github.com/repos/{OWNER}/{REPO}/commits'
    body = curl_wrapper(url)
    body_json = json.loads(body)

    last_commit = body_json[-1]
    last_commit_sha = last_commit['commit']['tree']['sha']
    return last_commit_sha

def get_all_files(owner, repo, last_commit_sha):
    """
    get_all_files

    """
    url = f'https://api.github.com/repos/{OWNER}/{REPO}/git/trees/{last_commit_sha}'
    query = {'recursive': '1'}
    tree = curl_wrapper(url, query)
    tree_json = json.loads(tree)
    paths = []
    for tree in tree_json['tree']:
        paths.append(tree['path'])
    return paths


def get_all_python_files(owner, repo, last_commit_sha):
    """
    get_all_python_files

    """
    all_paths = get_all_files(owner, repo, last_commit_sha)
    python_paths = []
    for path in all_paths:
        if path.endswith(tuple(EXTENSIONS)):
            python_files.append(path)
    return python_paths
    

def get_content(python_paths):
    """
    get_content

    """
    for path in python_paths:
        url = f'https://raw.githubusercontent.com/{OWNER}/{REPO}/master/{path}'
        contents = curl_wrapper(url)

        pattern = f'([^\/]*.py)'
        file_name = re.findall(pattern, path)[0]
        dir_name = re.sub(pattern, '', path)

        if not os.path.exists(f'test_files/{REPO}/' + dir_name):
            os.makedirs(f'test_files/{REPO}/' + dir_name)
    
        with open(f'test_files/{REPO}/' + dir_name + file_name, 'w+') as f:
            f.write(contents)
        