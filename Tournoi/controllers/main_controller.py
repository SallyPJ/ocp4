import sys
from controllers.tournament_controller import TournamentController
from controllers.player_controller import PlayerController
from views.main_view import MainView
from models.database import Database
from views.report_view import ReportView
from controllers.report_controller import ReportController

class MainController:
    def __init__(self):
        # Initialize views and controllers
        self.main_view = MainView()
        self.player_controller = PlayerController()
        self.tournament_controller = TournamentController()
        self.database = Database()
        self.report_view = ReportView()
        self.report_controller = ReportController()

    def run(self):
        # Main loop for menu
        while True:
            choice = self.main_view.display_main_menu()
            if choice == '1':
                # Create a new player
                player_details = self.main_view.get_player_details()
                self.player_controller.create_player(*player_details)
            elif choice == '2':
                # Create a new tournament
                self.tournament_controller.create_tournament()
            elif choice == '3':
                # Display list of registered players
                self.report_controller.manage_reports()
            elif choice == '4':
                # Exit application
                sys.exit()
            else:
                print("Option invalide. Veuillez réessayer.")
