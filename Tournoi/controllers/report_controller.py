from views.report_view import ReportView
from controllers.player_controller import PlayerController
from views.player_view import PlayerView
from models.database import Database
from views.tournament_view import TournamentView
from controllers.tournament_controller import TournamentController

class ReportController:

    def __init__(self):
        # Initialize view and database
        self.report_view = ReportView()
        self.player_controller = PlayerController()
        self.tournament_view = TournamentView()
        self.player_view = PlayerView()
        self.database = Database()
        self.tournament_controller = TournamentController()



    def manage_reports(self):
        while True:
            choice = self.report_view.show_reports_main_menu()
            if choice == '1':
                # Display registered players by alphabetical order
                loaded_players = self.database.load_players()
                players = sorted(loaded_players)  # Le tri utilise la méthode __lt__ de la classe Player
                self.player_view.display_players_list(players)
            elif choice == '2':
                # Display tournaments list
                tournaments = self.database.load_tournaments()
                self.tournament_view.display_tournaments_list(tournaments)
                user_input = self.tournament_view.get_tournament_selection()
                selected_tournaments = self.tournament_controller.process_tournament_choices(user_input,tournaments)
                for tournament in selected_tournaments:
                    self.tournament_view.display_all_tournament_details(tournament)
                    #self.report_view.display_tournament_players(tournaments)
            elif choice == '3':
                # Display the list of all tournaments
                break
            elif choice == '4':
                # Exit application
                break
            else:
                print("Option invalide. Veuillez réessayer.")