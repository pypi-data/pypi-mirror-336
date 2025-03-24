class FileHandler:
    @staticmethod
    def read_file(file_path):
        """Read text from a file."""
        with open(file_path, 'r') as f:
            return f.read()

    @staticmethod
    def write_file(file_path, content):
        """Write text to a file."""
        with open(file_path, 'w') as f:
            f.write(content)