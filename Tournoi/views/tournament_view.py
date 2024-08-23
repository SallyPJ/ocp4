from utils import date_utils
from tabulate import tabulate



class TournamentView:

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
                print("La date de début n'est pas valide. Veuillez entrer la date au format JJ/MM/AAAA.")

        # Validate end date
        while True:
            end_date = input("Entrer la date de fin (JJ/MM/AAAA): ")
            if date_utils.validate_date(end_date):
                break
            else:
                print("La date de fin n'est pas valide. Veuillez entrer la date au format JJ/MM/AAAA.")
        return name, location, start_date, end_date
    def get_tournament_feedbacks(self,tournament) :
        feedback = input("Entrer vos remarques ou commentaires généraux sur le tournoi:")
        tournament.description = feedback if feedback else "Aucune remarque disponible."

    def get_round_count(self, default_rounds: int = 4) -> int:
        """
                Prompts the user for the number of rounds and validates the input.

                Args:
                    default_rounds (int): Default number of rounds if the user does not provide a custom value.

                Returns:
                    int: The number of rounds for the tournament.
                """
        while True:
            choice = input(
                f"Le nombre de rounds par défaut est {default_rounds}. Souhaitez-vous le modifier ? (O/N) : ").strip().lower()
            if choice == 'o':
                while True:
                    try:
                        number_of_rounds = int(input("Nombre de tours (entre 1 et 30) : "))
                        if 1 <= number_of_rounds <= 30:
                            return number_of_rounds
                        else:
                            print("Le nombre de tours doit être compris entre 1 et 30.")
                    except ValueError:
                        print("Ce n'est pas un nombre entier. Veuillez entrer un nombre entier entre 1 et 30.")
            elif choice == 'n':
                return default_rounds
            else:
                print("Choix invalide. Veuillez entrer 'O' pour oui ou 'N' pour non.")



    def show_tournament_menu(self, tournament):
        # Display tournament management menu
        print("==========================================")
        print("           [ Menu du Tournoi ]")
        print("==========================================")
        print(f"1. Sélectionner des Joueurs pour le Tournoi ({tournament.number_of_players - len(tournament.selected_players)} joueurs à sélectionner)")
        print("2. Débuter le Tournoi")
        print("3. Retour au menu principal")
        print("==========================================")
        return input("Choisissez une option: ")

    def display_tournament_details(self, tournament):
        if tournament:
            print(f"Tournoi: {tournament.name}")
            print(f"Dates: {tournament.start_date} - {tournament.end_date}")
        else:
            print("Tournoi non trouvé.")

    def display_tournaments_list(self, tournaments):
        """
        Displays the list of tournaments sorted by start date from most recent to oldest.
        """


        # Sort tournaments by start date
        tournaments_sorted = sorted(tournaments, key=lambda t: date_utils.parse_date(t.start_date), reverse=True)

        # Prepare the data for the table and UUID index map
        table = []
        uuid_index_map = {}
        for index, tournament in enumerate(tournaments_sorted):
            table.append([index + 1, tournament.name, tournament.start_date, tournament.end_date])
            uuid_index_map[index + 1] = tournament.reference

        # Define the table headers
        headers = ["No", "Nom", "Date de début", "Date de fin" ]

        # Print the table
        print("Liste de tous les tournois:")
        print(tabulate(table, headers, tablefmt="pretty", colalign=("left","left","left","left")))

        # Return the UUID index map for future reference
        return uuid_index_map
    def select_players_input(self):
        # Get user input for player selection
        return input("Entrez les numéros des joueurs que vous voulez sélectionner (séparés par des virgules): ")

    def display_selected_players(self, players):
        # Display selected players
        print("Joueurs sélectionnés:")
        for player in players:
            print(player)

    def confirm_selection(self):
        # Confirm player selection
        return input("Confirmer la sélection ? (o/n): ")

    def display_match_info(self):
        print(f"Round {self.round_number}: {self.player1.first_name} vs {self.player2.first_name}")

    def get_tournament_selection(self):
        """
        Demande à l'utilisateur de sélectionner un ou plusieurs tournois.
        """
        return input("Entrez le numéro d'un ou plusieurs tournois (séparés par une virgule): ")

    def display_all_tournament_details(self, tournament):
        """
        Display tournament's details
        """
        # Tournament details table
        tournament_details = [
            ["Nom", tournament.name],
            ["Lieu", tournament.location],
            ["Dates", f"{tournament.start_date} - {tournament.end_date}"],
            ["Nombre de rounds", tournament.number_of_rounds],
            ["Nombre de joueurs", tournament.number_of_players]
        ]
        print("Détails du tournoi :")
        print(tabulate(tournament_details, tablefmt="grid", colalign=("left", "left")))

        # Selected players details tablee
        if hasattr(tournament, "selected_players") and tournament.selected_players:
            print(f'Joueurs inscrits au tournoi "{tournament.name}":')
            players = sorted(tournament.selected_players, key=lambda player: player.last_name)
            player_table = [
                [player.national_id, player.last_name, player.first_name, player.date_of_birth]
                for player in players
            ]
            player_headers = ["Identifiant National", "Nom", "Prénom", "Date de naissance"]

            print(tabulate(player_table, player_headers, tablefmt="grid", colalign=("left", "left", "left", "left")))
        else:
            print(f"Le tournoi '{tournament.name}' n'a pas de joueurs sélectionnés.")

        # Affichage des rounds et des matchs
        print("Détails des rounds :")
        for round in tournament.rounds:
            print(f"Round {round.round_number}:")
            if round.matches:
                match_table = []
                for index, match in enumerate(round.matches, start=1):
                    results = match.get_match_results()
                    player1_result = results.get(match.players[0].first_name, "N/A")
                    player2_result = results.get(match.players[1].first_name, "N/A")
                    match_table.append([
                        f"Match {index}",
                        match.players[0].first_name,  # Joueur 1
                        player1_result,  # Résultat du Joueur 1
                        match.players[1].first_name,  # Joueur 2
                        player2_result

                    ])

                match_headers = ["Match","Joueur 1", "Résultat Joueur 1", "Joueur 2", "Résultat Joueur 2"]
                print(tabulate(match_table, headers=match_headers, tablefmt="grid"))
            else:
                print("Aucun match pour ce round.")

            print(f"Durée : {round.start_time} - {round.end_time}")

        print(f"Remarques et commentaires généraux sur le tournoi : {tournament.description} ")


    def display_tournament_rounds_and_matches(self, tournament):
        print(f"Tournoi : {tournament.name}")
        for round in tournament.rounds:
            print(f"Tour {round.round_number} :")
            for match in round.matches:
                player1, player2 = match.players
                result1 = match.results[player1.first_name]
                result2 = match.results[player2.first_name]
                print(
                    f" - {player1.first_name} {player1.last_name} vs {player2.first_name} {player2.last_name} : {result1}-{result2}")

    def display_final_scores(self,tournament):
        # Display final scores of players
        print("Scores finaux:")
        for player in tournament.selected_players:
            print(f"{player.first_name}: {player.total_points}")


    def display_message(self, message):
        # Display a message to the user
        print(message)