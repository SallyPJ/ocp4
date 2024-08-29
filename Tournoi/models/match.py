from models.player import Player
class Match:
    def __init__(self, player1, player2, round_number, finished=False, in_progress=False):
        self.players = [player1, player2]
        self.round_number = round_number
        self.results = {player1.first_name: 0, player2.first_name: 0}
        self.finished = finished
        self.in_progress = in_progress

    def to_dict(self):
        return {
            "players": [player.to_dict() for player in self.players],
            "round_number": self.round_number,
            "results": self.results,
            "finished": self.finished,
            "in_progress": self.in_progress
        }

    @classmethod
    def from_dict(cls, data):

        players = [Player.from_dict(player_data) for player_data in data["players"]]
        match = cls(players[0], players[1], data["round_number"])
        match.results = data["results"]
        match.finished = data.get("finished", "Error")
        match.in_progress = data.get("in_progress", "Error")
        return match

    def get_match_results(self):
        return self.results

