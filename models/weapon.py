class Weapon:
    def __init__(self, key: str, data: dict):
        self.key = key
        self.name = data.get('name')
        self.type = data.get('type')
        self.notes = data.get('notes')
        self.image_file = data.get('image_file')

    def format_entry(self):
        return f'• {self.name}'
