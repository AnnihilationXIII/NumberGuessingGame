import random
import time
from player import ProgramPlayer
from leaderboard import Leaderboard
from tournament import Tournament
from extensions import coin_toss, choose_difficulty

class Game:
    def __init__(self, players):
        self.players = players
        self.program = ProgramPlayer()
        self.leaderboard = Leaderboard()
        self.tournament = Tournament()

    def start(self):
        while True:
            print("\nWybierz tryb gry:")
            print("1. Single Player")
            print("2. Multiplayer")
            print("3. Turniej")
            print("4. Tryb odwrotny")
            print("5. Tryb mieszany")
            print("6. Wyświetl wyniki")
            print("7. Wyjście")

            choice = input("Twój wybór: ")
            if choice == "1":
                self.repeat_game(self.single_player_mode)
            elif choice == "2":
                self.repeat_game(self.multiplayer_mode)
            elif choice == "3":
                self.repeat_game(self.tournament_mode)
            elif choice == "4":
                self.repeat_game(self.reverse_mode)
            elif choice == "5":
                self.repeat_game(self.mixed_mode)
            elif choice == "6":
                self.leaderboard.display_leaders()
            elif choice == "7":
                print("Dziękujemy za grę!")
                break
            else:
                print("Niepoprawny wybór.")

    @staticmethod
    def repeat_game(game_mode):
        while True:
            game_mode()
            replay = input("\nCzy chcesz zagrać ponownie w ten tryb? (tak/nie): ").strip().lower()
            if replay != "tak":
                print("Powrót do menu głównego.")
                break

    def single_player_mode(self):
        print("\n--- Tryb Single Player ---")
        player = self.players[0]
        difficulty, range_start, range_end = choose_difficulty()

        number_to_guess = random.randint(range_start, range_end)
        attempts = 0

        print(f"\nZgadnij liczbę w zakresie {range_start} - {range_end}.")

        while True:
            try:
                guess = int(input(f"Twoja liczba ({range_start} - {range_end}): "))
                attempts += 1

                if guess < range_start or guess > range_end:
                    print(f"Liczba spoza zakresu! Wprowadź liczbę z zakresu {range_start} - {range_end}.")
                    continue

                if guess < number_to_guess:
                    print("Za mało!")
                    range_start = max(range_start, guess + 1)
                elif guess > number_to_guess:
                    print("Za dużo!")
                    range_end = min(range_end, guess - 1)
                else:
                    print(f"Brawo! Zgadłeś liczbę w {attempts} próbach!")
                    if player.best_score is None or attempts < player.best_score:
                        player.best_score = attempts
                    player.wins += 1
                    player.save()
                    self.leaderboard.update_leader(player.name, attempts)
                    break
            except ValueError:
                print("Niepoprawny format liczby. Wprowadź liczbę całkowitą.")

    def multiplayer_mode(self):
        print("\n--- Tryb Multiplayer ---")
        if len(self.players) < 2:
            print("Potrzebujesz przynajmniej dwóch graczy!")
            return

        champion = next((p for p in self.players if p.is_champion), None)
        if champion:
            print(f"\nMistrz {champion.name} ma przywilej wyboru poziomu trudności!")
            difficulty, range_start, range_end = choose_difficulty(leader=champion)
            self.players.remove(champion)
            self.players.insert(0, champion)
        else:
            difficulty, range_start, range_end = choose_difficulty()

        number_to_guess = random.randint(range_start, range_end)
        print(f"\nZgadnij liczbę w zakresie {range_start} - {range_end}.")

        while True:
            for player in self.players:
                print(f"\nTura gracza {player.name}")
                guess = player.guess_number(range_start, range_end)
                if guess < number_to_guess:
                    print("Za mało!")
                    range_start = max(range_start, guess + 1)
                elif guess > number_to_guess:
                    print("Za dużo!")
                    range_end = min(range_end, guess - 1)
                else:
                    print(f"\nBrawo! {player.name} zgadł liczbę!")
                    player.wins += 1
                    player.save()
                    self.leaderboard.update_leader(player.name, +1)
                    for p in self.players:
                        if p != player:
                            p.losses += 1
                            p.save()

    def reverse_mode(self):
        print("\n--- Rozgrywka odwrotna ---")
        difficulty, range_start, range_end = choose_difficulty()

        while True:
            try:
                target_number = int(input(f"\nPodaj swoją liczbę z zakresu {range_start} - {range_end}: "))
                if range_start <= target_number <= range_end:
                    break
                else:
                    print(f"Liczba musi być z zakresu {range_start} - {range_end}")
            except ValueError:
                print("To nie jest prawidłowa liczba. Spróbuj ponownie.")

        attempts = 0
        current_start = range_start
        current_end = range_end

        while current_start <= current_end:
            guess = (current_start + current_end) // 2
            attempts += 1
            print("\nT1000 analizuje...")
            time.sleep(0.5)
            print(f"Program zgaduje: {guess}")
            time.sleep(0.5)

            if guess == target_number:
                print("\nT1000 przetwarza wynik...")
                time.sleep(1)
                print(f"Program zgadł liczbę {target_number} w {attempts} próbach!")
                self.program.best_score = min(self.program.best_score or attempts, attempts)
                self.program.wins += 1
                self.program.save()
                self.leaderboard.update_leader(self.program.name, attempts)
                break
            elif guess < target_number:
                print("T1000 dostosowuje zakres w górę...")
                time.sleep(0.5)
                current_start = guess + 1
            else:
                print("T1000 dostosowuje zakres w dół...")
                time.sleep(0.5)
                current_end = guess - 1

        if current_start > current_end:
            print("Coś poszło nie tak. Program nie mógł znaleźć twojej liczby.")

    def mixed_mode(self):
        print("\n--- Tryb Mieszany ---")
        difficulty, range_start, range_end = choose_difficulty()
        number_to_guess = random.randint(range_start, range_end)
        attempts_player, attempts_program = 0, 0
        player_turn = coin_toss()
        print(f"Rozpoczyna {'gracz' if player_turn else 'program'}!")

        while True:
            if player_turn:
                guess = int(input(f"Zgadnij liczbę ({range_start} - {range_end}): "))
                attempts_player += 1
                if guess < number_to_guess:
                    print("Za mało!")
                    range_start = max(range_start, guess + 1)
                elif guess > number_to_guess:
                    print("Za dużo!")
                    range_end = min(range_end, guess - 1)
                else:
                    print(f"Brawo! Gracz zgadł liczbę w {attempts_player} próbach!")
                    self.players[0].wins += 1
                    self.players[0].save()
                    self.leaderboard.update_leader(self.players[0].name, attempts_player)
                    break
            else:
                guess = random.randint(range_start, range_end)
                print(f"Program zgaduje: {guess}")
                attempts_program += 1
                if guess < number_to_guess:
                    print("Program: Za mało!")
                    range_start = max(range_start, guess + 1)
                elif guess > number_to_guess:
                    print("Program: Za dużo!")
                    range_end = min(range_end, guess - 1)
                else:
                    print(f"Program zgadł liczbę w {attempts_program} próbach!")
                    self.program.wins += 1
                    self.program.save()
                    self.leaderboard.update_leader(self.program.name, attempts_program)
                    break
            player_turn = not player_turn

    def tournament_mode(self):
        print("\n--- Tryb Turniejowy ---")

        try:
            mode = input("Wybierz tryb turnieju (BO1, BO3, BO5): ").strip().upper()
            if mode not in {"BO1", "BO3", "BO5"}:
                raise ValueError("Niepoprawny tryb turnieju. Dostępne: BO1, BO3, BO5.")

            difficulty, range_start, range_end = choose_difficulty()

            if any(player.is_champion for player in self.players):
                champion = next(player for player in self.players if player.is_champion)
                print(f"\nMistrz {champion.name} bierze udział w turnieju!")

            self.tournament.setup_bracket(self.players, mode)
            winner = self.tournament.play_tournament(range_start, range_end)
            self.tournament.award_title(winner)
            print(f"\nZwycięzca turnieju: {winner.name}")

        except ValueError as e:
            print(f"Błąd: {e}")
        except Exception as e:
            print(f"Nieoczekiwany błąd: {e}")
