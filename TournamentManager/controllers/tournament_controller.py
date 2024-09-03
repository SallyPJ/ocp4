from utils import date_utils

from models.database import Database
from models.tournament import Tournament
from views.tournament_view import TournamentView
from controllers.player_controller import PlayerController
from controllers.round_controller import RoundController

class TournamentController:
    """
    TournamentController manages the lifecycle of tournaments, including creation,
    selection, launching, running, and finalizing tournaments.
    """
    def __init__(self):
        # Initialize tournament view, database, and player view
        self.database = Database()
        self.tournament_view = TournamentView()
        self.round_controller = RoundController()
        self.player_controller = PlayerController()

    def run_tournament_menu(self):
        """
        Displays and manages the main tournament menu.

        Prompts the user for input to create a tournament, display and manage
        ongoing or completed tournaments, or exit the menu.

        Returns:
            None
        """
        while True:
            choice = self.tournament_view.display_tournaments_menu()
            if choice == "1":
                self.create_and_launch_tournament()
            elif choice == "2":
                self.select_and_manage_tournaments("not_finished")
            elif choice == "3":
                self.select_and_manage_tournaments("finished")
            elif choice == "4":
                break
            else:
                self.tournament_view.display_feedback("invalid_option")

    def create_and_launch_tournament(self):
        """
        Creates a new tournament and launches its management session.

        Returns:
            None
        """
        tournament = self.create_tournament()
        self.launch_tournament_menu(tournament)

    def select_and_manage_tournaments(self, filter_status):
        """
        Handles the selection and management of tournaments based on their status.

        Args:
            filter_status (str): The status to filter tournaments by
            ("not_finished" or "finished").

        Returns:
            None
        """
        tournaments = self.database.load_tournaments()
        uuid_index_map = (self.display_tournaments_list
                          (tournaments, filter_status=filter_status))
        if not uuid_index_map:
            self.tournament_view.display_feedback("no_tournaments_available")
            return
        user_input = self.tournament_view.get_tournament_selection()
        selected_tournaments = self.process_selected_tournaments(
            user_input, tournaments, uuid_index_map)
        for tournament in selected_tournaments:
            if filter_status == "finished":
                self.tournament_view.display_tournament_report(tournament)
            else:
                self.launch_tournament_menu(tournament)

    def launch_tournament_menu(self, tournament):
        """
        Manages the launch or continuation of a tournament session.

        Args:
            tournament (Tournament): The tournament instance to manage.

        Returns:
            None
        """
        while True:
            choice = self.tournament_view.show_tournament_launcher_menu(tournament)
            if choice == "1":
                self.run_tournament(tournament)
                break
            elif choice == "2":
                break
            else:
                self.tournament_view.display_feedback("invalid_option")

    def run_tournament(self, tournament):
        """
         Starts or resumes a tournament session.

        This includes managing rounds, collecting feedback, and finalizing the tournament.

        Args:
            tournament (Tournament): The tournament instance to start or resume.

        Returns:
            None
        """
        self.tournament_view.display_tournament_details(tournament)
        self.manage_tournament_rounds(tournament)
        self.collect_tournament_feedback(tournament)
        self.finalize_tournament(tournament)

    def collect_tournament_feedback(self, tournament):
        """
        Collects feedback from the user after a tournament has concluded.

        Args:
            tournament (Tournament): The tournament instance for which feedback is collected.

        Returns:
            None
        """
        while True:
            feedback = self.tournament_view.get_tournament_feedbacks(tournament)
            if feedback.strip():  # Check if the feedback is not empty
                tournament.description = feedback
                break
            else:
                self.tournament_view.display_feedback("empty_feedback")

    def finalize_tournament(self, tournament):
        """
        Finalizes the tournament by updating its status and saving its current state to the database.

        Args:
            tournament (Tournament): The tournament instance to finalize.

        Returns:
            None
        """
        tournament.in_progress = False
        self.save_tournament_progress(tournament)

    def create_tournament(self):
        """
        Creates a new tournament by collecting necessary details from the user.

        Returns:
            Tournament: The newly created Tournament instance.
        """
        details = self.get_tournament_details()
        number_of_rounds = self.tournament_view.get_round_count()
        number_of_players = self.player_controller.get_player_count()
        tournament = Tournament(*details, number_of_rounds, number_of_players)
        self.assign_players_to_tournament(tournament)
        self.save_tournament(tournament)
        return tournament

    def assign_players_to_tournament(self, tournament):
        """
        Selects and assigns players to the tournament.

        Args:
            tournament (Tournament): The tournament instance to which players are assigned.

        Returns:
            None
        """
        players = self.player_controller.display_sorted_players()
        while True:
            selected_players = self.player_controller.select_multiple_players(players)
            if selected_players:
                if len(selected_players) == tournament.number_of_players:
                    tournament.selected_players.extend(selected_players)
                    self.tournament_view.display_feedback("players_added")
                    break
                else:
                    self.tournament_view.display_feedback("incorrect_players_number", tournament)
                    selected_players.clear()
            else:
                self.tournament_view.display_feedback("no_players_selected")

    def process_selected_tournaments(self, user_input, tournaments, uuid_index_map):
        """
        Processes the user's selection of tournaments.

        Args:
            user_input (str): The user's input indicating selected tournaments.
            tournaments (list): The list of all available tournaments.
            uuid_index_map (dict): A mapping of indices to tournament UUIDs.

        Returns:
            list: A list of selected Tournament instances.
        """
        try:
            indices = [int(choice.strip()) - 1 for choice in user_input.split(',')]
            selected_uuids = {uuid_index_map.get(idx + 1) for idx in indices
                              if 0 <= idx < len(tournaments)}
            selected_tournaments = [tournament for tournament in tournaments
                                    if tournament.reference in selected_uuids]

            if not selected_tournaments:
                self.tournament_view.display_feedback("no_tournaments_selected")
            return selected_tournaments
        except ValueError:
            self.tournament_view.display_feedback("invalid_selection")
            return []

    def manage_tournament_rounds(self, tournament):
        """
        Manages the rounds of the tournament, including playing matches and processing results.

        Args:
            tournament (Tournament): The tournament instance whose rounds are being managed.

        Returns:
            None
        """
        tournament.in_progress = True
        if tournament.rounds_completed:
            return
        current_round_index = self.determine_current_round_index(tournament)
        for round_number in range(current_round_index + 1,
                                  tournament.number_of_rounds + 1):
            round_instance = self.round_controller.get_or_create_round(
                tournament, round_number)
            self.round_controller.play_round(round_instance, tournament)
            self.round_controller.process_round_results(tournament, round_instance)
            self.tournament_view.display_scores(tournament)
            self.save_tournament_progress(tournament)
        tournament.rounds_completed = True
        self.save_tournament_progress(tournament)

    def determine_current_round_index(self, tournament):
        """
        Determines the index of the current round to either resume or start a new round.

        Args:
            tournament (Tournament): The tournament instance whose round index is being determined.

        Returns:
            int: The index of the current round.
        """
        for i in range(tournament.number_of_rounds):
            if self.round_controller.get_current_round(tournament, i + 1):
                return i
        return 0

    def save_tournament(self, tournament):
        """
        Saves the tournament to the database.

        Args:
            tournament (Tournament): The tournament instance to save.

        Returns:
            None
        """
        tournaments = self.database.load_tournaments()
        tournaments.append(tournament)
        self.database.save_tournament(tournaments)

    def save_tournament_progress(self, tournament):
        """
        Encapsulates the logic to save the current state of a tournament.

        Args:
            tournament (Tournament): The tournament instance to save.

        Returns:
            None
        """
        self.database.save_tournament_update(tournament)

    def filter_tournaments(self, tournaments, filter_status):
        """
        Filter the list of tournaments based on their status.

        :param tournaments: List of Tournament objects.
        :param filter_status: Status to filter
        ('not_started', 'in_progress', not_finished or 'finished').
        :return: Filtered list of tournaments.
        """
        if filter_status is None:
            # Return all tournaments if no filter status is specified
            self.tournament_view.display_feedback("no_filter")
            return tournaments

        if filter_status == "not_started":
            # Tournament is not started if it's neither
            # in progress nor finished
            return [tournament for tournament in tournaments
                    if not tournament.in_progress and not tournament.rounds_completed]
        elif filter_status == "in_progress":
            return [tournament for tournament in tournaments
                    if tournament.in_progress and not tournament.rounds_completed]
        elif filter_status == "finished":
            return [tournament for tournament in tournaments
                    if tournament.rounds_completed and not tournament.in_progress]
        elif filter_status == "not_finished":
            return [tournament for tournament in tournaments
                    if tournament.in_progress or (not tournament.rounds_completed
                                                  and not tournament.in_progress)]
        else:
            raise ValueError(self.tournament_view.display_feedback("invalid_filter"))

    def display_tournaments_list(self, tournaments, filter_status=None):
        """
        Displays the list of tournaments sorted by start date
        from most recent to oldest.
        """
        # Filter tournaments based on status if filter_status is provided
        if filter_status:
            tournaments = self.filter_tournaments(tournaments, filter_status)
        # Check if tournaments list is empty
        if not tournaments:
            print("Aucun tournoi à afficher pour le statut spécifié.")
            return {}
        # Sort tournaments by start date
        tournaments_sorted = sorted(
            tournaments, key=lambda t: date_utils.parse_date(t.start_date),
            reverse=True)
        # Prepare the data for the table and UUID index map
        table = []
        uuid_index_map = {}
        for index, tournament in enumerate(tournaments_sorted):
            table.append([index + 1, tournament.name, tournament.start_date,
                          tournament.end_date])
            uuid_index_map[index + 1] = tournament.reference
        # Define the table headers
        headers = ["No", "Nom", "Date de début", "Date de fin"]
        # Print the table
        print("Liste de tous les tournois:")
        print(tabulate(table, headers, tablefmt="pretty",
                       colalign=("left", "left", "left", "left")))
        # Return the UUID index map for future reference
        return uuid_index_map

    def get_tournament_details(self):
        # Get tournament details from user input
        name = input("Entrer le nom du tournoi: ")
        location = input("Entrer le lieu du tournoi: ")
        # Validate start date
        while True:
            start_date = input("Entrer la date de début (JJ/MM/AAAA): ")
            if date_utils.validate_date(start_date):
                break
            else:
                print("La date de début n'est pas valide. "
                      "Veuillez entrer la date au format JJ/MM/AAAA.")

        # Validate end date
        while True:
            end_date = input("Entrer la date de fin (JJ/MM/AAAA): ")
            if date_utils.validate_date(end_date):
                break
            else:
                print("La date de fin n'est pas valide. "
                      "Veuillez entrer la date au format JJ/MM/AAAA.")
        return name, location, start_date, end_date

