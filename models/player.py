import uuid


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
       Defines the behavior for the less-than operator (<) based on the player's last name.

       Args:
           other (Player): Another Player object for comparison.

       Returns:
           bool: True if the player's last name comes before the other's last name alphabetically.
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
