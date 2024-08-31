import random
from utils import date_utils
from models.database import Database
#from models.match import Match
#from models.round import Round
from models.tournament import Tournament
from views.player_view import PlayerView
from controllers.round_controller import RoundController
from views.tournament_view import TournamentView



class TournamentController:
    def __init__(self):
        # Initialize tournament view, database, and player view
        self.database = Database()
        self.player_view = PlayerView()
        self.tournament_view = TournamentView()
        self.round_controller = RoundController()

    def manage_tournament(self):
        """
        Manage the tournament lifecycle.

        This method repeatedly prompts the user for input until a valid choice is made.
        1. Create a tournament
        2. Display not_started or in_progress tournaments
        3. Display finished tournaments
        4. Exit tournament menu and open Main Menu
        """
        while True:
            choice = self.tournament_view.display_tournaments_menu()

            if choice == "1":
                # Create a new tournament
                self.handle_create_tournament()

            elif choice == "2":
                # Display a list of in progress tournaments
                self.handle_tournament_selection("not_finished")

            elif choice == "3":
                # Display a list of finished tournaments
                self.handle_tournament_selection("finished")

            elif choice == "4":
                break

            else:
                self.tournament_view.display_message("invalid_option")

    def handle_create_tournament(self):
        """Handles the creation of a new tournament."""
        tournament = self.create_tournament()
        self.handle_tournament_launch(tournament)

    def handle_tournament_selection(self, filter_status):
        """
        Handles the selection of tournaments based on their status.

        Args:
            filter_status (str): The status to filter tournaments by ("not_finished" or "finished").
        """
        tournaments = self.database.load_tournaments()
        uuid_index_map = self.tournament_view.display_tournaments_list(tournaments, filter_status=filter_status)
        user_input = self.tournament_view.get_tournament_selection()
        selected_tournaments = self.process_tournament_choices(user_input, tournaments, uuid_index_map)

        for tournament in selected_tournaments:
            if filter_status == "finished":
                self.tournament_view.display_tournament_report(tournament)
            else:
                self.handle_tournament_launch(tournament)

    def handle_tournament_launch(self, tournament):
        """
        Handle the launch or continuation of a tournament session.

        Args:
            tournament (Tournament): The tournament instance to manage.
        """
        while True:
            choice = self.tournament_view.show_tournament_launcher_menu(tournament)
            if choice == "1":
                self.start_tournament(tournament)
                break
            elif choice == "2":
                break
            else:
                self.tournament_view.display_message("invalid_option")

    def start_tournament(self, tournament):
        """
        Start or resume a tournament session.

        Args:
            tournament (Tournament): The tournament instance to start or resume.
        """
        self.tournament_view.display_tournament_details(tournament)
        self.run_tournament(tournament)
        self.tournament_view.display_final_scores(tournament)
        self.collect_tournament_feedback(tournament)
        self.finalize_tournament(tournament)

    def collect_tournament_feedback(self, tournament):
        """Collect feedback from the user after the tournament ends."""
        self.tournament_view.get_tournament_feedbacks(tournament)

    def finalize_tournament(self, tournament):
        """Finalize the tournament by setting its status and saving its state."""
        tournament.in_progress = False
        tournament.finished = True
        self.database.save_tournament_update(tournament)

    def create_tournament(self):
        """Create a new tournament by collecting user input and initializing a Tournament object."""
        details = self.tournament_view.get_tournament_details()
        number_of_rounds = self.tournament_view.get_round_count()
        number_of_players = self.player_view.get_player_count()
        tournament = Tournament(*details, number_of_rounds, number_of_players)

        self.add_players_to_tournament(tournament)
        self.save_tournament(tournament)

        return tournament

    def add_players_to_tournament(self, tournament):
        """Select and add players to the tournament."""
        players = sorted(self.database.load_players())
        selected_players = self.select_multiple_players(players, tournament)

        if selected_players:
            tournament.selected_players.extend(selected_players)
            self.tournament_view.display_message("players_added")
        else:
            self.tournament_view.display_message("no_players_selected")

    def select_multiple_players(self, players, tournament):
        """Handle the selection of multiple players for the tournament."""
        while True:
            self.player_view.display_players_list(players)
            player_choices = self.tournament_view.select_players_input()
            selected_players = self.process_player_choices(player_choices, players)

            if not selected_players:
                self.tournament_view.display_message("invalid_selection")
                continue

            self.tournament_view.display_selected_players(selected_players)
            if len(selected_players) == tournament.number_of_players:
                if self.tournament_view.confirm_selection().lower() == 'o':
                    return selected_players
                else:
                    self.tournament_view.display_message("players_reset")
                    selected_players.clear()
            else:
                self.tournament_view.display_message("incorrect_players_number")


    def process_player_choices(self, choices, players):
        """Process the user's player selection input."""
        try:
            indices = [int(choice.strip()) - 1 for choice in choices.split(',')]
            return [players[idx] for idx in indices if 0 <= idx < len(players)]
        except ValueError:
            self.tournament_view.display_message("invalid_selection")
            return []

    def process_tournament_choices(self, user_input, tournaments, uuid_index_map):
        """Process the user's tournament selection input."""
        try:
            indices = [int(choice.strip()) - 1 for choice in user_input.split(',')]
            selected_uuids = {uuid_index_map.get(idx + 1) for idx in indices if 0 <= idx < len(tournaments)}
            selected_tournaments = [tournament for tournament in tournaments if tournament.reference in selected_uuids]

            if not selected_tournaments:
                self.tournament_view.display_message("no_tournaments_selected")
            return selected_tournaments
        except ValueError:
            self.tournament_view.display_message("invalid_selection")
            return []

    def run_tournament(self, tournament):
        """Run or resume a tournament, iterating through rounds and handling matches."""
        tournament.in_progress = True
        current_round_index = self.get_current_round_index(tournament)

        for round_number in range(current_round_index + 1, tournament.number_of_rounds + 1):
            round_instance = self.round_controller.get_or_create_round(tournament, round_number)
            self.round_controller.play_round(round_instance, tournament)
            self.round_controller.process_round_results(tournament, round_instance)
            self.database.save_tournament_update(tournament)

    def get_current_round_index(self, tournament):
        """Determine the index of the current round to resume or start a new round."""
        for i in range(tournament.number_of_rounds):
            if self.round_controller.get_current_round(tournament, i + 1):
                return i
        return 0

    def save_tournament(self, tournament):
        """Save the tournament to the database."""
        tournaments = self.database.load_tournaments()
        tournaments.append(tournament)
        self.database.save_tournament(tournaments)





