import io


class LexicalAnalyzer:
    buffer = ""
    # Modes
    # LETTER | NUMBER | REAL | LINE_COMMENT | BLOCK_COMMENT | CHAIN | CHAR
    mode = None
    counter = 0
    line = 1
    skip_next = False
    chain_started = False
    char_started = False

    def __init__(self, file_management, utils):
        self.file_management = file_management
        self.utils = utils
        self.reserved_words = self.utils.get_reserved_table()

    def process_current_char(self, char, next_char):
        if not self.mode:
            if self.utils.is_line_comment_start(char, next_char):
                self.mode = "LINE_COMMENT"
            elif self.utils.is_block_comment_start(char, next_char):
                self.mode = "BLOCK_COMMENT"
            elif self.utils.is_letter(char):
                self.mode = "LETTER"
            elif self.utils.is_number(char):
                self.mode = "NUMBER"
            elif char == '"':
                self.mode = "CHAIN"
            elif char == "'":
                self.mode = "CHAR"

        if self.mode == "LETTER":
            self.process_var(char, next_char)
        elif self.mode == "NUMBER" or self.mode == "REAL":
            self.process_number(char, next_char)
        elif self.mode == "LINE_COMMENT":
            self.process_line_comment(char, next_char)
        elif self.mode == "BLOCK_COMMENT":
            self.process_block_comment(char, next_char)
        elif self.mode == "CHAIN":
            self.process_chain(char, next_char)
        elif self.mode == "CHAR":
            self.process_char(char, next_char)

    def analyse(self, path):
        with self.file_management.open_file(path) as file:
            uppercase_file = file.read().upper()
            transformed_file = io.StringIO(uppercase_file)
            string_file = transformed_file.getvalue()
            for index, char in enumerate(string_file):
                if self.skip_next:
                    self.skip_next = False
                else:
                    # Filter level 1
                    if self.utils.is_valid_char(char):
                        next_char = self.utils.get_next_char(string_file, index)
                        self.process_current_char(char, next_char)
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
        self.utils.add_text_lex_table(f"Lexeme: {self.buffer[:30]},")

        if self.mode == "LETTER":
            # if is a delimiter, check if is a reserved word
            if self.is_reserved_word(self.buffer):
                self.utils.add_text_lex_table("RESERVADO,")
                print("RESERVADO")
            else:
                self.utils.add_symbol(self.buffer, "variavel", self.line, code="C07")
                self.utils.add_text_lex_table("Codigo: C07,")
                self.utils.add_text_lex_table(
                    f"ÍndiceTabSimb: {self.utils.get_lex_index(self.buffer)},"
                )
                print("VARIABLE")

        if self.mode == "NUMBER":
            print("Number")
            self.utils.add_symbol(self.buffer, "consInteiro", self.line, code="C03")
            self.utils.add_text_lex_table("Codigo: C03,")
            self.utils.add_text_lex_table(
                f"ÍndiceTabSimb: {self.utils.get_lex_index(self.buffer)},"
            )

        if self.mode == "REAL":
            self.utils.add_symbol(self.buffer, "consReal", self.line, code="C04")
            self.utils.add_text_lex_table("Codigo: C04,")
            self.utils.add_text_lex_table(
                f"ÍndiceTabSimb: {self.utils.get_lex_index(self.buffer)},"
            )
            print("REAL")

        if self.mode == "CHAIN":
            self.utils.add_symbol(self.buffer, "consCadeia", self.line, code="C01")
            self.utils.add_text_lex_table("Codigo: C01,")
            self.utils.add_text_lex_table(
                f"ÍndiceTabSimb: {self.utils.get_lex_index(self.buffer)},"
            )
            print("CHAIN")

        if self.mode == "CHAR":
            self.utils.add_symbol(self.buffer, "consCaracter", self.line, code="C02")
            self.utils.add_text_lex_table("Codigo: C02,")
            self.utils.add_text_lex_table(
                f"ÍndiceTabSimb: {self.utils.get_lex_index(self.buffer)},"
            )
            print("CHAR")

        print(f"Lexeme size: {self.counter}")
        self.utils.add_text_lex_table(f"Linha: {self.line}")
        print(f"Line: {self.line}")
        self.utils.add_line("")
        self.utils.add_line("-" * 100)
        print("-" * 50)

        # Reset the internal control variables
        self.reset_status()

    def process_var(self, char, next_char):
        if self.utils.is_letter(char) or self.utils.is_number(char):
            self.buffer += char
            self.counter += 1
        else:
            self.check_delimiter()
            self.process_current_char(char, next_char)

    def process_number(self, char, next_char):
        if self.utils.is_number(char):
            self.buffer += char
            self.counter += 1
        # Check if is number mode, and do not have any . in the number
        elif char == "." and self.utils.is_number(next_char) and self.mode == "NUMBER":
            self.mode = "REAL"
            self.buffer += char
            self.counter += 1
        else:
            self.check_delimiter()
            self.process_current_char(char, next_char)

    def process_line_comment(self, char, next_char):
        if self.utils.is_line_comment_end(char):
            self.reset_status()

    def process_block_comment(self, char, next_char):
        if self.utils.is_block_comment_end(char, next_char):
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
        else:
            print(f"Invalid char for chain: {char}")
            self.chain_started = False
            self.reset_status()
            self.process_current_char(char, next_char)

    def process_char(self, char, next_char):
        # Empry char
        if char == "'" and next_char == "'":
            self.skip_next = True
            self.reset_status()
            print("-" * 50)

        # char start
        elif char == "'" and self.char_started == False:
            self.char_started = True
            self.buffer += char
            self.counter += 1

        # char end
        elif char == "'" and self.char_started == True:
            self.char_started = False
            self.buffer += char
            self.counter += 1
            self.check_delimiter()

        # Check if char is a valid char char
        elif self.utils.is_letter(char):
            self.buffer += char
            self.counter += 1

        # Check if the char is a valid char for the language
        # if yes, should work as delimiter
        else:
            print(f"Invalid char for char: {char}")
            self.char_started = False
            self.reset_status()
            self.process_current_char(char, next_char)
