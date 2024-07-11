from models.tournament import Tournament
from models.database import load_tournaments, save_tournament
from models.database import load_players
from controllers.player import get_player_info, create_player, select_player

from views.player import display_players

def create_tournament():
    number_of_rounds_default = 4

    name = input("Nom : ")
    location = input("Lieu : ")
    start_date = input("Date de début : ")
    end_date = input("Date de fin : ")
    while True:
        number_of_rounds_choice = input(f"Le nombre de tour par défaut est à {number_of_rounds_default}, souhaitez-vous le modifier ? (O/N)")
        if number_of_rounds_choice.lower() == "o": # Conversion en minuscule
            while True:
                try:
                    number_of_rounds = int(input("Nombre de tours (entre 1 et 30) : "))
                    if 1 <= number_of_rounds <= 30:
                        break
                    else:
                        print("Le nombre de tours doit être compris entre 1 et 30.")
                except ValueError:
                    print("Ce n'est pas un nombre entier. Veuillez entrer un nombre entier entre 1 et 30.")
            break
        elif number_of_rounds_choice.lower() == "n":
            number_of_rounds = number_of_rounds_default
            break
        else:
            print("Le caractère n'est pas valide. Veuillez entrer 'O' pour oui ou 'N' pour non.")
    description = input("Description : ")
    while True:
        try:
            number_of_players = int(input("Nombre de joueurs : "))
            if number_of_players > 0 and (number_of_players % 2) == 0:
                print(f"le nombre de joueurs est de {number_of_players}")
                break
            elif number_of_players <= 0:
                print("Le nombre de joueurs doit être un nombre positif.")
            else:
                print("Le nombre de joueurs doit être un chiffre pair")
        except ValueError:
            print("Veuillez entrer un nombre entier")

        # Création de l'objet Tournament avec les informations saisies
    tournament = Tournament(name, location, start_date, end_date, number_of_rounds, description, number_of_players)




    display_tournament_menu(tournament)




def display_tournament_menu(tournament):
    while True:
        print("1.Sélectionner des joueurs pour le tournoi")
        print("2.Créer un nouveau joueur")
        print("3.Lancer le tournoi")
        print("4.Quitter")
        choice = input("Choisissez une option : ")

        if choice == '1':
            players = load_players()
            display_players()
            selected_player = select_player(players)
            if selected_player:
                tournament.add_selected_player(selected_player)
            else:
                print("Aucun joueur sélectionné.")
        elif choice == '2':
            last_name, first_name, date_of_birth, national_id = get_player_info()
            create_player(last_name, first_name, date_of_birth, national_id)
            print("Joueur ajouté avec succès !")
        elif choice == '3':
            print(Tournament.to_dict)
            tournament.display_tournament_details()
            tournaments = load_tournaments()
            tournaments.append(tournament)
            save_tournament(tournaments)

            #tournament = Tournament(selected_players, number_of_rounds)
            tournament.run_tournament()
            tournament.display_final_scores()

            #run_tournament()
            break
        elif choice == '4':
            break
        else:
            print("Option invalide. Veuillez réessayer.")