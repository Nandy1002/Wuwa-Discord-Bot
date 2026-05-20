from typing import List

class Character:
    def __init__(self, key: str, data: dict, weapons: dict, echosets: dict):
        self.key = key
        self.name = data.get('name')
        self.element = data.get('element')
        self.weapon_type = data.get('weapon_type')
        self.color = data.get('color')
        self.description = data.get('description')
        self.thumbnail = data.get('thumbnail')
        self.banner = data.get('banner')
        self.image_file = data.get('image_file')

        # references
        self.best_set_key = data.get('best_set')
        self.alt_set_key = data.get('alternate_set')
        self.weapon_keys = data.get('weapons', {}).get('best', [])
        self.f2p_keys = data.get('weapons', {}).get('f2p', [])
        self.substats = data.get('substats', [])
        self.forte_priority = data.get('forte_priority', [])
        self.teams = data.get('teams', [])

        # resolve referenced objects
        self.best_set = echosets.get(self.best_set_key)
        self.alt_set = echosets.get(self.alt_set_key)
        self.weapons = [weapons[k] for k in self.weapon_keys if k in weapons]
        self.f2p = [weapons[k] for k in self.f2p_keys if k in weapons]

    def weapon_list(self) -> List[str]:
        return [w.name for w in self.weapons]

    def f2p_list(self) -> List[str]:
        return [w.name for w in self.f2p]
