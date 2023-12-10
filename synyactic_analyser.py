from file_management import FileManagement
from lexical_analyzer import LexicalAnalyzer
from tui import TUI
from utils import Utils


class SyntacticAnalyzer:
    def __init__(self):
        self.file_management = FileManagement()
        self.utils = Utils()
        self.lexical_analyzer = LexicalAnalyzer(self.file_management, self.utils)
        self.tui = TUI(self.file_management)

    def start(self):
        self.tui.show_greetings()
        # path = self.tui.get_user_file_path()
        path = "test.232"
        self.utils.add_line(
            f"RELATÓRIO DA ANALISE LÉXICA. Texto fonte analisado: {path}"
        )
        self.utils.add_line("-" * 100)

        self.lexical_analyzer.analyse(path)

        symbol_table = self.utils.get_symbol_table()
        self.file_management.map_to_file(symbol_table, path.replace(".232", ".TAB"))

        lexical_table = self.utils.get_lex_table()
        self.file_management.text_to_file(lexical_table, path.replace(".232", ".LEX"))


syntactic_analyzer = SyntacticAnalyzer()

syntactic_analyzer.start()
