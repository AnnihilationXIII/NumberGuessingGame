import os
import json


def determine_leader(players):
    if not players:
        return None

    def win_rate(player):
        if player.losses == 0:
            return float('inf')
        return player.wins / player.losses

    leader = max(players, key=lambda p: (win_rate(p), p.wins))
    return leader


class Leaderboard:
    def __init__(self, file_path="data/leaderboards.json"):
        self.file_path = file_path
        self.leaders = self.load()

    def load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as file:
                try:
                    data = json.load(file)
                    print(f"Załadowano tablicę liderów: {data}.")
                    return data
                except json.JSONDecodeError:
                    print("Plik wyników istnieje, ale jest uszkodzony. Tworzę pustą tablicę liderów.")
        else:
            print("Plik wyników nie istnieje. Tworzę nową tablicę liderów.")
        return {}

    def save(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(self.leaders, file, ensure_ascii=False, indent=4)
        print(f"Tablica liderów zapisana do {self.file_path}.")

    def update_leader(self, player_name, score):
        if player_name not in self.leaders:
            print(f"Nowy gracz {player_name} dodany do tabeli wyników z wynikiem {score}.")
            self.leaders[player_name] = score
        elif score < self.leaders[player_name]:
            print(f"Gracz {player_name} poprawił wynik: {self.leaders[player_name]} -> {score}.")
            self.leaders[player_name] = score
        else:
            print(f"Gracz {player_name} nie poprawił swojego wyniku: {self.leaders[player_name]}.")

        self.save()

    def display_leaders(self):
        if not self.leaders:
            print("\n--- Tablica liderów ---")
            print("Brak zapisanych liderów. Rozegraj kilka gier, aby uzupełnić dane.")
            return

        print("\n--- Tablica liderów ---")
        sorted_leaders = sorted(self.leaders.items(), key=lambda x: x[1])
        for rank, (player, score) in enumerate(sorted_leaders, start=1):
            print(f"{rank}. {player}: {score} prób")
