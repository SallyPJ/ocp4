import random
from utils import date_utils
from models.database import Database
from models.match import Match
from models.round import Round
from models.tournament import Tournament
from views.player_view import PlayerView
from views.tournament_view import TournamentView


class TournamentController:
    def __init__(self):
        # Initialize tournament view, database, and player view
        self.database = Database()
        self.player_view = PlayerView()
        self.tournament_view = TournamentView()


    def manage_tournament(self):
        """
        Manage the tournament lifecycle.

        This method repeatedly prompts the user for input until a valid choice is made.

        Parameters:
        - tournament (Tournament): The tournament object to manage.

        Returns:
        None
        """
        while True:
            choice = self.tournament_view.display_tournaments_menu()
            if choice == "1":
                # Create a new tournament
                tournament = self.create_tournament()
                self.tournament_launcher_menu(tournament)
            elif choice == "2":
                # Display a list of in progress tournaments
                tournaments = self.database.load_tournaments()  # Load tournaments from the database
                uuid_index_map = self.tournament_view.display_tournaments_list(tournaments, filter_status="not_finished")  # Display tournament list
                user_input = self.tournament_view.get_tournament_selection()  # Get user selection
                selected_tournaments = self.process_tournament_choices(
                    user_input, tournaments, uuid_index_map)  # Process the user's tournament choices
                for tournament in selected_tournaments:
                    self.tournament_launcher_menu(tournament)
            elif choice == "3":
                # Display a list of co tournaments
                tournaments = self.database.load_tournaments()  # Load tournaments from the database
                uuid_index_map = self.tournament_view.display_tournaments_list(tournaments,
                                                                               filter_status="finished")  # Display tournament list
                user_input = self.tournament_view.get_tournament_selection()  # Get user selection
                selected_tournaments = self.process_tournament_choices(
                    user_input, tournaments, uuid_index_map)  # Process the user's tournament choices
                for tournament in selected_tournaments:
                    # Display details of selected tournaments
                    self.tournament_view.display_tournament_report(tournament)
            elif choice == "4":
                break
            else:
                print("Option invalide. Veuillez réessayer.")
    def tournament_launcher_menu(self,tournament):
        while True:
            choice = self.tournament_view.show_tournament_launcher_menu(tournament)
            if choice == "1":
            # Start the tournament
                if self.check_players_count(tournament):
                    self.tournament_view.display_tournament_details(tournament)
                    self.run_tournament(tournament)
                    self.tournament_view.display_final_scores(tournament)
                    self.tournament_view.get_tournament_feedbacks(tournament)
                    tournament.in_progress = False
                    tournament.finished = True
                    self.database.save_tournament_update(tournament)
                    break
                else:  #A modifier là,mettre un contrôle avant sur le nombre de joueurs
                    self.tournament_view.display_message(f"Nombre incorrect de joueurs sélectionnés.\n"
                                                        f"Joueurs enregistrés : {len(tournament.selected_players)}, Joueurs attendus : {tournament.number_of_players}.\n"
                                                        f"Réinitialisation des joueurs effectuée.\n")
                    tournament.selected_players.clear()
            elif choice == "2":
                 # Exit tournament management
                break
            else:
                print("Option invalide. Veuillez réessayer.")

    def create_tournament(self):
        """
        Create a new tournament by collecting user input and initializing a Tournament object.
        Then, call the manage_tournament method to manage the tournament lifecycle.

        Returns:
            None
        """
        # Get tournament details from the user
        details = self.tournament_view.get_tournament_details()
        # Get the number of rounds for the tournament
        number_of_rounds = self.tournament_view.get_round_count()
        # Get the number of players for the tournament
        number_of_players = self.player_view.get_player_count()
        # Create a new Tournament object
        tournament = Tournament(*details, number_of_rounds, number_of_players)

        self.add_players_to_tournament(tournament)
        tournaments = self.database.load_tournaments()
        tournaments.append(tournament)
        self.database.save_tournament(tournaments)

        return tournament


    def add_players_to_tournament(self, tournament):
        # Select players for the tournament
        loaded_players = self.database.load_players()
        players = sorted(loaded_players)  # Le tri utilise la méthode __lt__ de la classe Player
        selected_players = self.select_multiple_players(players, tournament)
        if selected_players:
            tournament.selected_players.extend(selected_players)
            self.tournament_view.display_message("Joueurs ajoutés avec succès.")
        else:
            self.tournament_view.display_message("Aucun joueur sélectionné.")
    @staticmethod
    def check_players_count(tournament):
        return len(tournament.selected_players) == tournament.number_of_players

    def select_multiple_players(self, players, tournament):
        # Select multiple players for the tournament
        while True:
            self.player_view.display_players_list(players)
            player_choices = self.tournament_view.select_players_input()
            selected_players = self.process_player_choices(player_choices, players)

            if selected_players:
                self.tournament_view.display_selected_players(selected_players)
                if len(selected_players) == tournament.number_of_players:
                    confirmation = self.tournament_view.confirm_selection()
                    if confirmation.lower() == 'o':
                        return selected_players
                    else:
                        self.tournament_view.display_message("La sélection des joueurs a été réinitialisée.")
                else:
                    self.tournament_view.display_message(f"Nombre incorrect de joueurs sélectionnés.\n"
                                                         f"Vous devez sélectionner {tournament.number_of_players} "
                                                         f"joueurs. Veuillez réessayer.")
            else:
                self.tournament_view.display_message("Sélection invalide. Veuillez réessayer.")

    def process_player_choices(self, choices, players):
        # Process player choices based on user input
        try:
            indices = [int(choice.strip()) - 1 for choice in choices.split(',')]
            return [players[idx] for idx in indices if 0 <= idx < len(players)]
        except ValueError:
            self.tournament_view.display_message("Entrée invalide. Veuillez entrer des numéros valides.")
            return []



    def process_tournament_choices(self, user_input,tournaments, uuid_index_map):
        """
        Traite les choix de tournois basés sur l'entrée utilisateur.
        """
        try:
            indices = [int(choice.strip()) - 1 for choice in user_input.split(',')]

            # Trouver les UUID correspondant aux indices
            selected_uuids = {uuid_index_map.get(idx + 1) for idx in indices if 0 <= idx < len(tournaments)}

            # Trouver les tournois correspondant aux UUID sélectionnés
            selected_tournaments = [tournament for tournament in tournaments
                                    if tournament.reference in selected_uuids]
            if not selected_tournaments:
                self.tournament_view.display_message("Aucun tournoi sélectionné.")
            return selected_tournaments
        except ValueError:
            self.tournament_view.display_message("Entrée invalide. Veuillez entrer des numéros valides.")
            return []

    def run_tournament(self, tournament):
        """
        Run or resume a tournament, iterating through rounds and handling matches.

        Args:
            tournament (Tournament): The tournament instance to be run.
        """
        tournament.in_progress = True
        current_round_index = 0



        # Determine the current round to resume or start a new round
        for i in range(tournament.number_of_rounds):
            round_instance = self.get_current_round(tournament, i + 1)
            if round_instance:
                current_round_index = i
                break

        # Execute or resume rounds from the current incomplete round
        for i in range(current_round_index, tournament.number_of_rounds):
            round_instance = self.get_current_round(tournament, i + 1)
            if round_instance is None:
                # This condition is met when there's no existing round instance to resume, thus a new round is started
                is_first_round = (i == 0)  # Check if it's the first round
                start_time = date_utils.get_current_datetime()
                round_instance = Round(tournament, round_number=i + 1, is_first_round=is_first_round)
                round_instance.start_time = start_time
                self.play_round(round_instance, tournament)
                end_time = date_utils.get_current_datetime()
                round_instance.end_time = end_time
                self.process_round_results(tournament, round_instance)
                self.database.save_tournament_update(tournament)
            else:
                # Update scores from all previously finished matches before resuming or starting the tournament
                #self.update_scores_from_finished_matches(tournament)
                # If the round exists and needs to be resumed or continued
                self.play_round(round_instance, tournament)
                end_time = date_utils.get_current_datetime()
                round_instance.end_time = end_time

                self.process_round_results(tournament, round_instance)
                self.database.save_tournament_update(tournament)


