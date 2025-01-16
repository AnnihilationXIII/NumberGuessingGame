from game import Game
from extensions import welcome_message, load_players

def main():
    welcome_message()
    players = load_players()
    game = Game(players)
    game.start()

if __name__ == "__main__":
    main()
