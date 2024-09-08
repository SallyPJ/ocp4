import uuid
import os
import json

from utils import text_utils, date_utils


class Player:
    """
    Represents a player in the tournament system, including personal details,
    tournament points, and their list of opponents.

    Attributes:
        last_name (str): The player's last name.
        first_name (str): The player's first name.
        date_of_birth (str): The player's date of birth.
        national_id (str): The player's national identification number.
        total_points (int): The player's total points in the tournament.
        opponents (list): A list of opponents the player has faced.
        id (str): A unique identifier for the player.
    """
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    PLAYERS_FILE = os.path.join(BASE_DIR, "data", "players.json")

    def __init__(self, last_name, first_name, date_of_birth,
                 national_id, total_points=0):
        self.id = str(uuid.uuid4())
        self.last_name = last_name
        self.first_name = first_name
        self.date_of_birth = date_of_birth
        self.national_id = national_id
        self.total_points = total_points
        self.opponents = []

    def __lt__(self, other):
        """
       Defines the behavior for the less-than operator (<)
       based on the player's last name.

       Args:
           other (Player): Another Player object for comparison.

       Returns:
           bool: True if the player's last name comes
           before the other's last name alphabetically.
       """
        return self.last_name.lower() < other.last_name.lower()

    def __str__(self):
        return (f"{self.last_name} {self.first_name} "
                f"{self.date_of_birth} {self.national_id}")

    def to_dict(self):
        """
        Converts the Player object to a dictionary format for serialization.

        Returns:
            dict: A dictionary representing the player's data.
        """
        return {
            "id": self.id,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "date_of_birth": self.date_of_birth,
            "national_id": self.national_id,
            "total_points": self.total_points,
        }

    @classmethod
    def from_dict(cls, data):
        """
        Creates a Player object from a dictionary.

        Args:
            data (dict): A dictionary containing player data.

        Returns:
            Player: A Player object instantiated from the dictionary.
        """
        return cls(
            data.get("last_name", "Unknown"),
            data.get("first_name", "Unknown"),
            data.get("date_of_birth", "01/01/1900"),
            data.get("national_id", "000000"),
            data.get("total_points", 0)
        )

    def add_opponent(self, opponent):
        """
        Adds an opponent to the player's list of opponents, if not already present.

        Args:
            opponent (Player): The opponent to add.
        """
        if opponent not in self.opponents:
            self.opponents.append(opponent)

    def has_played_against(self, opponent):
        """
        Checks if the player has played against a specified opponent.

       Args:
           opponent (Player): The opponent to check.

       Returns:
           bool: True if the player has played against the opponent, False otherwise.
       """
        return opponent in self.opponents

    @staticmethod
    def check_for_data_directory():
        """
        Ensures the data directory for storing player information exists.
        If the directory doesn't exist, it is created.
        """
        if not os.path.exists(os.path.dirname(Player.PLAYERS_FILE)):
            os.makedirs(os.path.dirname(Player.PLAYERS_FILE))

    @classmethod
    def load_players(cls):
        """
        Loads the list of players from the JSON file.

        Returns:
            list: A list of Player objects, or an empty list if no file is found.

        If the file does not exist, it is created and an empty list is returned.
        """
        cls.check_for_data_directory()
        if not os.path.exists(cls.PLAYERS_FILE):
            with open(cls.PLAYERS_FILE, 'w', encoding='utf-8') as file:
                json.dump([], file)
            return []
        with open(cls.PLAYERS_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return [cls.from_dict(player) for player in data]

    @classmethod
    def save_players(cls, players):
        """
        Saves the list of players to the JSON file.

        Args:
            players (list): A list of Player objects to be saved.

        The data directory is created if it does not exist.
        """
        cls.check_for_data_directory()
        with open(cls.PLAYERS_FILE, 'w', encoding='utf-8') as file:
            json.dump([player.to_dict() for player in players], file,
                      ensure_ascii=False, indent=4)

    @classmethod
    def sort_players_alphabetically(cls):
        """
        Sorts the list of players alphabetically by their last name.

        Returns:
            list: A sorted list of player objects.

        Exceptions:
            If no players are found, a message is displayed.
        """
        players = sorted(Player.load_players(),
                         key=lambda player: player.last_name)
        return players

    def update_player_total_points(self, score):
        """
        Updates the player's total points by adding the given score.

        Args:
            score (float): The score to add to the player's total points.
        """
        self.total_points += score

    @classmethod
    def players_file_exists(cls):
        """Checks if the players file exists."""
        return os.path.exists(cls.PLAYERS_FILE)

    @classmethod
    def has_enough_players(cls, min_players=2):
        """Checks if there are enough players."""
        players = cls.load_players()
        return len(players) >= min_players

    @classmethod
    def add_new_player(cls, new_player):
        """
        Adds a new player to the player list and saves it to the database.

        Args:
            new_player (Player): The new player to add.

        """
        players = cls.load_players()
        players.append(new_player)
        cls.save_players(players)

    @classmethod
    def delete_players(cls, players, selected_players):
        """
        Deletes the selected players from the player list and saves the updated list.

        Args:
            players_to_delete (list): List of players to delete.

        Raises:
            IOError: If there is an error accessing the database.
        """
        for player in selected_players:
            players.remove(player)
        cls.save_players(players)

    @staticmethod
    def validate_national_id(national_id):
        """
        Validates the national ID format.

        Args:
            national_id (str): The national ID to validate.

        Returns:
            bool: True if the national ID is valid, False otherwise.
        """
        return text_utils.validate_national_id(national_id)

    @staticmethod
    def validate_birthdate(birthdate):
        """
        Validates the birthdate format.

        Args:
            birthdate (str): The birthdate to validate.

        Returns:
            bool: True if the birthdate is valid, False otherwise.
        """
        return date_utils.validate_date(birthdate)
