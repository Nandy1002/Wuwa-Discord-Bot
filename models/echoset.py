class EchoSet:
    def __init__(self, key: str, data: dict):
        self.key = key
        self.name = data.get('name')
        self.pieces = data.get('pieces', [])
        self.description = data.get('description')

    def format_pieces(self):
        return '\n'.join(f'• {p}' for p in self.pieces)
