import uuid

class Player:
    def __init__(self, last_name, first_name, date_of_birth, national_id):
        self.id = str(uuid.uuid4())
        self.last_name = last_name
        self.first_name = first_name
        self.date_of_birth = date_of_birth
        self.national_id = national_id
        self.total_points = 0
        self.opponents = []


    def __str__(self):
        return f"{self.id} {self.last_name} {self.first_name} {self.date_of_birth} {self.national_id}"

    def to_dict(self):
        # Convert Player object to dictionary
        return {
            "id": self.id,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "date_of_birth": self.date_of_birth,
            "national_id": self.national_id
        }

    @classmethod
    def from_dict(cls, data):
        # Create Player object from dictionary
        return cls(data["last_name"], data["first_name"], data["date_of_birth"], data["national_id"])

    def add_opponent(self, opponent):
        # Ajoute un adversaire à la liste
        if opponent not in self.opponents:
            self.opponents.append(opponent)

    def has_played_against(self, opponent):
        # Vérifie si le joueur a déjà joué contre l'adversaire
        return opponent in self.opponents
