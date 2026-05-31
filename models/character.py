class Character:
    def __init__(self, key: str, data: dict):
        self.key = key
        self.name = data.get('name')
        self.rarity = data.get('rarity')
        self.type = data.get('type')
        self.element = data.get('element')
        self.weapon_type = data.get('weapon_type')
        self.color = data.get('color')
        self.description = data.get('description')
        self.thumbnail = data.get('thumbnail')
        self.banner = data.get('banner')
        self.background_url = data.get('background_url')
        self.image_url = data.get('image_url')
        self.image_file = data.get('image_file')
        self.best_set = data.get('best_set')
        self.alternate_set = data.get('alternate_set')
        self.substats = data.get('substats', [])
        self.weapons = data.get('weapons', {})
        self.forte_priority = data.get('forte_priority', [])
        self.teams = data.get('teams', [])
        self.ascension_materials = data.get('ascension_materials', {})
        self.skill_materials = data.get('skill_materials', {})

    def weapon_list(self):
        return self.weapons.get('best', [])

    def f2p_list(self):
        return self.weapons.get('f2p', [])

    @property
    def alt_set(self):
        return self.alternate_set
