class ReportView:

    def show_reports_main_menu(self):
        print("==========================================")
        print("           [ Menu des rapports ]")
        print("==========================================")
        print("1. Liste des Joueurs")
        print("2. Tournois Enregistrés")
        print("3. Vue d'Ensemble des Tournois")
        print("4. Retour au menu principal")
        return input("Choisir une option: ")


    def display_tournament_rounds_and_matches(self, rounds):
        for round in rounds:
            print(f"Tour : {round.name}")
            for match in round.matches:
                print(f"Match : {match.player1.name} vs {match.player2.name} - Score : {match.score1} - {match.score2}")