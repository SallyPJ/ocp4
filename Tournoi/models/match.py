class Match:
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.results = {player1.first_name: 0, player2.first_name: 0}

    def play_match(self):
        print(f"Match entre {self.players[0].first_name} et {self.players[1].first_name}.")
        print("Qui a gagné ?")
        print(f"1. {self.players[0].first_name}")
        print(f"2. {self.players[1].first_name}")
        print(f"3. Égalité")
        choice = int(input("Entrez votre choix (1, 2 ou 3) : "))
        if choice == 1:
            self.results[self.players[0].first_name] = 1
            self.results[self.players[1].first_name] = 0
        elif choice == 2:
            self.results[self.players[0].first_name] = 0
            self.results[self.players[1].first_name] = 1
        else:
            self.results[self.players[0].first_name] = 0.5
            self.results[self.players[1].first_name] = 0.5
        print("Résultat enregistré.")

    def get_results(self):
        return self.results