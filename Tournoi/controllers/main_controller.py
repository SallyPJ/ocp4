import sys

from controllers.player_controller import PlayerController
from controllers.report_controller import ReportController
from controllers.tournament_controller import TournamentController
from views.main_view import MainView


class MainController:
    def __init__(self):
        # Initialize the main view, player controller, tournament controller, database, and report view/controller
        self.main_view = MainView()
        self.player_controller = PlayerController()
        self.tournament_controller = TournamentController()
        self.report_controller = ReportController()

    def run(self):
        """
        Main loop for handling user input and navigating between different functionalities
        such as creating players, managing tournaments, and generating reports.
        """
        while True:
            choice = self.main_view.display_main_menu()  # Display the main menu and get the user's choice
            if choice == '1':
                # Opens the players management menu
                self.player_controller.manage_player()
            elif choice == '2':
                # Handle tournament creation
                self.tournament_controller.manage_tournament()  # Create a new tournament
            elif choice == '3':
                # Display list of registered players
                self.report_controller.manage_reports()
            elif choice == '4':
                # Exit the application
                sys.exit()
            else:
                print("Option invalide. Veuillez réessayer.")
