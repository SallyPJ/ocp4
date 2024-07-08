import json
import os
import sys

# Chemin du fichier JSON contenant la base de données des joueurs
LIST_OF_PLAYERS = 'players.json'

class Player:
    def __init__(self, last_name, first_name, date_of_birth, national_id):
        self.last_name = last_name
        self.first_name = first_name
        self.date_of_birth = date_of_birth
        self.national_id = national_id


    def to_dict(self):
        # Convertit un objet Player en dictionnaire pour faciliter la sérialisation JSON
        return {
            "last_name": self.last_name,#Attention, que faire en cas d'ajout d'une cat ?
            "first_name": self.first_name,
            "date_of_birth": self.date_of_birth,
            "national_id": self.national_id
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["last_name"], data["first_name"], data["date_of_birth"],data["national_id"])


def load_players():
    if not os.path.exists(LIST_OF_PLAYERS):
        # Create the file with an empty list if it does not exist
        with open(LIST_OF_PLAYERS, 'w', encoding='utf-8') as file:
            json.dump([], file)
        return []
    else:
        with open(LIST_OF_PLAYERS, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return [Player.from_dict(player) for player in data]# Ajout message d'erreur json empty ?

# Fonction pour enregistrer la base de données des joueurs
def save_players(players):
    with open(LIST_OF_PLAYERS, 'w', encoding='utf-8') as file:
        json.dump([player.to_dict() for player in players], file, ensure_ascii=False, indent=4)

# Fonction pour ajouter un nouveau joueur
def add_player(last_name, first_name, date_of_birth, national_id):
    players = load_players()
    new_player = Player(last_name, first_name, date_of_birth, national_id)
    players.append(new_player)
    save_players(players)

# Fonction pour obtenir les informations du joueur depuis la console
def get_player_info():
    last_name = input("Nom de famille : ")
    first_name = input("Prénom : ")
    date_of_birth = input("Date de naissance (AAAA-MM-JJ) : ")
    national_id = input("Identifiant : ")
    return last_name, first_name, date_of_birth, national_id

def display_players():
    try:
        with open(LIST_OF_PLAYERS, 'r', encoding='utf-8') as file:
            data = json.load(file)
            print("Liste des joueurs :")
            for i,item in enumerate(data, start=1):
                print(f"{i}. Nom de famille: {item["last_name"]}, Prénom: {item["first_name"]}, Date de naissance: {item["date_of_birth"]}, Identifiant :{item["national_id"]}")
    except FileNotFoundError:
        print("Liste des joueurs non trouvé")

class Tournament:
    def __init__(self,name,location,start_date,end_date, number_of_round, description):
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_rounds = number_of_rounds
        self.description = description

    def to_dict(self):
        # Convertit un objet tournament en dictionnaire pour faciliter la sérialisation JSON
        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "number_of_rounds": self.number_of_rounds,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["location"], data["start_date"],data["end_date"], data["number_of_rounds"], data["description"])

def get_tournament_info():
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

    return name, location, start_date, end_date, number_of_rounds, description

def select_player(players):
    while True:
        try:
            choix = int(input("Entrez le numéro du joueur que vous souhaitez sélectionner : "))
            if 1 <= choix <= len(players):
                joueur_selectionne = players[choix - 1]
                print(
                    f"Vous avez sélectionné le joueur : {joueur_selectionne['last_name']} {joueur_selectionne['first_name']}")
                return joueur_selectionne  # Retourne le joueur sélectionné
            else:
                print(f"Veuillez entrer un numéro entre 1 et {len(players)}.")
        except ValueError:
            print("Veuillez entrer un numéro valide.")

class Menu :
    @staticmethod
    def display_main_menu():
        print("1. Ajouter un joueur")
        print("2. Afficher la liste des joueurs")
        print("3. Créer un tournoi")
        print("4. Quitter")
        choice = input("Choisissez une option : ")

        if choice == '1':
            last_name, first_name, date_of_birth, national_id = get_player_info()
            add_player(last_name, first_name, date_of_birth, national_id)
            print("Joueur ajouté avec succès !")
        elif choice == '2':
            display_players()
        elif choice == '3':
            get_tournament_info()
        elif choice == '4':
            sys.exit()
        else:
            print("Option invalide. Veuillez réessayer.")

    @staticmethod
    def display_tournament_menu(self):
        print("1.Sélectionner des joueurs enregistrés")
        print("2.Ajouter de nouveaux")

# Programme principal
if __name__ == "__main__":
    while True:
        Menu.display_main_menu()
