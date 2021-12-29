"""
Update index and commit with git in an analysis.
"""

import subprocess
import json
import os

from varial.toolinterface import Tool
from varial import analysis
from varial import wrappers


def show_git_stat_and_log():
    print 'Found the following UNSTAGED changes in the code:'
    os.system('git diff --stat')
    print 'Found the following STAGED changes in the code:'
    os.system('git diff --cached --stat')
    print 'Last 5 commits:'
    os.system('git log --oneline -4')


class GitAdder(Tool):
    """
    A tool to stage the latest changes in git.
    """
    can_reuse = False

    def run(self):
        unstaged_changes = subprocess.check_output(
            'git diff --stat', shell=True)
        staged_changes = subprocess.check_output(
            'git diff --cached --stat', shell=True)
        last_commit_hash = subprocess.check_output(
            'git rev-parse --verify HEAD', shell=True)
        show_git_stat_and_log()
        if not unstaged_changes and not staged_changes:
            self.message('NOTE: no changes in working directory and no staged '
                'changes in index!')
            last_commit_hash = '-2'
        if staged_changes:
            run_gittagger = raw_input('WARNING Staged changes in working '
                'directory found! To continue without staging, press Enter, '
                'to continue and stage new changes type "y" or "yes" '
                '(To abort kill process): ')
            if not any((run_gittagger.lower() == i) for i in ['y', 'yes']):
                self.message('Not staging commits.')
                last_commit_hash = '-1'
        if last_commit_hash != '-1':
            self.message('Staging commits.')
            os.system('git add -u :/')
        self.result = wrappers.Wrapper(
            commit_hash = last_commit_hash
        )

