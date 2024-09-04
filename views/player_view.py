from tabulate import tabulate
from views.base_view import BaseView


class PlayerView(BaseView):
    """
    PlayerView handles the user interface for player management within the application.

    It provides methods for displaying menus, prompting user inputs, displaying lists of players,
    and showing feedback messages related to player operations.
    """
    def display_players_menu(self):
        """
        Displays the player management menu and prompts the user to choose an option.

        The menu includes options for:
        1. Registering a new player.
        2. Deleting an existing player.
        3. Displaying the list of registered players.
        4. Returning to the main menu.

        Returns:
            str: The user's selected option as a string.
        """
        print("==========================================")
        print("      [ Menu de Gestion des Joueurs ]")
        print("==========================================")
        print("1. Enregistrer un Nouveau Joueur")
        print("2. Supprimer un Joueur")
        print("3. Liste des Joueurs Enregistrés")
        print("4. Retour au Menu Principal")
        print("==========================================")
        return input("Choisir une option: ")

    def prompt_for_player_details(self):
        """
        Prompts the user to enter the details of a new player.

        The details include:
        - Last name
        - First name
        - Date of birth
        - National chess ID

        Returns:
            tuple: A tuple containing the player's last name, first name, date of birth, and national ID.
        """
        print("Enregistrement d'un nouveau joueur")
        last_name = input("Entrer le nom de famille: ")
        first_name = input("Entrer le prénom: ")
        date_of_birth = input("Entrer la date de naissance (JJ/MM/AAAA): ")
        national_id = input("Entrer l'identifiant national d'échec: ")
        return last_name, first_name, date_of_birth, national_id

    def select_players_input(self):
        """
        Prompts the user to select players by entering their corresponding numbers.

        Returns:
            str: A comma-separated string of selected player numbers.
        """
        return input("Entrez les numéros des joueurs que vous "
                     "voulez sélectionner (séparés par des virgules): ")

    def display_players_list(self, players):
        """
        Displays a list of registered players in a tabulated format.

        Args:
            players (list): A list of Player objects to display.
        """
        print("Liste des joueurs enregistrés :")
        table = [[index + 1, player.national_id, player.last_name, player.first_name,
                  player.date_of_birth] for index, player in enumerate(players)]
        headers = ["No", "Identifiant", "Nom", "Prénom", "Date de naissance", ]
        print(tabulate(table, headers, tablefmt="pretty", colalign="left"))

    def display_feedback(self, message_type, players=None, error_message=None):
        """
        Displays feedback messages to the user based on the operation performed.

        Args:
            message_type (str): The type of feedback message to display.
            players (list, optional): A list of players involved in the operation (used for deletion feedback).
            error_message (str, optional): An error message to display if applicable.
        """
        if message_type == "player_created":
            print("✅ Joueur créé avec succès.")
        elif message_type == "player_creation_error" and error_message:
            print(f"❌ Erreur lors de la création du joueur : {error_message}")
        elif message_type == "players_display_error" and error_message:
            print(f"Une erreur est survenue lors de l'affichage des joueurs : {error_message}")
        elif message_type == "no_players":
            print("⚠️ Aucun joueur enregistré.")
        elif message_type == "players_reset":
            print("⚠️ La sélection des joueurs a été réinitialisée.")
        elif message_type == "players_deleted" and players:
            print("✅ Les joueurs suivants ont été supprimés avec succès:")
            for player in players:
                print(f"- {player.first_name} {player.last_name}")
        elif message_type == "player_deletion_error" and error_message:
            print(f"❌ Erreur lors de la suppression du/des joueur(s): {error_message}")
        elif message_type == "invalid_birthdate":
            print("La date de naissance n'est pas valide. Veuillez entrer la date au format JJ/MM/AAAA.")
        else:
            super().display_feedback(message_type)

    def display_quit_message(self):
        """Displays a message to the user indicating that they can press 'Q' to quit."""
        print("Appuyer sur 'Q' pour revenir au menu précédent.")

    def display_selected_players(self, players):
        """
        Displays the details of the players selected by the user.

        Args:
            players (list): A list of Player objects representing the selected players.
        """
        print("**** Sélection ****")
        for player in players:
            print(player)

    def confirm_selection(self):
        """
        Prompts the user to confirm their selection.

        Returns:
            str: The user's confirmation input, typically 'O' for yes or 'N' for no.
        """
        return input("Confirmez-vous la sélection du ou des joueurs suivants ? (O/N): ")

    def prompt_for_player_count(self):
        """
        Prompts the user to enter the number of players to create a tournament.

        Returns:
            str: The user's input as a string.
        """
        return input("Entrer le nombre de joueurs: ")

    def display_invalid_player_count_message(self, message_type):
        """
        Displays an error message if the entered player count is invalid.

        Args:
            message_type (str): The type of error message to display.
        """
        if message_type == "negative_or_zero":
            print("Le nombre de joueurs doit être un nombre positif.")
        elif message_type == "not_even":
            print("Le nombre de joueurs doit être un chiffre pair.")
        elif message_type == "not_integer":
            print("Veuillez entrer un nombre entier.")
