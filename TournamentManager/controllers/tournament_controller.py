from utils import date_utils
from models.database import Database
from models.round import Round
from models.tournament import Tournament
from views.tournament_view import TournamentView
from controllers.player_controller import PlayerController

class TournamentController:
    """
    TournamentController manages the lifecycle of tournaments, including creation,
    selection, launching, running, and finalizing tournaments.
    """
    def __init__(self):
        # Initialize tournament view, database, and player view
        self.date_utils = date_utils
        self.database = Database()
        self.tournament_view = TournamentView()
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
                self.display_tournament_report(tournament)
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
            choice = self.tournament_view.show_tournament_launcher_menu()
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
        self.display_basic_tournament_details(tournament)
        self.manage_tournament_rounds(tournament)
        self.collect_tournament_user_feedback(tournament)
        self.finalize_tournament(tournament)

    def handle_round_progress(self, tournament):
        """
        Manages the progress of tournament rounds, playing matches and updating scores.

        Args:
            tournament (Tournament): The tournament instance to manage.
        """
        current_round_index = self.determine_current_round_index(tournament)
        for round_number in range(current_round_index + 1, tournament.number_of_rounds + 1):
            round_instance = self.get_or_create_round(tournament, round_number)
            self.play_round(round_instance, tournament)
            self.process_round_results(tournament, round_instance)
            self.tournament_view.display_players_global_scores(tournament)
            self.save_tournament_progress(tournament)
        tournament.rounds_completed = True
        self.save_tournament_progress(tournament)

    def collect_tournament_user_feedback(self, tournament):
        """
        Collects feedback from the user after a tournament has concluded.

        Args:
            tournament (Tournament): The tournament instance for which feedback is collected.

        Returns:
            None
        """
        while True:
            feedback = self.tournament_view.get_tournament_user_feedbacks()
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
        if not tournament.rounds_completed:
            self.handle_round_progress(tournament)

    def determine_current_round_index(self, tournament):
        """
        Determines the index of the current round to either resume or start a new round.

        Args:
            tournament (Tournament): The tournament instance whose round index is being determined.

        Returns:
            int: The index of the current round.
        """
        for i in range(tournament.number_of_rounds):
            if self.get_current_round(tournament, i + 1):
                return i
        return 0

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
        Prépare la liste des tournois à afficher et délègue l'affichage à la vue.
        """
        # Filtrer les tournois si un filtre est fourni
        if filter_status:
            tournaments = self.filter_tournaments(tournaments, filter_status)

        # Vérifier si la liste de tournois est vide
        if not tournaments:
            self.tournament_view.display_no_tournaments_message()
            return {}

        # Trier les tournois par date de début
        tournaments_sorted = sorted(
            tournaments, key=lambda t: self.date_utils.parse_date(t.start_date),
            reverse=True)

        # Préparer les données pour le tableau
        table, uuid_index_map = self.prepare_tournament_table(tournaments_sorted)

        # Définir les en-têtes du tableau
        headers = ["No", "Nom", "Date de début", "Date de fin"]

        # Déléguer l'affichage à la vue
        self.tournament_view.display_tournament_table(table, headers)

        # Retourner le mapping des UUID pour référence future
        return uuid_index_map

    def prepare_tournament_table(self, tournaments):
        """
        Prépare la structure des données pour l'affichage des tournois.
        """
        table = []
        uuid_index_map = {}

        for index, tournament in enumerate(tournaments):
            table.append([index + 1, tournament.name, tournament.start_date, tournament.end_date])
            uuid_index_map[index + 1] = tournament.reference

        return table, uuid_index_map

    def get_tournament_details(self):
        """Collecte les détails du tournoi auprès de l'utilisateur via la vue."""
        name = self.tournament_view.get_tournament_name()
        location = self.tournament_view.get_tournament_location()
        start_date = self.get_valid_date("début")
        end_date = self.get_valid_date("fin")
        return name, location, start_date, end_date

    def get_valid_date(self, date_type):
        """Valide la date entrée par l'utilisateur."""
        while True:
            date_input = self.tournament_view.get_tournament_date(date_type)
            if self.date_utils.validate_date(date_input):
                return date_input
            else:
                self.tournament_view.display_invalid_date_message(date_type)

    def get_current_round(self, tournament, round_number):
        """
        Get the current round instance from the tournament.

        Args:
            tournament (Tournament): The tournament instance.
            round_number (int): The round number to check.

        Returns:
            Round: The current round instance if found, otherwise None.
        """
        for round_instance in tournament.rounds:
            if round_instance.round_number == round_number:
                # Check if there are any unfinished matches in this round
                for match in round_instance.matches:
                    if not match.finished:
                        return round_instance
        return None

    def play_round(self, round_instance, tournament):
        """
        Play or resume a round by iterating through its matches.

        Args:
            round_instance (Round): The current round instance.
            tournament (Tournament): The tournament instance.
        """
        if round_instance not in tournament.rounds:
            tournament.rounds.append(round_instance)
        if not round_instance.matches:
            round_instance.create_pairs()
            round_instance.matches = round_instance.pairs
            self.database.save_tournament_update(tournament)
        for match in round_instance.matches:
            if not match.finished:
                self.play_match(round_instance, match, tournament)
        round_instance.end_time = date_utils.get_current_datetime()
        self.database.save_tournament_update(tournament)

    def get_next_match_number(self, round_instance):
        completed_matches = sum(1 for match in round_instance.matches if match.finished)
        return completed_matches + 1

    def play_match(self, round_instance, match, tournament):
        """
        Plays a match within a specific round instance of the tournament.
        """
        if match.in_progress:
            self.tournament_view.resume_match(match)
        else:
            match.in_progress = True
            self.save_tournament_progress(tournament)
        match_number = self.get_next_match_number(round_instance)
        self.tournament_view.display_match_details(round_instance, match, match_number)
        result = self.tournament_view.get_match_result(match)
        self.tournament_view.update_match_score(match, result)
        self.end_match(match, tournament)
        self.tournament_view.display_match_end(match)

    def end_match(self, match, tournament):
        """Marks the match as finished and updates the players' total points."""
        for player, score in match.match:
            player.total_points += score
        match.finished = True
        match.in_progress = False
        self.database.save_tournament_update(tournament)

    def get_round_results(self, round_instance):
        return [pair.get_match_results() for pair in round_instance.pairs]

    def process_round_results(self, tournament, round_instance):
        """Traite les résultats des matchs pour un round donné."""
        for match in round_instance.matches:
            results = match.get_match_results()
            player1, player2 = self.get_players_from_results(tournament, results)
            if not player1 or not player2:
                print(f"Erreur: Impossible de trouver les joueurs pour le match {results}")
                continue
            # Ajouter les adversaires respectifs
            self.add_opponents(player1, player2)

    def get_players_from_results(self, tournament, results):
        """Extrait les noms des joueurs et les trouve dans la liste des joueurs du tournoi."""
        try:
            (player1_name, score1), (player2_name, score2) = list(results.items())
        except ValueError:
            print(f"Erreur dans le format du résultat du match: {results}")
            return None, None

        player1 = self.find_player_by_name(tournament, player1_name)
        player2 = self.find_player_by_name(tournament, player2_name)

        return player1, player2

    def find_player_by_name(self, tournament, player_name):
        """Trouve un joueur par son nom complet dans le tournoi."""
        return next((player for player in tournament.selected_players
                     if f"{player.first_name} {player.last_name}" == player_name), None)

    def add_opponents(self, player1, player2):
        """Ajoute les adversaires respectifs aux joueurs."""
        player1.add_opponent(player2)
        player2.add_opponent(player1)

    def get_or_create_round(self, tournament, round_number):
        """
        Get the current round or create a new one if it doesn't exist.

        Args:
            tournament (Tournament): The tournament instance.
            round_number (int): The round number.

        Returns:
            Round: The current or newly created round instance.
        """
        round_instance = self.get_current_round(tournament, round_number)
        if round_instance is None:
            is_first_round = (round_number == 1)
            round_instance = Round(tournament, round_number=round_number,
                                   is_first_round=is_first_round)
            round_instance.start_time = date_utils.get_current_datetime()
            tournament.rounds.append(round_instance)
            self.database.save_tournament_update(tournament)
        return round_instance

    def display_tournament_report(self, tournament):
        """Génère le rapport complet du tournoi."""
        self.display_basic_tournament_details(tournament)
        self.display_tournament_players(tournament)
        self.display_tournament_rounds(tournament)
        self.display_player_scores(tournament)
        self.display_tournament_description(tournament)

    def display_basic_tournament_details(self, tournament):
        """Prépare et affiche les détails du tournoi."""
        tournament_details = [
            ["Nom", tournament.name],
            ["Lieu", tournament.location],
            ["Dates", f"{tournament.start_date} - {tournament.end_date}"],
            ["Nombre de rounds", tournament.number_of_rounds],
            ["Nombre de joueurs", tournament.number_of_players]
        ]
        self.tournament_view.display_tournament_details(tournament_details)

    def display_tournament_players(self, tournament):
        """Affiche les joueurs inscrits au tournoi."""
        if hasattr(tournament, "selected_players") and tournament.selected_players:
            players = sorted(tournament.selected_players, key=lambda player: player.last_name)
            player_table = [
                [player.national_id, player.last_name, player.first_name, player.date_of_birth]
                for player in players
            ]
            player_headers = ["Identifiant National", "Nom", "Prénom", "Date de naissance"]
            self.tournament_view.display_players(player_table, player_headers)
        else:
            self.tournament_view.display_no_players_message(tournament.name)

    def display_tournament_rounds(self, tournament):
        """Affiche les détails des rounds et des matchs."""
        rounds_data = []
        for round in tournament.rounds:
            match_table = []
            for index, match in enumerate(round.matches, start=1):
                player1_name = f"{match.match[0][0].first_name} {match.match[0][0].last_name}"
                player2_name = f"{match.match[1][0].first_name} {match.match[1][0].last_name}"
                player1_result = match.match[0][1]
                player2_result = match.match[1][1]
                match_table.append([f"Match {index}", player1_name, player1_result, player2_name, player2_result])

            round_info = {
                'round_number': round.round_number,
                'matches': match_table,
                'headers': ["Match", "Joueur 1", "Résultat Joueur 1", "Joueur 2", "Résultat Joueur 2"],
                'start_time': round.start_time,
                'end_time': round.end_time
            }
            rounds_data.append(round_info)
        self.tournament_view.display_rounds(rounds_data)

    def display_player_scores(self, tournament):
        """Affiche le tableau des scores des joueurs."""
        table_data = [
            [f"{player.first_name} {player.last_name}", player.total_points]
            for player in tournament.selected_players
        ]
        headers = ["Joueur", "Score total"]
        self.tournament_view.display_player_scores(table_data, headers)

    def display_tournament_description(self, tournament):
        """Affiche la description du tournoi."""
        self.tournament_view.display_tournament_description(tournament.description)

    def get_round_count(self, default_rounds: int = 4) -> int:
        """
        Handles the logic for prompting and validating the number of rounds for a tournament.

        Args:
            default_rounds (int): The default number of rounds if no custom value is provided.

        Returns:
            int: The valid number of rounds for the tournament
        """
        while True:
            choice = self.tournament_view.prompt_for_round_modification(default_rounds)
            if choice == 'o':
                while True:
                    try:
                        number_of_rounds = int(self.tournament_view.prompt_for_round_count())
                        if 1 <= number_of_rounds <= 30:
                            return number_of_rounds
                        else:
                            self.tournament_view.display_feedback("invalid_round_count")
                    except ValueError:
                        self.tournament_view.display_feedback("invalid_number_input")
            elif choice == 'n':
                return default_rounds
            else:
                self.tournament_view.display_feedback("invalid_choice_YN")

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