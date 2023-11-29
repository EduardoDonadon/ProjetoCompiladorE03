from file_management import FileManagement
from lexical_analyzer import LexicalAnalyzer
from tui import TUI


class SyntacticAnalyzer:
    def __init__(self):
        self.file_management = FileManagement()
        self.lexical_analyzer = LexicalAnalyzer()
        self.tui = TUI(self.file_management)

    def start(self):
        self.tui.show_greetings()
        path = self.tui.get_user_file_path()

        with self.file_management.open_file(path) as file:
            for line in file:
                self.lexical_analyzer.analyse_line(line.strip())


syntactic_analyzer = SyntacticAnalyzer()

syntactic_analyzer.start()
