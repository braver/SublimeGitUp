import os
import subprocess

import sublime
import sublime_plugin


def has_git(path):
    return os.path.exists(os.path.join(path, '.git'))


def is_parent(parent, child):
    if os.path.commonprefix([parent, child]) == parent:
        return True
    else:
        return False


class GitupOpenCommand(sublime_plugin.WindowCommand):

    def is_enabled(self):
        return True

    def get_path(self):
        filepath = self.window.active_view().file_name()
        if filepath:
            # look for the git root in the sidebar root folders
            for folder in self.window.folders():
                if is_parent(folder, filepath) and has_git(folder):
                    return folder

        elif self.window.folders() and has_git(self.window.folders()[0]):
            return self.window.folders()[0]
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
        subprocess.call(['open', '-a', app_path, path])


class SideBarGitupCommand(sublime_plugin.WindowCommand):

    def is_visible(self, paths):
        for path in paths:
            return os.path.isdir(path)

    def is_enabled(self, paths):
        for path in paths:
            return has_git(path)

    def get_path(self, paths):
        try:
            return paths[0]
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
        subprocess.call(['open', '-a', app_path, path])
