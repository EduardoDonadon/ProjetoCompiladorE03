import os
from contextlib import contextmanager


class FileManagement:
    def check_file_exists(self, path):
        if os.path.isabs(path):
            full_path = path
        else:
            current_directory = os.getcwd()
            full_path = os.path.join(current_directory, path)

        if os.path.exists(full_path):
            if os.path.isfile(full_path):
                _, file_extension = os.path.splitext(full_path)
                if file_extension == ".232":
                    return True
                else:
                    print(
                        f"The file extension '{file_extension}' does not "
                        "match with .232"
                    )
            else:
                print(f"The path '{full_path}' exists, but it is not a file.")
        else:
            print(f"The path '{full_path}' does not exist.")

        return False

    def get_file_header(self):
        return """
Código da Equipe: E03
Componentes:
    \tEduardo Donadon; eduardodonadon.silva@ucsal.edu.br; (71) 99175-7234
    \tLuis Felipe; luisfelipe.santos@ucsal.edu.br; (71) 98669-2228
    \tMatheus Medeiros; matheus.medeiros@ucsal.edu.br; (71) 98821-8445
"""

    @contextmanager
    def open_file(self, file_path, mode="r"):
        file = None
        try:
            file = open(file_path, mode)
            yield file
        except Exception as error:
            print(f"An error occurred while opening the file: {error}")
            raise
        finally:
            if file:
                file.close()

    def map_to_file(self, input_map, output_file):
        with open(output_file, "w") as file:
            file.write(self.get_file_header() + "\n")
            file.write(
                f"RELATÓRIO DA TABELA ED SÍMBOLOS. Texto fonte analisado: {output_file}\n"
            )
            file.write("-" * 100)
            file.write("\n")
            for _, value in input_map.items():
                line = f"{value}"
                file.write(line + "\n")

    def text_to_file(self, text, output_file):
        with open(output_file, "w") as file:
            file.write(self.get_file_header() + "\n")
            file.write(
                f"RELATÓRIO DA ANALISE LÉXICA. Texto fonte analisado: {output_file}\n"
            )
            file.write("-" * 100)
            file.write("\n")
            file.write(text)
