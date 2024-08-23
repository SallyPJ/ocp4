from models.player import Player
class Match:
    def __init__(self, player1, player2, round_number):
        self.players = [player1, player2]
        self.round_number = round_number
        self.results = {player1.first_name: 0, player2.first_name: 0}

    def to_dict(self):
        return {
            "players": [player.to_dict() for player in self.players],
            "round_number": self.round_number,
            "results": self.results
        }

    @classmethod
    def from_dict(cls, data):
        players = [Player.from_dict(player_data) for player_data in data["players"]]
        match = cls(players[0], players[1], data["round_number"])
        match.results = data["results"]
        return match

    def get_match_results(self):
        return self.results

