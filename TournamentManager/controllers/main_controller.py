import sys
from controllers.player_controller import PlayerController
from controllers.report_controller import ReportController
from controllers.tournament_controller import TournamentController
from views.main_view import MainView
from views.base_view import BaseView


class MainController:
    def __init__(self):
        """
        Initialize the main view and controllers for managing players, tournaments,
        and generating reports.
        """
        self.main_view = MainView()
        self.player_controller = PlayerController()
        self.tournament_controller = TournamentController()
        self.report_controller = ReportController()
        self.base_view = BaseView()

    def run(self):
        """
        Main loop for handling user input and navigating
        between different functionalities such as creating players,
        managing tournaments, and generating reports.
        """
        while True:
            # Display the main menu and get the user's choice
            choice = self.main_view.display_main_menu()
            if choice == '1':
                # Opens the players management menu
                self.player_controller.manage_player()
            elif choice == '2':
                # Handle tournament creation
                (self.tournament_controller.
                 manage_tournament())  # Create a new tournament
            elif choice == '3':
                # Display list of registered players
                self.report_controller.manage_reports()
            elif choice == '4':
                # Exit the application
                sys.exit()
            else:
                self.base_view.display_message("invalid_option")
