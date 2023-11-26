from file_management import FileManagement
from tui import TUI


class SyntacticAnalyzer:
    def __init__(self):
        self.file_management = FileManagement()
        self.tui = TUI(self.file_management)

    def start(self):
        self.tui.show_greetings()
        path = self.tui.get_user_file_path()

        with self.file_management.open_file(path) as file:
            content = file.read()
            print(content)


syntactic_analyzer = SyntacticAnalyzer()

syntactic_analyzer.start()
