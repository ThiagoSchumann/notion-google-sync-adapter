import os


def list_files(start_directory, ignore_directories=('venv', '.git')):
    for root, dirs, files in os.walk(start_directory):
        # Ignorar o conteúdo das pastas especificadas
        dirs[:] = [d for d in dirs if d not in ignore_directories]

        for file in files:
            print(os.path.join(root, file))


if __name__ == "__main__":
    # Substitua '.' pelo caminho do seu projeto, se necessário
    list_files('./')
