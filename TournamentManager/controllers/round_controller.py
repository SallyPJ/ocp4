from models.round import Round
from models.match import Match
from utils import date_utils
from models.database import Database

class RoundController:
    def __init__(self):
        self.database = Database()
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
            round_instance = Round(tournament, round_number=round_number, is_first_round=is_first_round)
            round_instance.start_time = date_utils.get_current_datetime()
            tournament.rounds.append(round_instance)
        return round_instance