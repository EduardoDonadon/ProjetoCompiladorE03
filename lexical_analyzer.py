import io
from utils import Utils


class LexicalAnalyzer:
    buffer = ""
    # Modes
    # LETTER | NUMBER | LINE_COMMENT | BLOCK_COMMENT
    mode = None
    counter = 0

    def __init__(self, file_management):
        self.file_management = file_management
        self.utils = Utils()
        self.reserved_words = self.utils.get_reserved_table()

    def analyse(self, path):
        with self.file_management.open_file(path) as file:
            uppercase_file = file.read().upper()
            transformed_file = io.StringIO(uppercase_file)
            string_file = transformed_file.getvalue()
            for index, char in enumerate(string_file):
                next_char = self.utils.get_next_char(string_file, index)
                # Filter level 1
                if self.utils.is_valid_char(char):
                    if not self.mode:
                        if self.utils.is_line_comment_start(char, next_char):
                            print("Begin line comment")
                            self.mode = "LINE_COMMENT"
                        elif self.utils.is_block_comment_start(char, next_char):
                            print("Begin block comment")
                            self.mode = "BLOCK_COMMENT"
                        elif self.utils.is_letter(char):
                            self.mode = "LETTER"
                        elif self.utils.is_number(char):
                            self.mode = "NUMBER"

                    if self.mode == "LETTER":
                        self.process_var(char)
                    elif self.mode == "NUMBER":
                        self.process_number(char)
                    elif self.mode == "LINE_COMMENT":
                        self.process_line_comment(char, next_char)
                    elif self.mode == "BLOCK_COMMENT":
                        self.process_block_comment(char, next_char)
                else:
                    print(f"Char {char} is invalid")

    def reset_status(self):
        self.buffer = ""
        self.mode = None
        self.counter = 0

    def is_reserved_word(self, buffer):
        return any(buffer == value for value in self.reserved_words.values())

    def check_delimiter(self, char):
        # Check if is a delimiter or is a not allowed char for this structure
        print(f"Buffer: {self.buffer}")

        # if is a delimiter, checj if is a reserved word
        if self.is_reserved_word(self.buffer):
            print("RESERVADO")
        else:
            print("VARIABLE")

        print(f"Lexeme size: {self.counter}")

        print("-" * 50)

        # Reset the internal control variables
        self.reset_status()

    def process_var(self, char):
        if self.utils.is_letter(char):
            # print("Is Letter")
            self.buffer += char
            self.counter += 1
        else:
            self.check_delimiter(char)

    def process_number(self, char):
        if self.utils.is_number(char):
            # print("Is Letter")
            self.buffer += char
            self.counter += 1
        else:
            self.check_delimiter(char)

    def process_line_comment(self, char, next_char):
        # print(f"line_comment {char}  --  next {next_char}")
        pass

    def process_block_comment(self, char, next_char):
        # print(f"block_comment {char}  --  next {next_char}")
        pass
        if self.utils.is_block_comment_end(char, next_char):
            print("block end")
            self.reset_status()
