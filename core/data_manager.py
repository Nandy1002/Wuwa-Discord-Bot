import json
import os
import sys
from typing import Dict

if __name__ == '__main__' and __package__ is None:
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if root not in sys.path:
        sys.path.insert(0, root)

from models.character import Character
from models.echoset import EchoSet
from models.weapon import Weapon


class DataManager:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        self.characters = {}
        self.weapons = {}
        self.echosets = {}

    def load(self):
        self._load_weapons()
        self._load_echosets()
        self._load_characters()

    def _load_weapons(self):
        filepath = os.path.join(self.base_dir, 'weapons.json')
        if not os.path.exists(filepath):
            return
        with open(filepath, 'r', encoding='utf-8') as f:
            raw = json.load(f)
        self.weapons = {
            key.strip().lower(): Weapon(key.strip().lower(), value)
            for key, value in raw.items()
        }

    def _load_echosets(self):
        filepath = os.path.join(self.base_dir, 'echosets.json')
        if not os.path.exists(filepath):
            return
        with open(filepath, 'r', encoding='utf-8') as f:
            raw = json.load(f)
        self.echosets = {
            key.strip().lower(): EchoSet(key.strip().lower(), value)
            for key, value in raw.items()
        }

    def _load_characters(self):
        filepath = os.path.join(self.base_dir, 'characterbuilds.json')
        if not os.path.exists(filepath):
            return
        with open(filepath, 'r', encoding='utf-8') as f:
            raw = json.load(f)
        self.characters = {
            key.strip().lower(): Character(key.strip().lower(), value, self.weapons, self.echosets)
            for key, value in raw.items()
        }

    def get_character(self, key: str):
        return self.characters.get(key.strip().lower())

    def get_all_character_names(self):
        return [character.name for character in self.characters.values()]


if __name__ == '__main__':
    manager = DataManager(os.path.join(os.path.dirname(__file__), '..', 'data'))
    manager.load()
    print('Loaded characters:', manager.get_all_character_names())
