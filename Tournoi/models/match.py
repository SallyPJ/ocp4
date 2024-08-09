class Match:
    def __init__(self, player1, player2, round_number):
        self.players = [player1, player2]
        self.round_number = round_number
        self.results = {player1.first_name: 0, player2.first_name: 0}

    def play_match(self):
        # Record the results of a match
        print(f"Round {self.round_number}: Match entre {self.players[0].first_name} et {self.players[1].first_name}.")
        while True:
            try:
                choice = int(input(f"Qui a gagné ? :\n"
                               f"1. {self.players[0].first_name}\n"
                               f"2. {self.players[1].first_name}\n"
                               f"3. Match nul\n"))
                if choice == 1:
                    self.results[self.players[0].first_name] = 1
                    break
                elif choice == 2:
                    self.results[self.players[1].first_name] = 1
                    break
                elif choice == 3:
                    self.results[self.players[0].first_name] = 0.5
                    self.results[self.players[1].first_name] = 0.5
                    break
                else:
                    print("Choix invalide, veuillez entrer 1, 2 ou 3.")

            except ValueError:
                print("Entrée invalide, veuillez entrer un nombre entier .")

        print("Résultat enregistré.")



    def get_results(self):
        return self.results

