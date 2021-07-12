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


# Grab the body of json
# Write the API code here
url = f'https://api.github.com/repos/{OWNER}/{REPO}/commits'
body = curl_wrapper(url)
body_json = json.loads(body)

# print(type(body))
# print(type(body_json))
# print(len(body_json))

# Grab the SHA of the last commit in the repo
last_commit = body_json[-1]
last_commit_sha = last_commit['commit']['tree']['sha']
# print(last_commit_sha)

# Get the tree for a specific commit (i.e. the last one)
# GET /repos/:owner/:repo/git/trees/:sha
url = f'https://api.github.com/repos/{OWNER}/{REPO}/git/trees/{last_commit_sha}'
query = {'recursive': '1'}
tree = curl_wrapper(url, query)
tree_json = json.loads(tree)
print(type(tree))
print(type(tree_json))

# Add all of paths into a list
paths = []
for tf in tree_json['tree']:
    paths.append(tf['path'])

# print(paths)



count = 0
python_files = []
for path in paths:
    if path.endswith(tuple(EXTENSIONS)):
        python_files.append(path)
        # print(str(count) + '\t' + path)
        count += 1
    

for index, path in enumerate(python_files):
    url = f'https://raw.githubusercontent.com/{OWNER}/{REPO}/master/{path}'
    contents = curl_wrapper(url)

    # print(path)
    # print(type(path))

    # Quick debugging!
    pattern = f'([^\/]*.py)'
    file_name = re.findall(pattern, path)[0]
    # print(file_name)
    dir_path = re.sub(pattern, '', path)
    # print(dir_path)

    # print(f'test_files/{REPO}/' + dir_path)

    if not os.path.exists(f'test_files/{REPO}/' + dir_path):
        os.makedirs(f'test_files/{REPO}/' + dir_path)
    
    with open(f'test_files/{REPO}/' + dir_path + file_name, 'w+') as f:
        f.write(contents)
