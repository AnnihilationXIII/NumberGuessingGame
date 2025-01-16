import os
import json
import random

class Player:
    def __init__(self, name):
        self.name = name
        self.best_score = None
        self.wins = 0
        self.losses = 0
        self.is_champion = False

    def save(self):
        file_path = f"data/players/{self.name}.json"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(self.__dict__, file)

    @staticmethod
    def load(name):
        file_path = f"data/players/{name}.json"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                player = Player(data["name"])
                player.best_score = data.get("best_score")
                player.wins = data.get("wins", 0)
                player.losses = data.get("losses", 0)
                player.is_champion = data.get("is_champion", False)
                return player
        return None

    def guess_number(self, range_start, range_end):
        while True:
            try:
                return int(input(f"{self.name}, zgadnij liczbę ({range_start} - {range_end}): "))
            except ValueError:
                print("Niepoprawna liczba. Spróbuj ponownie.")

class ProgramPlayer(Player):
    def __init__(self):
        super().__init__("T1000")

    def guess_number(self, range_start, range_end):
        return random.randint(range_start, range_end)
