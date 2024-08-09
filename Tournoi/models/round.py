import random
from models.match import Match

class Round:
    def __init__(self, tournament,round_number, is_first_round=False):
        self.players = tournament.selected_players
        self.pairs = []
        self.round_number = round_number
        self.is_first_round = is_first_round

    def create_pairs(self):
        if self.is_first_round:
            self.create_random_pairs()
        else:
            self.create_pairs_based_on_points()

    def create_random_pairs(self):
        # Create random pairs of players
        random.shuffle(self.players)
        self.pairs = [
            Match(self.players[i], self.players[i + 1],  self.round_number)
            for i in range(0, len(self.players), 2)
            if i + 1 < len(self.players)
        ]

    def create_pairs_based_on_points(self):
        # Trier les joueurs par leurs points totaux
        self.players.sort(key=lambda player: player.total_points, reverse=True)

        # Groupes de joueurs avec le même nombre de points
        grouped_players = {}
        for player in self.players:
            points = player.total_points
            if points not in grouped_players:
                grouped_players[points] = []
            grouped_players[points].append(player)

        # Mélanger les groupes ayant les mêmes points
        for points, players in grouped_players.items():
            random.shuffle(players)

        # Reformer la liste des joueurs
        self.players = [player for group in grouped_players.values() for player in group]

        # Créer les paires
        available_players = self.players[:]
        while len(available_players) >= 2:
            player1 = available_players.pop(0)
            paired = False
            for i, player2 in enumerate(available_players):
                if not player1.has_played_against(player2):
                    self.pairs.append(Match(player1, player2, self.round_number))
                    player1.add_opponent(player2)
                    player2.add_opponent(player1)
                    available_players.pop(i)
                    paired = True
                    break
            if not paired:
                # If no valid pair is found, add player1 back to the list
                available_players.append(player1)

    def has_played_before(self, player1, player2):
        # Vérifie si les deux joueurs ont déjà joué l'un contre l'autre
        return player1.has_played_against(player2)

    def play_round(self):
        self.create_pairs()
        for pair in self.pairs:
            pair.play_match()

    def get_results(self):
        # Return match results
        return [pair.get_results() for pair in self.pairs]
