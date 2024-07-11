import uuid
class Player:
    def __init__(self, last_name, first_name, date_of_birth, national_id):
        self.id = str(uuid.uuid4())
        self.last_name = last_name
        self.first_name = first_name
        self.date_of_birth = date_of_birth
        self.national_id = national_id
        self.total_points = 0

    def __str__(self):
        return f"{self.id} {self.last_name} {self.first_name} {self.date_of_birth} {self.national_id}"

    def to_dict(self):
        # Convertit un objet Player en dictionnaire pour faciliter la sérialisation JSON
        return {
            "id": self.id,
            "last_name": self.last_name,#Attention, que faire en cas d'ajout d'une cat ?
            "first_name": self.first_name,
            "date_of_birth": self.date_of_birth,
            "national_id": self.national_id
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["last_name"], data["first_name"], data["date_of_birth"],data["national_id"])

    def display_selected_players(self):
        selected_players = ", ".join(str(player) for player in self.selected_players)
        print(f"Joueurs sélectionnés : {selected_players}")