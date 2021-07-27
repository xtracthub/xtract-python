import urllib.parse
import pycurl
import json
import io
import re
import os

EXTENSIONS = ['.py', '.py3']

class Getter(object):
    def __init__(self, owner=None, repo=None, direc=None, token=None):
        self.owner = owner
        self.repo = repo
        self.direc = direc
        self.token = token

    def curl_wrapper(self, url, query=None):
        """wrapper for basic pycurl functionality
        
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
        """Returns the hash of the most recent commit on a GitHub repository.

        Return:
        last_commit_sha (dict): the hash of the most recent commit on a GitHub
        repository.
        """
        url = f'https://api.github.com/repos/{self.owner}/{self.repo}/commits'
        body = self.curl_wrapper(url)
        body_json = json.loads(body)

        if 'message' in body_json and body_json['message'] == 'Bad credentials':
            print('(ERROR) Bad credentials. Create another API key.')
            return None

        last_commit = body_json[-1]
        last_commit_sha = last_commit['commit']['tree']['sha']
        return last_commit_sha

    def get_all_files(self, last_commit_sha):
        """Returns a list of all files in a Github Repository for a given
        commit (specified by its hash).

        Parameter:
        last_commit_sha (dict): the hash of the most recent commit on a GitHub
        repository.

        Return:
        paths (list): a list of all files paths in a Github repository. 
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
        """Returns a list of all python files in a Github Repository for a 
        given commit (specified by its hash).

        Parameter:
        last_commit_sha (dict): the hash of the most recent commit on a GitHub
        repository.

        Return:
        paths (list): a list of all python paths in a Github repository.
        """
        all_paths = self.get_all_files(last_commit_sha)
        python_paths = []
        for path in all_paths:
            if path.endswith(tuple(EXTENSIONS)):
                python_paths.append(path)
        return python_paths
    

    def get_content(self, python_paths):
        """Retrieves content from GitHub and copies it into appropriate
        directory based on the directory of the GitHub repository.

        Parameter:
        python_paths (list): list of python paths (represented as strings) to
        where the acquired code will be written.

        Return:
        None
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
        return