from models.player import Player
class Match:
    def __init__(self, player1, player2, round_number, finished=False, in_progress=False):
        self.match = ([player1, 0], [player2, 0])  # Tuple contenant deux listes
        self.round_number = round_number
        self.finished = finished
        self.in_progress = in_progress

    def set_result(self, score1, score2):
        self.match[0][1] = score1  # Met à jour le score du joueur 1
        self.match[1][1] = score2  # Met à jour le score du joueur 2

    def get_match_results(self):
        return {
            f"{self.match[0][0].first_name} {self.match[0][0].last_name}": self.match[0][1],
            f"{self.match[1][0].first_name} {self.match[1][0].last_name}": self.match[1][1]
        }

    def to_dict(self):
        return {
            "match": [
                {"player": {"id": player[0].id, "last_name": player[0].last_name, "first_name": player[0].first_name},
                 "score": player[1]}
                for player in self.match
            ],
            "round_number": self.round_number,
            "finished": self.finished,
            "in_progress": self.in_progress
        }

    @classmethod
    def from_dict(cls, data):
        players = [Player.from_dict(player_data["player"]) for player_data in data["match"]]
        match = cls(players[0], players[1], data.get("round_number", 1))
        match.match[0][1] = data["match"][0]["score"]
        match.match[1][1] = data["match"][1]["score"]
        match.finished = data.get("finished", False)
        match.in_progress = data.get("in_progress", False)
        return match


