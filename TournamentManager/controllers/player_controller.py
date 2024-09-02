from models.database import Database
from models.player import Player
from views.player_view import PlayerView
from views.base_view import BaseView


class PlayerController:
    """
    Controller class responsible for managing player-related operations such as
    creating players, displaying registered players, and interacting with the view.
    """
    def __init__(self):
        """
        Initialize the PlayerController with an associated view and database.
        """
        self.player_view = PlayerView()
        self.database = Database()
        self.base_view = BaseView()

    def manage_player(self):
        """
       Main loop to manage player operations. Presents a menu to the user and
       executes the corresponding actions based on the user's choice.
       1. Create a new player
       2. Display registered players
       3. Exit to the main menu
       """
        while True:
            choice = self.player_view.display_players_menu()
            if choice == "1":
                self.handle_create_player()
            elif choice == "2":
                self.display_registered_players()
            elif choice == "3":
                # Exit the loop and return to the main menu
                break
            else:
                self.base_view.display_message("invalid_option")

    def create_player(self, last_name, first_name, date_of_birth, national_id):
        try:
            # Create a new player and save to the database
            new_player = Player(last_name, first_name, date_of_birth, national_id)
            players = self.database.load_players()
            players.append(new_player)
            self.database.save_players(players)
            print("Joueur créé avec succès !")
        except Exception as e:
            print(f"Erreur lors de la création du joueur : {str(e)}")

    def handle_create_player(self):
        """
        Handles the creation of a new player. It interacts with the view to gather
        player details, creates a Player instance, and saves it to the database.

        Exceptions:
            Handles any exceptions that might occur during player creation.
        """
        try:
            # Get player details from the user
            player_details = self.player_view.get_player_details()
            # Create the player using player controller
            self.create_player(*player_details)
        except Exception as e:
            print(f"Une erreur est survenue lors de la création du joueur : {str(e)}")

    def display_registered_players(self):
        """
        Retrieves and displays a list of registered players, sorted alphabetically
        by their last name.

        Exceptions:
            Handles any exceptions that might occur while loading or displaying players.
        """
        try:
            # Load and sort players alphabetically
            players = sorted(self.database.load_players())
            # Display the sorted list of players
            self.player_view.display_players_list(players)
        except Exception as e:
            print(f"Une erreur est survenue lors de l'affichage des joueurs : {str(e)}")
