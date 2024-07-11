import sys

from controllers.tournament import create_tournament
from views.player import display_players
from controllers.player import create_player, get_player_info, select_player

def display_main_menu():
    print("1. Créer un nouveau joueur")
    print("2. Afficher la liste des joueurs enregistrés")
    print("3. Créer un tournoi")
    print("4. Quitter")
    choice = input("Choisissez une option : ")

    if choice == '1':
        last_name, first_name, date_of_birth, national_id = get_player_info()
        create_player(last_name, first_name, date_of_birth, national_id)
        print("Joueur ajouté avec succès !")
    elif choice == '2':
        display_players()
    elif choice == '3':
        create_tournament()
    elif choice == '4':
        sys.exit()
    else:
        print("Option invalide. Veuillez réessayer.")




