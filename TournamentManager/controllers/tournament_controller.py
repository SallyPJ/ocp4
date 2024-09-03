from models.database import Database
from models.tournament import Tournament
from views.tournament_view import TournamentView
from controllers.player_controller import PlayerController
from controllers.round_controller import RoundController



class TournamentController:
    def __init__(self):
        # Initialize tournament view, database, and player view
        self.database = Database()
        self.tournament_view = TournamentView()
        self.round_controller = RoundController()
        self.player_controller = PlayerController()

    def manage_tournament(self):
        """
        Manage the tournament lifecycle.

        This method repeatedly prompts the user for input
        until a valid choice is made.
        1. Create a tournament
        2. Display not_started or in_progress tournaments
        3. Display finished tournaments
        4. Exit tournament menu and open Main Menu
        """
        while True:
            choice = self.tournament_view.display_tournaments_menu()

            if choice == "1":
                self.handle_create_tournament()

            elif choice == "2":
                self.handle_tournament_selection("not_finished")

            elif choice == "3":
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
            filter_status (str): The status to filter tournaments
            by ("not_finished" or "finished").
        """
        tournaments = self.database.load_tournaments()
        uuid_index_map = (self.tournament_view.display_tournaments_list
                          (tournaments, filter_status=filter_status))
        if not uuid_index_map:
            self.tournament_view.display_message("no_tournaments_available")
            return
        user_input = self.tournament_view.get_tournament_selection()
        selected_tournaments = self.process_tournament_choices(
            user_input, tournaments, uuid_index_map)
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
                self.run_tournament(tournament)
                break
            elif choice == "2":
                break
            else:
                self.tournament_view.display_message("invalid_option")

    def run_tournament(self, tournament):
        """
        Start or resume a tournament session.

        Args:
            tournament (Tournament): The tournament instance to start or resume.
        """
        self.tournament_view.display_tournament_details(tournament)
        self.execute_tournament_rounds(tournament)
        self.collect_tournament_feedback(tournament)
        self.finalize_tournament(tournament)

    def collect_tournament_feedback(self, tournament):
        """Collect feedback from the user after the tournament ends."""
        while True:
            feedback = self.tournament_view.get_tournament_feedbacks(tournament)
            if feedback.strip():  # Check if the feedback is not empty
                tournament.description = feedback
                break
            else:
                self.tournament_view.display_message("empty_feedback")

    def finalize_tournament(self, tournament):
        """Finalize the tournament by setting its status and saving its state."""
        tournament.in_progress = False
        self.database.save_tournament_update(tournament)

    def create_tournament(self):
        """Create a new tournament by collecting user input
        and initializing a Tournament object."""
        details = self.tournament_view.get_tournament_details()
        number_of_rounds = self.tournament_view.get_round_count()
        number_of_players = self.player_view.get_player_count()
        tournament = Tournament(*details, number_of_rounds, number_of_players)

        self.add_players_to_tournament(tournament)
        self.save_tournament(tournament)

        return tournament

    def add_players_to_tournament(self, tournament):
        """Select and add players to the tournament."""
        players = self.player_controller.sort_players_alphabetically()
        self.player_view.display_players_list(players)
        selected_players = self.player_controller.select_multiple_players(players)

        if selected_players:
            tournament.selected_players.extend(selected_players)
            self.tournament_view.display_message("players_added")
        else:
            self.tournament_view.display_message("no_players_selected")

    def process_tournament_choices(self, user_input, tournaments, uuid_index_map):
        """Process the user's tournament selection input."""
        try:
            indices = [int(choice.strip()) - 1 for choice in user_input.split(',')]
            selected_uuids = {uuid_index_map.get(idx + 1) for idx in indices
                              if 0 <= idx < len(tournaments)}
            selected_tournaments = [tournament for tournament in tournaments
                                    if tournament.reference in selected_uuids]

            if not selected_tournaments:
                self.tournament_view.display_message("no_tournaments_selected")
            return selected_tournaments
        except ValueError:
            self.tournament_view.display_message("invalid_selection")
            return []

    def execute_tournament_rounds(self, tournament):
        """Run or resume a tournament, iterating through rounds and handling matches."""
        tournament.in_progress = True
        if tournament.rounds_completed:
            return
        current_round_index = self.get_current_round_index(tournament)
        for round_number in range(current_round_index + 1,
                                  tournament.number_of_rounds + 1):
            round_instance = self.round_controller.get_or_create_round(
                tournament, round_number)
            self.round_controller.play_round(round_instance, tournament)
            self.round_controller.process_round_results(tournament, round_instance)
            self.tournament_view.display_scores(tournament)
            self.database.save_tournament_update(tournament)
        tournament.rounds_completed = True
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
