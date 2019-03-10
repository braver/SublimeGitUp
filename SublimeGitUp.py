import os
import subprocess

import sublime
import sublime_plugin


def climb_dirs(start_dir):
    right = True
    while right:
        yield start_dir
        start_dir, right = os.path.split(start_dir)


# look for the git root by traversing up the dir
def find_git_root(path):
    for folder in climb_dirs(path):
        if os.path.exists(os.path.join(folder, '.git')):
            return folder


class GitupOpenCommand(sublime_plugin.WindowCommand):

    def is_enabled(self):
        return True

    def get_path(self):
        filepath = self.window.active_view().file_name()
        if filepath:
            return find_git_root(os.path.dirname(filepath))

        elif self.window.folders():
            return find_git_root(self.window.folders()[0])

        else:
            sublime.status_message('No place to open GitUp to')
            return False

    def run(self, *args):
        sublime.status_message('GitUp: running')
        path = self.get_path()
        if not path:
            sublime.status_message('GitUp: No path')
            return False
        if os.path.isfile(path):
            path = os.path.dirname(path)

        app_path = '/Applications/GitUp.app'
        subprocess.Popen(['open', '-a', app_path, path])


class SideBarGitupCommand(sublime_plugin.WindowCommand):

    def is_enabled(self, paths):
        for path in paths:
            if find_git_root(path):
                return True
        return False

    def get_path(self, paths):
        try:
            return find_git_root(paths[0])
        except IndexError:
            return self.window.active_view().file_name()

    def run(self, paths):
        sublime.status_message('GitUp: running')
        path = self.get_path(paths)
        if not path:
            sublime.status_message('GitUp: No path')
            return False
        if os.path.isfile(path):
            path = os.path.dirname(path)

        app_path = '/Applications/GitUp.app'
        subprocess.Popen(['open', '-a', app_path, path])
