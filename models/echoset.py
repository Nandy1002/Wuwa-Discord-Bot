class EchoSet:
    def __init__(self, key: str, data: dict):
        self.key = key
        self.name = data.get('name')
        self.icon = data.get('icon')
        self.set_bonus = data.get('set_bonus', {})
        #self.pieces = data.get('pieces', [])
        self.description = data.get('description')

    def format_pieces(self):
        return '\n'.join(f'• {p}' for p in self.pieces)

    def format_set_bonus(self):
        if not self.set_bonus:
            return 'No set bonus data available.'
        
        return '\n\n'.join(
            f'**{pc}pc Set Bonus:**\n{effect}'
            for pc, effect in self.set_bonus.items()
        )
