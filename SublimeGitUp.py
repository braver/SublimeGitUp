import locale
import os
import subprocess
import sublime, sublime_plugin

class GitupOpenCommand(sublime_plugin.WindowCommand):

    def is_enabled(self):
        return True

    def get_path(self):
        if self.window.active_view():
            return self.window.active_view().file_name()
        elif self.window.folders():
            return self.window.folders()[0]
        else:
            sublime.status_message(__name__ + ': No place to open GitUp to')
            return False

    def run(self, *args):
        sublime.status_message(__name__ + ': running')
        path = self.get_path()
        if not path:
            sublime.status_message(__name__ + ': No path')
            return False
        if os.path.isfile(path):
            path = os.path.dirname(path)

        app_path = '/Applications/GitUp.app'
        subprocess.call(['open', '-a', app_path, path])
