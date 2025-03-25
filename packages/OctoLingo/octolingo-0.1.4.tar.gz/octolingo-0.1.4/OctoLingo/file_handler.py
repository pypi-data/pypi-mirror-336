class FileHandler:
    @staticmethod
    def read_file(file_path):
        """Read text from a file with UTF-8 encoding."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def write_file(file_path, content):
        """Write text to a file with UTF-8 encoding."""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)