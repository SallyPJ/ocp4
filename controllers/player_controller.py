from utils import date_utils, text_utils
from models.database import Database
from models.player import Player
from views.player_view import PlayerView

class PlayerController:
    """
    Controller class responsible for managing player-related operations such as
    creating players, displaying registered players, and interacting with the view.
    """
    def __init__(self):
        self.player_view = PlayerView()
        self.database = Database()

    def run_player_menu(self):
        """
       Main loop to manage player operations. Presents a menu to the user and
        executes the corresponding actions based on the user's choice.
        Options:
        1. Create a new player
        2. Delete a player
        3. Display registered players
        4. Exit to the main menu
       """
        while True:
            choice = self.player_view.display_players_menu()
            if choice == "1":
                self.create_player()
            elif choice == "2":
                self.delete_player()
            elif choice == "3":
                self.display_sorted_players()
            elif choice == "4":
                break
            else:
                self.player_view.display_feedback("invalid_option")

    def create_player(self):
        """
        Handles the creation of a new player by gathering details from the user and saving
        the player to the database.

        Exceptions:
            If an error occurs during the player creation process, an error message is displayed.
        """
        try:
            player_details = self.get_player_details()
            new_player = Player(*player_details)
            players = self.database.load_players()
            players.append(new_player)
            self.database.save_players(players)
            self.player_view.display_feedback("player_created")
        except ValueError as ve:
            self.player_view.display_feedback("invalid_player_data", error_message=str(ve))
        except IOError as io_error:
            self.player_view.display_feedback("database_io_error", error_message=str(io_error))

    def delete_player(self):
        """
        Handles the deletion of a player by allowing the user to select one or more players
        from the list of registered players.

        The user can press 'Q' to cancel the operation and return to the main menu.

        Exceptions:
            If an error occurs during the deletion process, an error message is displayed.
        """
        try:
            players = self.display_sorted_players()
            while True:
                if players:
                    self.player_view.display_quit_message()
                selected_players = self.select_multiple_players(players)
                if selected_players == "quit":
                    self.player_view.display_feedback("operation_cancelled")
                    break
                if not selected_players:
                    self.player_view.display_feedback("no_players_selected")
                    continue
                if self.confirm_players_selection(selected_players):
                    for player in selected_players:
                        players.remove(player)
                    self.database.save_players(players)
                    self.player_view.display_feedback("players_deleted", selected_players)
                    break
                else:
                    continue
        except FileNotFoundError as fnf:
            self.player_view.display_feedback("fnf_error", error_message=str(fnf))
        except Exception as e:
            self.player_view.display_feedback("database_io_error", error_message=str(e))

    def display_sorted_players(self):
        """
        Displays a list of registered players in alphabetical order.

        Returns:
            list: A sorted list of player objects.

        Exceptions:
            If an error occurs during the player display process, an error message is displayed.
        """
        try:
            players = self.sort_players_alphabetically()
            if not players:
                self.player_view.display_feedback("no_players")
                return None
            self.player_view.display_players_list(players)
            return players
        except FileNotFoundError as fnf:
            self.player_view.display_feedback("fnf_error", error_message=str(fnf))



    def select_multiple_players(self, players):
        """
        Handles the selection of multiple players using indices but verifies the selection with UUIDs.

        Args:
            players (list): The list of player objects to select from.

        Returns:
            list or str: A list of selected player objects, or 'quit' if the user chooses to exit.
        """
        index_uuid_map = {idx + 1: player.id for idx, player in enumerate(players)}
        selected_indices = self.player_view.select_players_input()
        if selected_indices.strip().lower() == 'q':
            return "quit"
        selected_players = self.process_player_choices(selected_indices, players, index_uuid_map)
        return selected_players

    def process_player_choices(self, user_input, players, uuid_index_map):
        """Processes the user's player selection input based on indices and maps them to player objects.

        Args:
            user_input (str): The indices entered by the user.
            players (list): The list of player objects.
            uuid_index_map (dict): A dictionary mapping indices to player UUIDs.

        Returns:
            list: A list of selected player objects.
        """
        try:
            indices = [int(choice.strip()) - 1 for choice in user_input.split(',')]
            selected_uuids = {uuid_index_map.get(idx + 1) for idx in indices if 0 <= idx < len(players)}
            selected_players = [player for player in players if player.id in selected_uuids]

            return selected_players
        except ValueError:
            self.player_view.display_feedback("invalid_selection")
            return []

    def confirm_players_selection(self, selected_players):
        """
        Confirms the selection of players before proceeding with deletion.

        Args:
            selected_players (list): The list of selected player objects.

        Returns:
            bool: True if the selection is confirmed, False otherwise.
        """
        self.player_view.display_selected_players(selected_players)
        confirmation = self.player_view.confirm_selection().lower()

        if confirmation == 'o':
            return True  # Proceed with the deletion
        elif confirmation == 'n':
            self.player_view.display_feedback("players_reset")
            selected_players.clear()  # Clear the selection
            return False  # Indicate that the user wants to restart the selection
        else:
            self.player_view.display_feedback("invalid_option")  # Invalid option

    def sort_players_alphabetically(self):
        """
        Sorts the list of players alphabetically by their last name.

        Returns:
            list: A sorted list of player objects.

        Exceptions:
            If no players are found, a message is displayed.
        """
        players = sorted(self.database.load_players(), key=lambda player: player.last_name)
        return players

    def get_player_count(self):
        """
        Gets and validates the number of players from user input.

        Returns:
            int: The validated number of players.
        """
        registered_players = self.database.load_players()
        while True:
            user_input = self.player_view.prompt_for_player_count()
            try:
                number_of_players = int(user_input)
                if number_of_players <= 0:
                    self.player_view.display_invalid_player_count_message("negative_or_zero")
                elif number_of_players % 2 != 0:
                    self.player_view.display_invalid_player_count_message("not_even")
                    # Check if the selected number of players is less than or equal to the registered players
                elif number_of_players > len(registered_players):
                    self.player_view.display_invalid_player_count_message("too_many_players", len(registered_players))
                else:
                    return number_of_players
            except ValueError:
                self.player_view.display_invalid_player_count_message("not_integer")

    def check_new_player_birthdate(self):
        while True:
            date_of_birth = self.player_view.get_new_player_date_of_birth()
            if not date_utils.validate_date(date_of_birth):
                self.player_view.display_feedback("invalid_birthdate")
            else:
                return date_of_birth

    def check_new_player_national_id(self):
        while True:
            national_id = self.player_view.get_new_player_national_id()
            if not text_utils.validate_national_id(national_id):
                self.player_view.display_feedback("invalid_national_id")
            else:
                return national_id

    def check_new_player_last_name(self):
        while True:
            last_name = self.player_view.get_new_player_last_name()
            if last_name is None:
                self.player_view.display_feedback("empty_field")
            else:
                return last_name.upper()

    def check_new_player_first_name(self):
        while True:
            first_name = self.player_view.get_new_player_first_name()
            if first_name is None:
                self.player_view.display_feedback("empty_field")
            else:
                return first_name.capitalize()

    def get_player_details(self):
        """
        Collect player details from user input and validate the date of birth.

        Returns:
            tuple: A tuple containing last_name, first_name, date_of_birth, and national_id.
        """

        last_name = self.check_new_player_last_name()
        first_name = self.check_new_player_first_name()
        national_id = self.check_new_player_birthdate()
        date_of_birth = self.check_new_player_national_id()
        return last_name, first_name, date_of_birth, national_id
