class ReportView:

    def show_reports_main_menu(self):
        print("Menu des rapports:")
        print("1. Liste des joueurs par ordre alphabétique")
        print("2. Liste des tournois passés")
        print("3. Rapport global")
        print("4. Quitter")
        return input("Choisir une option: ")

    def select_tournament_report(self):
        return input("Choisir un tournoi: ")

    def show_tournament_details_menu(self):
       print("Menu des tournois")
       print("1. Voir")


    def display_tournament_rounds_and_matches(self, rounds):
        for round in rounds:
            print(f"Tour : {round.name}")
            for match in round.matches:
                print(f"Match : {match.player1.name} vs {match.player2.name} - Score : {match.score1} - {match.score2}")