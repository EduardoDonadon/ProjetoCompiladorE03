import re


class Utils:
    def __init__(self, symbol_table, lex_table):
        self.symbol_table = symbol_table
        self.symbol_table = lex_table

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
            # --------------
            "B01": "%",
            "B02": "(",
            "B03": ")",
            "B04": ",",
            "B05": ":",
            "B06": ":=",
            "B07": ";",
            "B08": "?",
            "B09": "[",
            "B10": "]",
            "B11": "{",
            "B12": "}",
            "B13": "-",
            "B14": "*",
            "B15": "/",
            "B16": "+",
            "B17": "!=",
            "B17.2": "#",
            "B18": "<",
            "B19": "<=",
            "B20": "==",
            "B21": ">",
            "B22": ">=",
            # --------------
            "C01": "consCadeia",
            "C02": "consCaracter",
            "C03": "consInteiro",
            "C04": "consReal",
            "C05": "nomFuncao",
            "C06": "nomPrograma",
            "C07": "variavel",
        }

    def get_lex_code(self, lexeme):
        table = self.get_reserved_table()
        if any(lexeme == value for value in table.values()):
            for key, value in table.items():
                if value == lexeme:
                    return key
        return "A02"

    def add_lex_table(self, lexeme, line):
        code = self.get_lex_code(lexeme)

        if len(lexeme) > 0 and not lexeme == "\n":
            self.lex_table.append(
                {
                    "Lexeme": lexeme,
                    "Codigo": code,
                    "IndiceTabSimb": None,
                    "Linha": line,
                }
            )

    def update_lex_codes(self):
        for item in self.lex_table:
            index_tab_simb = self.get_lex_index(item.get("Lexeme"))
            item["IndiceTabSimb"] = index_tab_simb

    def get_symbol_table(self):
        return self.symbol_table

    def get_lex_table(self):
        return self.lex_table

    def get_lex_index(self, lexeme):
        symbol = self.symbol_table.get(lexeme)
        return symbol["index"] if symbol else ""

    def get_lexeme_code(self, lexeme):
        if lexeme.startswith('"'):
            return "C01"
        if lexeme.startswith("'"):
            return "C02"
        if self.is_number(lexeme) and "." not in lexeme:
            return "C03"
        if self.is_number(lexeme) and "." in lexeme:
            return "C04"
        return "C07"

    def truncate(self, lexeme):
        return lexeme[:30]

    def get_lex_type(self, lexeme):
        if lexeme == "TRUE" or lexeme == "FALSE":
            return "BOO"
        elif lexeme.startswith("'") or lexeme.startswith('"'):
            return "CHC"
        elif self.is_letter(lexeme):
            return "STR"
        elif self.is_number(lexeme) and "." in lexeme:
            return "PFO"
        elif self.is_number(lexeme) and "." not in lexeme:
            return "INT"
        else:
            return "VOI"

    def add_symbol(self, lexeme, line):
        should_update = lexeme in self.symbol_table
        index = len(self.symbol_table) + 1
        symbol_code = self.get_lexeme_code(lexeme)
        type = self.get_lex_type(lexeme)

        lenBeforeTrunc = len(lexeme)
        lenAfterTrunc = None
        if lenBeforeTrunc > 30:
            lexeme = self.truncate(lexeme)
            lenAfterTrunc = len(lexeme)

        symbol = {
            "index": index,
            "code": symbol_code,
            "lexeme": lexeme,
            "type": type,
            "lenBeforeTrunc": lenBeforeTrunc,
            "lenAfterTrunc": lenAfterTrunc,
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
        allowed_symbols = r"_$.=\"\'"
        pattern = f"[a-zA-Z0-9\\s{re.escape(allowed_symbols)}]"
        is_valid = bool(re.search(pattern, char))
        return (
            any(char == value for value in self.get_reserved_table().values())
            or is_valid
        )

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
