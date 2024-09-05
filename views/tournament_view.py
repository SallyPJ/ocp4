from tabulate import tabulate
from views.base_view import BaseView


class TournamentView(BaseView):

    def display_tournaments_menu(self):
        """
        Displays the tournament management menu to the user.

        This menu provides options to:
        1. Create a new tournament.
        2. Launch or resume a tournament.
        3. View completed tournaments and details.
        4. Return to the main menu.

        Returns:
            str: The user's selected option from the menu.
        """
        print("==========================================")
        print("     [ Menu de Gestion des Tournois ]")
        print("==========================================")
        print("1. Créer un Nouveau Tournoi")
        print("2. Lancer/Reprendre un Tournoi")
        print("3. Liste et détails des Tournois Terminés")
        print("4. Retour au Menu Principal")
        print("==========================================")
        return input("Choisir une option: ")

    def get_tournament_name(self):
        """
        Prompts the user to input the name of the tournament.

        Returns:
            str: The name entered by the user.
        """
        """Demande le nom du tournoi à l'utilisateur."""
        return input("Entrer le nom du tournoi: ")

    def get_tournament_location(self):
        """
        Prompts the user to input the location of the tournament.

        Returns:
            str: The location entered by the user.
        """
        return input("Entrer le lieu du tournoi: ")

    def get_tournament_date(self, date_type):
        """
        Prompts the user to input a specific date for the tournament.

        Args:
            date_type (str): Specifies whether it's the start or end date.

        Returns:
            str: The date entered by the user in the format DD/MM/YYYY.
        """
        return input(f"Entrer la date de {date_type} (JJ/MM/AAAA): ")

    def display_invalid_date_message(self, date_type):
        """
        Displays an error message when an invalid date is entered.

        Args:
            date_type (str): Specifies whether the error is for the start or end date.
        """
        print(f"La date de {date_type} n'est pas valide. "
              "Veuillez entrer la date au format JJ/MM/AAAA.")

    def get_tournament_user_feedbacks(self):
        """
        Prompts the user to enter feedback or general remarks
        about a completed tournament.

        Returns:
            str: The feedback entered by the user.
        """
        print("*** FIN DU TOURNOI ***")
        feedback = input("Entrer vos remarques ou "
                         "commentaires généraux sur le tournoi:")
        return feedback

    def show_tournament_launcher_menu(self):
        """
        Displays the tournament launcher menu, allowing the user
        to start or resume the tournament.

        Returns:
            str: The option selected by the user.
        """
        print("==========================================")
        print("     [ Menu du lancement du Tournoi ]")
        print("==========================================")
        print("1. Débuter/Relancer le Tournoi")
        print("2. Retour au menu principal")
        print("==========================================")
        return input("Choisissez une option: ")

    def get_tournament_selection(self):
        """
        Prompts the user to select one or more tournaments.

        Returns:
            str: The user's input, representing the selected tournament(s).
        """
        return input("Entrez le numéro d'un ou plusieurs tournois "
                     "(séparés par une virgule): ")

    def display_players_global_scores(self, tournament):
        """
        Displays the cumulative scores of players in the tournament.

        Args:
            tournament (Tournament): The tournament instance containing
            the players and their scores.
        """
        print("+-+-+-+ Scores cumulés  +-+-+-+")
        table_data = []
        for player in tournament.selected_players:
            full_name = f"{player.last_name} {player.first_name} "
            table_data.append([full_name, player.total_points])
        headers = ["Nom et prénom du joueur", "Points totaux"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

    def display_feedback(self, message_type, tournament=None):
        """
        Displays feedback messages based on the given message type.

        Args:
            message_type (str): The type of message to display.
            tournament (Tournament, optional): The tournament
            instance for additional context.
        """
        if message_type == "players_added":
            print("✅ Joueurs ajoutés au tournoi avec succès.")
        elif message_type == "incorrect_players_number" and tournament is not None:
            print(f"❌ Nombre incorrect de joueurs sélectionnés.\n"
                  f"Vous devez sélectionner {tournament.number_of_players} joueurs."
                  f"Veuillez réessayer.")
        elif message_type == "no_tournament_selected":
            print("⚠️ Aucun tournoi sélectionné.")
        elif message_type == "empty_feedback":
            print("⚠️ Veuillez renseigner un commentaire.")
        elif message_type == "no_filter":
            print("⚠️ Aucun statut de filtre spécifié. Affichage de "
                  "tous les tournois.")
        elif message_type == "invalid_filter_status":
            print("❌ Statut du filtre non valide. Veuillez utiliser 'not_started', "
                  "'in_progress', 'not_finished' ou 'finished'.")
        elif message_type == "invalid_round_count":
            print("❌ Le nombre de tours doit être compris entre 1 et 30.")
        elif message_type == "invalid_number_input":
            print("❌ Ce n'est pas un nombre entier valide. Veuillez entrer "
                  "un nombre entier entre 1 et 30.")
        elif message_type == "invalid_choice_YN":
            print("❌ Choix invalide. Veuillez entrer 'O' pour oui ou "
                  "'N' pour non.")
        if message_type == "no_player_file":
            print("⚠️ Le fichier 'players.json' n'existe pas. Impossible "
                  "de créer un tournoi sans joueurs.")
        elif message_type == "not_enough_players":
            print("⚠️ Il doit y avoir au moins deux joueurs enregistrés "
                  "pour créer un tournoi.")
        elif message_type == "filter_no_tournament":
            print("❌ Aucun tournoi à afficher pour le statut spécifié.")
        else:
            super().display_feedback(message_type)

    def resume_match(self, match):
        """Displays the message when resuming an in-progress match."""
        print(
            f"⏸️  Reprise du match en cours entre {match.match[0][0].first_name} "
            f"{match.match[0][0].last_name} et {match.match[1][0].first_name} "
            f"{match.match[1][0].last_name}."
        )

    def display_match_details(self, round_instance, match, match_number):
        """Displays the match details."""
        print(f"\n=== ROUND {round_instance.round_number} : MATCH {match_number}  ===")
        print(
            f"♟️ {match.match[0][0].first_name} {match.match[0][0].last_name} (Noirs) "
            f"vs {match.match[1][0].first_name} {match.match[1][0].last_name} (Blancs)"
        )
        print("=========================================\n")

    def prompt_for_match_result(self, match):
        """Prompts the user to input the result of the match."""
        while True:
            try:
                print("Veuillez choisir le résultat du match :")
                print(f"1️⃣  Victoire pour {match.match[0][0].first_name} "
                      f"{match.match[0][0].last_name}")
                print(f"2️⃣  Victoire pour {match.match[1][0].first_name} "
                      f"{match.match[1][0].last_name}")
                print("3️⃣  Egalité")
                choice = int(input("Votre choix (1, 2, 3) : "))
                if choice in [1, 2, 3]:
                    return choice
                else:
                    print("Choix invalide, veuillez entrer 1, 2 ou 3")
            except ValueError:
                print("Entrée invalide, veuillez entrer un nombre entier.")

    def update_match_score(self, match, result):
        """Updates the score of the match based on the result."""
        if result == 1:
            match.match[0][1] = 1
            print(f"\n✅  {match.match[0][0].first_name} "
                  f"{match.match[0][0].last_name} remporte la partie !\n")
        elif result == 2:
            match.match[1][1] = 1
            print(f"\n✅  {match.match[1][0].first_name} "
                  f"{match.match[1][0].last_name} remporte la partie !\n")
        elif result == 3:
            match.match[0][1] = 0.5
            match.match[1][1] = 0.5
            print("\n🤝  La partie se termine par un match nul.\n")

    def display_match_end(self, match):
        """Displays the final result of the match."""
        print(f"Fin du match. Résultats: {match.get_match_results()}")

    def display_tournament_table(self, table, headers):
        """Displays tournament's list as a table"""
        print("Liste de tous les tournois:")
        print(tabulate(table, headers, tablefmt="pretty",
                       colalign=("left", "left", "left", "left")))

    def display_tournament_details(self, tournament_details):
        print("Détails du tournoi :")
        print(tabulate(tournament_details, tablefmt="grid",
                       colalign=("left", "left")))

    def display_players(self, players, player_headers):
        print("Joueurs inscrits au tournoi:")
        print(tabulate(players, player_headers, tablefmt="grid",
                       colalign=("left", "left", "left", "left")))

    def display_no_players_message(self, tournament_name):
        print(f"Le tournoi '{tournament_name}' n'a pas de joueurs sélectionnés.")

    def display_rounds(self, rounds):
        print("Détails des rounds :")
        for round_info in rounds:
            print(f"Round {round_info['round_number']}:")
            if round_info['matches']:
                print(tabulate(round_info['matches'],
                               headers=round_info['headers'], tablefmt="grid"))
            else:
                print("Aucun match pour ce round.")
            print(f"Début du round: {round_info['start_time']} - "
                  f"Fin du round : {round_info['end_time']}")

    def display_player_scores(self, table_data, headers):
        print(tabulate(table_data, headers=headers, tablefmt="pretty",
                       colalign=("left", "right")))

    def display_tournament_description(self, description):
        print(f"Remarques et commentaires généraux sur le tournoi : {description}")

    def prompt_for_round_modification(self, default_rounds: int) -> str:
        """
        Asks the user if they want to modify the default number of rounds.

        Args:
            default_rounds (int): The default number of rounds.

        Returns:
            str: The user's choice ('o' for yes or 'n' for no).
        """
        return input(
            f"Le nombre de rounds par défaut est {default_rounds}. "
            "Souhaitez-vous le modifier ? (O/N) : ").strip().lower()

    def prompt_for_round_count(self) -> str:
        """
         Asks the user to input the number of rounds for the tournament.

        Returns:
            str: The user's input for the number of rounds.
        """
        return input("Nombre de tours (entre 1 et 30) : ")