class GitTagger(Tool):
    """
    A tool to automatically commit when running new tools in git.

    Amending a commit if tools are re-run is also possible. In order to use
    this correctly, insert this tool at the end of your main ToolChain.
    """
    can_reuse = False

    def __init__(self, 
                 logfilename="GITTAGGER_LOG.txt",
                 commit_prefix="From GitTagger"):
        super(GitTagger, self).__init__()
        self.logfilename = logfilename
        self.commit_prefix = commit_prefix
        self.log_data = {}

    def log_tool_tree(self, toollist, res):
        if not len(res.children):
            toollist[res.name] = 0
        else:
            toollist[res.name] = {}
            for rname in sorted(res.children):
                self.log_tool_tree(toollist[res.name], res.children[rname])

    def compare_tool_tree(self, dict1, dict2):
        is_dict = lambda obj: isinstance(obj, dict)
        new_tool = 0
        for tool1 in dict1:
            if tool1 in dict2.keys():
                if is_dict(dict1[tool1]) and is_dict(dict2[tool1]):
                    new_tool = self.compare_tool_tree(dict1[tool1],
                                                      dict2[tool1])
                    if new_tool == -1:
                        return new_tool
                elif is_dict(dict1[tool1]) != is_dict(dict2[tool1]):  # xor
                    replace_tool = raw_input(
                        'WARNING: two tools with same name but not of same '
                        'class (i.e. Tool or ToolChain) found! To replace old '
                        'tool, type "yes", to abort press Enter: ')
                    if any((replace_tool.lower() == i) for i in ['y', 'yes']):
                        dict2[tool1] = dict1[tool1]
                        new_tool = 1
                    else:
                        self.message('Not committed, abort GitTagger.')
                        new_tool = -1
                        return new_tool
            else:
                dict2[tool1] = dict1[tool1]
                new_tool = 1
        return new_tool

    def set_commit_hash(self, tool_dict, commit_hash=0, old_commit_hash=0):
        for tool in tool_dict:
            if isinstance(tool_dict[tool], dict):
                self.set_commit_hash(
                    tool_dict[tool], commit_hash, old_commit_hash)
            else:
                if not old_commit_hash:
                    if tool_dict[tool] == 0:
                        tool_dict[tool] = commit_hash
                else:
                    if tool_dict[tool] == old_commit_hash:
                        tool_dict[tool] = commit_hash

    def check_commit_hash(self, tool_dict, old_commit_hash):
        found_hash = False
        for tool in tool_dict:
            if isinstance(tool_dict[tool], dict):
                found_hash = self.check_commit_hash(
                    tool_dict[tool], old_commit_hash)
            else:
                if tool_dict[tool] == old_commit_hash:
                    found_hash = True
                    return found_hash
        return found_hash

    def amend_commit(self):
        previous_commit_msg = subprocess.check_output(
            'git log -1 --pretty=%B', shell=True)
        previous_commit_hash = subprocess.check_output(
            'git rev-parse --verify HEAD', shell=True)[:-2]
        found_hash = self.check_commit_hash(self.log_data, previous_commit_hash)
        if not found_hash:
            commit_msg = raw_input('Commit hash from last commit not found in '
                'log file! If you want to make a new commit (and replace the '
                'commit hashs of the latest commit), type a commit message; if '
                'you want to abort, press Enter: ')
            if commit_msg == '':
                self.message('Not committed.')
                return -1
            else:
                previous_commit_msg = commit_msg
                previous_commit_hash = self.log_data['LatestCommit']
        os.system(
            'git commit --amend -m "{0}"'.format(previous_commit_msg))
        new_commit_hash = subprocess.check_output(
            'git rev-parse --verify HEAD', shell=True)[:-2]
        self.set_commit_hash(
            self.log_data, new_commit_hash, previous_commit_hash)
        return new_commit_hash

    def new_commit(self, message=''):
        commit_msg = raw_input(message)
        if commit_msg == '':
            self.message('Not committed.')
            return -1
        elif commit_msg == 'amend':
            new_commit_hash = self.amend_commit()
            return new_commit_hash
        else:
            os.system(
                'git commit -m "{0}: {1}"'.format(
                    self.commit_prefix, commit_msg))
            new_hash =subprocess.check_output(
                'git rev-parse --verify HEAD', shell=True)[:-2]
            self.log_data['LatestCommit'] = new_hash
            return new_hash

    def update_logfile(self, logfilepath, log_data, commit_hash=-1):
        if isinstance(commit_hash, str):
            self.set_commit_hash(log_data, commit_hash)
        else:
            self.set_commit_hash(log_data, -1)
        with open(logfilepath, 'w') as logfile:
            json.dump(
                log_data, logfile,
                sort_keys=True, indent=4, separators=(',', ': '))

    def run(self):
        last_stored_commit = self.lookup_result('../GitAdder')

        if not last_stored_commit:
            self.message('ERROR I could not find "../GitAdder". Returning.')
            return

        latest_commit_hash = subprocess.check_output(
            'git rev-parse --verify HEAD', shell=True)
        if (last_stored_commit.commit_hash != latest_commit_hash and
            last_stored_commit.commit_hash != '-1'):
            want_continue = raw_input(
                'WARNING discrepancy in staging area before and after running '
                'the analysis found! It is highly encouraged not to commit in '
                'order not to mess up your GitTagger log file!')
        toollist = {}
        toollist[analysis.results_base.name] = {}
        for rname in sorted(analysis.results_base.children):
            self.log_tool_tree(
                toollist[analysis.results_base.name],
                analysis.results_base.children[rname]
            )

        if os.path.isfile(self.cwd+self.logfilename):
            with open(self.cwd+self.logfilename, 'r') as logfile:
                self.log_data = json.load(logfile)
                new_tool = self.compare_tool_tree(toollist, self.log_data)
            if new_tool > 0:
                show_git_stat_and_log()
                commit_hash = self.new_commit(
                    'New tool found, if you want to make new commit type a '
                    'commit message; '
                    'If you want to amend the latest commit, type "amend"; '
                    'If you do not want to commit, just press enter: ')
                self.update_logfile(
                    self.cwd+self.logfilename, self.log_data, commit_hash)
            elif new_tool < 0:
                return
            else:
                show_git_stat_and_log()
                commit_msg = raw_input(
                    'No new Tool found, want to amend commit? '
                    'Press Enter if you do not want to amend; '
                    'type "amend", "y" or "yes" to amend and keep the old '
                    'commit message; '
                    'to amend with a new message, type a new message: ')
                if commit_msg == '':
                    self.message('Not committed.')
                    new_commit_hash = ''
                elif any((commit_msg.lower() == i)
                    for i in ['y', 'yes', 'amend']):
                    new_commit_hash = self.amend_commit()
                else:
                    previous_commit_hash = subprocess.check_output(
                        'git rev-parse --verify HEAD', shell=True)[:-2]
                    os.system(
                        'git commit --amend -m "{0}: {1}"'.format(
                            self.commit_prefix, commit_msg))
                    new_commit_hash = subprocess.check_output(
                        'git rev-parse --verify HEAD', shell=True)[:-2]
                    self.set_commit_hash(
                        self.log_data, new_commit_hash, previous_commit_hash)
                self.update_logfile(
                    self.cwd+self.logfilename, self.log_data, new_commit_hash)
        else:
            self.log_data = toollist
            self.log_data['LatestCommit'] = 0
            show_git_stat_and_log()
            commit_hash = self.new_commit(
                'No logfile found, if you want to make new commit type a '
                'commit message; '
                'If you want to amend the latest commit, type "amend"; '
                'If you do not want to commit, just press enter: ')
            self.update_logfile(
                self.cwd+self.logfilename, self.log_data, commit_hash)


