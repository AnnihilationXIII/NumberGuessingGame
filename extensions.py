import random
from player import Player

def welcome_message():
    print("===================================")
    print("Gra w zgadywanie liczb")
    print("===================================")

def load_players():
    while True:
        try:
            num_players = int(input("Podaj liczbę graczy: "))
            if num_players < 1:
                raise ValueError("Liczba graczy musi być większa od 0.")
            break
        except ValueError as e:
            print(f"Błąd: {e}. Spróbuj ponownie.")

    players = []
    for _ in range(num_players):
        name = input("Podaj nazwę gracza: ").strip()
        if not name:
            print("Nazwa gracza nie może być pusta.")
            continue

        player = Player.load(name) or Player(name)
        players.append(player)

    return players

def choose_difficulty(leader=None):
    if leader:
        print(f"\n{leader.name}, jako lider/mistrz masz przywilej wyboru poziomu trudności!")
    print("\nWybierz poziom trudności:")
    print("1. Łatwy (0–100)")
    print("2. Normalny (0–10,000)")
    print("3. Trudny (0–1,000,000)")
    print("4. Zaawansowany (własny zakres)")

    choice = input("Twój wybór: ")
    if choice == "1":
        return "Łatwy", 0, 100
    elif choice == "2":
        return "Normalny", 0, 10000
    elif choice == "3":
        return "Trudny", 0, 1000000
    elif choice == "4":
        try:
            start = int(input("Podaj początek zakresu: "))
            end = int(input("Podaj koniec zakresu: "))
            return "Zaawansowany", start, end
        except ValueError:
            print("Nieprawidłowy zakres. Ustawiono poziom łatwy.")
            return "Łatwy", 0, 100
    else:
        print("Niepoprawny wybór, ustawiam łatwy.")
        return "Łatwy", 0, 100

def coin_toss():
    return random.choice([True, False])
