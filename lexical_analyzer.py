import io


class LexicalAnalyzer:
    buffer = ""
    # Modes
    # LETTER | NUMBER | REAL | LINE_COMMENT | BLOCK_COMMENT
    mode = None
    counter = 0
    line = 1

    def __init__(self, file_management, utils):
        self.file_management = file_management
        self.utils = utils
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
                    elif self.mode == "NUMBER" or self.mode == "REAL":
                        self.process_number(char)
                    elif self.mode == "LINE_COMMENT":
                        self.process_line_comment(char, next_char)
                    elif self.mode == "BLOCK_COMMENT":
                        self.process_block_comment(char, next_char)
                else:
                    print(f"Char {char} is invalid")
                if char == "\n":
                    self.line += 1

    def reset_status(self):
        self.buffer = ""
        self.mode = None
        self.counter = 0

    def is_reserved_word(self, buffer):
        return any(buffer == value for value in self.reserved_words.values())

    def check_delimiter(self, char):
        # Check if is a delimiter or is a not allowed char for this structure
        print(f"Buffer: {self.buffer}")

        if self.mode == "LETTER":
            # if is a delimiter, check if is a reserved word
            if self.is_reserved_word(self.buffer):
                print("RESERVADO")
            else:
                self.utils.add_symbol(self.buffer, "variavel", self.line, code="C07")
                print("VARIABLE")
        if self.mode == "NUMBER":
            print("Number")
            self.utils.add_symbol(self.buffer, "consInteiro", self.line, code="C03")
        if self.mode == "REAL":
            self.utils.add_symbol(self.buffer, "consReal", self.line, code="C04")
            print("REAL")
        print(f"Lexeme size: {self.counter}")
        print(f"Line: {self.line}")

        print("-" * 50)

        # Reset the internal control variables
        self.reset_status()

    def process_var(self, char):
        if self.utils.is_letter(char):
            self.buffer += char
            self.counter += 1
        else:
            self.check_delimiter(char)

    def process_number(self, char):
        if self.utils.is_number(char):
            self.buffer += char
            self.counter += 1
        # Check if is number mode, and do not have any . in the number
        elif char == "." and self.mode == "NUMBER":
            self.mode = "REAL"
            self.buffer += char
            self.counter += 1
        else:
            self.check_delimiter(char)

    def process_line_comment(self, char, next_char):
        # print(f"line_comment {char}  --  next {next_char}")
        if self.utils.is_line_comment_end(char):
            print("line comment end")
            self.reset_status()

    def process_block_comment(self, char, next_char):
        # print(f"block_comment {char}  --  next {next_char}")
        if self.utils.is_block_comment_end(char, next_char):
            print("block comment end")
            self.reset_status()
