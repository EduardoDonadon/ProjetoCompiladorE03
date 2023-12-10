import re


class Utils:
    symbol_table = {}
    lex_table = """
Código da Equipe: E03
Componentes:
    \tEduardo Donadon; eduardodonadon.silva@ucsal.edu.br; (71) 99175-7234
    \tLuis Felipe; luisfelipe.santos@ucsal.edu.br; (71) 98669-2228
    \tMatheus Medeiros; matheus.medeiros@ucsal.edu.br; (71) 98821-8445\n
"""

    def get_reserved_table(self):
        return {
            "A01": "CADEIA",
            "A02": "CARACTER",
            "A03": "DECLARACOES",
            "A04": "ENQUANTO",
            "A05": "FALSE",
            "A06": "FIMDECLARACOES",
            "A07": "FIMENQUANTO",
            "A08": "FIMFUNC",
            "A09": "FIMFUNCOES",
            "A10": "FIMPROGRAMA",
            "A11": "FIMSE",
            "A12": "FUNCOES",
            "A13": "IMPRIME",
            "A14": "INTEIRO",
            "A15": "LOGICO",
            "A16": "PAUSA",
            "A17": "PROGRAMA",
            "A18": "REAL",
            "A19": "RETORNA",
            "A20": "SE",
            "A21": "SENAO",
            "A22": "TIPOFUNC",
            "A23": "TIPOPARAM",
            "A24": "TIPOVAR",
            "A25": "TRUE",
            "A26": "VAZIO",
        }

    def get_symbol_table(self):
        return self.symbol_table

    def get_lexeme_code(self, lexeme):
        return "C02"

    def get_lex_table(self):
        return self.lex_table

    def get_lex_index(self, lexeme):
        symbol = self.symbol_table[lexeme]
        return symbol["index"] if symbol else ""

    def add_line(self, text):
        self.lex_table += text + "\n"

    def add_text_lex_table(self, text):
        self.lex_table += f"{text} "

    def add_symbol(self, lexeme, type, line, code=None):
        should_update = lexeme in self.symbol_table
        index = len(self.symbol_table) + 1
        symbol_code = self.get_lexeme_code(lexeme) if not code else code

        symbol = {
            "index": index,
            "code": symbol_code,
            "lexeme": lexeme,
            "type": type,
            "lines": f"{line}",
        }
        if should_update:
            old_lines = self.symbol_table[lexeme]["lines"]
            number_of_lines = len(old_lines.split(" "))
            symbol["lines"] = (
                f"{old_lines} {line}" if number_of_lines < 5 else old_lines
            )
            symbol["index"] = self.symbol_table[lexeme]["index"]

        self.symbol_table[lexeme] = symbol

    def get_next_char(self, string, index):
        if index < len(string) - 1:
            return string[index + 1]
        else:
            return None

    def is_letter(self, char):
        # return char.isalpha()
        return re.match(r"[a-zA-Z]", char) is not None

    def is_number(self, char):
        return re.match(r"\d", char) is not None

    def is_valid_char(self, char):
        allowed_symbols = r"%(),.:;?[]{}-*/+!=#<>$\"_\'"
        pattern = f"[^a-zA-Z0-9\\s{re.escape(allowed_symbols)}]"
        return not bool(re.search(pattern, char))
        # filtered_string = re.sub(pattern, "", char)
        # return filtered_string

    def is_valid_chain_char(self, char):
        return (
            True
            if (
                self.is_letter(char)
                or self.is_number(char)
                or char == " "
                or char == "$"
                or char == "_"
                or char == "."
            )
            else False
        )

    def is_valid_exponential_char(self, char):
        return (
            True
            if (self.is_number(char) or char == "-" or char == "+" or char == "e")
            else False
        )

    def is_line_comment_start(self, char, next_char):
        return True if char == "/" and next_char == "/" else False

    def is_block_comment_start(self, char, next_char):
        return True if char == "/" and next_char == "*" else False

    def is_line_comment_end(self, char):
        return True if char == "\n" else False

    def is_block_comment_end(self, char, next_char):
        return True if char == "*" and next_char == "/" else False
