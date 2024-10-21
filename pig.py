#Stephon Kumar
import random
import argparse
import time

# Base Player class
class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.turn_total = 0

    def reset_turn_total(self):
        self.turn_total = 0

    def add_to_turn_total(self, value):
        self.turn_total += value

    def hold(self):
        self.score += self.turn_total
        self.reset_turn_total()

    def reset_score(self):
        self.score = 0

# Human Player class (inherits from Player)
class HumanPlayer(Player):
    def take_turn(self, die):
        while True:
            print(f"{self.name}'s turn. Current turn total: {self.turn_total}, Current score: {self.score}")
            action = input("Enter 'r' to roll or 'h' to hold: ").lower()

            if action == 'r':
                roll_value = die.roll()
                print(f"Rolled: {roll_value}")
                if roll_value == 1:
                    print(f"{self.name} rolled a 1. Turn over with no points added.")
                    self.reset_turn_total()
                    break
                else:
                    self.add_to_turn_total(roll_value)
            elif action == 'h':
                self.hold()
                print(f"{self.name} holds. Total score: {self.score}")
                break

# Computer Player class (inherits from Player)
class ComputerPlayer(Player):
    def take_turn(self, die):
        print(f"{self.name}'s turn. Current turn total: {self.turn_total}, Current score: {self.score}")

        while True:
            # Computer's strategy: hold if turn total >= 25 or score + turn total >= 100
            if self.turn_total >= min(25, 100 - self.score):
                self.hold()
                print(f"{self.name} holds. Total score: {self.score}")
                break
            else:
                roll_value = die.roll()
                print(f"{self.name} rolled: {roll_value}")

                if roll_value == 1:
                    print(f"{self.name} rolled a 1. Turn over with no points added.")
                    self.reset_turn_total()
                    break
                else:
                    self.add_to_turn_total(roll_value)

# Player Factory to instantiate correct player type
class PlayerFactory:
    @staticmethod
    def create_player(player_type, name):
        if player_type == "human":
            return HumanPlayer(name)
        elif player_type == "computer":
            return ComputerPlayer(name)
        else:
            raise ValueError(f"Unknown player type: {player_type}")

# Die class
class Die:
    def __init__(self):
        random.seed(0)  # Seed for consistency in testing
        self.value = 0

    def roll(self):
        self.value = random.randint(1, 6)
        return self.value

# Original Game class
class PigGame:
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.current_player = 0
        self.die = Die()
        self.winner = None

    def switch_player(self):
        self.current_player = 1 - self.current_player  # Switch between 0 and 1

    def check_winner(self):
        if self.players[self.current_player].score >= 100:
            self.winner = self.players[self.current_player].name

    def play_turn(self):
        player = self.players[self.current_player]
        player.take_turn(self.die)

        self.check_winner()
        if self.winner:
            print(f"{self.winner} wins the game!")
            return

        self.switch_player()

    def play_game(self):
        print("Welcome to the Pig Game!")
        while not self.winner:
            self.play_turn()

        print("Game over!")
        for player in self.players:
            print(f"{player.name}: {player.score}")

# Timed Game Proxy class
class TimedGameProxy(PigGame):
    def __init__(self, player1, player2):
        super().__init__(player1, player2)
        self.start_time = time.time()  # Record the start time

    def check_time_up(self):
        elapsed_time = time.time() - self.start_time
        if elapsed_time >= 60:  # 60 seconds = 1 minute
            print("Time's up!")
            # Determine the winner based on the highest score
            self.winner = max(self.players, key=lambda p: p.score).name
            print(f"{self.winner} wins based on score!")
            return True
        return False

    def play_turn(self):
        if self.check_time_up():
            return
        super().play_turn()

# Main function with argument parsing
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play the Pig game with humans or computer players.")
    parser.add_argument('--player1', type=str, default="human", help="Type of player1: 'human' or 'computer'")
    parser.add_argument('--player2', type=str, default="human", help="Type of player2: 'human' or 'computer'")
    parser.add_argument('--timed', action='store_true', help="Play the timed version of the game")

    args = parser.parse_args()

    # Create players using the factory
    player1 = PlayerFactory.create_player(args.player1, "Player 1")
    player2 = PlayerFactory.create_player(args.player2, "Player 2")

    # Determine if the game should be timed
    if args.timed:
        game = TimedGameProxy(player1, player2)
    else:
        game = PigGame(player1, player2)

    # Play the game
    game.play_game()
