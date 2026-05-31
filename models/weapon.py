class Weapon:
    def __init__(self, key: str, data: dict):
        self.key = key
        self.name = data.get('name')
        self.rarity = data.get('rarity')
        self.type = data.get('type')
        self.base_stat = data.get('base_stat')
        self.sub_stat = data.get('sub_stat')
        self.passive = data.get('passive')
        self.icon = data.get('icon')

    def format_entry(self):
        return f'• {self.name}'