def update_scores_from_finished_matches(self, tournament):
    """Update players' scores based on the results of finished matches."""
    for round in tournament.rounds:
        for match in round.matches:
            if match.finished:
                # Assume the results dictionary stores scores with player first names as keys
                for player in match.players:
                    player_score = match.results.get(player.first_name, 0)
                    player.total_points += player_score


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
    # Ensure round is part of tournament
    if round_instance not in tournament.rounds:
        tournament.rounds.append(round_instance)

    # Only create pairs if no matches have been generated yet
    if not round_instance.matches:
        round_instance.create_pairs()
        round_instance.matches = round_instance.pairs
        self.database.save_tournament_update(tournament)  # Sauvegarde de l'état du tournoi entier

    # Go through each match and play it if it hasn't finished yet
    for match in round_instance.matches:
        if match.in_progress:
            print(
                f"Reprise du match en cours entre {match.players[0].first_name} et {match.players[1].first_name}.")
            self.play_match(round_instance, match, tournament)
        elif not match.finished:
            self.play_match(round_instance, match, tournament)

    self.database.save_tournament_update(tournament)  # Save tournament state after the round


def play_match(self, round_instance, match, tournament):
    """
    Plays a match within a specific round instance of the tournament.

    This method handles the logic for playing a match, recording results,
    and updating the match state. It prints information about the match
    and prompts the user to input the match result.

    Args:
        round_instance (Round): The current round instance in which the match is being played.
        match (Match): The match instance to be played.
        tournament (Tournament): The tournament instance.
    """
    if match.finished:
        print(
            f"⚠️  Ce match entre {match.players[0].first_name} {match.players[0].last_name} et {match.players[1].first_name} {match.players[1].last_name} est déjà terminé.")
        return

    if match.in_progress:
        print(
            f"⏸️  Reprise du match en cours entre {match.players[0].first_name} {match.players[0].last_name} et {match.players[1].first_name} {match.players[1].last_name}.")
    else:
        match.in_progress = True
        self.database.save_tournament_update(tournament)

    # Record the results of a match
    print(f"\n=== ROUND {round_instance.round_number} : MATCH D'ÉCHECS ===")
    print(
        f"♟️ {match.players[0].first_name} {match.players[0].last_name} (Noirs) vs {match.players[1].first_name} {match.players[1].last_name} (Blancs)")
    print("=========================================\n")
    while True:
        try:
            print("Veuillez choisir le résultat du match :")
            print(f"1️⃣  Victoire pour {match.players[0].first_name} {match.players[0].last_name} (Noirs)")
            print(f"2️⃣  Victoire pour {match.players[1].first_name} {match.players[1].last_name} (Blancs)")
            print("3️⃣  Egalité")
            choice = int(input("Votre choix (1, 2, 3) : "))

            if choice == 1:
                match.results[match.players[0].first_name] = 1
                match.finished = True
                print(f"\n✅  {match.players[0].first_name} {match.players[0].last_name} remporte la partie !\n")
                break
            elif choice == 2:
                match.results[match.players[1].first_name] = 1
                match.finished = True
                print(f"\n✅  {match.players[1].first_name} {match.players[1].last_name} remporte la partie !\n")
                break
            elif choice == 3:
                match.results[match.players[0].first_name] = 0.5
                match.results[match.players[1].first_name] = 0.5
                match.finished = True
                print(f"\n🤝  La partie se termine par un match nul.\n")
                break
            else:
                print("Choix invalide, veuillez entrer 1, 2 ou 3")

        except ValueError:
            print("Entrée invalide, veuillez entrer un nombre entier.")

    # Record total_points for each player
    for player in match.players:
        player.total_points += match.results[player.first_name]
    # Mark match as finished and save state
    match.finished = True
    match.in_progress = False
    print(f"Fin du match. Résultats: {match.results}")
    self.database.save_tournament_update(tournament)


def get_round_results(self, round_instance):
    # Return match results
    return [pair.get_match_results() for pair in round_instance.pairs]


def process_round_results(self, tournament, round_instance):
    results = self.get_round_results(round_instance)
    for match_result in results:
        if isinstance(match_result, dict) and len(match_result) == 2:
            # Assurez-vous que match_result est un dictionnaire avec exactement deux éléments
            player1_name, score1 = list(match_result.items())[0]
            player2_name, score2 = list(match_result.items())[1]

            # Trouvez les objets Player correspondant aux noms
            player1 = next(player for player in tournament.selected_players if player.first_name == player1_name)
            player2 = next(player for player in tournament.selected_players if player.first_name == player2_name)

            # Ajouter les adversaires aux listes correspondantes
            player1.opponents.append(player2)
            player2.opponents.append(player1)
        else:
            print(f"Erreur dans le résultat du match: {match_result}")



