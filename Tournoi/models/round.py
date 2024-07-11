import random
from models.match import Match

class Round:
    def __init__(self, tournament):
        self.players = tournament.selected_players
        self.pairs = []

    def create_random_pairs(self):
        random.shuffle(self.players)  # Mélanger la liste des joueurs

        for i in range(0, len(self.players), 2):
            if i + 1 < len(self.players):
                pair = Match(self.players[i], self.players[i + 1])
                self.pairs.append(pair)


    def play_first_round(self):
        self.create_random_pairs()
        for pair in self.pairs:
            pair.play_match()

    def update_scores(self):
        for pair in self.pairs:
            results = pair.get_results()
            for player in results:
                for p in self.players:
                    if p.first_name == player:
                        p.total_points += results[player]
