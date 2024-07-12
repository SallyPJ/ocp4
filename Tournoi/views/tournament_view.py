from .base_view import BaseView
#Gestion des messages d'erreur à implémenter
class TournamentView:
    def get_tournament_details(self):
        name = input("Nom : ")
        location = input("Lieu : ")
        start_date = input("Date de début : ")
        end_date = input("Date de fin : ")
        description = input("Description : ")
        return name, location, start_date, end_date, description

    def get_round_count(self, default_rounds=4):
        while True:
            number_of_rounds_choice = input(
                f"Le nombre de tour par défaut est à {default_rounds}, souhaitez-vous le modifier ? (O/N)"
            )
            if number_of_rounds_choice.lower() == "o":
                while True:
                    try:
                        number_of_rounds = int(input("Nombre de tours (entre 1 et 30) : "))
                        if 1 <= number_of_rounds <= 30:
                            return number_of_rounds
                        else:
                            print("Le nombre de tours doit être compris entre 1 et 30.")
                    except ValueError:
                        print("Ce n'est pas un nombre entier. Veuillez entrer un nombre entier entre 1 et 30.")
            elif number_of_rounds_choice.lower() == "n":
                return default_rounds
            else:
                print("Le caractère n'est pas valide. Veuillez entrer 'O' pour oui ou 'N' pour non.")

    def get_player_count(self):
        while True:
            try:
                number_of_players = int(input("Nombre de joueurs : "))
                if number_of_players > 0 and (number_of_players % 2) == 0:
                    print(f"Le nombre de joueurs est de {number_of_players}")
                    return number_of_players
                elif number_of_players <= 0:
                    print("Le nombre de joueurs doit être un nombre positif.")
                else:
                    print("Le nombre de joueurs doit être un chiffre pair")
            except ValueError:
                print("Veuillez entrer un nombre entier")

    def show_tournament_menu(self):
        print("1.Sélectionner des joueurs pour le tournoi")
        print("2.Créer un nouveau joueur")
        print("3.Lancer le tournoi")
        print("4.Quitter")
        return input("Choisissez une option : ")