class Dataset:
    def __init__(self, path: str):
        self.path = path

    def print_info(self):
        print(f"Dataset loaded from {self.path}")

    def load(self):
        pass

    def save(self):
        pass

    def merge(self, other):
        pass

