import io


class LexicalAnalyzer:
    buffer = ""
    # Modes
    # LETTER | NUMBER | REAL | LINE_COMMENT | BLOCK_COMMENT | CHAIN
    mode = None
    counter = 0
    line = 1
    chain_started = False
    skip_next = False

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
                if self.skip_next:
                    self.skip_next = False
                else:
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
                            elif char == '"':
                                print("### CHAIN MODE ON")
                                self.mode = "CHAIN"

                        if self.mode == "LETTER":
                            self.process_var(char)
                        elif self.mode == "NUMBER" or self.mode == "REAL":
                            self.process_number(char)
                        elif self.mode == "LINE_COMMENT":
                            self.process_line_comment(char, next_char)
                        elif self.mode == "BLOCK_COMMENT":
                            self.process_block_comment(char, next_char)
                        elif self.mode == "CHAIN":
                            self.process_chain(char, next_char)
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

    def check_delimiter(self):
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

        if self.mode == "CHAIN":
            self.utils.add_symbol(self.buffer, "consCadeia", self.line, code="C01")
            print("CHAIN")

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
            self.check_delimiter()

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
            self.check_delimiter()

    def process_line_comment(self, char, next_char):
        if self.utils.is_line_comment_end(char):
            print("line comment end")
            self.reset_status()

    def process_block_comment(self, char, next_char):
        if self.utils.is_block_comment_end(char, next_char):
            print("block comment end")
            self.reset_status()

    def process_chain(self, char, next_char):
        # Empry chain
        if char == '"' and next_char == '"':
            self.skip_next = True
            self.reset_status()
            print("-" * 50)

        # Chain start
        elif char == '"' and self.chain_started == False:
            self.chain_started = True
            self.buffer += char
            self.counter += 1

        # Chain end
        elif char == '"' and self.chain_started == True:
            self.chain_started = False
            self.buffer += char
            self.counter += 1
            self.check_delimiter()

        # Check if char is a valid chain char
        elif self.utils.is_valid_chain_char(char):
            self.buffer += char
            self.counter += 1

        # Check if the char is a valid char for the language
        # if yes, should work as delimiter
        elif self.utils.is_valid_char(char):
            print(f"Invalid char for chain: {char}")
