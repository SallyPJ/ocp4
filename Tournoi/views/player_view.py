from utils import date_utils
from tabulate import tabulate



class PlayerView:
    def get_player_details(self):
        # Get player details from user input
        last_name = input("Entrer le nom de famille: ")
        first_name = input("Entrer le prénom: ")
        while True:
            date_of_birth = input("Entrer la date de naissance (JJ/MM/AAAA): ")
            if date_utils.validate_date(date_of_birth):
                break
            else:
                print("La date de début n'est pas valide. Veuillez entrer la date au format JJ/MM/AAAA.")
        national_id = input("Entrer l'identifiant national d'échec: ")
        return last_name, first_name, date_of_birth, national_id

    def display_players_list(self, players):
        print("Liste des joueurs enregistrés :")
        table = [[index + 1, player.national_id, player.last_name, player.first_name, player.date_of_birth ] for index, player in
                 enumerate(players)]
        headers = ["No", "Identifiant", "Nom", "Prénom", "Date de naissance", ]
        print(tabulate(table, headers, tablefmt="pretty", colalign=("left")))

    def get_player_count(self):
        # Get number of players from user input
        while True:
            try:
                number_of_players = int(input("Entrer le nombre de joueurs: "))
                if number_of_players > 0 and (number_of_players % 2) == 0:
                    return number_of_players
                elif number_of_players <= 0:
                    print("Le nombre de joueurs doit être un nombre positif.")
                else:
                    print("Le nombre de joueurs doit être un chiffre pair")

            except ValueError:
                print("Veuillez entrer un nombre entier")


