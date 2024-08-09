from utils import date_utils


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

    def get_player_count(self):
        # Get number of players from user input
        return int(input("Entrer le nombre de joueurs: "))

    def show_tournament_menu(self, tournament):
        # Display tournament management menu
        print("Menu du tournoi:")
        print(f"1. Sélectionner des joueurs pour le tournoi ({tournament.number_of_players - len(tournament.selected_players)})")
        print("2. Débuter le tournoi")
        print("3. Menu principal")
        return input("Choisissez une option: ")

    def display_players(self, players):
        # Display list of players
        print("Joueurs disponibles:")
        for index, player in enumerate(players):
            print(f"{index + 1}. {player}")

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
        return input("Confirmer la sélection ? (o/n) : ")

    def display_match_info(self):
        print(f"Round {self.round_number}: {self.player1.first_name} vs {self.player2.first_name}")

    def display_message(self, message):
        # Display a message to the user
        print(message)