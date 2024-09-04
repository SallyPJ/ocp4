import sys
from controllers.player_controller import PlayerController
from controllers.report_controller import ReportController
from controllers.tournament_controller import TournamentController
from views.main_view import MainView
from views.base_view import BaseView


class MainController:
    """
    The MainController class is responsible for coordinating the main flow of the application.

    It acts as the central controller, managing the navigation between different components
    of the application, including player management, tournament management, and report generation.
    """
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

    def run_main_menu(self):
        """
        Runs the main menu loop, handling user input and navigating between different functionalities.

        This method displays the main menu to the user and processes their choice to either:
        - Manage players,
        - Manage tournaments,
        - Generate and view reports, or
        - Exit the application.

        If an invalid option is selected, an error message is displayed.
        """
        while True:
            # Display the main menu and get the user's choice
            choice = self.main_view.display_main_menu()
            if choice == '1':
                # Opens the players management menu
                self.player_controller.run_player_menu()
            elif choice == '2':
                # Handle tournament creation
                (self.tournament_controller.
                 run_tournament_menu())  # Create a new tournament
            elif choice == '3':
                # Display list of registered players
                self.report_controller.run_report_menu()
            elif choice == '4':
                # Exit the application
                sys.exit()
            else:
                self.base_view.display_feedback("invalid_option")
