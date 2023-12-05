from file_management import FileManagement
from lexical_analyzer import LexicalAnalyzer
from tui import TUI


class SyntacticAnalyzer:
    def __init__(self):
        self.file_management = FileManagement()
        self.lexical_analyzer = LexicalAnalyzer(self.file_management)
        self.tui = TUI(self.file_management)

    def start(self):
        self.tui.show_greetings()
        # path = self.tui.get_user_file_path()
        path = "test.232"

        self.lexical_analyzer.analyse(path)


syntactic_analyzer = SyntacticAnalyzer()

syntactic_analyzer.start()
