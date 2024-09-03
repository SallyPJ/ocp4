from tabulate import tabulate
from views.base_view import BaseView


class TournamentView(BaseView):

    def display_tournaments_menu(self):
        print("==========================================")
        print("     [ Menu de Gestion des Tournois ]")
        print("==========================================")
        print("1. Créer un Nouveau Tournoi")
        print("2. Lancer/Reprendre un Tournoi")
        print("3. Liste et détails des Tournois Terminés")
        print("4. Retour au Menu Principal")
        print("==========================================")
        return input("Choisir une option: ")

    def get_tournament_feedbacks(self, tournament):
        print("*** FIN DU TOURNOI ***")
        feedback = input("Entrer vos remarques ou "
                         "commentaires généraux sur le tournoi:")
        return feedback

    def show_tournament_launcher_menu(self, tournament):
        # Display tournament management menu
        print("==========================================")
        print("     [ Menu du lancement du Tournoi ]")
        print("==========================================")
        print("1. Débuter/Relancer le Tournoi")
        print("2. Retour au menu principal")
        print("==========================================")
        return input("Choisissez une option: ")


    def get_round_count(self, default_rounds: int = 4) -> int:
        """
                Prompts the user for the number of rounds
                and validates the input.

                Args:
                    default_rounds (int): Default number of rounds
                    if the user does not provide a custom value.

                Returns:
                    int: The number of rounds for the tournament.
                """
        while True:
            choice = input(
                f"Le nombre de rounds par défaut est {default_rounds}."
                f" Souhaitez-vous le modifier ? (O/N) : ").strip().lower()
            if choice == 'o':
                while True:
                    try:
                        number_of_rounds = int(input(
                            "Nombre de tours (entre 1 et 30) : "))
                        if 1 <= number_of_rounds <= 30:
                            return number_of_rounds
                        else:
                            print("Le nombre de tours doit être compris entre 1 et 30.")
                    except ValueError:
                        print("Ce n'est pas un nombre entier. "
                              "Veuillez entrer un nombre entier entre 1 et 30.")
            elif choice == 'n':
                return default_rounds
            else:
                print("Choix invalide. Veuillez entrer 'O' pour oui ou 'N' pour non.")


    def display_tournament_details(self, tournament):
        if tournament:
            print(f"Tournoi: {tournament.name}")
            print(f"Dates: {tournament.start_date} - {tournament.end_date}")
        else:
            print("Tournoi non trouvé.")

    def display_match_info(self):
        print(f"Round {self.round_number}: {self.player1.first_name} vs "
              f"{self.player2.first_name}")

    def get_tournament_selection(self):
        """
        Demande à l'utilisateur de sélectionner un ou plusieurs tournois.
        """
        return input("Entrez le numéro d'un ou plusieurs tournois "
                     "(séparés par une virgule): ")

    def display_scores(self, tournament):
        print("+-+-+-+ Scores cumulés  +-+-+-+")
        table_data = []
        for player in tournament.selected_players:
            full_name = f"{player.last_name} {player.first_name} "
            table_data.append([full_name, player.total_points])
        headers = ["Nom et prénom du joueur", "Points totaux"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

    def display_feedback(self, message_type, tournament=None):
        # Display a message to the user
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
            print("⚠️ Aucun statut de filtre spécifié. Affichage de tous les tournois.")
        elif message_type == "invalid_filter_status":
            print("❌ Statut du filtre non valide. Veuillez utiliser 'not_started', "
                  "'in_progress', 'not_finished' ou 'finished'.")
        else:
            super().display_feedback(message_type)

    def display_tournament_report(self, tournament):
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
            players = sorted(tournament.selected_players,
                             key=lambda player: player.last_name)
            player_table = [
                [player.national_id, player.last_name, player.first_name,
                 player.date_of_birth] for player in players
            ]
            player_headers = ["Identifiant National", "Nom",
                              "Prénom", "Date de naissance"]

            print(tabulate(player_table, player_headers, tablefmt="grid",
                           colalign=("left", "left", "left", "left")))
        else:
            print(f"Le tournoi '{tournament.name}' n'a pas"
                  f" de joueurs sélectionnés.")
        # Affichage des rounds et des matchs
        print("Détails des rounds :")
        for round in tournament.rounds:
            print(f"Round {round.round_number}:")
            if round.matches:
                match_table = []
                for index, match in enumerate(round.matches, start=1):
                    # Access players and their scores correctly
                    player1_name = (f"{match.match[0][0].first_name} "
                                    f"{match.match[0][0].last_name}")
                    player2_name = (f"{match.match[1][0].first_name} "
                                    f"{match.match[1][0].last_name}")
                    player1_result = match.match[0][1]
                    player2_result = match.match[1][1]
                    match_table.append([
                        f"Match {index}",
                        player1_name,
                        player1_result,
                        player2_name,
                        player2_result
                    ])
                match_headers = ["Match", "Joueur 1", "Résultat Joueur 1",
                                 "Joueur 2", "Résultat Joueur 2"]
                print(tabulate(match_table, headers=match_headers,
                               tablefmt="grid"))
            else:
                print("Aucun match pour ce round.")
            print(f"Début du round: {round.start_time} "
                  f"- Fin du round : {round.end_time}")
        table_data = []
        for player in tournament.selected_players:
            table_data.append([f"{player.first_name} {player.last_name}", player.total_points])

        # Define headers
        headers = ["Joueur", "Points"]

        # Display the table using tabulate
        print(tabulate(table_data, headers=headers, tablefmt="pretty", colalign=("left", "right")))
        print(f"Remarques et commentaires généraux sur "
              f"le tournoi : {tournament.description} ")

