class Item:
    def __init__(self, item_id: str, data: dict):
        self.id = item_id
        self.name = data.get('name')
        self.icon = data.get('icon')
