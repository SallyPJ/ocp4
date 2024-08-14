from utils import date_utils

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
        national_id = input("Entrer le numéro de licence FFE: ")
        return last_name, first_name, date_of_birth, national_id

    def display_players_list(self, players):
        print("Liste des joueurs enregistrés par ordre alphabétique :")
        for index, player in enumerate(players):
            print(f"{index + 1}. {player}")

    def get_player_count(self):
        # Get number of players from user input
        return int(input("Entrer le nombre de joueurs: "))
