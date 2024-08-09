import sys
from controllers.tournament_controller import TournamentController
from controllers.player_controller import PlayerController
from views.main_view import MainView
from views.player_view import PlayerView
from views.tournament_view import TournamentView
from models.database import Database

class MainController:
    def __init__(self):
        # Initialize views and controllers
        self.main_view = MainView()
        self.player_controller = PlayerController()
        self.tournament_controller = TournamentController()

    def run(self):
        # Main loop for menu
        while True:
            choice = self.main_view.display_main_menu()
            if choice == '1':
                # Create a new player
                player_details = self.main_view.get_player_details()
                self.player_controller.create_player(*player_details)
            elif choice == '2':
                # Display list of registered players
                players = self.player_controller.load_players()
                self.main_view.display_players(players)
            elif choice == '3':
                # Create a new tournament
                self.tournament_controller.create_tournament()
            elif choice == '4':
                # Exit application
                sys.exit()
            else:
                print("Option invalide. Veuillez réessayer.")
