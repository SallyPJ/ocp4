import json
import os

# Chemin du fichier JSON contenant la base de données des joueurs
FILENAME = 'players.json'

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
    if not os.path.exists(FILENAME):
        # Create the file with an empty list if it does not exist
        with open(FILENAME, 'w', encoding='utf-8') as file:
            json.dump([], file)
        return []
    else:
        with open(FILENAME, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return [Player.from_dict(player) for player in data]# Ajout message d'erreur json empty ?

# Fonction pour enregistrer la base de données des joueurs
def save_players(players):
    with open(FILENAME, 'w', encoding='utf-8') as file:
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
        with open(FILENAME, 'r', encoding='utf-8') as file:
            data = json.load(file)
            print("Liste des joueurs :")
            for item in data:
                print(f"Nom de famille: {item["last_name"]}, Prénom: {item["first_name"]}, Date de naissance: {item["date_of_birth"]}, Identifiant :{item["national_id"]}")
    except FileNotFoundError:
        print("Liste des joueurs non trouvé")

# Programme principal
if __name__ == "__main__":
    while True:
        print("1. Ajouter un joueur")
        print("2. Afficher la liste des joueurs")
        print("3. Quitter")
        choice = input("Choisissez une option : ")

        if choice == '1':
            last_name, first_name, date_of_birth, national_id = get_player_info()
            add_player(last_name, first_name, date_of_birth, national_id)
            print("Joueur ajouté avec succès !")
        elif choice == '2':
            display_players()
        elif choice == '3':
            break
        else:
            print("Option invalide. Veuillez réessayer.")