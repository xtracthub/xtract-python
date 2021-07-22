import urllib.parse
import pycurl
import json
import io
import re
import os

EXTENSIONS = ['.py', '.py3']

class Tester(object):
    def __init__(self, owner=None, repo=None, direc=None, token=None):
        self.owner = owner
        self.repo = repo
        self.direc = direc
        self.token = token

    def curl_wrapper(self, url, query=None):
        """
        curl_wrapper:

        """
        buffer = io.BytesIO()
        c = pycurl.Curl()
        if not query:
            c.setopt(c.URL, url)
        else:
            c.setopt(c.URL, url + '?' + urllib.parse.urlencode(query))
        c.setopt(c.HTTPHEADER, ['Accept: application/vnd.github.v3+json', f'Authorization: token {self.token}'])
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close()
        buffer_contents = buffer.getvalue() 
        return buffer_contents.decode('iso-8859-1')

    def get_last_commit_sha(self):
        """
        get_last_commit_sha

        """
        url = f'https://api.github.com/repos/{self.owner}/{self.repo}/commits'
        body = self.curl_wrapper(url)
        body_json = json.loads(body)

        if isinstance(body_json, dict):
            return body_json

        last_commit = body_json[-1]
        last_commit_sha = last_commit['commit']['tree']['sha']
        return last_commit_sha

    def get_all_files(self, last_commit_sha):
        """
        get_all_files

        """
        url = f'https://api.github.com/repos/{self.owner}/{self.repo}/git/trees/{last_commit_sha}'
        query = {'recursive': '1'}
        tree = self.curl_wrapper(url, query)
        tree_json = json.loads(tree)
        paths = []
        for tree in tree_json['tree']:
            paths.append(tree['path'])
        return paths


    def get_all_python_files(self, last_commit_sha):
        """
        get_all_python_files

        """
        all_paths = self.get_all_files(last_commit_sha)
        python_paths = []
        for path in all_paths:
            if path.endswith(tuple(EXTENSIONS)):
                python_paths.append(path)
        return python_paths
    

    def get_content(self, python_paths):
        """
        get_content

        """
        for path in python_paths:
            url = f'https://raw.githubusercontent.com/{self.owner}/{self.repo}/master/{path}'
            contents = self.curl_wrapper(url)

            pattern = f'([^\/]*.py)'
            file_name = re.findall(pattern, path)[0]
            dir_name = re.sub(pattern, '', path)

            if not os.path.exists(f'test_files/{self.repo}/' + dir_name):
                os.makedirs(f'test_files/{self.repo}/' + dir_name)
        
            with open(f'test_files/{self.repo}/' + dir_name + file_name, 'w+') as f:
                f.write(contents)

test = Tester(owner='edeng23', repo='binance-trade-bot', direc='test_files/binance_trade_bot/', token='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')
last_commit_sha = test.get_last_commit_sha()
python_paths = test.get_all_python_files(last_commit_sha)
test.get_content(python_paths)
