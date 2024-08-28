from models.database import Database
from models.player import Player
from views.player_view import PlayerView

class PlayerController:
    def __init__(self):
        # Initialize view and database
        self.player_view = PlayerView()
        self.database = Database()

    def manage_player(self):
        while True:
            choice = self.player_view.display_players_menu()
            if choice == "1":
                # Handle player creation
                player_details = self.player_view.get_player_details()  # Get player details from the user
                self.create_player(*player_details)  # Create the player using player controller
            elif choice == "2":
                # Display registered players by alphabetical order
                loaded_players = self.database.load_players()  # Load players from the database
                players = sorted(loaded_players)  # Sort players alphabetically (last name)
                self.player_view.display_players_list(players)  # Display the sorted list of players
            elif choice == "3":
                # Main menu
                break
            else:
                print("Option invalide. Veuillez réessayer.")

    def create_player(self, last_name, first_name, date_of_birth, national_id):
        # Create a new player and save to the database
        new_player = Player(last_name, first_name, date_of_birth, national_id)
        players = self.database.load_players()
        players.append(new_player)
        self.database.save_players(players)





