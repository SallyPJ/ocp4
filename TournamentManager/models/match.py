from models.player import Player


class Match:
    """
    A class to represent a match between two players in a tournament round.

    Attributes:
        match (list): A list containing two sub-lists, each with a Player object and their score.
        round_number (int): The number of the round in which this match takes place.
        finished (bool): A flag indicating whether the match has finished.
        in_progress (bool): A flag indicating whether the match is currently in progress.
    """
    def __init__(self, player1, player2, round_number,
                 finished=False, in_progress=False):
        """
        Initialize a Match object with two players, the round number, and flags for status.

        Args:
            player1 (Player): The first player in the match.
            player2 (Player): The second player in the match.
            round_number (int): The round number in which the match occurs.
            finished (bool): Defaults to False. Indicates if the match is finished.
            in_progress (bool): Defaults to False. Indicates if the match is in progress.
        """
        self.match = ([player1, 0], [player2, 0])
        self.round_number = round_number
        self.finished = finished
        self.in_progress = in_progress

    def to_dict(self):
        """
        Convert the Match object into a dictionary for serialization. Used to serialize data to the database.

        Returns:
            dict: A dictionary representation of the match, including players' details and scores.
        """
        return {
            "match": [
                {"player": {"id": player[0].id, "last_name": player[0].last_name,
                            "first_name": player[0].first_name}, "score": player[1]}
                for player in self.match
            ],
            "round_number": self.round_number,
            "finished": self.finished,
            "in_progress": self.in_progress
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a Match object from a dictionary. Used to unserialize data from the database.

        Args:
            data (dict): A dictionary containing match information.

        Returns:
            Match: A Match object created from the provided dictionary.
        """
        players = [Player.from_dict(player_data["player"])
                   for player_data in data["match"]]
        match = cls(players[0], players[1], data.get("round_number", 1))
        match.match[0][1] = data["match"][0]["score"]
        match.match[1][1] = data["match"][1]["score"]
        match.finished = data.get("finished", False)
        match.in_progress = data.get("in_progress", False)
        return match

    def set_result(self, score1, score2):
        """
        Set the result of the match by updating the scores of both players.

        Args:
            score1 (int): The score of the first player.
            score2 (int): The score of the second player.

        """
        self.match[0][1] = score1
        self.match[1][1] = score2

    def get_match_results(self):
        """
        Get the results of the match as a dictionary.

        Returns:
            dict: A dictionary with player names as keys and their scores as values.
        """
        return {
            f"{self.match[0][0].first_name} {self.match[0][0].last_name}":
                self.match[0][1],
            f"{self.match[1][0].first_name} {self.match[1][0].last_name}":
                self.match[1][1]
        }

