import re


class Utils:
    def get_reserved_table(self):
        return {
            "A01": "CADEIA",
            "A02": "CARACTER",
            "A03": "DECLARACOES",
        }

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
        allowed_symbols = r"%(),:;?[]{}-*/+!=#<>"
        pattern = f"[^a-zA-Z0-9\\s{re.escape(allowed_symbols)}]"
        return not bool(re.search(pattern, char))
        # filtered_string = re.sub(pattern, "", char)
        # return filtered_string

    def is_line_comment_start(self, char, next_char):
        return True if char == "/" and next_char == "/" else False

    def is_block_comment_start(self, char, next_char):
        return True if char == "/" and next_char == "*" else False

    def is_line_comment_end(self, char, next_char):
        pass

    def is_block_comment_end(self, char, next_char):
        return True if char == "*" and next_char == "/" else False
