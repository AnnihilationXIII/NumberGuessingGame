import random


class Tournament:
    def __init__(self):
        self.matches = []
        self.winner = None

    def setup_bracket(self, players, mode="BO3"):
        if len(players) < 2:
            raise ValueError("Do turnieju potrzebujesz przynajmniej dwóch graczy.")

        print(f"\nTworzenie drabinki turniejowej w trybie {mode}...")
        shuffled_players = players[:]
        random.shuffle(shuffled_players)
        self.matches = [(shuffled_players[i], shuffled_players[i + 1], mode)
                        for i in range(0, len(shuffled_players) - 1, 2)]

        if len(shuffled_players) % 2 == 1:
            print(f"Gracz {shuffled_players[-1].name} automatycznie przechodzi do następnej rundy.")
            self.matches.append((shuffled_players[-1], None, mode))

    @staticmethod
    def play_match(player1, player2, range_start, range_end):
        if player2 is None:
            print(f"{player1.name} przechodzi automatycznie do następnej rundy.")
            return player1

        number_to_guess = random.randint(range_start, range_end)
        attempts_player1, attempts_player2 = 0, 0

        print(f"\nMecz: {player1.name} VS {player2.name}")
        print(f"Zgadnij liczbę w zakresie {range_start} - {range_end}")

        while True:
            print(f"\nTura gracza {player1.name}")
            guess = player1.guess_number(range_start, range_end)
            attempts_player1 += 1
            if guess < number_to_guess:
                print("Za mało!")
                range_start = max(range_start, guess + 1)
            elif guess > number_to_guess:
                print("Za dużo!")
                range_end = min(range_end, guess - 1)
            else:
                print(f"\n{player1.name} zgadł liczbę w {attempts_player1} próbach!")
                player1.wins += 1
                player1.save()
                return player1

            print(f"\nTura gracza {player2.name}")
            guess = player2.guess_number(range_start, range_end)
            attempts_player2 += 1
            if guess < number_to_guess:
                print("Za mało!")
                range_start = max(range_start, guess + 1)
            elif guess > number_to_guess:
                print("Za dużo!")
                range_end = min(range_end, guess - 1)
            else:
                print(f"\n{player2.name} zgadł liczbę w {attempts_player2} próbach!")
                player2.wins += 1
                player2.save()
                return player2

    def play_tournament(self, range_start, range_end):
        if not self.matches:
            raise ValueError("Drabinka turniejowa nie została skonfigurowana.")

        print("\n--- Rozpoczynamy turniej! ---")
        round_num = 1

        while len(self.matches) > 0:
            print(f"\n--- Runda {round_num} ---")
            next_round = []

            for match in self.matches:
                winner = self.play_match(*match[:2], range_start, range_end)
                next_round.append((winner, None, match[2]))

            self.matches = []
            if len(next_round) == 1 and next_round[0][1] is None:
                self.winner = next_round[0][0]
                break
            else:
                self.matches = [(next_round[i][0], next_round[i + 1][0], next_round[i][2])
                                for i in range(0, len(next_round) - 1, 2)]

                if len(next_round) % 2 == 1:
                    self.matches.append((next_round[-1][0], None, next_round[-1][2]))

            round_num += 1

        return self.winner

    def award_title(self, winner):
        print(f"{winner.name} otrzymuje tytuł mistrza turnieju!")
        for player, _, _ in self.matches:
            player.is_champion = False
            player.save()

        winner.is_champion = True
        winner.wins += 1
        winner.save()
