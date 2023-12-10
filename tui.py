class TUI:
    def __init__(self, file_management):
        self.file_management = file_management

    def show_greetings(self):
        print("Código da Equipe: E03")
        print("Componentes:")
        print("\tEduardo Donadon; eduardodonadon.silva@ucsal.edu.br; (71) 99175-7234")
        print("\tLuis Felipe; luisfelipe.santos@ucsal.edu.br; (71) 98669-2228")
        print("\tMatheus Medeiros; matheus.medeiros@ucsal.edu.br; (71) 98821-8445\n")

    def get_user_file_path(self):
        path = input("Digite o caminho para o arquivo: ")

        if not path.endswith(".232"):
            path += ".232"

        return (
            path
            if self.file_management.check_file_exists(path)
            else self.get_user_file_path()
        )
