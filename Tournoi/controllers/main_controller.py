import sys
from controllers.tournament_controller import TournamentController
from controllers.player_controller import PlayerController
from views.main_view import MainView
from views.player_view import PlayerView
from views.tournament_view import TournamentView
from models.database import Database


class MainController:
    def __init__(self):
        self.main_view = MainView()
        self.player_controller = PlayerController()
        self.player_view = PlayerView()
        self.tournament_view = TournamentView()
        self.tournament_controller = TournamentController()
        self.database = Database()

    def run(self):
        while True:
            choice = self.main_view.display_main_menu()
            if choice == '1':
                last_name, first_name, date_of_birth, national_id = self.player_view.get_player_details()
                self.player_controller.create_player(last_name, first_name, date_of_birth, national_id)
            elif choice == '2':
                players = self.database.load_players()
                self.player_view.display_players(players)
            elif choice == '3':
                self.tournament_controller.create_tournament()
            elif choice == '4':
                sys.exit()
            else:
                #self.view.display_message("Option invalide. Veuillez réessayer.")
                print("pouet pouet")

