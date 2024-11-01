class Colored:
    GREEN = '\033[92m'  # Success
    YELLOW = '\033[93m'  # Warning
    RED = '\033[91m'  # Error
    RESET = '\033[0m'  # Reset

    @staticmethod
    def success(message):
        """Print a success message in green."""
        print(f"{Colored.GREEN}{message}{Colored.RESET}")

    @staticmethod
    def warning(message):
        """Print a warning message in yellow."""
        print(f"{Colored.YELLOW}{message}{Colored.RESET}")

    @staticmethod
    def error(message):
        """Print an error message in red."""
        print(f"{Colored.RED}{message}{Colored.RESET}")

    @staticmethod
    def info(message):
        """Print an informational message in default color."""
        print(message)
